# Weekly deep dive runbook

One company per week gets a full fundamental analysis, so that over about three months (one
holding a week) every holding's thesis is rebuilt from primary documents and Santi learns how a professional reads a company.

## 1. Choose the company

- Any holding that reported earnings in the last 7 days goes first.
- Otherwise, the holding whose `theses/<TICKER>.md` has the oldest "Last deep dive" date
  (or none), up to `run.deep_dive_max_age_days`.
- Read the latest holdings file in `data/holdings/` to know what is open.

## 2. Run the stock-analysis skill in Standard mode

Read `.claude/skills/stock-analysis/SKILL.md` and follow its stages, using the sector playbook
from `config/portfolio.toml` `[sector_playbooks]`. Primary documents first: the latest 10-K and
10-Qs, the last two earnings releases and call transcripts, the investor presentation. Use
`data/fundamentals/<TICKER>.json` for the quarterly numbers (run
`python3 .claude/skills/earnings-analysis/scripts/fetch_fundamentals.py --tickers <TICKER>` if stale).

Respect its non-negotiables: never invent a number, cite every figure, run its
`scripts/verify_data.py` and `scripts/lint_report.py`, write a genuine bear case, and do the
challenge pass (use the challenger agent). Analysis, not advice: no price target for Santi,
no buy/sell call.

## 3. Write two things

1. `reports/deep-dives/<TICKER>-<DATE>.md`: the full stock-analysis report, plus at the top a
   "Plain-English summary" (300 words max) written with `explain-like-a-teacher`: what the
   company sells, who buys it, how it makes money, what the numbers say, the strongest case
   for and against, and what would prove the thesis wrong.
2. Update `theses/<TICKER>.md`: refresh "What the company does", "How it makes money", "Facts as
   of" and "Metrics that matter", each with sources, and set "Last deep dive". "What must stay
   true" and "Invalidation triggers" are Santi's to edit: add new sourced items, but never delete
   or reword his; propose any other change in the "Change log". **Never rewrite "Why I own it"**: Santi approved it
   (2026-10-05). Only its auto-built numbers block and the sourced "Key trends" lines are refreshed. If the
   evidence contradicts it, say so in the deep dive instead.
   Also refresh "Key trends" and every pillar's "Now" line and trigger's "Status now" from the
   primary documents, run `thesis_tools.py numbers` and `check`, and add a dated change-log line.
   If the evidence contradicts a thesis, pillar or trigger, propose the change ("Proposed:" in the
   change log and in the deep dive) for Santi to approve; never rewrite his approved wording.
3. Add the deep dive's material, sourced events (results, guidance, filings) to the news log the
   same way as the daily runbook, step 10, so the stock's long-run record includes them.

## 4. Teach

Add the new concepts this deep dive used to `learning/` (lesson file and ledger), exactly as
in the daily runbook, steps 7 and 10.

## 5. PDF, commit, push

`python3 .claude/skills/portfolio-daily-report/scripts/render_pdf.py reports/deep-dives/<TICKER>-<DATE>.md`
writes `reports/pdf/deep-dive-<TICKER>-<DATE>.pdf`. Everything stays on this computer: do not
commit or push, and no email.
