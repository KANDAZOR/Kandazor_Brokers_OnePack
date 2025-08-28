# 🛡️ Gestão de Risco v2 (objetivo: Max DD ≤ 5%)
- **Per-trade cap**: 0,5% do equity.
- **Loss diário**: 2% (kill‑switch do dia).
- **Exposure total**: 20% (portfólio).
- **Kelly fracionado** capado (máx 0.25) + **stop ATR** adaptativo.
- **Cooldown** após N perdas (padrão 3; duração 30 min).
- **Vol‑gate**: bloqueio acima do quantil alto de volatilidade.
