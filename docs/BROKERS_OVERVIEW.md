# 🌐 Brokers (Adapters) — visão unificada
**Contrato base** (`src/brokers/base.py`):
- `name()`
- `fetch_ohlcv(symbol, timeframe, limit)`
- `place_order(symbol, side, qty, price=None, order_type="market")`
- `cancel_order(order_id)`
- `get_balance()`
- `get_positions()`

**Incluídos neste pacote**
- `PaperBroker` — simulação determinística (sem taxas).
- `ReplayBroker` — reexecuta barras de CSV (data/csv).
- Stubs opcionais (exigem libs externas e chaves): `BinanceCCXTAdapter`, `OKXCCXTAdapter`, `IBInsyncAdapter`, `MT5Adapter`.
> Por padrão, **não** instalamos ccxt/ib_insync/MetaTrader5; os adapters apenas ilustram a integração.
