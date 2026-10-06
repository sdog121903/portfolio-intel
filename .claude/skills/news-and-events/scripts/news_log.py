#!/usr/bin/env python3
"""Keep a running news log per stock: what happened, and how the price reacted.

Every report run adds its fact-checked news items for each stock to
data/news-log/<TICKER>.json (the record) and rebuilds theses/news/<TICKER>.md (the page Santi
reads), newest first. Nothing is ever deleted, so over months the log shows how each stock
tends to react to each kind of news.

Input, written by the main session after the quality gates:
data/research/<DATE>/news-log.json
    {"date": "2026-10-04", "fact_checked": true,
     "tickers": {"ASML": [{"key": "asml-2026-07-15-q2-raise", "date": "2026-07-15",
                           "timing": "before open", "type": "earnings", "materiality": "high",
                           "direction": "good", "what": "Plain-English sentence.",
                           "source": {"name": "ASML 6-K", "date": "2026-07-15",
                                      "url": "https://...", "tier": 1}}]}}
An optional "upcoming": {"<TICKER>": [{"date", "event", "confirmed", "source"}]} replaces that stock's
"Coming up" calendar on its page. If that file is missing, the researcher files data/research/<DATE>/<TICKER>.json are used
instead and every item is marked "not fact-checked".

Price reactions are calculated from data/prices/<TICKER>.csv and the market benchmark (SPY):
the move on the first trading day the news could affect, the market's move that day, the
difference ("beyond market"), its size against a normal day for that stock, and the next five
days. Report-day moves come from data/metrics/<DATE>.json and attribution-<DATE>.json.

    python3 news_log.py update --date 2026-10-04 [--tickers ASML LITE]
    python3 news_log.py render --tickers ASML

This is a diary of facts and arithmetic. It never turns a pattern into a buy or sell call.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

DATA = pilib.DATA
PAGES = pilib.ROOT / "theses" / "news"
MIN_ITEMS_FOR_PATTERNS = 20
DIRECTION = {"supports": "good", "weakens": "bad", "neutral": "neutral",
             "good": "good", "bad": "bad", "mixed": "mixed"}


# ---------------------------------------------------------------- inputs
def item_key(ticker: str, item: dict) -> str:
    if item.get("key"):
        return str(item["key"])
    text = re.sub(r"[^a-z0-9]+", " ", str(item.get("what", "")).lower()).strip()[:80]
    digest = hashlib.sha1(f"{ticker}|{item.get('date')}|{text}".encode()).hexdigest()[:10]
    return f"{ticker.lower()}-{item.get('date')}-{digest}"


def load_items(date: str, ticker: str) -> tuple[list, bool]:
    """Items for one ticker on one report date, and whether they were fact-checked."""
    folder = DATA / "research" / date
    curated = folder / "news-log.json"
    if curated.exists():
        doc = pilib.read_json(curated)
        if ticker in doc.get("tickers", {}):
            return list(doc["tickers"][ticker]), bool(doc.get("fact_checked", False))
    raw = folder / f"{ticker}.json"
    if not raw.exists():
        return [], False
    items = []
    for e in pilib.read_json(raw).get("events", []):
        src = (e.get("sources") or [{}])[0]
        items.append({"date": e.get("date"), "timing": e.get("timing", "unknown"),
                      "type": e.get("type", ""), "materiality": e.get("materiality", ""),
                      "direction": e.get("direction", "neutral"), "what": e.get("summary", ""),
                      "source": {k: src.get(k) for k in ("name", "date", "url", "tier")}})
    return items, False


def load_upcoming(date: str, ticker: str) -> Optional[list]:
    """Upcoming events for one ticker from news-log.json, or None when the file has none."""
    curated = DATA / "research" / date / "news-log.json"
    if not curated.exists():
        return None
    up = pilib.read_json(curated).get("upcoming", {})
    return list(up[ticker]) if ticker in up else None


def load_prices(ticker: str) -> list:
    path = DATA / "prices" / f"{ticker}.csv"
    return pilib.read_prices_csv(path) if path.exists() else []


def market_symbol() -> str:
    try:
        return pilib.portfolio_config().get("benchmarks", {}).get("market", "SPY")
    except Exception:
        return "SPY"


# ---------------------------------------------------------------- price reaction
def _first_date(text: str) -> Optional[str]:
    m = re.search(r"\d{4}-\d{2}-\d{2}", str(text or ""))
    return m.group(0) if m else None


def reaction(stock: list, market: list, event_date: str, timing: str = "unknown") -> Optional[dict]:
    """How the stock moved on the first trading day the news could affect."""
    day = _first_date(event_date)
    if not day or len(stock) < 2:
        return None
    after_close = "after" in str(timing).lower()
    idx = next((i for i, r in enumerate(stock)
                if (r["date"] > day if after_close else r["date"] >= day)), None)
    if idx is None or idx == 0:
        return None
    closes = [r["adj_close"] for r in stock]
    stock_pct = pilib.pct_change(closes[idx], closes[idx - 1])
    mkt = {r["date"]: r["adj_close"] for r in market}
    rday, prev = stock[idx]["date"], stock[idx - 1]["date"]
    market_pct = pilib.pct_change(mkt.get(rday), mkt.get(prev)) if rday in mkt and prev in mkt else None
    excess = stock_pct - market_pct if stock_pct is not None and market_pct is not None else None
    # A normal day for this stock: spread of its daily moves beyond the market over the prior year.
    diffs = []
    for i in range(max(1, idx - 252), idx):
        d0, d1 = stock[i - 1]["date"], stock[i]["date"]
        s = pilib.pct_change(closes[i], closes[i - 1])
        m = pilib.pct_change(mkt.get(d1), mkt.get(d0)) if d0 in mkt and d1 in mkt else None
        if s is not None and m is not None:
            diffs.append(s - m)
    typical = robust_spread(diffs) if len(diffs) >= 20 else None
    z = excess / typical if excess is not None and typical else None
    next5 = pilib.pct_change(closes[idx + 5], closes[idx]) if idx + 5 < len(closes) else None
    return {"day": rday, "stock_pct": pilib.r(stock_pct), "market_pct": pilib.r(market_pct),
            "beyond_market_pct": pilib.r(excess), "typical_day_pct": pilib.r(typical),
            "z": pilib.r(z), "next_5_days_pct": pilib.r(next5)}


def robust_spread(xs: list) -> Optional[float]:
    """A typical day's size that one huge jump cannot inflate: 1.4826 x the median absolute
    deviation, which equals the standard deviation for ordinary, bell-shaped data."""
    if not xs:
        return None
    med = sorted(xs)[len(xs) // 2]
    mad = sorted(abs(x - med) for x in xs)[len(xs) // 2]
    return 1.4826 * mad or pilib.stdev(xs)


def short(text: str, n: int = 90) -> str:
    text = _cell(text)
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "..."


def size_label(z: Optional[float]) -> str:
    if z is None:
        return "n/a"
    a = abs(z)
    return "normal" if a < 1 else "big" if a < 2 else "very big"


# ---------------------------------------------------------------- the log
def empty_log(ticker: str) -> dict:
    return {"ticker": ticker, "items": [], "days": []}


def load_log(ticker: str) -> dict:
    path = DATA / "news-log" / f"{ticker}.json"
    return pilib.read_json(path) if path.exists() else empty_log(ticker)


def merge_items(log: dict, ticker: str, items: list, report_date: str, fact_checked: bool) -> int:
    """Add new items; an item seen before keeps its first entry and gains the new report date."""
    known = {it["key"]: it for it in log["items"]}
    added = 0
    for raw in items:
        if not raw.get("what") or not raw.get("date"):
            continue
        key = item_key(ticker, raw)
        if key in known:
            seen = known[key].setdefault("reports", [])
            if report_date not in seen:
                seen.append(report_date)
            if fact_checked and not known[key].get("fact_checked"):
                known[key].update({k: raw[k] for k in ("what", "direction", "materiality", "source") if k in raw})
                known[key]["fact_checked"] = True
            continue
        entry = {"key": key, "date": raw["date"], "timing": raw.get("timing", "unknown"),
                 "type": raw.get("type", ""), "materiality": raw.get("materiality", ""),
                 "direction": DIRECTION.get(str(raw.get("direction", "neutral")).lower(), "neutral"),
                 "what": raw["what"], "source": raw.get("source") or {},
                 "fact_checked": fact_checked, "logged": report_date, "reports": [report_date]}
        log["items"].append(entry)
        known[key] = entry
        added += 1
    return added


def refresh_reactions(log: dict, stock: list, market: list) -> None:
    """Recalculate reactions whenever prices are available (fills 'next 5 days' later on)."""
    if not stock:
        return
    for it in log["items"]:
        new = reaction(stock, market, it["date"], it.get("timing", "unknown"))
        if new:
            it["reaction"] = new


def day_row(date: str, ticker: str, log: dict) -> Optional[dict]:
    metrics = DATA / "metrics" / f"{date}.json"
    attrib = DATA / "metrics" / f"attribution-{date}.json"
    if not metrics.exists():
        return None
    m = pilib.read_json(metrics).get("positions", {}).get(ticker)
    if not m:
        return None
    a = pilib.read_json(attrib).get(ticker, {}) if attrib.exists() else {}
    last = a.get("last_day", {})
    trading_day = last.get("to") or m.get("as_of")
    same_day = [it for it in log["items"]
                if it.get("reaction", {}).get("day") == trading_day or _first_date(it["date"]) == trading_day]
    order = {"high": 0, "medium": 1, "low": 2}
    same_day.sort(key=lambda it: order.get(it.get("materiality"), 3))
    return {"report": date, "trading_day": trading_day, "close": m.get("close"),
            "day_pct": m.get("day_change_pct"), "market_part_pct": last.get("market_part_pct"),
            "industry_part_pct": last.get("industry_part_pct"),
            "company_part_pct": last.get("company_specific_pct"),
            "z": last.get("company_specific_zscore"),
            "main_news": same_day[0]["what"] if same_day else None}


def merge_day(log: dict, row: dict) -> None:
    """One row per trading day; a later report about the same day replaces the earlier one."""
    log["days"] = [d for d in log["days"] if d.get("trading_day") != row["trading_day"]] + [row]


# ---------------------------------------------------------------- page
def _pct(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x:+.2f}%"


def _cell(text: str) -> str:
    return str(text or "").replace("|", "/").replace("\n", " ").strip()


def _source(src: dict) -> str:
    if not src or not src.get("name"):
        return "not recorded"
    tier = f", tier {src['tier']}" if src.get("tier") else ""
    label = f"{src['name']}, {src.get('date') or 'date n/a'}"
    url = src.get("url") or ""
    return (f"[{_cell(label)}]({url}){tier}" if url.startswith("http") else f"{_cell(label)}{tier}")


def patterns(log: dict) -> list:
    items = log["items"]
    lines = [f"- **{len(items)}** news items and **{len(log['days'])}** report days logged"
             + (f" (first report {min(d['report'] for d in log['days'])}, latest {max(d['report'] for d in log['days'])})."
                if log["days"] else ".")]
    if len(items) < MIN_ITEMS_FOR_PATTERNS:
        lines.append(f"- **Too early to draw conclusions:** fewer than {MIN_ITEMS_FOR_PATTERNS} items. "
                     "Read this page as a diary for now, not as a rule about how the stock behaves.")
    for label, want in (("good", "good"), ("bad", "bad")):
        xs = [it["reaction"]["beyond_market_pct"] for it in items
              if it.get("direction") == want and it.get("reaction", {}).get("beyond_market_pct") is not None]
        if xs:
            lines.append(f"- Average move beyond the market on the reaction day to **{label}** news: "
                         f"{_pct(pilib.mean(xs))} ({len(xs)} item{'s' if len(xs) != 1 else ''}).")
    ranked = sorted((it for it in items if it.get("reaction", {}).get("beyond_market_pct") is not None),
                    key=lambda it: -abs(it["reaction"]["beyond_market_pct"]))[:3]
    if ranked:
        lines.append("- Biggest reactions so far: " + "; ".join(
            f"{it['reaction']['day']} {_pct(it['reaction']['beyond_market_pct'])} beyond the market "
            f"({size_label(it['reaction'].get('z'))}) after: {short(it['what'])}" for it in ranked) + ".")
    faded = [it for it in ranked if (it["reaction"].get("next_5_days_pct") is not None
             and it["reaction"]["stock_pct"] is not None
             and it["reaction"]["next_5_days_pct"] * it["reaction"]["stock_pct"] < 0)]
    if faded:
        lines.append(f"- Of those biggest moves, {len(faded)} partly reversed over the next five trading days.")
    unexplained = [d for d in log["days"] if d.get("z") is not None and abs(d["z"]) >= 2 and not d.get("main_news")]
    lines.append(f"- Report days with a very big company-specific move and no news found: {len(unexplained)}.")
    lines.append("- Several items can share one reaction day, so their reactions are not independent.")
    return lines


def render(log: dict) -> str:
    t = log["ticker"]
    items = sorted(log["items"], key=lambda it: (_first_date(it["date"]) or "", it["logged"]), reverse=True)
    days = sorted(log["days"], key=lambda d: (d.get("trading_day") or "", d["report"]), reverse=True)
    out = [f"# {t} news log: what happened, what is coming, and how the stock reacted", "",
           f"Every report that covers {t} adds its news here, newest first. Nothing is deleted, so over "
           "months this page shows how the stock tends to react to each kind of news. Thesis file: "
           f"[`theses/{t}.md`](../{t}.md).", "",
           "This page is rebuilt on every run from `data/news-log/" + t + ".json` by "
           "`.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.", "",
           "**How to read the reaction columns.** *Reaction day* is the first trading day the news could "
           "move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the "
           "price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is "
           "the difference, the part the market does not explain. *Size* compares that difference with "
           "a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one "
           "to two), very big (two or more). *Next 5 days* shows whether the move held or faded.", "",
           "## What the log shows so far", ""]
    out += patterns(log)
    up = log.get("upcoming") or {}
    out += ["", f"## Coming up (calendar as of {up.get('as_of', 'n/a')})", "",
            "Dated events that could move the stock. When one happens, it moves into the news table below.", "",
            "| Date | Event | Confirmed? | Source |", "|---|---|---|---|"]
    events = sorted(up.get("events", []), key=lambda e: _first_date(e.get("date")) or "9999")
    for e in events:
        out.append(f"| {_cell(e.get('date'))} | {_cell(e.get('event'))} | "
                   f"{'yes' if e.get('confirmed') else 'not confirmed'} | {_source(e.get('source'))} |")
    if not events:
        out.append("| - | Nothing scheduled in the log yet | | |")
    out += ["", "## News, newest first", "",
            "| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for it in items:
        rx = it.get("reaction") or {}
        what = _cell(it["what"]) + ("" if it.get("fact_checked") else " *(not fact-checked)*")
        out.append(f"| {_cell(it['date'])} | {what} | {it.get('direction', 'neutral')} | "
                   f"{it.get('materiality') or 'n/a'} | {rx.get('day', 'n/a')} | {_pct(rx.get('stock_pct'))} | "
                   f"{_pct(rx.get('market_pct'))} | {_pct(rx.get('beyond_market_pct'))} | "
                   f"{size_label(rx.get('z'))} | {_pct(rx.get('next_5_days_pct'))} | {_source(it.get('source'))} |")
    if not items:
        out.append("| - | Nothing logged yet | | | | | | | | | |")
    out += ["", "## Price on each report day, newest first", "",
            "The day's move split into the part from the whole market, the part from its industry and "
            "the part that is the company's own (from the report's move attribution).", "",
            "| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |",
            "|---|---|---|---|---|---|---|---|---|"]
    for d in days:
        close = f"${d['close']:,.2f}" if d.get("close") is not None else "n/a"
        out.append(f"| {d['report']} | {d.get('trading_day') or 'n/a'} | {close} | {_pct(d.get('day_pct'))} | "
                   f"{_pct(d.get('market_part_pct'))} | {_pct(d.get('industry_part_pct'))} | "
                   f"{_pct(d.get('company_part_pct'))} | {size_label(d.get('z'))} | "
                   f"{_cell(d.get('main_news')) or 'no news found'} |")
    if not days:
        out.append("| - | | | | | | | | |")
    out += ["", "Informational research and education, not investment advice.", ""]
    return "\n".join(out)


def write_page(log: dict) -> Path:
    path = PAGES / f"{log['ticker']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(log), encoding="utf-8")
    return path


# ---------------------------------------------------------------- commands
def tickers_for(date: str) -> list:
    curated = DATA / "research" / date / "news-log.json"
    if curated.exists():
        return sorted(pilib.read_json(curated).get("tickers", {}))
    folder = DATA / "research" / date
    return sorted(p.stem for p in folder.glob("*.json") if p.stem != "news-log")


def update(date: str, tickers: list) -> list:
    market = load_prices(market_symbol())
    results = []
    for t in tickers:
        log = load_log(t)
        items, checked = load_items(date, t)
        added = merge_items(log, t, items, date, checked)
        upcoming = load_upcoming(date, t)
        if upcoming is not None:
            log["upcoming"] = {"as_of": date, "events": upcoming}
        refresh_reactions(log, load_prices(t), market)
        row = day_row(date, t, log)
        if row:
            merge_day(log, row)
        pilib.write_json(DATA / "news-log" / f"{t}.json", log)
        page = write_page(log)
        results.append({"ticker": t, "added": added, "fact_checked": checked, "page": str(page)})
    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("update", help="add a report's news and price rows, then rebuild the pages")
    up.add_argument("--date", default=None)
    up.add_argument("--tickers", nargs="*")
    rn = sub.add_parser("render", help="rebuild the pages from the saved logs")
    rn.add_argument("--tickers", nargs="*")
    a = ap.parse_args(argv)
    if a.cmd == "update":
        date = a.date or pilib.run_date()
        tickers = a.tickers or tickers_for(date)
        if not tickers:
            print(f"No research for {date}; nothing to log."); return 1
        for r in update(date, tickers):
            note = "" if r["fact_checked"] else " (NOT fact-checked: researcher file used)"
            print(f"{r['ticker']}: {r['added']} new item(s){note} -> {r['page']}")
        return 0
    names = a.tickers or sorted(p.stem for p in (DATA / "news-log").glob("*.json"))
    for t in names:
        print(f"{t} -> {write_page(load_log(t))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
