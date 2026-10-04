# Setup log

No secrets are recorded here.

## 2026-10-04: local install, tests, audit

- Location: `~/portfolio/portfolio-intel` (unpacked from `~/portfolio/portfolio-intel.zip`; the
  folder matched the zip file for file).
- Inventory: every file and folder listed in the setup prompt is present (13 skills, 4 agents).
- Local Python is 3.9.6, so tests ran in a scratch virtual environment with `tomli`. Nothing was
  installed system-wide.
- Google Drive connector check: the FIDELITY sheet (owner sgomezo2003@gmail.com) and its Trades tab
  are readable from this Claude account. It holds **11** open rows (STRL, CRWD, MRNA, CRDO, LITE,
  TSM, AMD, PANW, BE, SNOW, A), not the 5 the repository was built for; NVDA is only on the
  Watchlist. All dated 2026-10-05 (weekend orders that fill Monday).
- First live data run: holdings OK, **prices failed for every ticker** (Yahoo 429, Stooq behind a
  browser check), so metrics and portfolio risk failed; filings OK; fundamentals ran but returned
  stale quarters for NVDA (2020) and LITE (2025).

### Changes made

- Prices: honest User-Agent (Yahoo now answers); Stooq replaced by Nasdaq's free API.
- Fundamentals: XBRL revenue/profit tags merged; staleness warning; IFRS filers explained.
- Filings: 6-K / 20-F / 40-F decoded; per-ticker error handling; negative 10b5-1 footnotes read correctly.
- Linter: full position contract, one position per open holding, lesson file saved, cited analyst
  opinions allowed, paraphrased advice caught, whole-word new-term check.
- Security: API keys redacted from error text; sheet read-only rule; `.gitignore` secrets patterns.
- Goals lens: volatility, beta, high movers, unclassified tickers.
- Config: sector fund, sector, themes and playbook for the 7 new tickers; tier-1 domains;
  fallback CSV mirrors the sheet; thesis files for MRNA, TSM, AMD, PANW, BE, SNOW, A.
- Runbook: email file written, then commit and push, then send; deep dive no longer overwrites the owner's pillars and triggers;
  researcher always fills next earnings.
- Docs: README, setup prompt (allowlist, counts, holdings), data endpoints, requirements audit.

### Verified

- `python -m unittest discover -s tests`: 37 tests OK.
- Example report lints PASS.
- Live run from sheet-shaped rows: 8/8 pipeline steps OK; 20 tickers priced (closes match the sheet);
  fundamentals current for 10 of 11 (BE flagged stale, TSM explained).
- Advice grep: only allowed matches.

## Still to do

- ~~Private GitHub repository and push; `repo.url` in `config/portfolio.toml`.~~ Done, see below.
- Cloud access (`/web-setup`), environment `portfolio-intel` with the allowlist in the setup prompt.
- Daily routine 07:07 Europe/Madrid; weekly deep dive Sundays 10:07 (optional).
- First run and checks; retire the Cowork task (not visible from this session) and any Apps Script trigger.

## 2026-10-04: pre-push adversarial review

A multi-agent review (5 finders, 3 skeptics per finding, 110 agents) checked every change above.
35 findings, 11 survived verification (9 distinct), all fixed with tests:
- Bloom Energy revenue used the narrower contract-revenue tag; total "Revenues" now preferred
  (matches the company's release: $751.1M, not $746.4M).
- Derived Q4 EPS (annual minus three quarters) is no longer shown; it was far off for LITE and PANW.
- Year-ago quarters carried the next year's fiscal label; labels now come from the first filing.
- Net income no longer mixes in a different tag (ProfitLoss); only revenue merges tags.
- fetch_edgar now exits non-zero when a ticker's filings cannot be read, so the report lists it.
- 10b5-1 reading is per footnote, so an unrelated "not" no longer cancels a real plan.
- The email markdown is written before the commit, so it is saved with the report.
- Leftover Stooq mentions, sheet-access wording, audit counts; also references keyed to the
  current 11 holdings, KPIs for the new industries, a non-existent Sterling host removed,
  AMD and PANW thesis wording corrected.

## 2026-10-04: GitHub repository

- Owner's choice: GitHub account **sdog121903** (not santiago848). `gh auth login` added it as the
  active GitHub CLI account; santiago848 stays logged in (`gh auth switch` to change).
- Repository: https://github.com/sdog121903/portfolio-intel (**private**), branch `main`.
- History: commit 1 is the zip exactly as shipped; commit 2 is every local fix (diff = the review
  surface); later commits are configuration.
- Commit author: Santiago Gomez <145298037+sdog121903@users.noreply.github.com> (GitHub's private
  no-reply address, set in this repository only).
- Re-verified before pushing: 37 tests OK, example report lints PASS, live pipeline 8/8 OK,
  secret scan clean.
- `repo.url` set to the repository address.

## 2026-10-04: decisions for the routines

- Routines will run on the owner's **personal** Claude account, not the account used for this setup
  session (santiago@hobetu.ai). Routines, connectors, environment and billing are per account, so
  they are created there; step-by-step values are in `setup/ROUTINE_SETUP.md`.
- Model: Opus 5.5. Daily report 07:07 Europe/Madrid; weekly deep dive Sundays 10:07 Europe/Madrid.
- Old Cowork task "Daily portfolio report" (07:50 daily, on the setup account, routine id
  trig_01EsqNyLTgh3utJMNPgcJ5Cw, 11 connectors attached): pause after the first clean run of the
  new routine (owner's choice).

## 2026-10-04: delivery and scheduling changed

- Email switched off; every report is saved as Markdown and as a PDF (`reports/pdf/`, `render_pdf.py`).
- Research (74-agent check of docs and terms, every claim verified by two skeptics): the cloud-session
  credit does **not** cover Routines; there is no supported way to start an ordinary cloud session
  on a timer. Owner's choice: **tap to run** (`daily report` at 07:07, `deep dive` Sundays 10:07),
  paid by the credit until it ends. Steps in `setup/ROUTINE_SETUP.md`.
- Noted: the Claude CLI on this Mac reports a Pro plan for the setup account (Pro credit is $100);
  the credit must be on the account used to start the runs.
