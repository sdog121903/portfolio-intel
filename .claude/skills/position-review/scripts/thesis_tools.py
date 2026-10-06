#!/usr/bin/env python3
"""Keep the thesis files current: refresh their numbers, and flag what is out of date.

    python3 thesis_tools.py numbers [--date DATE] [--tickers ...]
        Rebuilds the "The numbers behind it" block in each theses/<TICKER>.md, between
        <!-- numbers:start --> and <!-- numbers:end -->, from data/fundamentals/<TICKER>.json
        (quarterly SEC figures) and data/metrics/<DATE>.json (price trend). Only that block changes.

    python3 thesis_tools.py check [--date DATE] [--tickers ...] [--strict]
        Lists every thesis file that needs attention: missing sections, TODO left in an
        approved section, "Facts as of" older than a high-importance news item in the news log
        or older than 45 days, or a change log with no entry since the facts were last updated.
        --strict exits 1 when anything is flagged.

Facts and arithmetic only; nothing here is a buy or sell signal.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

THESES = pilib.ROOT / "theses"
DATA = pilib.DATA
START, END = "<!-- numbers:start", "<!-- numbers:end -->"
REQUIRED = ["Why I own it", "What the company does", "How it makes money", "Metrics that matter",
            "What must stay true", "Invalidation triggers", "Facts as of", "Change log"]
MAX_FACTS_AGE_DAYS = 45


# ---------------------------------------------------------------- numbers
def _money(x: Optional[float]) -> str:
    if x is None:
        return "n/a"
    a = abs(x)
    s = f"${a / 1e9:,.2f}bn" if a >= 1e9 else f"${a / 1e6:,.1f}m"
    return ("-" if x < 0 else "") + s


def _pct(x: Optional[float], sign: bool = True) -> str:
    return "n/a" if x is None else (f"{x:+.1f}%" if sign else f"{x:.1f}%")


def _direction(first: Optional[float], last: Optional[float], unit: str = " points") -> str:
    if first is None or last is None:
        return "not enough data"
    d = last - first
    word = "rising" if d > 0.5 else "falling" if d < -0.5 else "about flat"
    return f"{word} ({first:.1f}% to {last:.1f}%, {d:+.1f}{unit})"


def business_block(fund: dict) -> list:
    qs = [q for q in fund.get("latest_quarters") or [] if q.get("revenue") is not None]
    if not qs:
        return ["*No quarterly SEC figures for this company (it files as a foreign company); see the key trends "
                "below, taken from its own results releases.*"]
    last5 = qs[-5:]
    out = ["**The business, last five quarters** (SEC filings via `data/fundamentals/`; Q4 figures marked * are the "
           "annual total minus the three other quarters)", "",
           "| Quarter (period end) | Revenue | vs a year earlier | Gross margin | Operating margin | Net income |",
           "|---|---|---|---|---|---|"]
    for q in reversed(last5):
        star = "*" if (q.get("source") or {}).get("derived") else ""
        out.append(f"| {q.get('fiscal')}{star} ({q.get('period_end')}) | {_money(q.get('revenue'))} | "
                   f"{_pct(q.get('revenue_yoy_pct'))} | {_pct(q.get('gross_margin_pct'), False)} | "
                   f"{_pct(q.get('operating_margin_pct'), False)} | {_money(q.get('net_income'))} |")
    newest = qs[-1]
    up_in_a_row = 0
    for a, b in zip(reversed(qs[:-1]), reversed(qs)):
        if b["revenue"] > a["revenue"]:
            up_in_a_row += 1
        else:
            break
    last4 = qs[-4:]
    profitable = sum(1 for q in last4 if (q.get("net_income") or 0) > 0)
    yoys = [q.get("revenue_yoy_pct") for q in last4 if q.get("revenue_yoy_pct") is not None]
    accel = ""
    if len(yoys) >= 2:
        accel = (" Growth is speeding up" if yoys[-1] > yoys[0] + 1 else
                 " Growth is slowing" if yoys[-1] < yoys[0] - 1 else " Growth is steady")
        accel += f" (from {yoys[0]:+.1f}% to {yoys[-1]:+.1f}% over the last four quarters)."
    out += ["", "*What the trend says:*",
            f"- Revenue: {_money(newest['revenue'])} in the latest quarter, {_pct(newest.get('revenue_yoy_pct'))} from a year "
            f"earlier; it has grown {up_in_a_row} quarter{'' if up_in_a_row == 1 else 's'} in a row.{accel}",
            f"- Gross margin (share of each sale left after making the product): "
            f"{_direction(last4[0].get('gross_margin_pct'), last4[-1].get('gross_margin_pct'))} over the last four quarters.",
            f"- Operating margin (share left after all running costs): "
            f"{_direction(last4[0].get('operating_margin_pct'), last4[-1].get('operating_margin_pct'))}.",
            f"- Profit: positive net income in {profitable} of the last {len(last4)} quarters."]
    if fund.get("stale_warning"):
        out.append(f"- **Data warning:** {fund['stale_warning']}")
    return out


def stock_block(m: Optional[dict]) -> list:
    if not m:
        return ["*No price data for this run.*"]
    r = m.get("returns_pct") or {}
    vs = (m.get("pct_vs_sma") or {}).get("200")
    return [f"**The stock** (to {m.get('as_of')}, `data/metrics/`)", "",
            "| 1 month | 3 months | 6 months | 1 year | vs its 200-day average | Worst fall in the past year | Typical day |",
            "|---|---|---|---|---|---|---|",
            f"| {_pct(r.get('1m'))} | {_pct(r.get('3m'))} | {_pct(r.get('6m'))} | {_pct(r.get('1y'))} | {_pct(vs)} | "
            f"{_pct(m.get('max_drawdown_1y_pct'))} | {_pct(m.get('atr_pct_of_price'), False)} |", "",
            f"*Price trend:* {m.get('trend_state') or 'n/a'}. (The 200-day average is the average closing price over "
            "about the last ten months; trading above it usually means a longer uptrend.)"]


def numbers_block(ticker: str, date: str) -> str:
    fpath = DATA / "fundamentals" / f"{ticker}.json"
    mpath = DATA / "metrics" / f"{date}.json"
    fund = pilib.read_json(fpath) if fpath.exists() else {}
    m = pilib.read_json(mpath).get("positions", {}).get(ticker) if mpath.exists() else None
    lines = [f"{START} (rebuilt by thesis_tools.py from data as of {date}; edits inside this block are lost) -->", ""]
    lines += business_block(fund) + [""] + stock_block(m) + ["", END]
    return "\n".join(lines)


def replace_block(text: str, block: str) -> str:
    if START in text and END in text:
        head, rest = text.split(START, 1)
        _, tail = rest.split(END, 1)
        return head + block + tail
    raise ValueError("no numbers block markers")


# ---------------------------------------------------------------- check
def sections(text: str) -> dict:
    out = {}
    for part in re.split(r"(?m)^## ", text)[1:]:
        head, _, body = part.partition("\n")
        out[head.strip()] = body
    return out


def check_file(ticker: str, today: str) -> list:
    path = THESES / f"{ticker}.md"
    if not path.exists():
        return ["no thesis file"]
    text = path.read_text(encoding="utf-8")
    secs = sections(text)
    issues = []
    for want in REQUIRED:
        if not any(h.startswith(want) for h in secs):
            issues.append(f"missing section: {want}")
    for h, body in secs.items():
        if h.startswith(("Why I own it", "What must stay true", "Invalidation triggers")) and "TODO" in body:
            issues.append(f"TODO left in '{h}'")
    facts_head = next((h for h in secs if h.startswith("Facts as of")), "")
    m = re.search(r"\d{4}-\d{2}-\d{2}", facts_head)
    facts_date = m.group(0) if m else None
    if not facts_date:
        issues.append("'Facts as of' has no date")
    else:
        if pilib.days_between(facts_date, today) > MAX_FACTS_AGE_DAYS:
            issues.append(f"'Facts as of' is {pilib.days_between(facts_date, today)} days old (over {MAX_FACTS_AGE_DAYS})")
        log = DATA / "news-log" / f"{ticker}.json"
        if log.exists():
            newer = [it for it in pilib.read_json(log).get("items", [])
                     if it.get("materiality") == "high" and str(it.get("date", ""))[:10] > facts_date]
            if newer:
                issues.append(f"{len(newer)} high-importance news item(s) since 'Facts as of {facts_date}' "
                              f"(newest {max(str(i['date'])[:10] for i in newer)}): refresh the facts")
        changes = re.findall(r"(?m)^- (\d{4}-\d{2}-\d{2})", secs.get("Change log", ""))
        if not changes or max(changes) < facts_date:
            issues.append("change log has no entry since the facts were last updated")
    if START not in text:
        issues.append("no numbers block (run: thesis_tools.py numbers)")
    return issues


def held_tickers() -> list:
    try:
        return sorted({p["ticker"] for p in pilib.load_holdings().get("positions", []) if p.get("ticker")})
    except Exception:
        return sorted(p.stem for p in THESES.glob("*.md") if p.stem.isupper() and p.stem != "README")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["numbers", "check"])
    ap.add_argument("--date", default=None)
    ap.add_argument("--tickers", nargs="*")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    date = a.date or pilib.run_date()
    tickers = a.tickers or held_tickers()
    flagged = 0
    for t in tickers:
        path = THESES / f"{t}.md"
        if a.cmd == "numbers":
            if not path.exists():
                print(f"{t}: no thesis file"); continue
            try:
                path.write_text(replace_block(path.read_text(encoding="utf-8"), numbers_block(t, date)), encoding="utf-8")
                print(f"{t}: numbers refreshed")
            except ValueError:
                print(f"{t}: no numbers block markers; add them under 'Why I own it'")
        else:
            issues = check_file(t, date)
            flagged += bool(issues)
            print(f"{t}: " + ("OK" if not issues else "; ".join(issues)))
    return 1 if (a.strict and flagged) else 0


if __name__ == "__main__":
    sys.exit(main())
