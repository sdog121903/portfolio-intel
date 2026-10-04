#!/usr/bin/env python3
"""Normalise trade rows into data/holdings/<DATE>.json.

Two inputs are supported:
  --from-rows data/holdings/raw-<DATE>.json   rows the agent read from the Google Sheet
  --from-csv  config/holdings_fallback.csv     manual fallback when the sheet cannot be read

Raw row keys (missing keys are fine): open_date, ticker, side, order_type, shares, name,
entry_price_estimate, fill_price, limit_or_stop_price, stop_loss_alert, target_price,
fees, fee_override, exit_date, exit_price, notes.

Rules: a row is OPEN when it has a ticker and no exit_date. Several open rows of the same
ticker are merged (shares summed, share-weighted average entry). Entry price = fill_price if
present, else entry_price_estimate (flagged as an estimate so the report can say so).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402


def to_float(v):
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("$", "").replace(",", "").strip()
    if s in ("", "-", "#N/A", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def to_date(v):
    if v in (None, ""):
        return None
    s = str(v).strip()
    try:
        return pilib.parse_date(s).isoformat()
    except ValueError:
        pass
    import datetime as dt
    for fmt in ("%d %b %Y", "%d/%m/%Y", "%m/%d/%Y", "%b-%d-%Y", "%d-%b-%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def normalise(rows: list, source: str, as_of: str) -> dict:
    warnings, positions, closed = [], {}, []
    for i, raw in enumerate(rows, start=1):
        ticker = str(raw.get("ticker") or "").strip().upper()
        if not ticker:
            continue
        shares = to_float(raw.get("shares"))
        if not shares or shares <= 0:
            warnings.append(f"row {i} ({ticker}): shares missing or not positive, row skipped")
            continue
        fill = to_float(raw.get("fill_price"))
        est = to_float(raw.get("entry_price_estimate"))
        entry, entry_src = (fill, "fill") if fill else (est, "sheet-estimate") if est else (None, "missing")
        fees = to_float(raw.get("fee_override"))
        if fees is None:
            fees = to_float(raw.get("fees")) or 0.0
        row = {
            "ticker": ticker,
            "name": (raw.get("name") or "").strip() if isinstance(raw.get("name"), str) and not str(raw.get("name")).startswith("#") else "",
            "side": "Short" if str(raw.get("side") or "").strip().lower() == "short" else "Long",
            "order_type": (raw.get("order_type") or "Market").strip() if isinstance(raw.get("order_type"), str) else "Market",
            "shares": shares,
            "entry_price": entry,
            "entry_price_source": entry_src,
            "open_date": to_date(raw.get("open_date")),
            "fees": fees,
            "stop_loss": to_float(raw.get("stop_loss_alert")),
            "target": to_float(raw.get("target_price")),
            "limit_or_stop_price": to_float(raw.get("limit_or_stop_price")),
            "notes": (raw.get("notes") or "") if isinstance(raw.get("notes"), str) else "",
        }
        if entry is None:
            warnings.append(f"{ticker}: no fill price or estimate yet; P&L cannot be computed until one is entered")
        elif entry_src == "sheet-estimate":
            warnings.append(f"{ticker}: entry price is the sheet's estimate, not your Fidelity fill price")
        if row["open_date"] and row["open_date"] > as_of:
            warnings.append(f"{ticker}: open date {row['open_date']} is in the future (order not filled yet?)")
        exit_date = to_date(raw.get("exit_date"))
        if exit_date:
            row.update({"exit_date": exit_date, "exit_price": to_float(raw.get("exit_price"))})
            closed.append(row)
            continue
        if ticker in positions:
            p = positions[ticker]
            if p["side"] != row["side"]:
                warnings.append(f"{ticker}: long and short rows both open; kept separately as {ticker}-{row['side']}")
                positions[f"{ticker}-{row['side']}"] = row
                continue
            total = p["shares"] + row["shares"]
            if p["entry_price"] is not None and row["entry_price"] is not None:
                p["entry_price"] = (p["entry_price"] * p["shares"] + row["entry_price"] * row["shares"]) / total
            else:
                p["entry_price"] = None
                p["entry_price_source"] = "missing"
            if row["entry_price_source"] == "sheet-estimate" and p["entry_price_source"] == "fill":
                p["entry_price_source"] = "mixed"
            p["shares"] = total
            p["fees"] += row["fees"]
            p["lots"] += 1
            if row["open_date"] and (not p["open_date"] or row["open_date"] < p["open_date"]):
                p["open_date"] = row["open_date"]
            for k in ("stop_loss", "target"):
                if row[k] is not None:
                    p[k] = row[k]  # the most recent row's level wins
        else:
            row["lots"] = 1
            positions[ticker] = row
    for p in positions.values():
        if p["entry_price"] is not None:
            p["entry_price"] = round(p["entry_price"], 4)
            p["invested"] = round(p["entry_price"] * p["shares"], 2)
        else:
            p["invested"] = None
    return {"as_of": as_of, "source": source, "positions": list(positions.values()),
            "closed": closed, "warnings": warnings}


def read_csv_rows(path: Path) -> list:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-rows", type=Path)
    g.add_argument("--from-csv", type=Path)
    ap.add_argument("--date", default=None, help="as-of date (default: today in the owner's time zone)")
    a = ap.parse_args(argv)
    as_of = a.date or pilib.run_date()
    if a.from_rows:
        data = pilib.read_json(a.from_rows)
        rows = data["rows"] if isinstance(data, dict) else data
        source = "google-sheet"
    else:
        rows = read_csv_rows(a.from_csv)
        source = "fallback-csv"
    out = normalise(rows, source, as_of)
    path = pilib.write_json(pilib.DATA / "holdings" / f"{as_of}.json", out)
    print(f"{len(out['positions'])} open positions, {len(out['closed'])} closed -> {path}")
    for w in out["warnings"]:
        print("WARNING:", w)
    return 0 if out["positions"] or out["closed"] else 2


if __name__ == "__main__":
    sys.exit(main())
