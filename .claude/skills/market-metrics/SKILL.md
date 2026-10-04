---
name: market-metrics
description: Price-based measurements for each holding and benchmark (returns, trend, moving averages, RSI, ATR, volatility, drawdown, 52-week range, beta, correlation, relative strength, relative volume) and the position math (invested, value, P&L, days held). Use to describe how a stock is behaving, to judge whether a move is unusual, and to explain these measures in plain English. Descriptive, never predictive.
---

# Market metrics

These numbers describe what the price has done. None of them predicts what it will do, and none
is a buy or sell signal by itself; say so whenever a reader might take it that way.

## Where the numbers come from

- `scripts/fetch_prices.py`: daily prices (Yahoo, then Stooq, then Alpha Vantage) for every
  holding, the benchmarks and each holding's industry fund (`[sector_etf]`). Which provider
  served each ticker is in `data/prices/_provenance.json`.
- `scripts/market_metrics.py`: `data/metrics/<DATE>.json`, per holding:
  returns (1 week to 1 year, year to date), 52-week high/low and position in the range,
  20/50/200-day moving averages and the trend state, 14-day RSI with a plain label, 14-day ATR,
  20- and 60-day volatility, 1-year maximum drawdown, relative volume, beta and correlation
  versus the market, excess return versus the market and the industry, and the position block
  (entry price and its source, invested, value, P&L, peak since entry, days held).
- Entry price order: your Fidelity fill price; else the sheet's estimate; else an estimate from
  market data (the close on the open date, or the next trading day's open for orders placed while
  the market was closed). Estimated entries are labelled; always say so in the report.

## How to use them in a report

- **Is today's move big?** Compare it with the ATR % or the typical daily move: "a 3% day for a
  stock that usually moves 2.4% is normal; an 8% day is about three normal days".
- **Trend in one sentence:** use `trend_state` and the distance from the 200-day average.
- **Momentum:** RSI above 70 = rose fast recently; below 30 = fell fast. Neither is a signal.
- **Risk:** volatility and maximum drawdown say how bumpy the ride has been; beta says how much
  it tends to move when the market moves (beta 1.8: about 1.8% for each 1% market move).
- **Relative strength:** excess return versus the market and the industry separates "my stock
  is special" from "my whole industry is moving".
- Always translate into dollars for his position: "a 5% drop is about $1.00 on your $19.98".

Definitions, formulas and plain-English meanings: `references/metric-definitions.md`.
