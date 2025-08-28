"""
Why-log robusto: serializa datetime/numpy automaticamente.
"""
import os, json, datetime
from typing import Any

def _default(o: Any):
    try:
        import numpy as np
        if isinstance(o, np.generic):
            return o.item()
    except Exception:
        pass
    if hasattr(o, "isoformat"):
        return o.isoformat()
    return str(o)

def path_for(run_id: str) -> str:
    base = os.path.join("backtests","whylogs")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, f"{run_id}.jsonl")

def append(run_id: str, event_type: str, payload: dict):
    rec = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "type": event_type, **payload}
    with open(path_for(run_id), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, default=_default) + "\n")
