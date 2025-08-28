"""
Atores mínimos: FeedActor, StrategyActor, RiskActor, RouterActor.
(Para simplificar, é sincrono; pode ser portado p/ asyncio conforme crescer.)
"""
import time, os, yaml, math, random
from typing import Dict, Any, List
from src.runtime.bus import EventBus
from src.telemetry import whylog
from src.agents import momentum, meanrev, allocator_bandit, regime as regime_mod
from src.risk.risk_brain_v2 import RiskBrainV2, RiskLimits
from src.brokers.paper import PaperBroker
from src.brokers.replay import ReplayBroker

def ema(prev, value, alpha=0.1):
    return value if prev is None else (alpha*value + (1-alpha)*prev)

class Context:
    def __init__(self, run_id: str, cfg: Dict[str, Any]):
        self.run_id = run_id
        self.cfg = cfg
        self.equity = 100000.0
        self.peak_equity = 100000.0
        self.daily_loss = 0.0

class FeedActor:
    def __init__(self, bus: EventBus, symbol: str, path_csv: str, max_steps: int, rate_ms: int):
        self.bus, self.symbol, self.path_csv = bus, symbol, path_csv
        self.max_steps, self.rate_ms = max_steps, rate_ms

    def run(self):
        from src.data.feature_store import stream_csv
        steps = 0
        for bar in stream_csv(self.path_csv):
            self.bus.publish(f"BAR:{self.symbol}", bar)
            steps += 1
            if self.max_steps and steps >= self.max_steps: break
            time.sleep(self.rate_ms/1000.0)

class StrategyActor:
    def __init__(self, bus: EventBus, ctx: Context, symbol: str):
        self.bus, self.ctx, self.symbol = bus, ctx, symbol
        self.ma_fast = None
        self.bb_low = None
        self.closes: List[float] = []
        bus.subscribe(f"BAR:{symbol}", self.on_bar)

    def on_bar(self, bar: Dict[str, Any]):
        c = bar["close"]; self.closes.append(c)
        self.ma_fast = ema(self.ma_fast, c, 0.15)
        # BB-low simplificada
        if len(self.closes) >= 20:
            win = self.closes[-20:]
            m = sum(win)/len(win); sd = (sum((x-m)**2 for x in win)/len(win))**0.5
            self.bb_low = m - 2*sd
        else:
            self.bb_low = c*0.995

        votes = [
            momentum.decide(bar, self.ma_fast or c),
            meanrev.decide(bar, self.bb_low or c*0.99),
        ]
        choice = allocator_bandit.choose(votes)
        decision = {
            "symbol": self.symbol, "chosen": choice["expert"], "chosen_side": choice["side"],
            "confidence": choice["confidence"], "votes": votes,
            "inputs": {"ma_fast": self.ma_fast, "bb_low": self.bb_low}
        }
        whylog.append(self.ctx.run_id, "decision", decision)
        self.bus.publish(f"DECISION:{self.symbol}", decision)

class RiskActor:
    def __init__(self, bus: EventBus, ctx: Context, limits: RiskLimits):
        self.bus, self.ctx = bus, ctx
        self.brain = RiskBrainV2(limits)
        bus.subscribe("EQUITY", self.on_equity)
        # subscrever todas decisões genéricas
        # (em um sistema maior, usar lista de símbolos a partir do cfg)
        for topic in []: pass

    def on_equity(self, payload: Dict[str, Any]):
        self.brain.update_equity(payload["dd_now"], payload["daily_loss"], payload["now_epoch"])

    def approve(self, symbol: str, conf: float, atr_norm: float, vol_q: float) -> (bool, str, float, float):
        equity = self.ctx.equity
        edge = min(max(conf - 0.5, 0.0), 0.5)  # placeholder
        winrate = 0.55
        ok, reason = self.brain.gates(atr_norm, vol_q, int(time.time()))
        if not ok: return False, reason, 0.0, 0.0
        size_frac, stop_pct = self.brain.size_and_stop(equity, edge, winrate, atr_norm)
        return True, "ok", size_frac, stop_pct

class RouterActor:
    def __init__(self, bus: EventBus, ctx: Context, broker_type: str, csv_dir: str):
        self.bus, self.ctx = bus, ctx
        if broker_type == "paper":
            self.broker = PaperBroker(fee_bps=3)
        elif broker_type == "replay":
            self.broker = ReplayBroker(csv_dir)
        else:
            self.broker = PaperBroker()
        bus.subscribe("ORDER", self.on_order)

    def on_order(self, order: Dict[str, Any]):
        # aqui apenas registramos a ordem (execução fictícia na sim)
        whylog.append(self.ctx.run_id, "order", order)

def run_pipeline(config_path: str):
    cfg = yaml.safe_load(open(config_path, encoding="utf-8"))
    run_id = f"{cfg['cluster'].get('run_id_prefix','kz')}_{int(time.time())}"
    ctx = Context(run_id, cfg)
    bus = EventBus()

    # sinalizar equity para risk a cada passo (placeholder)
    bus.publish("EQUITY", {"dd_now": 0.0, "daily_loss": 0.0, "now_epoch": int(time.time())})

    symbol = cfg["cluster"]["symbols"][0]
    tf = cfg["cluster"]["timeframe"]
    csv_dir = cfg["data"]["csv_dir"]
    path_csv = os.path.join(csv_dir, f"{symbol}_{tf}.csv")

    feed = FeedActor(bus, symbol, path_csv, cfg["cluster"]["max_steps"], cfg["cluster"]["rate_limit_ms"])
    strat = StrategyActor(bus, ctx, symbol)
    risk = RiskActor(bus, ctx, RiskLimits(
        max_drawdown=cfg["risk"]["max_drawdown"],
        daily_loss_limit=cfg["risk"]["daily_loss_limit"],
        exposure_cap_total=cfg["risk"]["exposure_cap_total"],
        per_trade_risk_cap=cfg["risk"]["per_trade_risk_cap"],
        cooldown_after_losses=cfg["risk"]["cooldown_after_losses"],
        cooldown_minutes=cfg["risk"]["cooldown_minutes"],
        vol_gate_quantile=cfg["risk"]["vol_gate_quantile"],
    ))
    router = RouterActor(bus, ctx, cfg["broker"]["adapter"], csv_dir)

    # loop simples: o feed publica e strategy->risk->router atuam.
    feed.run()
    return run_id
