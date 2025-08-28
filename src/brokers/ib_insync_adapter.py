"""
IBInsyncAdapter (stub): integra Interactive Brokers (TWS/Gateway) via ib_insync (opcional).
Requer: pip install ib_insync
"""
from typing import List, Dict, Any, Optional
try:
    from ib_insync import IB, Stock, MarketOrder  # type: ignore
except Exception:
    IB = None

class IBInsyncAdapter:
    def __init__(self, host="127.0.0.1", port=7497, clientId=1):
        if IB is None:
            raise RuntimeError("ib_insync não instalado. pip install ib_insync")
        self.ib = IB()
        self.ib.connect(host, port, clientId=clientId)

    def name(self) -> str: return "ib"
    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict[str, Any]]: return []
    def place_order(self, symbol: str, side: str, qty: float, price: Optional[float]=None, order_type: str="market") -> Dict[str, Any]:
        contract = Stock(symbol, 'SMART', 'USD')
        order = MarketOrder('BUY' if side=='buy' else 'SELL', qty)
        trade = self.ib.placeOrder(contract, order)
        return {"id": str(trade.order.orderId), "info": "submitted"}
    def cancel_order(self, order_id: str) -> bool: return True
    def get_balance(self) -> Dict[str, Any]: return {}
    def get_positions(self) -> List[Dict[str, Any]]: return []
