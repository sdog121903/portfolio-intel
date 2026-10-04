#!/usr/bin/env python3
"""Run every number-crunching tool for today, in order, and record what happened.

Order matters: holdings -> prices -> metrics -> move attribution -> portfolio risk -> rules
-> SEC filings -> fundamentals (when due). A failing step never stops the others; its error is
recorded in data/snapshots/<DATE>-pipeline.json so the report's "Data quality" section can say
exactly what is missing and why.

Usage:
  python scripts/run_daily_data.py --rows data/holdings/raw-<DATE>.json   (sheet rows read by the agent)
  python scripts/run_daily_data.py --fallback                             (use config/holdings_fallback.csv)
  add --fundamentals to force a refresh of XBRL fundamentals (otherwise weekly, or after a 10-Q/10-K)
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilib  # noqa: E402

S = pilib.ROOT / ".claude" / "skills"
TOOLS = {
    "holdings": S / "portfolio-daily-report" / "scripts" / "load_holdings.py",
    "prices": S / "market-metrics" / "scripts" / "fetch_prices.py",
    "metrics": S / "market-metrics" / "scripts" / "market_metrics.py",
    "attribution": S / "why-analysis" / "scripts" / "move_attribution.py",
    "portfolio": S / "portfolio-risk" / "scripts" / "portfolio_risk.py",
    "rules": S / "position-review" / "scripts" / "check_rules.py",
    "filings": S / "filings-decoder" / "scripts" / "fetch_edgar.py",
    "fundamentals": S / "earnings-analysis" / "scripts" / "fetch_fundamentals.py",
}


def run(name: str, args: list, timeout: int = 600) -> dict:
    t0 = dt.datetime.now(dt.timezone.utc)
    try:
        p = subprocess.run([sys.executable, str(TOOLS[name]), *args], capture_output=True, text=True, timeout=timeout)
        ok = p.returncode == 0
        return {"step": name, "ok": ok, "returncode": p.returncode, "stdout": p.stdout[-4000:], "stderr": p.stderr[-4000:],
                "seconds": (dt.datetime.now(dt.timezone.utc) - t0).seconds}
    except Exception as e:
        return {"step": name, "ok": False, "error": str(e)}


def fundamentals_due(date: str, filings_ok: bool) -> bool:
    folder = pilib.DATA / "fundamentals"
    files = list(folder.glob("*.json"))
    if not files:
        return True
    if dt.date.fromisoformat(date).weekday() == 6:  # Sundays
        return True
    fpath = pilib.DATA / "filings" / f"{date}.json"
    if filings_ok and fpath.exists():
        data = pilib.read_json(fpath)
        for t in data.get("tickers", {}).values():
            if any(f.get("form") in ("10-Q", "10-K", "10-Q/A", "10-K/A") for f in t.get("filings", [])):
                return True
    return False


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--rows", type=Path)
    g.add_argument("--fallback", action="store_true")
    ap.add_argument("--fundamentals", action="store_true")
    a = ap.parse_args(argv)
    date = pilib.run_date()
    steps = []
    h_args = ["--from-rows", str(a.rows)] if a.rows else ["--from-csv", str(pilib.CONFIG / "holdings_fallback.csv")]
    steps.append(run("holdings", h_args + ["--date", date]))
    if not steps[-1]["ok"]:
        print("holdings failed; nothing else can run"); print(steps[-1])
        pilib.write_json(pilib.DATA / "snapshots" / f"{date}-pipeline.json", {"date": date, "steps": steps})
        return 1
    for name in ("prices", "metrics", "attribution", "portfolio", "rules"):
        steps.append(run(name, ["--date", date] if name != "prices" else []))
    steps.append(run("filings", ["--date", date]))
    if a.fundamentals or fundamentals_due(date, steps[-1]["ok"]):
        steps.append(run("fundamentals", []))
    summary = {"date": date, "steps": steps, "ok": all(s["ok"] for s in steps)}
    pilib.write_json(pilib.DATA / "snapshots" / f"{date}-pipeline.json", summary)
    for s in steps:
        print(f"{'OK  ' if s['ok'] else 'FAIL'} {s['step']}" + ("" if s["ok"] else f": {(s.get('stderr') or s.get('error') or s.get('stdout') or '')[-300:]}"))
    return 0 if summary["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())
