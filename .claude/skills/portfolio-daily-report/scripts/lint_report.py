#!/usr/bin/env python3
"""Check a finished daily report against the report contract before it is committed or emailed.

ERRORS (must fix):
  - a required section is missing, or "The bottom line" is not the first section
  - a position section lacks one of its parts (Bottom line, What happened and why, How this works,
    Case to stay, Case to retreat, Thesis check, Coming up)
  - an open holding in data/holdings/<DATE>.json has no position section (date read from the file name)
  - today's lesson was not saved to learning/lessons/<DATE>.md (date read from the file name)
  - a news bullet has no citation in the form [Source, YYYY-MM-DD](https://...) and is not "No material news"
  - advice language ("you should sell", "we recommend", "consider selling", ...)
  - analyst-style calls ("price target of", "buy rating") on a line without a citation: reported
    analyst opinions are fine when cited, uncited they read as our own call
  - a link to an "avoid" source (config/sources.toml)
  - a jargon word that the learning ledger marks as "new" is used but not explained under "New words today"
WARNINGS:
  - fewer than half of the links come from tier-1 or tier-2 sources
  - the disclaimer line is missing
Usage: python lint_report.py reports/daily/2026/10/2026-10-05.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import pilib  # noqa: E402

REQUIRED = ["The bottom line", "Your rules today", "Your portfolio as a whole", "Lesson of the day",
            "New words today", "Data quality and sources"]
POSITION_PARTS = ["Bottom line", "What happened, and why", "How this works", "Case to stay", "Case to retreat",
                  "Thesis check", "Coming up"]
ADVICE = [r"\byou should (consider )?(buy|sell|hold|trim|add)(ing)?\b", r"\bwe recommend\b", r"\bi recommend\b",
          r"\bconsider (buying|selling|trimming|exiting)\b", r"\bi would (buy|sell|hold)\b",
          r"\bbuy now\b", r"\bsell now\b", r"\btime to (buy|sell)\b", r"\bposition siz(e|ing)\b", r"\bguaranteed\b"]
OPINION = [r"\bprice target of\b", r"\b(strong )?(buy|sell) rating\b"]
CITATION = re.compile(r"\[[^\]]+?,\s*\d{4}-\d{2}-\d{2}\]\((https?://[^)\s]+)\)")
LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
DISCLAIMER = "not investment advice"


def sections(text: str, level: str = "## ") -> dict:
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith(level):
            cur = line[len(level):].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def host_tier(url: str, tiers: dict) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    full = url.lower()
    for entry in tiers.get("avoid", {}).get("domains", []):
        if entry in full:
            return "avoid"
    for tier in ("tier1", "tier2", "tier3"):
        for d in tiers.get(tier, {}).get("domains", []):
            if host == d or host.endswith("." + d):
                return tier
    return "other"


def lint(text: str, tiers: dict, ledger: dict, jargon: list, open_tickers: list | None = None) -> tuple:
    errors, warnings = [], []
    secs = sections(text)
    names = list(secs)
    for req in REQUIRED:
        if not any(n.startswith(req) for n in names):
            errors.append(f"missing section: '## {req}'")
    if names and not names[0].startswith("The bottom line"):
        errors.append("the first section must be '## The bottom line' (conclusions first)")
    positions = [n for n in names if n.startswith("Position:")]
    if not positions:
        errors.append("no '## Position: TICKER ...' sections")
    if open_tickers is not None:
        covered = {n.split(":", 1)[1].split()[0].upper() for n in positions if n.split(":", 1)[1].split()}
        for t in sorted(set(open_tickers) - covered):
            errors.append(f"open holding {t} has no '## Position: {t}' section")
        for t in sorted(covered - set(open_tickers)):
            warnings.append(f"'## Position: {t}' is not an open holding today")
    for n in positions:
        body = secs[n]
        for part in POSITION_PARTS:
            if part.lower() not in body.lower():
                errors.append(f"{n}: missing '{part}'")
        m = re.search(r"what happened, and why\**\s*\n(.*?)(\n\*\*|\Z)", body, re.S | re.I)
        if m:
            for line in m.group(1).splitlines():
                s = line.strip()
                if s.startswith(("- ", "* ")) and "no material news" not in s.lower() and not CITATION.search(s):
                    errors.append(f"{n}: news bullet without a [Source, YYYY-MM-DD](url) citation: {s[:80]}")
    low = text.lower()
    for line in low.splitlines():
        for pat in ADVICE:
            for mm in re.finditer(pat, line):
                errors.append(f"advice language: '{mm.group(0)}'")
        if not CITATION.search(line):
            for pat in OPINION:
                for mm in re.finditer(pat, line):
                    errors.append(f"'{mm.group(0)}' without a citation: name and cite the analyst, or remove it")
    counts = {"tier1": 0, "tier2": 0, "tier3": 0, "other": 0, "avoid": 0}
    for url in LINK.findall(text):
        t = host_tier(url, tiers)
        counts[t] += 1
        if t == "avoid":
            errors.append(f"link to an avoid-list source: {url}")
    for kw in tiers.get("avoid", {}).get("keywords", []):
        if kw.lower() in low:
            warnings.append(f"avoid-list phrase appears: '{kw}'")
    total = sum(counts.values())
    if total and (counts["tier1"] + counts["tier2"]) / total < 0.5:
        warnings.append(f"only {counts['tier1'] + counts['tier2']} of {total} links are tier 1/2 sources")
    new_words = next((secs[n] for n in names if n.startswith("New words today")), "").lower()
    body_wo_glossary = "\n".join(v for k, v in secs.items() if not k.startswith("New words today")).lower()
    concepts = ledger.get("concepts", {})
    for term in jargon:
        tl = term.lower()
        if re.search(r"(?<![a-z])" + re.escape(tl) + r"(?![a-z])", body_wo_glossary):
            level = concepts.get(" ".join(tl.split()), {}).get("level", "new")
            if level == "new" and not re.search(r"(?<![a-z])" + re.escape(tl) + r"(?![a-z])", new_words):
                errors.append(f"jargon '{term}' is new to the reader but not explained under 'New words today'")
    if DISCLAIMER not in low:
        warnings.append("disclaimer line ('... not investment advice') is missing")
    return errors, warnings, counts


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    path = Path(argv[0])
    text = path.read_text(encoding="utf-8")
    tiers = pilib.load_toml(pilib.CONFIG / "sources.toml")
    ledger_path = pilib.LEARNING / "concepts.json"
    ledger = pilib.read_json(ledger_path) if ledger_path.exists() else {"concepts": {}}
    jl = Path(__file__).resolve().parents[2] / "explain-like-a-teacher" / "references" / "jargon-watchlist.txt"
    jargon = [l.strip() for l in jl.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if jl.exists() else []
    dm = re.search(r"\d{4}-\d{2}-\d{2}", path.name)
    open_tickers = None
    if dm:
        hp = pilib.DATA / "holdings" / f"{dm.group(0)}.json"
        if hp.exists():
            open_tickers = [p["ticker"].split("-")[0] for p in pilib.read_json(hp).get("positions", [])]
    errors, warnings, counts = lint(text, tiers, ledger, jargon, open_tickers)
    if dm and not (pilib.LEARNING / "lessons" / f"{dm.group(0)}.md").exists():
        errors.append(f"lesson of the day not saved to learning/lessons/{dm.group(0)}.md")
    print(f"links by tier: {counts}")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
