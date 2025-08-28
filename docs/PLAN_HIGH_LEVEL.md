# 🧠 Plano em Nível de Mercado — Kandazor SuperGrok (vNext+)
**Norte**: organismo digital de trading explicável, resiliente e escalável (**risk‑first**), com **Max DD ≤ 5%**, logs auditáveis e operação **terminal‑first**.

## Estratégia de Produto
- **Segurança**: risk‑budget + circuit‑breakers → confiança antes de escala.
- **Explicabilidade**: why‑logs por decisão → relatórios HTML automáticos.
- **Escalabilidade**: actor system (Feed/Strategy/Risk/Router) → +símbolos sem reescrever core.
- **Portabilidade**: adapters de broker isolados (paper → real), *feature store* por contrato.
- **Evolutivo**: CSV → API (paper) → painel (Streamlit) → ML/Regime.

## Diferenciais vs. mercado
- **RiskBrain v2** (cooldown, vol‑gate, Kelly capado) e **Regime v1** (SMA200 slope + vol quantis).
- **Contrato de brokers unificado**: `place_order/cancel/fetch_ohlcv/get_balance/get_positions`.
- **Operação 99% terminal**: scripts para validação, canário e relatório.
- **Qualidade**: CSV validator, healthbeat, model card, checklist de release.
