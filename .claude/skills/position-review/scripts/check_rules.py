#!/usr/bin/env python3
"""Check YOUR rules (config/rules.toml) against today's numbers.

Reads the latest holdings, data/metrics/<DATE>.json and (if present)
data/metrics/portfolio-<DATE>.json. Writes data/metrics/rules-<DATE>.json with, per position,
every rule that fired, the numbers behind it and a one-sentence plain-English explanation.

This is a calculator for the owner's own plan. It never adds rules of its own and never
turns a result into a buy or sell instruction.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402


def evaluate(rule: dict, pos: dict, m: dict, weight_pct) -> dict | None:
    t = rule.get("type")
    side = pos.get("side", "Long")
    close = m.get("close")
    posm = m.get("position", {})
    fire = lambda msg, **nums: {"id": rule.get("id", t), "action": rule.get("action", "watch"), "explain": msg, "numbers": nums}
    if close is None:
        return None
    if t == "stop_loss_from_sheet" and pos.get("stop_loss"):
        sl = pos["stop_loss"]
        hit = close <= sl if side == "Long" else close >= sl
        if hit:
            return fire(f"The price (${close:,.2f}) reached the stop-loss level you set (${sl:,.2f}).", close=close, stop_loss=sl)
    elif t == "target_from_sheet" and pos.get("target"):
        tg = pos["target"]
        hit = close >= tg if side == "Long" else close <= tg
        if hit:
            return fire(f"The price (${close:,.2f}) reached the target price you set (${tg:,.2f}).", close=close, target=tg)
    elif t == "loss_from_entry_pct" and posm.get("pnl_pct") is not None:
        if posm["pnl_pct"] <= -abs(rule["threshold"]):
            return fire(f"The position is down {abs(posm['pnl_pct']):.1f}% from your entry, past your {rule['threshold']}% limit.",
                        pnl_pct=posm["pnl_pct"], threshold=rule["threshold"])
    elif t == "drawdown_from_peak_since_entry_pct" and posm.get("drawdown_from_peak_since_entry_pct") is not None:
        dd = posm["drawdown_from_peak_since_entry_pct"]
        if dd <= -abs(rule["threshold"]):
            return fire(f"The price is {abs(dd):.1f}% below its highest close since you bought, past your {rule['threshold']}% limit.",
                        drawdown_pct=dd, threshold=rule["threshold"])
    elif t == "abs_day_move_pct" and m.get("day_change_pct") is not None:
        if abs(m["day_change_pct"]) >= rule["threshold"]:
            direction = "up" if m["day_change_pct"] > 0 else "down"
            return fire(f"The stock moved {direction} {abs(m['day_change_pct']):.1f}% in one day, more than your "
                        f"{rule['threshold']}% 'explain this' threshold, so the report must investigate why.",
                        day_change_pct=m["day_change_pct"], threshold=rule["threshold"])
    elif t == "close_below_sma":
        w = str(rule.get("window", 200))
        sma = (m.get("sma") or {}).get(w)
        if sma and close < sma:
            return fire(f"The price is below its {w}-day average (${sma:,.2f}), a common sign that the longer trend has weakened.",
                        close=close, sma=sma, window=int(w))
    elif t == "position_weight_pct" and weight_pct is not None:
        if weight_pct >= rule["threshold"]:
            return fire(f"This position is {weight_pct:.1f}% of your portfolio, above your {rule['threshold']}% comfort limit.",
                        weight_pct=weight_pct, threshold=rule["threshold"])
    return None


def run(holdings: dict, metrics: dict, rules: dict, weights: dict) -> dict:
    out = {}
    for pos in holdings.get("positions", []):
        key = pos["ticker"]
        m = metrics.get("positions", {}).get(key)
        if not m:
            out[key] = {"fired": [], "status": "no market data today: rules could not be checked"}
            continue
        fired = []
        for rule in rules.get("rule", []):
            if not rule.get("enabled", True):
                continue
            res = evaluate(rule, pos, m, weights.get(key))
            if res:
                fired.append(res)
        actions = {f["action"] for f in fired}
        status = ("RETREAT RULE HIT" if "retreat" in actions else "TARGET REACHED" if "target" in actions
                  else "WATCH" if "watch" in actions else "No rule fired")
        out[key] = {"fired": fired, "status": status}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=None)
    a = ap.parse_args(argv)
    date = a.date or pilib.run_date()
    holdings = pilib.load_holdings()
    metrics_path = pilib.DATA / "metrics" / f"{date}.json"
    if not metrics_path.exists():
        metrics_path = pilib.latest_file(pilib.DATA / "metrics", "20*.json")
    metrics = pilib.read_json(metrics_path)
    port_path = pilib.DATA / "metrics" / f"portfolio-{date}.json"
    weights = pilib.read_json(port_path).get("weights_pct", {}) if port_path.exists() else {}
    result = run(holdings, metrics, pilib.rules_config(), weights)
    pilib.write_json(pilib.DATA / "metrics" / f"rules-{date}.json",
                     {"date": date, "thesis_breakers_to_check": pilib.rules_config().get("thesis_breakers", {}).get("events", []),
                      "positions": result})
    for k, v in result.items():
        print(f"{k}: {v['status']}" + "".join(f"\n  - {f['explain']}" for f in v["fired"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
