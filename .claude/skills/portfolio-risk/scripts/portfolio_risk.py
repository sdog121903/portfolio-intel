#!/usr/bin/env python3
"""Portfolio-level risk, computed on today's holdings (current weights, past prices).

Outputs data/metrics/portfolio-<DATE>.json:
  weights_pct                 share of total market value per position
  concentration               HHI and "effective number of positions" (1 / HHI)
  theme_exposure_pct          from config [themes]; one position can belong to several themes
  sector_exposure_pct         from config [sectors]; each position belongs to one broad sector
  goals_check                 plain facts to compare with the owner's stated goals in config [goals]
  correlation_60d             pairwise correlation of daily returns, plus the average
  volatility_ann_pct          of the current-weights portfolio over the past year
  beta_vs_market              weighted average of position betas
  var_95_1d / cvar_95_1d      historical one-day Value at Risk and Expected Shortfall (% and $)
  max_drawdown_1y_pct         of the current-weights portfolio over the past year
  shocks                      rough beta-based estimates for market moves of -5% and -10%

All of this describes the past behaviour of today's mix. It is not a forecast.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402


def returns_by_date(rows: list) -> dict:
    out = {}
    for i in range(1, len(rows)):
        a, b = rows[i - 1]["adj_close"], rows[i]["adj_close"]
        if a:
            out[rows[i]["date"]] = b / a - 1.0
    return out


def corr(x: list, y: list):
    n = len(x)
    if n < 20:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5 if sxx and syy else None


def hist_var(rets: list, level: float = 0.95) -> tuple:
    if len(rets) < 60:
        return None, None
    s = sorted(rets)
    k = max(0, int((1 - level) * len(s)) - 1)
    var = -s[k]
    tail = s[: k + 1]
    return var * 100, -sum(tail) / len(tail) * 100


def sector_exposure(weights: dict, sectors: dict) -> dict:
    out = {}
    for t, w in weights.items():
        sec = sectors.get(t.split("-")[0], "Unclassified")
        out[sec] = out.get(sec, 0.0) + w * 100
    return {k: pilib.r(v, 1) for k, v in sorted(out.items(), key=lambda kv: -kv[1])}


def compute(values: dict, series: dict, betas: dict, themes: dict, sectors: dict | None = None,
            goals: list | None = None) -> dict:
    total = sum(values.values())
    weights = {t: v / total for t, v in values.items()} if total else {}
    hhi = sum(w * w for w in weights.values())
    theme_exp = {}
    for t, w in weights.items():
        for th in themes.get(t.split("-")[0], ["Unclassified"]):
            theme_exp[th] = theme_exp.get(th, 0.0) + w * 100
    sector_exp = sector_exposure(weights, sectors or {})
    common = sorted(set.intersection(*(set(s) for s in series.values()))) if series else []
    last_year = common[-252:]
    port = [sum(weights[t] * series[t][d] for t in weights if t in series) for d in last_year]
    vol = pilib.stdev(port) * (252 ** 0.5) * 100 if len(port) > 20 else None
    var, cvar = hist_var(port)
    level, peak, mdd = 1.0, 1.0, 0.0
    for r_ in port:
        level *= 1 + r_
        peak = max(peak, level)
        mdd = min(mdd, level / peak - 1)
    tick = [t for t in weights if t in series]
    last60 = common[-60:]
    pairs, matrix = [], {}
    for i, a in enumerate(tick):
        matrix[a] = {}
        for b in tick:
            c = corr([series[a][d] for d in last60], [series[b][d] for d in last60])
            matrix[a][b] = pilib.r(c)
        for b in tick[i + 1:]:
            c = corr([series[a][d] for d in last60], [series[b][d] for d in last60])
            if c is not None:
                pairs.append(c)
    beta = sum(weights[t] * betas[t] for t in weights if betas.get(t) is not None) if betas else None
    return {
        "total_value": pilib.r(total), "weights_pct": {t: pilib.r(w * 100, 1) for t, w in weights.items()},
        "concentration": {"hhi": pilib.r(hhi, 3), "effective_number_of_positions": pilib.r(1 / hhi, 1) if hhi else None},
        "theme_exposure_pct": {k: pilib.r(v, 1) for k, v in sorted(theme_exp.items(), key=lambda kv: -kv[1])},
        "sector_exposure_pct": sector_exp,
        "goals_check": {"stated_goals": goals or [],
                        "technology_share_pct": sector_exp.get("Technology", 0.0),
                        "largest_theme": max(theme_exp, key=theme_exp.get) if theme_exp else None,
                        "largest_theme_share_pct": pilib.r(max(theme_exp.values()), 1) if theme_exp else None,
                        "note": "Facts to compare with the owner's goals; never a recommendation to buy or sell."},
        "correlation_60d": matrix, "avg_pairwise_correlation_60d": pilib.r(sum(pairs) / len(pairs)) if pairs else None,
        "volatility_ann_pct": pilib.r(vol, 1), "beta_vs_market": pilib.r(beta),
        "var_95_1d_pct": pilib.r(var), "cvar_95_1d_pct": pilib.r(cvar),
        "var_95_1d_usd": pilib.r(var / 100 * total) if var is not None else None,
        "max_drawdown_1y_pct": pilib.r(mdd * 100) if port else None,
        "days_used": len(port),
        "shocks": {f"market_{s}pct": {"est_portfolio_move_pct": pilib.r(beta * s) if beta is not None else None,
                                     "est_usd": pilib.r(beta * s / 100 * total) if beta is not None else None}
                   for s in (-5, -10)},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=None)
    a = ap.parse_args(argv)
    date = a.date or pilib.run_date()
    cfg = pilib.portfolio_config()
    holdings = pilib.load_holdings()
    metrics_path = pilib.DATA / "metrics" / f"{date}.json"
    metrics = pilib.read_json(metrics_path) if metrics_path.exists() else {"positions": {}}
    values, series, betas = {}, {}, {}
    for p in holdings.get("positions", []):
        key, t = p["ticker"], p["ticker"].split("-")[0]
        m = metrics.get("positions", {}).get(key, {})
        close = m.get("close")
        if close is None:
            continue
        values[key] = close * p["shares"]
        betas[key] = m.get("beta_1y_vs_market")
        path = pilib.DATA / "prices" / f"{t}.csv"
        if path.exists():
            series[key] = returns_by_date(pilib.read_prices_csv(path))
    if not values:
        print("no priced positions; nothing to compute")
        return 1
    out = compute(values, series, betas, cfg.get("themes", {}), cfg.get("sectors", {}),
                  cfg.get("goals", {}).get("statements", []))
    out["date"] = date
    path = pilib.write_json(pilib.DATA / "metrics" / f"portfolio-{date}.json", out)
    print(f"portfolio risk -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
