"""
ReplayBroker: lê CSVs para simular 'ticks/barras' e permite fills fictícios.
Use para backtests simples acoplados ao actor system.
"""
from typing import List, Dict, Any
import os, csv, datetime

class ReplayBroker:
    def __init__(self, csv_dir: str):
        self.csv_dir = csv_dir

    def name(self) -> str: return "replay"

    def _path(self, symbol: str, timeframe: str) -> str:
        return os.path.join(self.csv_dir, f"{symbol}_{timeframe}.csv")

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List[Dict[str, Any]]:
        path = self._path(symbol, timeframe)
        data = []
        with open(path, newline='', encoding='utf-8') as f:
            rdr = csv.DictReader(f)
            rows = list(rdr)[-limit:]
            for r in rows:
                data.append({
                    "timestamp": r["timestamp"],
                    "open": float(r["open"]), "high": float(r["high"]),
                    "low": float(r["low"]), "close": float(r["close"]),
                    "volume": float(r["volume"]),
                })
        return data

    # Execução em replay é controlada pela engine; adapters reais implementam place_order.
    def place_order(self, *args, **kwargs): 
        return {"info":"replay adapter does not execute orders; engine simula fills"}

    def cancel_order(self, order_id: str) -> bool: return True
    def get_balance(self) -> Dict[str, Any]: return {"equity": 100000.0, "cash": 100000.0}
    def get_positions(self) -> List[Dict[str, Any]]: return []
