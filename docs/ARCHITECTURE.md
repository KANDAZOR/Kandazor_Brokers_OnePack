# 🏗️ Arquitetura (alto nível)
```
[CSV/Replay/API] → FeedActor(symbol)
                   ↓
            StrategyActor(symbol) ← experts (momentum/meanrev)
                   ↓
              RiskActor (global)  → gates (DD, loss dia, exposure, Kelly fracionado)
                   ↓
              RouterActor (global)→ broker adapter (paper/replay ou real autorizado)
                   ↓
       Why-Logs JSONL → Relatório HTML
```
- **EventBus** assíncrono → isolamento e backpressure.
- **RiskActor** tem **veto final**: sem passe, não há ordem.
