# How to run it

Everything runs on your own computer with your own Claude account. Type **`/go`** and the reports
appear in `reports/` (Markdown) and `reports/pdf/` (PDF). Nothing is uploaded, emailed or committed.

## One-time setup

1. Install Claude Code and sign in with **your** Claude account (`claude`, then `/login`).
2. Get this folder: `git clone https://github.com/sdog121903/portfolio-intel.git`
3. Connect **Google Drive** at **claude.ai/customize/connectors**, using the Google account that
   can open your trade sheet. (Without it, `/go` uses `config/holdings_fallback.csv` and says so.)
4. Make it yours: in `config/portfolio.toml` set `[owner]` (name and email, which the SEC requires
   as contact details for its free data) and `[sheet]` (your sheet's file id and tab); list each of
   your tickers in `[sector_etf]`, `[sectors]`, `[themes]` and `[sector_playbooks]`; copy
   `theses/TEMPLATE.md` for each stock.
5. Needs Python 3.9 or newer (`python3 --version`). `/go` creates its own `.venv` the first time.

## Every day

```bash
cd portfolio-intel
claude
```

Then type `/go`. Today's report and its PDF are written in this folder; on Sundays a deep dive on
one holding as well. It takes a while (it researches every holding): you can leave it running.

Usage is your Claude plan's normal usage on this computer.
