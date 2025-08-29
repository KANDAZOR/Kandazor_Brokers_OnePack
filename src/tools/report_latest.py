"""
Gera relatório do whylog mais recente (último arquivo em backtests/whylogs).
"""
import glob, os
from src.telemetry.report_html import generate

def main():
    files = glob.glob(os.path.join("backtests","whylogs","*.jsonl"))
    if not files:
        print("Nenhum whylog encontrado.")
        return
    files.sort(key=os.path.getmtime, reverse=True)
    run_id = os.path.basename(files[0]).replace(".jsonl","")
    out = generate(run_id)
    print(out)

if __name__ == "__main__":
    main()
