"""
MT5Adapter (stub): integra MetaTrader 5 via pacote MetaTrader5 (opcional).
Requer: pip install MetaTrader5
"""
from typing import List, Dict, Any, Optional
try:
    import MetaTrader5 as mt5  # type: ignore
except Exception:
    mt5 = None

class MT5Adapter:
    def __init__(self, login: int, password: str, server: str):
        if mt5 is None:
            raise RuntimeError("MetaTrader5 não instalado. pip install MetaTrader5")
        mt5.initialize(login=login, password=password, server=server)

    def name(self) -> str: return "mt5"
    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict[str, Any]]: return []
    def place_order(self, symbol: str, side: str, qty: float, price: Optional[float]=None, order_type: str="market") -> Dict[str, Any]: return {}
    def cancel_order(self, order_id: str) -> bool: return True
    def get_balance(self) -> Dict[str, Any]: return {}
    def get_positions(self) -> List[Dict[str, Any]]: return []
