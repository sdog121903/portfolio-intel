#!/usr/bin/env python3
"""Download daily prices for every holding plus the benchmark and sector ETFs.

Writes data/prices/<TICKER>.csv (date, open, high, low, close, adj_close, volume) and
data/prices/_provenance.json (which provider answered, when, how many rows).

Provider chain, tried in order until one works:
  1. yahoo        query1.finance.yahoo.com chart API   (free, unofficial, adjusted closes)
  2. stooq        stooq.com daily CSV                  (free, unofficial)
  3. alphavantage www.alphavantage.co                  (free key in ALPHAVANTAGE_API_KEY; compact = ~100 days)
These are unofficial or rate-limited sources: the report must say which one was used.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402


# ---------------------------------------------------------------- parsers (pure, unit-tested)
def parse_yahoo_chart(raw: bytes) -> list:
    data = json.loads(raw)
    res = (data.get("chart") or {}).get("result") or []
    if not res:
        err = (data.get("chart") or {}).get("error")
        raise ValueError(f"yahoo: no result ({err})")
    res = res[0]
    ts = res.get("timestamp") or []
    q = (res.get("indicators", {}).get("quote") or [{}])[0]
    adj = (res.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose")
    rows = []
    for i, t in enumerate(ts):
        close = q.get("close", [None] * len(ts))[i]
        if close is None:
            continue
        rows.append({
            "date": dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(),
            "open": q.get("open", [None] * len(ts))[i],
            "high": q.get("high", [None] * len(ts))[i],
            "low": q.get("low", [None] * len(ts))[i],
            "close": close,
            "adj_close": adj[i] if adj and adj[i] is not None else close,
            "volume": q.get("volume", [None] * len(ts))[i],
        })
    return dedupe(rows)


def parse_stooq_csv(raw: bytes) -> list:
    text = raw.decode("utf-8", errors="replace")
    if not text.lower().startswith("date"):
        raise ValueError("stooq: unexpected response (no CSV header)")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        try:
            close = float(r["Close"])
        except (KeyError, ValueError):
            continue
        rows.append({"date": r["Date"], "open": float(r["Open"]), "high": float(r["High"]),
                     "low": float(r["Low"]), "close": close, "adj_close": close,
                     "volume": float(r.get("Volume") or 0)})
    return dedupe(rows)


def parse_alphavantage(raw: bytes) -> list:
    data = json.loads(raw)
    series = data.get("Time Series (Daily)")
    if not series:
        raise ValueError(f"alphavantage: {data.get('Note') or data.get('Information') or data.get('Error Message')}")
    rows = []
    for d, v in series.items():
        close = float(v["4. close"])
        rows.append({"date": d, "open": float(v["1. open"]), "high": float(v["2. high"]),
                     "low": float(v["3. low"]), "close": close, "adj_close": close,
                     "volume": float(v["5. volume"])})
    return dedupe(rows)


def dedupe(rows: list) -> list:
    by_date = {r["date"]: r for r in rows}
    return [by_date[k] for k in sorted(by_date)]


# ---------------------------------------------------------------- providers
def fetch_yahoo(ticker: str, rng: str) -> list:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?range={rng}&interval=1d&includeAdjustedClose=true&events=div%2Csplits")
    return parse_yahoo_chart(pilib.http_get(url))


def fetch_stooq(ticker: str, rng: str) -> list:
    url = f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"
    rows = parse_stooq_csv(pilib.http_get(url))
    keep = {"1y": 400, "2y": 800, "5y": 2000}.get(rng, 800)
    return rows[-keep:]


def fetch_alphavantage(ticker: str, rng: str) -> list:
    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not key:
        raise RuntimeError("alphavantage: ALPHAVANTAGE_API_KEY not set")
    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}"
           f"&outputsize=compact&apikey={key}")
    return parse_alphavantage(pilib.http_get(url))


PROVIDERS = {"yahoo": fetch_yahoo, "stooq": fetch_stooq, "alphavantage": fetch_alphavantage}


def fetch_one(ticker: str, rng: str, order: list) -> tuple:
    errors = []
    for name in order:
        try:
            rows = PROVIDERS[name](ticker, rng)
            if len(rows) < 5:
                raise ValueError(f"{name}: only {len(rows)} rows")
            return name, rows, errors
        except Exception as e:
            errors.append(f"{name}: {e}")
            time.sleep(0.5)
    return None, [], errors


def universe(cfg: dict, holdings: dict) -> list:
    held = [p["ticker"].split("-")[0] for p in holdings.get("positions", [])]
    sec = cfg.get("sector_etf", {})
    tickers = held + list(cfg.get("benchmarks", {}).values())
    tickers += [sec.get(t, sec.get("default", "SPY")) for t in held]
    seen, out = set(), []
    for t in tickers:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tickers", nargs="*", help="override the ticker list")
    ap.add_argument("--providers", default="yahoo,stooq,alphavantage")
    a = ap.parse_args(argv)
    cfg = pilib.portfolio_config()
    rng = cfg.get("run", {}).get("price_history_range", "2y")
    tickers = a.tickers or universe(cfg, pilib.load_holdings())
    order = [p.strip() for p in a.providers.split(",") if p.strip()]
    prov_path = pilib.DATA / "prices" / "_provenance.json"
    provenance = pilib.read_json(prov_path) if prov_path.exists() else {}
    failed = []
    for t in tickers:
        name, rows, errors = fetch_one(t, rng, order)
        if not name:
            failed.append(t)
            provenance[t] = {"provider": None, "errors": errors, "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
            print(f"FAILED {t}: {' | '.join(errors)}")
            continue
        pilib.write_prices_csv(pilib.DATA / "prices" / f"{t}.csv", rows)
        provenance[t] = {"provider": name, "rows": len(rows), "first_date": rows[0]["date"],
                         "last_date": rows[-1]["date"], "errors_before_success": errors,
                         "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        print(f"{t}: {len(rows)} rows from {name}, last {rows[-1]['date']}")
    pilib.write_json(prov_path, provenance)
    return 1 if failed and len(failed) == len(tickers) else 0


if __name__ == "__main__":
    sys.exit(main())
