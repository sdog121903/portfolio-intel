# Requirements audit

Audited 2026-10-04 against `docs/requirements.md` (R1-R18). Every requirement's files were opened
and the behaviour checked. Code paths were exercised by the offline tests and by a live data run
on the owner's Mac. "Pending cloud" items can only be proven by the first routine run.

Result: **all 18 PASS on the repository side; the cloud part of R7, R8, R14, R16 and R18 is pending
the routine's first run.**
14 gaps were found and fixed (column "Fix made"). 37 tests pass (up from 23).

| ID | Result | Evidence | Fix made |
|---|---|---|---|
| R1 | PASS | `load_holdings.py` (open = ticker and no exit date, lots merged, blank rows skipped); live run read 11 sheet-shaped rows into 11 positions; `lint_report.py` now fails a report missing a position for any open holding (`test_position_contract_and_coverage`) | GAP fixed: the linter only checked that *some* position existed. Config and theses covered 4 of the 11 holdings in the sheet (and NVDA, which is not held); all 11 are now configured |
| R2 | PASS | `holding-researcher.md` schema (events, products with sales, earnings, analysts, insiders, filings, catalysts); `fetch_edgar.py` decodes 8-K items, Form 4 with 10b5-1 flag | GAP fixed: `next_earnings` (date, consensus, guidance) is now always filled; foreign-filer forms 6-K, 20-F, 40-F decoded (TSM); a footnote saying "not pursuant to a 10b5-1 plan" no longer counts as a plan; one failed ticker no longer drops every holding's filings |
| R3 | PASS | `source-hierarchy`, `config/sources.toml`, linter citation and avoid checks, `fact-checker.md` | GAP fixed: fact-checker now enforces the two-independent-sources rule; tier-1 domains added for the 7 new companies |
| R4 | PASS | `market_metrics.py`, `move_attribution.py`, `portfolio_risk.py`, `earnings-analysis`, vendored `stock-analysis` | GAP fixed: `fetch_fundamentals.py` took the first XBRL tag found, so NVDA's "latest quarter" was January 2020 and LITE's June 2025. Tags are now merged (NVDA: July 2026, LITE: June 2026); data older than a normal filing cycle carries a `stale_warning` (BE today) |
| R5 | PASS | `CLAUDE.md` bottom line, `explain-like-a-teacher`, `learning-tracker`, template order (Bottom line, Market vs company, How this works) | GAP fixed: linter now requires Bottom line, How this works and Coming up in every position, and that `learning/lessons/<DATE>.md` was saved; "New words today" matching is whole-word ("eps" no longer satisfied by "steps") |
| R6 | PASS | `check_rules.py`, `position-review`, `rules.toml`, template "Your rules today"; advice grep matches only lists of forbidden phrases | GAP fixed: the template now says why there is never a buy/sell call; the linter no longer rejects cited analyst ratings and price targets (R2 requires reporting them) and now catches paraphrased advice ("consider selling", "I would sell") |
| R7 | PASS (first cloud run pending) | Requirement changed 2026-10-04: no email, Markdown + PDF in `reports/`. `render_pdf.py` (tests `TestPdf`), runbook steps 11-12, routine prompts say never send email | Earlier gap (email before push) is moot now that email is off |
| R8 | PASS repo side; pending cloud | `daily-routine-prompt.md` pushes to `main` | Routine not yet created |
| R9 | PASS | 13 skills with SKILL.md and references/scripts, 4 agents, `docs/sources-and-credits.md`, `LICENSES/` | - |
| R10 | PASS (caveat) | Fill price, then sheet estimate, then market estimate, labelled; fees 0 default; tests `test_merge_and_estimates`, `test_weekend_and_future_dates` | GAP fixed: lots mixing a fill price and an estimate are labelled "mixed". Caveat: the sheet dates weekend orders as the Monday fill date, so the weekend-to-Monday-open rule cannot tell they were weekend orders; the entry is exact once the Fidelity fill price is typed in column Q |
| R11 | PASS | Yahoo, Nasdaq, SEC need no key; Alpha Vantage optional | GAP fixed: Stooq now serves a browser check instead of data; replaced by Nasdaq's free quote API |
| R12 | PASS | `portfolio_risk.py` `goals_check`; live: technology 68.9%, AI data centers 45.9%, beta 2.18, 7 high movers | GAP fixed: goals_check now includes portfolio volatility, beta and high movers (the "safe" and "high movers" goals had no numbers); a ticker missing from config is listed as unclassified and can no longer become the "largest theme" |
| R13 | PASS | `run_daily_data.py` fail-soft with status file; live run: 8/8 steps OK, 20 tickers priced | GAP fixed: every price download failed (Yahoo answered 429 to the spoofed browser User-Agent); an honest User-Agent fixed it |
| R14 | PASS (repository privacy pending creation) | `CLAUDE.md` hard rules, routine prompt, `.gitignore`; no secrets in any file | GAP fixed: an API key in a failed URL was written into committed status files (now redacted, `test_api_keys_are_redacted_from_errors`); "the sheet is read-only" added to `CLAUDE.md`, routine prompt and runbook; `.gitignore` covers `.env*`, `*.pem`, `*.key` |
| R15 | PASS | `weekly-deep-dive.md`, `stock-analysis`, "Why I own it" never edited | GAP fixed: the deep dive no longer overwrites the owner's edited pillars and triggers; it adds or proposes |
| R16 | PASS repo side; pending | Setup prompt Phase 11 | The Cowork task was not visible from this session; the owner checks it |
| R17 | PASS | Verified 2026-10-04: the Google Drive connector on this Claude account opens the FIDELITY sheet (owner sgomezo2003@gmail.com) and its Trades tab | Setup prompt's "five open rows" corrected to eleven |
| R18 | PASS (trigger pending) | `pilib.run_date()` uses Europe/Madrid; `monday_window_hours = 78`; template header shows close date and window | - |

## Specific checks from the setup prompt

| # | Check | Result |
|---|---|---|
| 1 | Every active holding daily; closed excluded; lots merged | PASS (linter now enforces coverage) |
| 2 | News, announcements, filings, earnings, projected earnings, products with sales, analyst actions, 14-day catalysts | PASS after fixes in R2 |
| 3 | Primary first, two sources, dated citations, avoid list rejected | PASS after fixes in R3 |
| 4 | Bottom line, then why, then how; jargon defined; lesson saved; ledger updated | PASS after fixes in R5 |
| 5 | Stay/Retreat as his rules, thesis status, three sourced reasons each way, never advice; grep clean | PASS. Grep matches: `setup/SETUP_PROMPT.md` (the check itself), `position-review/SKILL.md` ("What never appears"), vendored `stock-analysis/SKILL.md` (a counter-example) |
| 6 | Report committed (email switched off 2026-10-04) | PASS: Markdown and PDF committed to `main`; no step sends email |
| 7 | Entry price order, always labelled | PASS with the R10 caveat |
| 8 | Goals lens, facts only | PASS after fixes in R12 |
| 9 | Weekly deep dive uses stock-analysis, never edits "Why I own it" | PASS |
| 10 | Only MIT files vendored; nothing downloaded from skill repos at run time | PASS: no clone, curl or npm of third-party repos; only `pip install -r requirements.txt` (tomli on old Python) |

## Known limits (not gaps)

- TSM files under IFRS, so the SEC's structured data has no quarterly figures for it; the file
  says so and the researcher uses TSMC's own monthly and quarterly releases.
- BE's latest 10-Q (filed 2026-07-28) is missing from the SEC's structured data; flagged as stale.
- The local Mac runs Python 3.9 (tests pass with `tomli`); the cloud's first run exercises 3.11+.
- Price sources are free and unofficial; failures are reported in "Data quality and sources".
