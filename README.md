# Kandazor SuperGrok — **OnePack Brokers** (High-Level PRO)
_Updated: 2025-08-28 13:08:36Z_

Este pacote entrega **plano em nível de mercado** + **skeleton de código** com conectores de corretoras (modo paper/adapter),
gestão de risco v2, runtime simultâneo (actor model) e ferramentas 100% **Terminal (Windows PowerShell)**.

> **Compliance**: use **APIs oficiais** e **paper**. Não automatize GUI onde for proibido. Sem promessas de retorno.
> **Objetivo**: Max **Drawdown ≤ 5%** com explicabilidade (why‑logs) e relatório HTML.

## Quickstart (Terminal)
```powershell
# 1) Ative seu venv e aponte src
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\src"

# 2) Valide seu CSV (exemplos em data/csv)
python src\tools\csv_validate.py data\csv\SAMPLE_BTCUSDT_1m.csv

# 3) Rode uma simulação curta (actors em modo replay+paper)
python src\engine\pipeline.py --config configs\cluster.yaml

# 4) Gere o relatório do último run
python src\tools\report_latest.py
```

## Pastas
- **docs**: plano de alto nível, arquitetura, brokers, risco, comandos.
- **configs**: `cluster.yaml` (símbolos, riscos, dados, broker) e `secrets.sample.json`.
- **src**: runtime (atores), agentes (momentum/meanrev), risco v2, brokers (paper/replay + adapters stub).
- **data/csv**: exemplo de CSV com schema padrão.
- **backtests/whylogs**: onde ficam os why‑logs (auditáveis).
- **reports**: relatórios HTML gerados.

## Status
- **Pronto para sim/paper** por Terminal (sem GUI). Brokers reais via adapters **somente** quando houver chaves e autorização.
