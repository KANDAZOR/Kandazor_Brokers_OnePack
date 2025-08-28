"""
Healthbeat: escreve um JSON por ciclo com métricas de latência/estado.
"""
import os, json, time

def write(run_id: str, lag_ms: float, whylog_ms: float, status: str="ok"):
    path = os.path.join("backtests","whylogs", f"{run_id}.health.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rec = {"ts": int(time.time()*1000), "lag_ms": lag_ms, "whylog_ms": whylog_ms, "status": status}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f)
