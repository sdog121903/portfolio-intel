# Daily report runbook

Follow these steps in order. Each step names the skill to read and the file it produces.
Budget: a normal day is roughly 6-12 searches per holding; an earnings day or a big move
deserves more. Spend effort where something actually happened.

## 0. Get oriented (2 minutes)

- Read `CLAUDE.md`, `config/portfolio.toml`, `config/rules.toml`, `config/sources.toml`.
- `DATE` = today in Europe/Madrid (`python3 -c "import sys; sys.path.insert(0,'scripts'); import pilib; print(pilib.run_date())"`).
- News window: Monday = `run.monday_window_hours` (covers the weekend), otherwise `run.news_window_hours`.
- Open the most recent report in `reports/daily/` so today's report can say what changed
  since yesterday instead of repeating it.

## 1. Holdings from the Google Sheet

Read only: never write to, format, comment on or share the sheet. Read the sheet with the **Google Drive connector** (`sheet.file_id`, tab `sheet.tab`). Rows start
at `sheet.first_data_row`. Map columns with `[sheet.columns]` and write
`data/holdings/raw-<DATE>.json`:

```json
{"source": "google-sheet", "read_at": "<ISO timestamp>",
 "rows": [{"open_date": "2026-10-05", "ticker": "CRWD", "side": "Long", "order_type": "Market",
           "shares": 0.074, "name": "Crowdstrike Holdings Inc", "entry_price_estimate": 270.04,
           "fill_price": null, "limit_or_stop_price": null, "stop_loss_alert": null,
           "target_price": null, "fees": 0, "fee_override": null, "exit_date": null,
           "exit_price": null, "notes": ""}]}
```

Rules: include every row that has a ticker (open and closed); numbers as numbers; `#N/A`,
`-` and blanks become `null`; dates as `YYYY-MM-DD`. Do not "fix" the owner's data.
If the connector fails or the file is not visible: skip this step and use `--fallback` below.

## 2. Run the data pipeline

```bash
pip install -q -r requirements.txt 2>/dev/null || true
python3 scripts/run_daily_data.py --rows data/holdings/raw-<DATE>.json   # or: --fallback
```

It writes holdings, prices, metrics, move attribution, portfolio risk, rule checks, SEC filings
and (weekly or after a 10-Q/10-K) fundamentals. Read `data/snapshots/<DATE>-pipeline.json`:
every failed step becomes a line in "Data quality and sources". If every price download fails
with 403, the cloud environment's network allowlist is missing the data domains (see README).

## 3. Know what Santi already knows

```bash
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py due
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py status guidance EPS beta ...
```

New terms get a full explanation; "learning" terms a one-line reminder; "known" terms none.

## 4. Research each holding (in parallel)

Spawn one **holding-researcher** subagent per open position (`.claude/agents/holding-researcher.md`).
Give each: ticker, company name, news window, `theses/<TICKER>.md`, its slice of
`data/metrics/<DATE>.json`, `attribution-<DATE>.json`, `rules-<DATE>.json`,
`data/filings/<DATE>.json`, the thesis breakers from `config/rules.toml`, and yesterday's report
section. Each returns `data/research/<DATE>/<TICKER>.json` (schema in the agent file): events
with sources and tiers, why-chains, product facts with sales numbers or "not disclosed",
earnings facts, analyst actions, insider notes, upcoming catalysts and thesis-breaker checks.

## 5. Turn evidence into conclusions, per holding

Read these skills and apply them to each researcher output:
- `why-analysis`: split the move into market, industry and company parts, then climb the Why
  Ladder to a basic driver. No published reason = say so.
- `earnings-analysis`: if results came out in the window or are due within 14 days.
- `product-explainer`: for any product, technology or contract in the news.
- `filings-decoder`: what each new filing means in plain English.
- `news-and-events`: rank items by materiality; drop the noise.
- `position-review`: thesis status (Intact / Watch / Challenged / Broken), the three strongest
  reasons to stay and to retreat, HIS rules from `rules-<DATE>.json`, and any THESIS ALERT.

Every conclusion needs evidence `[Source, YYYY-MM-DD](url)` or a label: "inference, medium confidence".

## 6. The portfolio as a whole

Use `portfolio-risk` with `data/metrics/portfolio-<DATE>.json`: weights, theme concentration,
how much the holdings move together, a typical bad day in dollars, and the market and industry
shock scenarios. Write the **Against your goals** line from `goals_check` (his goals in
`config/portfolio.toml [goals]`: diversify beyond tech, keep it reasonably safe, still some high
movers): facts only, no suggestions. Add a 14-day calendar of earnings dates and events across
all holdings.

## 7. Teach

- Pick the **Lesson of the day** from today's news and `learning/curriculum.md` (next unchecked
  topic that today's events make concrete). 120-250 words, using his holdings, one worked
  example, one "check yourself" question. Save to `learning/lessons/<DATE>.md`.
- List **New words today**: every watchlist term used that is "new" for him, one plain line each.

## 8. Write the report

Fill `.claude/skills/portfolio-daily-report/templates/report.md` and save it to
`reports/daily/<YYYY>/<MM>/<DATE>.md`. Conclusion first, everywhere. Plain English
(`explain-like-a-teacher`). Say what changed since yesterday.

## 9. Quality gates (in this order)

1. **challenger** agent: attacks every bottom line and thesis status; revise when it wins.
2. **fact-checker** agent: every number and citation traced to `data/` files or the source page.
3. **plain-english-editor** agent: every term defined, every "what" has a "why", no jargon stacks.
4. Lint until PASS:
   `python3 .claude/skills/portfolio-daily-report/scripts/lint_report.py reports/daily/<YYYY>/<MM>/<DATE>.md`

## 10. Update the learning ledger

For each term explained today:
`python3 .claude/skills/learning-tracker/scripts/concept_ledger.py taught "<term>" --one-liner "<plain definition>"`
Tick topics covered in `learning/curriculum.md`.

## 11. Write the email file, then commit and push

Fill `templates/email.md` into `reports/daily/<YYYY>/<MM>/<DATE>-email.md` (it is saved with the
report; do not lint it, the linter is for the full report only). Then:

```bash
git add reports data learning
git commit -m "Daily report <DATE>"
git push origin HEAD:main
```

Push before emailing, so the email's "read the full report" link already works.

## 12. Send the email

Render the email file from step 11 with
`python3 .claude/skills/portfolio-daily-report/scripts/render_email.py <that file> > /tmp/email.html`,
and send it with the **Gmail connector** to `owner.email_to` only. Subject:
`Portfolio report <DATE>: <bottom line in under 10 words>`. If sending fails, say so in the
session summary; the report is still in the repo.

## If things go wrong

- Never skip the report because one step failed. A partial, honest report beats none.
- Never fill a gap with a guess or with figures from memory.
- A green run status only means the session ended without an infrastructure error; the summary
  at the end of the session must list what actually failed.
