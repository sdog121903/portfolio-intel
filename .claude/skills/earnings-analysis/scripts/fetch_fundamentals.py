#!/usr/bin/env python3
"""Quarterly fundamentals from the SEC's XBRL "company facts" API (the numbers companies file).

Endpoint: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json (needs SEC_USER_AGENT).
For each holding it extracts revenue, gross profit, operating income, net income, diluted EPS
and diluted share count per fiscal quarter, derives Q4 where only the annual figure was filed
(annual minus the three quarters), and computes year-over-year growth, margins and trailing
twelve months (TTM). Every value keeps the form, filing date and accession number it came from.

Writes data/fundamentals/<TICKER>.json. Derived values are flagged "derived": true.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

CONCEPTS = {  # first tag found wins
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
                "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "eps_diluted": ["EarningsPerShareDiluted"],
    "diluted_shares": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "rnd": ["ResearchAndDevelopmentExpense"],
}
UNITS = {"eps_diluted": "USD/shares", "diluted_shares": "shares"}


def duration_days(f: dict):
    if "start" not in f:
        return None
    return (pilib.parse_date(f["end"]) - pilib.parse_date(f["start"])).days


def pick_series(facts: dict, concept: str) -> tuple:
    gaap = facts.get("facts", {}).get("us-gaap", {})
    unit = UNITS.get(concept, "USD")
    for tag in CONCEPTS[concept]:
        entries = gaap.get(tag, {}).get("units", {}).get(unit)
        if entries:
            return tag, entries
    return None, []


def quarterly(entries: list) -> list:
    """Latest-filed value for each ~3-month period, plus Q4 derived from annual minus Q1-Q3."""
    q, annual = {}, {}
    for f in entries:
        d = duration_days(f)
        if d is None or f.get("form", "").startswith(("8-K", "S-", "424")):
            continue
        key = (f["start"], f["end"])
        bucket = q if 80 <= d <= 100 else annual if 350 <= d <= 380 else None
        if bucket is None:
            continue
        if key not in bucket or f.get("filed", "") > bucket[key].get("filed", ""):
            bucket[key] = f
    out = {k: {"start": k[0], "end": k[1], "value": v["val"], "form": v.get("form"), "filed": v.get("filed"),
               "accession": v.get("accn"), "fy": v.get("fy"), "fp": v.get("fp"), "derived": False} for k, v in q.items()}
    for (a_start, a_end), a in annual.items():
        inside = sorted([v for v in out.values() if v["start"] >= a_start and v["end"] <= a_end and not v["derived"]],
                        key=lambda v: v["end"])
        if len(inside) == 3 and inside[-1]["end"] < a_end:
            q4_start = (pilib.parse_date(inside[-1]["end"]) + dt.timedelta(days=1)).isoformat()
            key = (q4_start, a_end)
            if key not in out and not any(v["end"] == a_end for v in out.values()):
                out[key] = {"start": q4_start, "end": a_end, "value": a["val"] - sum(v["value"] for v in inside),
                            "form": a.get("form"), "filed": a.get("filed"), "accession": a.get("accn"),
                            "fy": a.get("fy"), "fp": "Q4", "derived": True}
    return sorted(out.values(), key=lambda v: v["end"])


def yoy(series: list, i: int):
    cur = series[i]
    target = pilib.parse_date(cur["end"]) - dt.timedelta(days=365)
    for prev in series[:i]:
        if abs((pilib.parse_date(prev["end"]) - target).days) <= 20 and prev["value"]:
            return (cur["value"] / prev["value"] - 1) * 100 if prev["value"] > 0 else None
    return None


def build(facts: dict) -> dict:
    series, tags = {}, {}
    for c in CONCEPTS:
        tag, entries = pick_series(facts, c)
        tags[c] = tag
        series[c] = quarterly(entries) if entries else []
    rev = series["revenue"]
    by_end = {c: {v["end"]: v for v in s} for c, s in series.items()}
    quarters = []
    for i, r in enumerate(rev[-8:]):
        idx = len(rev) - len(rev[-8:]) + i
        end = r["end"]
        gp = by_end["gross_profit"].get(end, {}).get("value")
        op = by_end["operating_income"].get(end, {}).get("value")
        ni = by_end["net_income"].get(end, {}).get("value")
        eps = by_end["eps_diluted"].get(end, {})
        quarters.append({
            "period_end": end, "fiscal": f"{r.get('fy')} {r.get('fp')}", "revenue": r["value"],
            "revenue_yoy_pct": pilib.r(yoy(rev, idx)),
            "gross_margin_pct": pilib.r(gp / r["value"] * 100) if gp is not None and r["value"] else None,
            "operating_margin_pct": pilib.r(op / r["value"] * 100) if op is not None and r["value"] else None,
            "net_income": ni, "eps_diluted": eps.get("value"), "eps_derived": eps.get("derived"),
            "source": {"form": r["form"], "filed": r["filed"], "accession": r["accession"], "derived": r["derived"]},
        })
    ttm = {}
    if len(rev) >= 4:
        last4 = rev[-4:]
        ttm["revenue"] = sum(v["value"] for v in last4)
        eps4 = [by_end["eps_diluted"].get(v["end"], {}).get("value") for v in last4]
        ttm["eps_diluted"] = round(sum(eps4), 4) if all(e is not None for e in eps4) else None
        ttm["periods"] = [v["end"] for v in last4]
    return {"entity": facts.get("entityName"), "cik": facts.get("cik"), "tags_used": tags,
            "latest_quarters": quarters, "ttm": ttm,
            "notes": ["Q4 values marked derived = annual 10-K figure minus the three 10-Q quarters.",
                      "Derived Q4 EPS is approximate because share counts change during the year."]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tickers", nargs="*")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "filings-decoder" / "scripts"))
    from fetch_edgar import sec_headers, cik_map  # noqa: E402
    hdr = sec_headers()
    cache = pilib.DATA / "filings" / "company_tickers.json"
    if not cache.exists():
        pilib.write_json(cache, json.loads(pilib.http_get("https://www.sec.gov/files/company_tickers.json", hdr)))
    ciks = cik_map(pilib.read_json(cache))
    tickers = a.tickers or sorted({p["ticker"].split("-")[0] for p in pilib.load_holdings().get("positions", [])})
    for t in tickers:
        cik = ciks.get(t)
        if not cik:
            print(f"{t}: not found in SEC ticker list")
            continue
        time.sleep(0.2)
        facts = json.loads(pilib.http_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json", hdr))
        out = build(facts)
        out["ticker"], out["fetched"] = t, dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        pilib.write_json(pilib.DATA / "fundamentals" / f"{t}.json", out)
        last = out["latest_quarters"][-1] if out["latest_quarters"] else {}
        print(f"{t}: latest quarter ends {last.get('period_end')}, revenue {last.get('revenue')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
