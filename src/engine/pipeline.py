"""
Pipeline CLI para rodar a simulação/replay em terminal.
"""
import argparse
from runtime.actors import run_pipeline
from src.telemetry.report_html import generate
import os, glob

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="configs/cluster.yaml")
    args = ap.parse_args()
    run_id = run_pipeline(args.config)
    # gerar relatório
    out = generate(run_id)
    print(out)

if __name__ == "__main__":
    main()
