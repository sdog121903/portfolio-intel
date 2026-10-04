# Data behind the reports

| Folder | Written by | Contents |
|---|---|---|
| `holdings/` | the agent (raw sheet rows) and `load_holdings.py` | `raw-<DATE>.json`, `<DATE>.json` |
| `prices/` | `fetch_prices.py` | daily price CSVs (not committed) and `_provenance.json` |
| `metrics/` | metrics, attribution, portfolio and rules scripts | `<DATE>.json`, `attribution-`, `portfolio-`, `rules-<DATE>.json` |
| `filings/` | `fetch_edgar.py` | `<DATE>.json`: recent SEC filings and parsed insider trades |
| `fundamentals/` | `fetch_fundamentals.py` | `<TICKER>.json`: quarterly results from SEC XBRL |
| `research/` | holding-researcher agents | `<DATE>/<TICKER>.json`: sourced evidence per stock |
| `snapshots/` | `run_daily_data.py` | `<DATE>-pipeline.json`: which steps worked |
