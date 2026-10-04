# Weekly deep dive runbook

One company per week gets a full fundamental analysis, so that over a month every holding's
thesis is rebuilt from primary documents and Santi learns how a professional reads a company.

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
2. Update `theses/<TICKER>.md`: refresh "What the company does", "Facts as of", "Metrics that
   matter", "What must stay true" and "Invalidation triggers", each with sources, and set
   "Last deep dive". **Never edit "Why I own it"**: that section is Santi's own words. If the
   evidence contradicts it, say so in the deep dive instead.

## 4. Teach

Add the new concepts this deep dive used to `learning/` (lesson file and ledger), exactly as
in the daily runbook, steps 7 and 10.

## 5. Commit, push, email

Commit to `main`. Email a short summary (the plain-English summary plus a link to the full
deep dive) to `owner.email_to` only, subject `Deep dive: <TICKER> - <one-line conclusion>`.
