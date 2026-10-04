#!/usr/bin/env python3
"""Pull each holding's recent SEC filings and decode them into plain English.

Uses only documented, free SEC endpoints:
  https://www.sec.gov/files/company_tickers.json          ticker -> CIK
  https://data.sec.gov/submissions/CIK##########.json      filing history
  https://www.sec.gov/Archives/edgar/data/<cik>/<acc>/...  the documents themselves
SEC requires a User-Agent with your name and email (set SEC_USER_AGENT) and at most
10 requests per second; this script stays well under that.

Writes data/filings/<DATE>.json: per ticker, every filing in the window with a plain-English
label and materiality, 8-K items decoded, and Form 4 insider trades parsed (who, what, how
many shares, at what price, and whether it was a pre-planned 10b5-1 trade).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

FORMS = {  # form: (plain-English meaning, materiality)
    "8-K": ("Current report: the company must tell investors about a major event within four business days", "depends on items"),
    "8-K/A": ("Amendment to an earlier current report", "depends on items"),
    "10-Q": ("Quarterly report: unaudited financial statements and management's discussion", "high"),
    "10-K": ("Annual report: audited financial statements, business description and risk factors", "high"),
    "10-Q/A": ("Amended quarterly report", "high"), "10-K/A": ("Amended annual report", "high"),
    "4": ("Insider trade: a director, officer or 10% owner bought, sold or received shares", "medium"),
    "4/A": ("Amended insider trade report", "low"),
    "3": ("New insider's first report of holdings", "low"), "5": ("Annual insider trade catch-up report", "low"),
    "144": ("Notice that an insider or affiliate plans to sell restricted or control shares", "medium"),
    "S-3": ("Shelf registration: lets the company sell new shares or debt later (possible dilution)", "medium"),
    "S-3ASR": ("Automatic shelf registration for large companies (possible future share or debt sales)", "medium"),
    "424B2": ("Prospectus for a specific securities sale", "medium"), "424B3": ("Prospectus supplement", "medium"),
    "424B5": ("Prospectus supplement: usually a specific new share or debt sale", "high"),
    "424B7": ("Prospectus supplement for shares sold by existing holders", "medium"),
    "S-8": ("Registers shares for employee stock plans (slow, routine dilution)", "low"),
    "SC 13D": ("An investor crossed 5% ownership and may try to influence the company", "high"),
    "SC 13D/A": ("Update from a 5%+ activist-style holder", "medium"),
    "SC 13G": ("A passive investor crossed 5% ownership", "low"), "SC 13G/A": ("Update from a passive 5%+ holder", "low"),
    "SCHEDULE 13D": ("An investor crossed 5% ownership and may try to influence the company", "high"),
    "SCHEDULE 13G": ("A passive investor crossed 5% ownership", "low"),
    "DEF 14A": ("Proxy statement: shareholder meeting agenda, executive pay, board elections", "low"),
    "DEFA14A": ("Additional proxy material", "low"), "8-A12B": ("Registers a class of securities on an exchange", "low"),
    "SD": ("Specialized disclosure (e.g. conflict minerals)", "low"), "11-K": ("Annual report of an employee stock plan", "low"),
    "425": ("Communication about a merger or acquisition", "high"), "SC TO-T": ("Tender offer by a third party", "high"),
    "SC TO-I": ("Company tender offer for its own shares", "medium"),
}

ITEMS_8K = {  # item: (plain-English meaning, materiality)
    "1.01": ("Signed a major contract or agreement", "high"), "1.02": ("Ended a major contract", "high"),
    "1.03": ("Bankruptcy or receivership", "high"), "1.05": ("Material cybersecurity incident", "high"),
    "2.01": ("Completed an acquisition or sale of assets", "high"),
    "2.02": ("Results of operations (earnings release)", "high"),
    "2.03": ("Took on a significant new debt or obligation", "medium"),
    "2.04": ("Something triggered faster repayment of debt", "high"),
    "2.05": ("Restructuring, layoffs or exit costs", "high"), "2.06": ("Material impairment (wrote down an asset)", "high"),
    "3.01": ("Exchange delisting notice or failed a listing rule", "high"),
    "3.02": ("Sold shares without public registration", "medium"), "3.03": ("Changed shareholders' rights", "medium"),
    "4.01": ("Changed auditor", "high"), "4.02": ("Past financial statements should no longer be relied upon", "high"),
    "5.01": ("Change in control of the company", "high"),
    "5.02": ("Director or senior officer left, joined, or pay arrangements changed", "high"),
    "5.03": ("Changed articles of incorporation or bylaws, or fiscal year", "low"),
    "5.07": ("Results of a shareholder vote", "low"), "5.08": ("Shareholder director nominations", "low"),
    "7.01": ("Regulation FD disclosure (often a presentation or press release)", "medium"),
    "8.01": ("Other events the company chose to report", "medium"),
    "9.01": ("Financial statements and exhibits attached", "low"),
}

FORM4_CODES = {
    "P": "open-market or private PURCHASE (insider spent their own money)",
    "S": "open-market or private SALE",
    "A": "grant or award from the company (compensation, not a purchase)",
    "M": "exercise or conversion of an option or similar derivative",
    "F": "shares withheld to pay taxes or the exercise price (routine)",
    "G": "gift", "D": "shares given back to the company", "C": "conversion of a derivative security",
    "X": "exercise of an in- or at-the-money option", "J": "other transaction (see footnotes)",
    "W": "acquired or disposed by will or inheritance", "I": "discretionary transaction",
    "V": "voluntarily reported transaction", "E": "expiration of a short derivative position",
    "H": "expiration of a long derivative position", "O": "exercise of an out-of-the-money option",
    "K": "equity swap or similar", "L": "small acquisition", "Z": "deposit into or withdrawal from a voting trust",
    "U": "tender of shares in a change-of-control transaction",
}


def sec_headers() -> dict:
    """SEC requires every automated request to say who is asking, with a contact email.
    Uses SEC_USER_AGENT if set, otherwise the owner's name and email from config/portfolio.toml."""
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua or "@" not in ua:
        owner = pilib.portfolio_config().get("owner", {})
        ua = f"{owner.get('name', '')} {owner.get('email_to', '')}".strip()
    if "@" not in ua:
        raise SystemExit("Set SEC_USER_AGENT to 'Your Name your@email.com' (SEC requires it).")
    return {"User-Agent": ua, "Accept-Encoding": "gzip"}


# ---------------------------------------------------------------- pure parsers (unit-tested)
def cik_map(tickers_json: dict) -> dict:
    return {v["ticker"].upper(): int(v["cik_str"]) for v in tickers_json.values()}


def recent_filings(submissions: dict, since: str, cik: int) -> list:
    rec = submissions.get("filings", {}).get("recent", {})
    out = []
    for i, form in enumerate(rec.get("form", [])):
        fdate = rec["filingDate"][i]
        if fdate < since:
            continue
        acc = rec["accessionNumber"][i]
        doc = rec.get("primaryDocument", [""] * (i + 1))[i]
        items = [x.strip() for x in (rec.get("items", [""] * (i + 1))[i] or "").split(",") if x.strip()]
        meaning, materiality = FORMS.get(form, ("Other filing (see document)", "low"))
        decoded = [{"item": it, "meaning": ITEMS_8K.get(it, ("see document", "low"))[0],
                    "materiality": ITEMS_8K.get(it, ("", "low"))[1]} for it in items]
        if form.startswith("8-K") and decoded:
            order = {"high": 3, "medium": 2, "low": 1}
            materiality = max((d["materiality"] for d in decoded), key=lambda m: order.get(m, 0))
        base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}"
        out.append({"form": form, "filing_date": fdate,
                    "accepted": (rec.get("acceptanceDateTime", [""] * (i + 1))[i] or "")[:19],
                    "accession": acc, "meaning": meaning, "materiality": materiality, "items": decoded,
                    "description": rec.get("primaryDocDescription", [""] * (i + 1))[i],
                    "url": f"{base}/{doc}" if doc else f"{base}/",
                    "index_url": f"{base}/{acc}-index.htm"})
    return out


def _txt(el, path):
    node = el.find(path)
    if node is None:
        return None
    v = node.find("value")
    return (v.text if v is not None else node.text or "").strip() or None


def parse_form4(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    for el in root.iter():  # drop any namespaces
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    owner = root.find("reportingOwner")
    rel = owner.find("reportingOwnerRelationship") if owner is not None else None
    roles = []
    if rel is not None:
        for tag, label in (("isDirector", "director"), ("isOfficer", "officer"), ("isTenPercentOwner", "10% owner"), ("isOther", "other")):
            if (rel.findtext(tag) or "").strip() in ("1", "true"):
                roles.append(label)
    plan_flag = (root.findtext("aff10b5One") or "").strip().lower() in ("1", "true")
    footnotes = " ".join((f.text or "") for f in root.iter("footnote")).lower()
    if "10b5-1" in footnotes:
        plan_flag = True
    trades = []
    for tx in root.iter("nonDerivativeTransaction"):
        code = (tx.findtext("transactionCoding/transactionCode") or "").strip()
        shares = _txt(tx, "transactionAmounts/transactionShares")
        price = _txt(tx, "transactionAmounts/transactionPricePerShare")
        ad = _txt(tx, "transactionAmounts/transactionAcquiredDisposedCode")
        after = _txt(tx, "postTransactionAmounts/sharesOwnedFollowingTransaction")
        sh = float(shares) if shares else None
        px = float(price) if price else None
        trades.append({"date": _txt(tx, "transactionDate"), "code": code, "code_meaning": FORM4_CODES.get(code, "see filing"),
                       "acquired_or_disposed": {"A": "acquired", "D": "disposed"}.get(ad, ad),
                       "shares": sh, "price": px, "value_usd": round(sh * px, 2) if sh and px else None,
                       "shares_owned_after": float(after) if after else None})
    return {"issuer": root.findtext("issuer/issuerName"), "ticker": root.findtext("issuer/issuerTradingSymbol"),
            "owner": owner.findtext("reportingOwnerId/rptOwnerName") if owner is not None else None,
            "roles": roles, "officer_title": rel.findtext("officerTitle") if rel is not None else None,
            "under_10b5_1_plan": plan_flag, "transactions": trades}


def summarise_insiders(form4s: list) -> dict:
    buys = [t for f in form4s for t in f["transactions"] if t["code"] == "P"]
    sells = [t for f in form4s for t in f["transactions"] if t["code"] == "S"]
    unplanned_sellers = {f["owner"] for f in form4s if not f["under_10b5_1_plan"] and any(t["code"] == "S" for t in f["transactions"])}
    return {"open_market_buys": len(buys), "buy_value_usd": round(sum(t["value_usd"] or 0 for t in buys), 2),
            "open_market_sells": len(sells), "sell_value_usd": round(sum(t["value_usd"] or 0 for t in sells), 2),
            "sellers_not_under_10b5_1_plan": sorted(x for x in unplanned_sellers if x),
            "note": "Grants (A), tax withholding (F) and option exercises (M) are usually routine compensation events."}


def form4_xml_url(filing_url: str) -> str:
    """Primary documents of Form 4 are often the XSL-rendered path (xslF345X05/file.xml); the raw XML drops that folder."""
    return re.sub(r"/xslF345X\d+/", "/", filing_url)


# ---------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--tickers", nargs="*")
    a = ap.parse_args(argv)
    cfg = pilib.portfolio_config()
    days = a.days or cfg.get("run", {}).get("filings_window_days", 10)
    date = a.date or pilib.run_date()
    since = (pilib.parse_date(date) - dt.timedelta(days=days)).isoformat()
    tickers = a.tickers or sorted({p["ticker"].split("-")[0] for p in pilib.load_holdings().get("positions", [])})
    hdr = sec_headers()
    cache = pilib.DATA / "filings" / "company_tickers.json"
    if not cache.exists() or (time.time() - cache.stat().st_mtime) > 7 * 86400:
        pilib.write_json(cache, json.loads(pilib.http_get("https://www.sec.gov/files/company_tickers.json", hdr)))
    ciks = cik_map(pilib.read_json(cache))
    out = {"window_start": since, "window_end": date, "tickers": {}}
    for t in tickers:
        cik = ciks.get(t)
        if not cik:
            out["tickers"][t] = {"error": "ticker not found in SEC list"}
            continue
        time.sleep(0.2)
        subs = json.loads(pilib.http_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", hdr))
        filings = recent_filings(subs, since, cik)
        form4s = []
        for f in filings:
            if f["form"] in ("4", "4/A") and f["url"].endswith(".xml"):
                time.sleep(0.2)
                try:
                    parsed = parse_form4(pilib.http_get(form4_xml_url(f["url"]), hdr))
                    f["insider"] = parsed
                    form4s.append(parsed)
                except Exception as e:
                    f["insider_error"] = str(e)
        out["tickers"][t] = {"cik": cik, "company": subs.get("name"), "filings": filings,
                             "insider_summary": summarise_insiders(form4s)}
        print(f"{t}: {len(filings)} filings since {since} ({len(form4s)} insider reports)")
    pilib.write_json(pilib.DATA / "filings" / f"{date}.json", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
