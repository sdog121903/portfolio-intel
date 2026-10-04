# portfolio-intel

A daily, sourced, beginner-friendly report on every stock in Santi's FIDELITY trade tracker,
produced by Claude Code on your own computer when you type `/go`. It reads the
Google Sheet, downloads prices and SEC filings, researches every holding, explains what happened
and **why** in plain English, checks his own Stay/Retreat rules, and saves the report (Markdown and PDF)
on your computer (in this folder) so the history and his learning build up over time.

> Informational research and education, not investment advice. The report never tells you to
> buy or sell: it explains the evidence and tells you which of **your** rules fired.

## What is in the box

| Folder | Purpose |
|---|---|
| `CLAUDE.md` | The operating manual every run reads first. Bottom line: teach a beginner |
| `routines/` | What `/go` runs: the daily report and weekly deep-dive runbooks |
| `.claude/skills/` | 13 skills: teaching, why-analysis, sources, filings, market metrics, earnings, products, news, position review, portfolio risk, learning tracker, the report itself, and the vendored stock-analysis deep-dive skill |
| `.claude/agents/` | Researcher (one per stock, in parallel), challenger, fact-checker, plain-English editor |
| `config/` | Your sheet, rules, source tiers, benchmarks and themes |
| `theses/` | Why you own each stock (write yours!) and what would prove it wrong |
| `learning/` | Your textbook: daily lessons, the terms you know, the curriculum |
| `reports/` | Every report ever written |
| `scripts/`, `tests/` | The tested number-crunching (standard-library Python) |

## Set it up and run it

Everything runs on your own computer with your own Claude account: open Claude Code in this
folder and type **`/go`**. The report and its PDF appear in `reports/` and `reports/pdf/`; nothing
is uploaded or emailed, and git ignores your reports. Step by step: `setup/HOW_TO_RUN.md`.

## Make it yours
- **Write your reasons** in `theses/<TICKER>.md` under "Why I own it". The report tests the news
  against them every day.
- **Set your rules** in `config/rules.toml` and the Stop-loss and Target columns of your sheet.
- **New stock?** Add it to the sheet; add its industry fund, sector, themes and playbook in `config/portfolio.toml`
  and copy `theses/TEMPLATE.md`.
- **Already know a term?** Mark it "known" in `learning/concepts.json` and it stops being defined.

## Honest limits
- Prices come from free sources (Yahoo, Nasdaq) that can rate-limit or change; failures are
  reported, never hidden. SEC data is official and free.
- Entry prices are only exact when your Fidelity fill price is in the sheet; otherwise they are
  estimated and labelled.
- The scripts were tested offline with synthetic data; live data sources are first exercised by
  your first `/go`, so read its summary.
