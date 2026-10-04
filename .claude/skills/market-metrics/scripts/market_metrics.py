#!/usr/bin/env python3
"""Compute descriptive market metrics for every open position.

Reads data/prices/*.csv and the latest holdings file; writes data/metrics/<DATE>.json.
Every metric is DESCRIPTIVE (what the price has done), never a prediction. The definitions,
and how to explain each one to a beginner, are in ../references/metric-definitions.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

TRADING_DAYS = 252


# ---------------------------------------------------------------- building blocks (unit-tested)
def daily_returns(closes: list) -> list:
    return [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes)) if closes[i - 1]]


def sma(values: list, n: int):
    return sum(values[-n:]) / n if len(values) >= n else None


def rsi_wilder(closes: list, n: int = 14):
    if len(closes) < n + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(max(-ch, 0.0))
    avg_g = sum(gains[:n]) / n
    avg_l = sum(losses[:n]) / n
    for i in range(n, len(gains)):
        avg_g = (avg_g * (n - 1) + gains[i]) / n
        avg_l = (avg_l * (n - 1) + losses[i]) / n
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return 100.0 - 100.0 / (1.0 + rs)


def atr_wilder(rows: list, n: int = 14):
    if len(rows) < n + 1:
        return None
    trs = []
    for i in range(1, len(rows)):
        h, l, pc = rows[i]["high"], rows[i]["low"], rows[i - 1]["close"]
        if h is None or l is None or pc is None:
            continue
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    if len(trs) < n:
        return None
    atr = sum(trs[:n]) / n
    for tr in trs[n:]:
        atr = (atr * (n - 1) + tr) / n
    return atr


def annualised_vol(rets: list, n: int):
    window = rets[-n:]
    sd = pilib.stdev(window) if len(window) >= max(10, n // 2) else None
    return None if sd is None else sd * (TRADING_DAYS ** 0.5) * 100.0


def max_drawdown(closes: list):
    peak, mdd = None, 0.0
    for c in closes:
        peak = c if peak is None or c > peak else peak
        mdd = min(mdd, c / peak - 1.0)
    return mdd * 100.0


def aligned_returns(a_rows: list, b_rows: list, n: int) -> tuple:
    """Daily returns of A and B on the dates both traded, last n observations."""
    b_map = {r["date"]: r["adj_close"] for r in b_rows}
    pairs = [(r["date"], r["adj_close"], b_map[r["date"]]) for r in a_rows if r["date"] in b_map]
    ra, rb = [], []
    for i in range(1, len(pairs)):
        if pairs[i - 1][1] and pairs[i - 1][2]:
            ra.append(pairs[i][1] / pairs[i - 1][1] - 1.0)
            rb.append(pairs[i][2] / pairs[i - 1][2] - 1.0)
    return ra[-n:], rb[-n:]


def beta_and_corr(ra: list, rb: list):
    if len(ra) < 30:
        return None, None
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / (len(ra) - 1)
    va = sum((x - ma) ** 2 for x in ra) / (len(ra) - 1)
    vb = sum((y - mb) ** 2 for y in rb) / (len(rb) - 1)
    beta = cov / vb if vb else None
    corr = cov / ((va * vb) ** 0.5) if va and vb else None
    return beta, corr


def window_return(rows: list, days: int):
    if len(rows) < 2:
        return None
    last = rows[-1]
    target = pilib.parse_date(last["date"]) - dt.timedelta(days=days)
    base = None
    for r in rows:
        if pilib.parse_date(r["date"]) <= target:
            base = r
        else:
            break
    return pilib.pct_change(last["adj_close"], base["adj_close"]) if base else None


def ytd_return(rows: list):
    last = rows[-1]
    year = last["date"][:4]
    prior = [r for r in rows if r["date"][:4] < year]
    return pilib.pct_change(last["adj_close"], prior[-1]["adj_close"]) if prior else None


def trend_state(close, s50, s200):
    if None in (close, s50, s200):
        return "not enough history"
    above50, above200 = close > s50, close > s200
    if above50 and above200 and s50 > s200:
        return "uptrend (price above its 50- and 200-day averages, and the 50 is above the 200)"
    if not above50 and not above200 and s50 < s200:
        return "downtrend (price below its 50- and 200-day averages, and the 50 is below the 200)"
    if above200 and not above50:
        return "pullback inside a longer uptrend (below the 50-day, still above the 200-day)"
    if above50 and not above200:
        return "short-term bounce inside a longer downtrend (above the 50-day, below the 200-day)"
    return "mixed / turning"


def rsi_state(v):
    if v is None:
        return "n/a"
    if v >= 70:
        return "hot (RSI 70+: rose fast recently; often cools off, not a sell signal by itself)"
    if v <= 30:
        return "washed out (RSI 30 or less: fell fast recently; not a buy signal by itself)"
    return "neutral"


# ---------------------------------------------------------------- per-ticker metrics
def ticker_metrics(t: str, rows: list, market: list, sector: list, position: dict) -> dict:
    closes = [r["adj_close"] for r in rows]
    last, prev = rows[-1], rows[-2] if len(rows) > 1 else None
    year = rows[-TRADING_DAYS:]
    hi = max(r["high"] or r["close"] for r in year)
    lo = min(r["low"] or r["close"] for r in year)
    s20, s50, s200 = sma([r["close"] for r in rows], 20), sma([r["close"] for r in rows], 50), sma([r["close"] for r in rows], 200)
    rets = daily_returns(closes)
    vols = [r["volume"] for r in rows if r["volume"] is not None]
    rel_vol = (vols[-1] / (sum(vols[-21:-1]) / 20)) if len(vols) >= 21 and sum(vols[-21:-1]) else None
    rm, rb = aligned_returns(rows, market, TRADING_DAYS) if market else ([], [])
    beta, _ = beta_and_corr(rm, rb)
    rm60, rb60 = aligned_returns(rows, market, 60) if market else ([], [])
    _, corr60 = beta_and_corr(rm60, rb60)
    rsi = rsi_wilder([r["close"] for r in rows])
    atr = atr_wilder(rows)

    def rel(days, bench):
        a, b = window_return(rows, days), window_return(bench, days) if bench else None
        return None if a is None or b is None else a - b

    out = {
        "ticker": t,
        "as_of": last["date"],
        "close": pilib.r(last["close"]),
        "prev_close": pilib.r(prev["close"]) if prev else None,
        "day_change_pct": pilib.r(pilib.pct_change(last["adj_close"], prev["adj_close"])) if prev else None,
        "returns_pct": {k: pilib.r(v) for k, v in {
            "1w": window_return(rows, 7), "1m": window_return(rows, 30), "3m": window_return(rows, 91),
            "6m": window_return(rows, 182), "ytd": ytd_return(rows), "1y": window_return(rows, 365)}.items()},
        "high_52w": pilib.r(hi), "low_52w": pilib.r(lo),
        "pct_below_52w_high": pilib.r(pilib.pct_change(last["close"], hi)),
        "position_in_52w_range_pct": pilib.r((last["close"] - lo) / (hi - lo) * 100) if hi > lo else None,
        "sma": {"20": pilib.r(s20), "50": pilib.r(s50), "200": pilib.r(s200)},
        "pct_vs_sma": {k: pilib.r(pilib.pct_change(last["close"], v)) for k, v in {"20": s20, "50": s50, "200": s200}.items()},
        "trend_state": trend_state(last["close"], s50, s200),
        "rsi_14": pilib.r(rsi, 1), "rsi_state": rsi_state(rsi),
        "atr_14": pilib.r(atr), "atr_pct_of_price": pilib.r(atr / last["close"] * 100) if atr else None,
        "volatility_ann_pct": {"20d": pilib.r(annualised_vol(rets, 20), 1), "60d": pilib.r(annualised_vol(rets, 60), 1)},
        "max_drawdown_1y_pct": pilib.r(max_drawdown([r["adj_close"] for r in year])),
        "relative_volume_vs_20d": pilib.r(rel_vol),
        "beta_1y_vs_market": pilib.r(beta),
        "corr_60d_vs_market": pilib.r(corr60),
        "excess_return_pct": {
            "vs_market_1m": pilib.r(rel(30, market)), "vs_market_3m": pilib.r(rel(91, market)),
            "vs_sector_1m": pilib.r(rel(30, sector)), "vs_sector_3m": pilib.r(rel(91, sector)),
        },
        "data_quality": {"rows": len(rows), "first_date": rows[0]["date"],
                          "warnings": [] if len(rows) >= 210 else ["fewer than ~210 trading days: 200-day average and 1-year figures may be missing"]},
    }
    if position:
        out["position"] = position_metrics(position, rows)
    return out


def estimate_entry(open_date, rows: list):
    """Entry price when the sheet has none (no fill price, or the sheet's estimate came through as #N/A).

    - open date is a trading day         -> that day's close
    - weekend / holiday (market closed)  -> next trading day's OPEN, because orders placed while the
                                            market is closed fill near the next open
    - open date after the latest price   -> latest close, flagged: the order may not have filled yet
    """
    if not open_date or not rows:
        return None, None
    same = [r for r in rows if r["date"] == open_date]
    if same:
        return same[0]["close"], f"estimated from market data: close on {open_date}"
    later = [r for r in rows if r["date"] > open_date]
    if later:
        r = later[0]
        return (r["open"] or r["close"]), f"estimated from market data: open on {r['date']} (next trading day)"
    return rows[-1]["close"], (f"estimated from market data: latest close {rows[-1]['date']} "
                               "(order may not be filled yet)")


def position_metrics(p: dict, rows: list) -> dict:
    last = rows[-1]["close"]
    sign = -1 if p.get("side") == "Short" else 1
    entry = p.get("entry_price")
    source = p.get("entry_price_source")
    if not entry:
        entry, est_source = estimate_entry(p.get("open_date"), rows)
        if entry:
            source = est_source
    res = {"shares": p["shares"], "side": p.get("side", "Long"), "entry_price": pilib.r(entry) if entry else entry,
           "entry_price_source": source, "open_date": p.get("open_date"),
           "fees": p.get("fees", 0.0)}
    if entry:
        invested = entry * p["shares"]
        value = last * p["shares"]
        pnl = sign * (value - invested) - (p.get("fees") or 0.0)
        res.update({"invested": pilib.r(invested), "value": pilib.r(value), "pnl": pilib.r(pnl),
                    "pnl_pct": pilib.r(pnl / invested * 100 if invested else None)})
    od = p.get("open_date")
    if od:
        since = [r for r in rows if r["date"] >= od]
        if since:
            peak = max(r["close"] for r in since)
            trough = min(r["close"] for r in since)
            res.update({"peak_close_since_entry": pilib.r(peak), "trough_close_since_entry": pilib.r(trough),
                        "drawdown_from_peak_since_entry_pct": pilib.r(pilib.pct_change(last, peak))})
        res["days_held"] = max(0, pilib.days_between(od, rows[-1]["date"]))
    return res


def load_rows(t: str):
    path = pilib.DATA / "prices" / f"{t}.csv"
    return pilib.read_prices_csv(path) if path.exists() else []


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=None)
    a = ap.parse_args(argv)
    cfg = pilib.portfolio_config()
    holdings = pilib.load_holdings()
    market_t = cfg.get("benchmarks", {}).get("market", "SPY")
    market = load_rows(market_t)
    sec_map = cfg.get("sector_etf", {})
    results, missing = {}, []
    for p in holdings.get("positions", []):
        t = p["ticker"].split("-")[0]
        rows = load_rows(t)
        if len(rows) < 3:
            missing.append(t)
            continue
        sector = load_rows(sec_map.get(t, sec_map.get("default", market_t)))
        results[p["ticker"]] = ticker_metrics(t, rows, market, sector, p)
        results[p["ticker"]]["sector_etf"] = sec_map.get(t, sec_map.get("default", market_t))
    bench = {}
    for name, t in cfg.get("benchmarks", {}).items():
        rows = load_rows(t)
        if len(rows) > 2:
            bench[t] = ticker_metrics(t, rows, market, None, None)
    date = a.date or pilib.run_date()
    out = {"generated_for": date, "market_benchmark": market_t, "positions": results,
           "benchmarks": bench, "missing_prices": missing}
    path = pilib.write_json(pilib.DATA / "metrics" / f"{date}.json", out)
    print(f"metrics for {len(results)} positions -> {path}" + (f"; missing prices: {missing}" if missing else ""))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
