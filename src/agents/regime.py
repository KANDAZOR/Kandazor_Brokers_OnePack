"""
RegimeDetector v1: tendência via slope de SMA200 + quantis de volatilidade (ATR/close).
"""
from typing import Dict, Any, List
import numpy as np

def classify(closes: List[float], atr_norm: float, vol_quantile: float) -> str:
    if len(closes) < 200: return "unknown"
    y = np.array(closes[-200:])
    x = np.arange(len(y))
    slope = float(np.polyfit(x, y, 1)[0])
    if vol_quantile > 0.9: return "vol_high"
    if slope > 0: return "trend_up"
    if slope < 0: return "trend_down"
    return "range"
