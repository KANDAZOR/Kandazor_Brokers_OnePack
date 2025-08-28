"""
BinanceCCXTAdapter (stub): ilustra a integração via CCXT (instalação opcional).
Requer: pip install ccxt
Use apenas modos permitidos (ex.: testnet/paper quando disponível).
"""
from typing import List, Dict, Any, Optional
try:
    import ccxt  # type: ignore
except Exception:
    ccxt = None

class BinanceCCXTAdapter:
    def __init__(self, apiKey: str="", secret: str=""):
        if ccxt is None:
            raise RuntimeError("ccxt não está instalado. Use: pip install ccxt")
        self.exchange = ccxt.binance({"apiKey": apiKey, "secret": secret})

    def name(self) -> str: return "binance_ccxt"

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict[str, Any]]:
        bars = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        out = []
        for ts, o, h, l, c, v in bars:
            out.append({"timestamp": ts, "open": o, "high": h, "low": l, "close": c, "volume": v})
        return out

    def place_order(self, symbol: str, side: str, qty: float, price: Optional[float]=None, order_type: str="market") -> Dict[str, Any]:
        if order_type == "market":
            o = self.exchange.create_order(symbol, "market", side, qty)
        else:
            o = self.exchange.create_order(symbol, "limit", side, qty, price)
        return o

    def cancel_order(self, order_id: str) -> bool:
        # Necessita symbol; exemplo ilustrativo.
        return True

    def get_balance(self) -> Dict[str, Any]:
        return self.exchange.fetch_balance()

    def get_positions(self) -> List[Dict[str, Any]]:
        return []
