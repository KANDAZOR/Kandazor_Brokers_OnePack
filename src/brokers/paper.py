"""
PaperBroker: simulação simples de ordens e posições (sem slippage real).
Para fins de pesquisa e testes em terminal.
"""
from typing import List, Dict, Any, Optional
import time, itertools

class PaperBroker:
    def __init__(self, fee_bps: float = 0.0):
        self._orders = {}
        self._positions = {}  # symbol -> qty, avg_price
        self._balance = {"equity": 100000.0, "cash": 100000.0}
        self._seq = itertools.count(1)
        self.fee_bps = fee_bps

    def name(self) -> str: return "paper"

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict[str, Any]]:
        # Esse broker não provê dados; use ReplayBroker ou Feed de CSV.
        return []

    def place_order(self, symbol: str, side: str, qty: float, price: Optional[float]=None, order_type: str="market") -> Dict[str, Any]:
        oid = f"paper_{next(self._seq)}"
        ts = int(time.time()*1000)
        px = float(price) if price is not None else 0.0
        fee = 0.0
        if order_type == "market" and px == 0.0:
            # para sim simples, preço será registrado pelo caller (engine) após execução
            pass
        # registrar posição de forma simplificada
        pos = self._positions.get(symbol, {"qty":0.0, "avg_price":0.0})
        if side.lower() == "buy":
            new_qty = pos["qty"] + qty
            new_avg = (pos["avg_price"]*pos["qty"] + (px*qty)) / new_qty if new_qty>0 else 0.0
            self._positions[symbol] = {"qty": new_qty, "avg_price": new_avg}
        elif side.lower() == "sell":
            new_qty = pos["qty"] - qty
            self._positions[symbol] = {"qty": new_qty, "avg_price": pos["avg_price"] if new_qty>0 else 0.0}
        order = {"id": oid, "symbol": symbol, "side": side, "qty": qty, "price": px, "type": order_type, "ts": ts, "fee": fee}
        self._orders[oid] = order
        return order

    def cancel_order(self, order_id: str) -> bool:
        return self._orders.pop(order_id, None) is not None

    def get_balance(self) -> Dict[str, Any]:
        return dict(self._balance)

    def get_positions(self) -> List[Dict[str, Any]]:
        out = []
        for s, p in self._positions.items():
            out.append({"symbol": s, **p})
        return out
