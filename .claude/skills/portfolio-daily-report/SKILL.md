---
name: portfolio-daily-report
description: End-to-end method and output contract for Santi's daily portfolio report. Use when running the daily routine, rebuilding a missed report, or answering "what happened in my portfolio today". Coordinates the data pipeline, the per-holding research, the conclusions, the teaching layer, the quality gates, the email and the commit.
---

# Daily portfolio report

The report answers four questions for every holding, in this order, for a beginner:
1. **What happened?** (conclusion in one sentence)
2. **Why?** (market, industry or company; then the cause underneath, with sources)
3. **How does it work?** (the business, product or concept behind it, in plain words)
4. **What does it mean for my reasons to own it, and for my rules?** (no buy/sell advice)

The runbook with exact commands is `routines/daily-report.md`. This file explains the method.

## The evidence stack

Conclusions are only as good as the evidence underneath them. Build from the bottom up:

| Layer | Question it answers | Tool or skill |
|---|---|---|
| Position math | How much did I put in, what is it worth, what did today cost or earn me? | `market-metrics` scripts |
| Price behaviour | Is the move big for this stock? Trend, momentum, volatility, 52-week range | `market-metrics` |
| Attribution | How much of the move was the market, the industry, the company? | `why-analysis/scripts/move_attribution.py` |
| Events | What new, material information appeared, and when? | `news-and-events`, `source-hierarchy` |
| Official filings | What did the company formally disclose (8-K, 10-Q, Form 4, 144, S-3)? | `filings-decoder` |
| Fundamentals | Is the business growing, profitable, and is that changing? | `earnings-analysis` |
| Products | What is the product, who buys it, how much has it sold? | `product-explainer` |
| Thesis and rules | Is the reason I own it still true? Did my own rules fire? | `position-review` |
| Portfolio | How concentrated am I, how much do my holdings move together? | `portfolio-risk` |

## From evidence to a conclusion

For each holding write a **Bottom line** that states: the move, its main cause (with the
attribution numbers), and the thesis status. Then the explanation. Rules for conclusions:

- **One cause per sentence, ranked by weight.** If the market explains 80% of today's move,
  lead with the market, not with a headline that happened to appear the same day.
- **Correlation is not cause.** A news item counts as the cause only if its timing lines up
  with the move and the company-specific part of the move is large (attribution z-score beyond
  about 1.5). Otherwise say "no company-specific reason needed: the market moved".
- **Profits or excitement?** When a stock re-rates, say whether expected profits changed
  (estimates, guidance) or only the price investors pay for them (the multiple), using
  `move_attribution.decompose_price_change` when earnings data exists.
- **Confidence labels.** High = primary source confirms it. Medium = top-tier reporting or a
  strong inference from data. Low = plausible, unconfirmed. Say which.
- **What changed since yesterday.** Repeat nothing that has not moved.

## The report contract

Use `templates/report.md`. The linter enforces it:
- First section `## The bottom line` (3-5 bullets for the whole portfolio).
- `## Your rules today`, `## Position: <TICKER> (<Company>)` per holding with **Where it stands**,
  **What happened, and why**, **How this works**, **Case to stay**, **Case to retreat**,
  **Thesis check**, **Coming up**.
- `## Your portfolio as a whole`, `## Lesson of the day`, `## New words today`,
  `## Data quality and sources` ending with the disclaimer.
- Every news bullet cites `[Source, YYYY-MM-DD](https://...)`. No sources from the avoid list.
- No advice language. New jargon explained under "New words today".

A calibrated example lives in `templates/example-report.md` (a fictional company, so its
numbers can never leak into a real report). Match its depth and tone, not its facts.

## Quality gates

challenger agent -> fact-checker agent -> plain-english-editor agent -> `scripts/lint_report.py`.
The challenger's job is to change the conclusion when the evidence is weak; take its findings
seriously rather than adding caveats.

## Scripts in this skill

- `scripts/load_holdings.py`: sheet rows or fallback CSV -> `data/holdings/<DATE>.json`
- `scripts/lint_report.py`: the report contract check (exit 1 on errors)
- `scripts/render_pdf.py`: finished report -> `reports/pdf/<DATE>.pdf` (fpdf2)
- `scripts/render_email.py`: markdown -> simple HTML (used by `render_pdf.py`; email delivery is off)
