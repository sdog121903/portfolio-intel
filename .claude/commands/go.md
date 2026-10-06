---
description: Generate today's portfolio report (Markdown + PDF) on this computer; on Sundays also the weekly deep dive
---

Run Santi's portfolio report **locally, on this computer**. Do not stop to ask questions; if a
step fails, use the documented fallback, keep going, and say what failed in the report's
"Data quality and sources" section.

1. Set up Python once: `bash scripts/bootstrap.sh`. From then on use `.venv/bin/python` wherever
   a runbook says `python3`.
2. Read `CLAUDE.md`, then follow `routines/daily-report.md` step by step. The report date is
   today in Europe/Madrid.
3. Read the trade log with the Google Drive connector (read only, never change the sheet): file id
   `1q0DLvB7WieV30mpA8a9rNgg6-GoqmXaWyr0Kyvrkf8M`, tab "Trades". If it cannot be read, run the
   pipeline with `--fallback` and put a warning at the top of the report.
4. If today is Sunday in Europe/Madrid, or no file in `reports/deep-dives/` is newer than 7 days,
   also follow `routines/weekly-deep-dive.md`.
5. When the report passes the linter and the PDF is made, commit and push the run's outputs
   (runbook step 14: reports, PDFs, data, news logs, lessons, learning and thesis updates). **Never
   send email**, and never commit secrets.
6. Finish with a short summary: what worked, what failed, the paths of the new report(s) and
   PDF(s) (`reports/pdf/`), and the commit that was pushed.
