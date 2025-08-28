"""
Feature store simples baseado em pandas para CSV.
"""
from typing import Iterator, Dict, Any, Optional
import pandas as pd

def stream_csv(path: str, limit: Optional[int]=None) -> Iterator[Dict[str, Any]]:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    if limit: df = df.head(limit)
    for _, r in df.iterrows():
        yield {"timestamp": r["timestamp"], "open": float(r["open"]), "high": float(r["high"]),
               "low": float(r["low"]), "close": float(r["close"]), "volume": float(r["volume"])}
