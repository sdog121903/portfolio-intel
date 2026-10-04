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

CONCEPTS = {  # preference order: for a period reported under several tags, the earlier tag wins
    # "Revenues" first: it is the total a company reports; the contract-revenue tag can leave out
    # lease or electricity revenue (Bloom Energy files both, and they differ).
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
                "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "eps_diluted": ["EarningsPerShareDiluted"],
    "diluted_shares": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "rnd": ["ResearchAndDevelopmentExpense"],
}
UNITS = {"eps_diluted": "USD/shares", "diluted_shares": "shares"}
MERGED = {"revenue"}  # other concepts use one tag, so e.g. ProfitLoss never mixes into NetIncomeLoss
STALE_AFTER_DAYS = 150  # a quarter (~91 days) plus the longest normal 10-K filing delay (60 days)


def duration_days(f: dict):
    if "start" not in f:
        return None
    return (pilib.parse_date(f["end"]) - pilib.parse_date(f["start"])).days


def pick_series(facts: dict, concept: str) -> tuple:
    """Revenue: merge every candidate tag. Companies switch tags over the years (NVDA did) and
    some file quarters under one tag and the annual figure under another (LITE does), so any
    single tag can stop years early or lose the quarters needed to derive Q4.
    Other concepts: the one tag with the most recent period (list order breaks ties), because
    their alternative tags measure something different."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    unit = UNITS.get(concept, "USD")
    if concept not in MERGED:
        best, best_end = (None, []), ""
        for tag in CONCEPTS[concept]:
            entries = gaap.get(tag, {}).get("units", {}).get(unit) or []
            last_end = max((f.get("end", "") for f in entries), default="")
            if last_end > best_end:
                best, best_end = (tag, entries), last_end
        return best
    used, merged, covered = [], [], set()
    for tag in CONCEPTS[concept]:
        entries = gaap.get(tag, {}).get("units", {}).get(unit) or []
        new = [f for f in entries if (f.get("start"), f.get("end")) not in covered]
        if new:
            used.append(tag)
            merged.extend(new)
        covered.update((f.get("start"), f.get("end")) for f in entries)
    return ("+".join(used) or None), merged


def quarterly(entries: list) -> list:
    """Latest-filed value for each ~3-month period, plus Q4 derived from annual minus Q1-Q3.
    The fiscal label comes from the first filing of the period: later filings repeat old
    quarters as comparatives and stamp them with their own (newer) fiscal year."""
    q, annual, first = {}, {}, {}
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
        if key not in first or f.get("filed", "") < first[key].get("filed", ""):
            first[key] = f
    out = {k: {"start": k[0], "end": k[1], "value": v["val"], "form": v.get("form"), "filed": v.get("filed"),
               "accession": v.get("accn"), "fy": first[k].get("fy"), "fp": first[k].get("fp"), "derived": False}
           for k, v in q.items()}
    for (a_start, a_end), a in annual.items():
        inside = sorted([v for v in out.values() if v["start"] >= a_start and v["end"] <= a_end and not v["derived"]],
                        key=lambda v: v["end"])
        if len(inside) == 3 and inside[-1]["end"] < a_end:
            q4_start = (pilib.parse_date(inside[-1]["end"]) + dt.timedelta(days=1)).isoformat()
            key = (q4_start, a_end)
            if key not in out and not any(v["end"] == a_end for v in out.values()):
                out[key] = {"start": q4_start, "end": a_end, "value": a["val"] - sum(v["value"] for v in inside),
                            "form": a.get("form"), "filed": a.get("filed"), "accession": a.get("accn"),
                            "fy": first[(a_start, a_end)].get("fy"), "fp": "Q4", "derived": True}
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
            # EPS does not add up across quarters (share counts change), so a derived Q4 EPS is not shown
            "net_income": ni, "eps_diluted": None if eps.get("derived") else eps.get("value"),
            "eps_derived": eps.get("derived"),
            "source": {"form": r["form"], "filed": r["filed"], "accession": r["accession"], "derived": r["derived"]},
        })
    ttm = {}
    if len(rev) >= 4:
        last4 = rev[-4:]
        ttm["revenue"] = sum(v["value"] for v in last4)
        eps4 = [by_end["eps_diluted"].get(v["end"], {}).get("value") for v in last4]
        ttm["eps_diluted"] = round(sum(eps4), 4) if all(e is not None for e in eps4) else None
        ttm["periods"] = [v["end"] for v in last4]
    notes = ["Q4 values marked derived = annual 10-K figure minus the three 10-Q quarters.",
             "Derived Q4 EPS is left empty (EPS does not add up across quarters): take Q4 EPS from the "
             "company's earnings release. TTM EPS that includes a derived Q4 is approximate."]
    if not facts.get("facts", {}).get("us-gaap") and facts.get("facts", {}).get("ifrs-full"):
        notes.insert(0, "No US-GAAP figures: a foreign filer reporting under IFRS (20-F / 6-K). "
                        "Use the company's own quarterly results release instead.")
    return {"entity": facts.get("entityName"), "cik": facts.get("cik"), "tags_used": tags,
            "latest_quarters": quarters, "ttm": ttm, "notes": notes}


def staleness(out: dict, today: str):
    """Warning text when the newest quarter is older than a normal filing cycle, else None."""
    qs = out.get("latest_quarters") or []
    if not qs:
        return None
    age = pilib.days_between(qs[-1]["period_end"], today)
    if age <= STALE_AFTER_DAYS:
        return None
    return (f"Newest quarter in the SEC data ends {qs[-1]['period_end']} ({age} days ago): a later report may exist "
            "but is missing from the XBRL data. Do not call these the latest results; check the newest 10-Q or 10-K.")


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
        out["stale_warning"] = staleness(out, pilib.run_date())
        pilib.write_json(pilib.DATA / "fundamentals" / f"{t}.json", out)
        last = out["latest_quarters"][-1] if out["latest_quarters"] else {}
        print(f"{t}: latest quarter ends {last.get('period_end')}, revenue {last.get('revenue')}")
        if out["stale_warning"]:
            print(f"WARNING {t}: {out['stale_warning']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
