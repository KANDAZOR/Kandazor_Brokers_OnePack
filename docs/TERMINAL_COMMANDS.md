# 💻 Comandos (Windows PowerShell)
```powershell
# ativar ambiente e sys.path
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"

# validar CSVs
python src\tools\csv_validate.py data\csv\SAMPLE_BTCUSDT_1m.csv

# rodar pipeline (sim/replay + paper)
python src\engine\pipeline.py --config configs\cluster.yaml

# gerar relatório do último whylog
python src\tools\report_latest.py

# tail do whylog mais recente (compatível)
$last = Get-ChildItem .\backtests\whylogs\*.jsonl | Sort-Object LastWriteTime -Descending | Select -First 1
if ($last) { Get-Content $last.FullName -Wait }
```
