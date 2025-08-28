"""
RiskBrain v2: camadas de proteção para DD <= 5%.
"""
from dataclasses import dataclass
from typing import Tuple

@dataclass
class RiskLimits:
    max_drawdown: float = 0.05
    daily_loss_limit: float = 0.02
    exposure_cap_total: float = 0.20
    per_trade_risk_cap: float = 0.005
    cooldown_after_losses: int = 3
    cooldown_minutes: int = 30
    vol_gate_quantile: float = 0.9

class RiskBrainV2:
    def __init__(self, limits: RiskLimits):
        self.l = limits
        self.dd_now = 0.0
        self.daily_loss = 0.0
        self.loss_streak = 0
        self.cooldown_until = 0

    def update_equity(self, dd_now: float, daily_loss: float, now_epoch: int):
        self.dd_now = dd_now
        self.daily_loss = daily_loss
        if self.cooldown_until and now_epoch >= self.cooldown_until:
            self.cooldown_until = 0
            self.loss_streak = 0

    def on_trade_close(self, pnl: float, now_epoch: int):
        if pnl < 0:
            self.loss_streak += 1
            if self.loss_streak >= self.l.cooldown_after_losses:
                self.cooldown_until = now_epoch + self.l.cooldown_minutes*60
        else:
            self.loss_streak = 0

    def gates(self, vol_norm_now: float, vol_quantile: float, now_epoch: int) -> Tuple[bool,str]:
        if self.dd_now <= -self.l.max_drawdown:
            return False, f"gate: max DD {self.dd_now:.2%}"
        if self.daily_loss <= -self.l.daily_loss_limit:
            return False, f"gate: daily loss {self.daily_loss:.2%}"
        if self.cooldown_until and now_epoch < self.cooldown_until:
            return False, f"gate: cooldown until {self.cooldown_until}"
        if vol_quantile >= self.l.vol_gate_quantile:
            return False, f"gate: vol {vol_quantile:.2f} >= q{self.l.vol_gate_quantile}"
        return True, "ok"

    def size_and_stop(self, equity: float, edge: float, winrate: float, atr_norm: float):
        kelly = max(0.0, min((winrate*(edge))/(1.0-edge) if edge>0 and winrate>0 else 0.0, 0.25))
        size_frac = min(self.l.per_trade_risk_cap, kelly)
        stop_pct = min(0.02, max(0.005, atr_norm * 1.2))
        return size_frac, stop_pct
