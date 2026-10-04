#!/usr/bin/env python3
"""Keep track of what Santi has already been taught (learning/concepts.json).

Levels:  new      -> never explained: give the full explanation (what, why, how, example)
         learning -> explained before: give a one-line reminder
         known    -> seen many times: no definition needed unless asked

Commands
  status TERM [TERM ...]       what level each term is at (unknown terms are "new")
  taught TERM --one-liner "…"  record that TERM was explained today (creates or bumps it)
  due                          concepts worth a refresher today (spaced repetition: 2, 7, 21, 60 days)
  list                         everything in the ledger
Promotion: a concept becomes "learning" after its first explanation and "known" after it has
been seen on 5 different days. Santi can also edit learning/concepts.json by hand.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

LEDGER = pilib.LEARNING / "concepts.json"
INTERVALS = [2, 7, 21, 60]


def load() -> dict:
    return pilib.read_json(LEDGER) if LEDGER.exists() else {"concepts": {}}


def save(d: dict) -> None:
    pilib.write_json(LEDGER, d)


def key(term: str) -> str:
    return " ".join(term.lower().split())


def status(d: dict, term: str) -> str:
    c = d["concepts"].get(key(term))
    return c["level"] if c else "new"


def taught(d: dict, term: str, one_liner: str, today: str) -> dict:
    k = key(term)
    c = d["concepts"].get(k)
    if not c:
        c = {"term": term, "first_explained": today, "last_seen": today, "days_seen": 1,
             "level": "learning", "one_liner": one_liner}
    else:
        if c["last_seen"] != today:
            c["days_seen"] += 1
        c["last_seen"] = today
        if one_liner:
            c["one_liner"] = one_liner
        if c["days_seen"] >= 5:
            c["level"] = "known"
    d["concepts"][k] = c
    return c


def due(d: dict, today: str) -> list:
    out = []
    for c in d["concepts"].values():
        if c["level"] == "known":
            continue
        age = pilib.days_between(c["last_seen"], today)
        step = INTERVALS[min(c["days_seen"] - 1, len(INTERVALS) - 1)]
        if age >= step:
            out.append({"term": c["term"], "days_since_seen": age, "one_liner": c["one_liner"]})
    return sorted(out, key=lambda x: -x["days_since_seen"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status"); s.add_argument("terms", nargs="+")
    t = sub.add_parser("taught"); t.add_argument("term"); t.add_argument("--one-liner", default="")
    sub.add_parser("due"); sub.add_parser("list")
    a = ap.parse_args(argv)
    d, today = load(), pilib.run_date()
    if a.cmd == "status":
        for term in a.terms:
            print(f"{term}: {status(d, term)}")
    elif a.cmd == "taught":
        c = taught(d, a.term, a.one_liner, today)
        save(d)
        print(f"{c['term']}: {c['level']} (seen on {c['days_seen']} day(s))")
    elif a.cmd == "due":
        for c in due(d, today):
            print(f"{c['term']} ({c['days_since_seen']} days): {c['one_liner']}")
    else:
        for c in sorted(d["concepts"].values(), key=lambda c: c["term"].lower()):
            print(f"[{c['level']}] {c['term']}: {c['one_liner']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
