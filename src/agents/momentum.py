"""
Expert Momentum: BUY quando preço acima da média curta.
"""
from typing import Dict, Any

def decide(bar: Dict[str, Any], ma_fast: float) -> Dict[str, Any]:
    side = "buy" if bar["close"] > ma_fast else "hold"
    conf = 0.6 if side=="buy" else 0.0
    return {"expert":"momentum", "side":side, "confidence":conf, "why":{"price":bar["close"], "ma_fast":ma_fast}}
