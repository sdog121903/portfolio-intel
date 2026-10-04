#!/usr/bin/env python3
"""Answer the first "why" question with numbers: did my stock move because of the whole
market, its industry, or something about the company itself?

Method (explained for beginners in ../references/move-attribution.md):
  stock return = alpha + b_m * market return + b_s * (sector return - market return) + residual
fitted on ~1 year of daily returns. For the latest day (and the last 5 days) the move is split into
  market part      = b_m * market return
  industry part    = b_s * (sector return - market return)
  company-specific = actual - market part - industry part
and the company-specific part is compared with how big such surprises usually are (its z-score).

Also provides decompose_price_change(): price change = change in earnings x change in the
multiple investors pay for those earnings (P/E), for "did it fall because profits fell or
because investors got less excited?".

Writes data/metrics/attribution-<DATE>.json.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402


def aligned(stock: list, market: list, sector: list) -> list:
    """Rows of (date, r_stock, r_market, r_sector) on dates all three traded."""
    m = {r["date"]: r["adj_close"] for r in market}
    s = {r["date"]: r["adj_close"] for r in sector} if sector else m
    pts = [(r["date"], r["adj_close"], m[r["date"]], s[r["date"]]) for r in stock if r["date"] in m and r["date"] in s]
    out = []
    for i in range(1, len(pts)):
        d, a, b, c = pts[i]
        _, a0, b0, c0 = pts[i - 1]
        if a0 and b0 and c0:
            out.append((d, a / a0 - 1.0, b / b0 - 1.0, c / c0 - 1.0))
    return out


def fit_two_factor(obs: list):
    """OLS of r_stock on [1, r_market, r_sector - r_market]. Returns (alpha, b_m, b_s, resid_sd)."""
    n = len(obs)
    if n < 40:
        return None
    y = [o[1] for o in obs]
    x1 = [o[2] for o in obs]
    x2 = [o[3] - o[2] for o in obs]
    my, m1, m2 = sum(y) / n, sum(x1) / n, sum(x2) / n
    s11 = sum((a - m1) ** 2 for a in x1)
    s22 = sum((b - m2) ** 2 for b in x2)
    s12 = sum((a - m1) * (b - m2) for a, b in zip(x1, x2))
    s1y = sum((a - m1) * (c - my) for a, c in zip(x1, y))
    s2y = sum((b - m2) * (c - my) for b, c in zip(x2, y))
    det = s11 * s22 - s12 * s12
    if abs(det) < 1e-18:  # sector identical to market: one-factor model
        b_m = s1y / s11 if s11 else 0.0
        b_s = 0.0
    else:
        b_m = (s1y * s22 - s2y * s12) / det
        b_s = (s2y * s11 - s1y * s12) / det
    alpha = my - b_m * m1 - b_s * m2
    resid = [c - alpha - b_m * a - b_s * b for a, b, c in zip(x1, x2, y)]
    sd = pilib.stdev(resid) or 0.0
    return alpha, b_m, b_s, sd


def attribute(window: list, model) -> dict:
    """Split the compounded return over the window (1 day or several) into parts."""
    alpha, b_m, b_s, sd = model
    actual = math.prod(1 + o[1] for o in window) - 1
    mkt = math.prod(1 + o[2] for o in window) - 1
    sec = math.prod(1 + o[3] for o in window) - 1
    market_part = b_m * mkt
    industry_part = b_s * (sec - mkt)
    company_part = actual - market_part - industry_part
    expected_sd = sd * math.sqrt(len(window)) if sd else None
    z = company_part / expected_sd if expected_sd else None
    if z is None:
        verdict = "not enough history to judge"
    elif abs(z) >= 2:
        verdict = "mostly company-specific and unusually large: look for company news"
    elif abs(company_part) >= abs(market_part) + abs(industry_part):
        verdict = "mostly company-specific, but within its normal day-to-day noise"
    else:
        verdict = "mostly explained by the market and/or its industry moving"
    pct = lambda x: round(x * 100, 2)
    return {"days": len(window), "from": window[0][0], "to": window[-1][0], "actual_pct": pct(actual),
            "market_part_pct": pct(market_part), "industry_part_pct": pct(industry_part),
            "company_specific_pct": pct(company_part), "company_specific_zscore": None if z is None else round(z, 2),
            "verdict": verdict}


def decompose_price_change(p0: float, p1: float, eps0: float, eps1: float) -> dict:
    """price = EPS x (P/E). Splits the % price change into an earnings part and a valuation part
    using log shares, so the two parts add up exactly. Needs positive EPS in both periods."""
    if min(p0, p1) <= 0 or eps0 is None or eps1 is None or eps0 <= 0 or eps1 <= 0:
        return {"ok": False, "reason": "needs positive prices and positive earnings in both periods"}
    pe0, pe1 = p0 / eps0, p1 / eps1
    total = math.log(p1 / p0)
    e_part, v_part = math.log(eps1 / eps0), math.log(pe1 / pe0)
    share = lambda part: round(part / total * 100, 1) if total else None
    return {"ok": True, "price_change_pct": round((p1 / p0 - 1) * 100, 2),
            "eps_change_pct": round((eps1 / eps0 - 1) * 100, 2), "pe_before": round(pe0, 1), "pe_after": round(pe1, 1),
            "pe_change_pct": round((pe1 / pe0 - 1) * 100, 2),
            "share_of_move_from_earnings_pct": share(e_part), "share_of_move_from_valuation_pct": share(v_part)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=None)
    ap.add_argument("--window", type=int, default=5, help="multi-day window in trading days (default 5)")
    a = ap.parse_args(argv)
    cfg = pilib.portfolio_config()
    holdings = pilib.load_holdings()
    load = lambda t: pilib.read_prices_csv(pilib.DATA / "prices" / f"{t}.csv") if (pilib.DATA / "prices" / f"{t}.csv").exists() else []
    market_t = cfg.get("benchmarks", {}).get("market", "SPY")
    market = load(market_t)
    sec_map = cfg.get("sector_etf", {})
    out = {}
    for p in holdings.get("positions", []):
        t = p["ticker"].split("-")[0]
        sec_t = sec_map.get(t, sec_map.get("default", market_t))
        stock, sector = load(t), load(sec_t)
        obs = aligned(stock, market, sector)
        model = fit_two_factor(obs[-252:])
        if not model:
            out[p["ticker"]] = {"error": "need at least 40 overlapping trading days of prices"}
            continue
        out[p["ticker"]] = {
            "market": market_t, "sector_etf": sec_t,
            "model": {"beta_market": round(model[1], 2), "beta_industry_excess": round(model[2], 2),
                      "typical_daily_company_move_pct": round(model[3] * 100, 2), "days_fitted": min(len(obs), 252)},
            "last_day": attribute(obs[-1:], model),
            f"last_{a.window}_days": attribute(obs[-a.window:], model),
        }
    date = a.date or pilib.run_date()
    path = pilib.write_json(pilib.DATA / "metrics" / f"attribution-{date}.json", out)
    print(f"attribution for {len(out)} positions -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
