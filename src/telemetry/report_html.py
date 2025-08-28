"""
Gera relatório HTML simples a partir de um whylog JSONL (último run).
"""
import os, json, glob
from typing import List

def generate(run_id: str) -> str:
    log_path = os.path.join("backtests","whylogs", f"{run_id}.jsonl")
    if not os.path.exists(log_path):
        raise FileNotFoundError(log_path)
    rows = []
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    # resumo
    total = len(rows)
    decisions = [r for r in rows if r.get("type")=="decision"]
    buys = sum(1 for r in decisions if r.get("chosen_side")=="buy")
    holds = sum(1 for r in decisions if r.get("chosen_side")=="hold")
    html = f"<html><body><h2>Kandazor Report — {run_id}</h2>"
    html += f"<p>events: {total} | decisions: {len(decisions)} | buys: {buys} | holds: {holds}</p>"
    html += "<table border='1' cellspacing='0' cellpadding='4'><tr><th>ts</th><th>type</th><th>symbol</th><th>side</th><th>conf</th></tr>"
    for r in decisions[:50]:
        html += f"<tr><td>{r.get('ts')}</td><td>{r.get('type')}</td><td>{r.get('symbol')}</td><td>{r.get('chosen_side')}</td><td>{r.get('confidence')}</td></tr>"
    html += "</table></body></html>"
    out = os.path.join("reports", f"{run_id}_report.html")
    os.makedirs("reports", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out
