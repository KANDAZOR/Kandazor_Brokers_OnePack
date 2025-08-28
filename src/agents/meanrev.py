"""
Expert Mean-Reversion: HOLD/BUY perto de BB-low (simplificado).
"""
from typing import Dict, Any

def decide(bar: Dict[str, Any], bb_low: float) -> Dict[str, Any]:
    side = "hold" if bar["close"] > bb_low else "buy"
    conf = 0.0 if side=="hold" else 0.55
    return {"expert":"meanrev", "side":side, "confidence":conf, "why":{"price":bar["close"], "bb_low":bb_low}}
