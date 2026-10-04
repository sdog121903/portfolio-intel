# portfolio-intel

A daily, sourced, beginner-friendly report on every stock in Santi's FIDELITY trade tracker,
produced by a Claude Code **routine** that runs entirely in the cloud. Each morning it reads the
Google Sheet, downloads prices and SEC filings, researches every holding, explains what happened
and **why** in plain English, checks his own Stay/Retreat rules, and saves the report (Markdown and PDF)
in this repository so the history and his learning build up over time.

> Informational research and education, not investment advice. The report never tells you to
> buy or sell: it explains the evidence and tells you which of **your** rules fired.

## What is in the box

| Folder | Purpose |
|---|---|
| `CLAUDE.md` | The operating manual every run reads first. Bottom line: teach a beginner |
| `routines/` | The prompts to paste into the routines, and step-by-step runbooks |
| `.claude/skills/` | 13 skills: teaching, why-analysis, sources, filings, market metrics, earnings, products, news, position review, portfolio risk, learning tracker, the report itself, and the vendored stock-analysis deep-dive skill |
| `.claude/agents/` | Researcher (one per stock, in parallel), challenger, fact-checker, plain-English editor |
| `config/` | Your sheet, rules, source tiers, benchmarks and themes |
| `theses/` | Why you own each stock (write yours!) and what would prove it wrong |
| `learning/` | Your textbook: daily lessons, the terms you know, the curriculum |
| `reports/` | Every report ever written |
| `scripts/`, `tests/` | The tested number-crunching (standard-library Python) |

## Set it up

### Fastest: let Claude Code do it for you
1. Download `portfolio-intel.zip` and `SETUP_PROMPT.md` to your Downloads folder.
2. Open Terminal and run `cd ~/Downloads && claude` (or open the Claude Desktop app's Code tab in
   Local mode on the Downloads folder).
3. Type: *"Read SETUP_PROMPT.md in this folder and follow it from start to finish."*

Claude Code unpacks and tests everything, audits it against `docs/requirements.md`, creates the
private GitHub repository for you (you only approve a GitHub login), and tells you exactly what to
click for the few steps only you can do: connecting Google Drive and Gmail, the cloud
environment's network settings, and the routine. It then runs the first report and helps you
switch off the old Cowork task so you don't get two emails. The same prompt also works inside a
cloud session at claude.ai/code, but cloud sessions need an existing repository, so in that case
create an empty private repo first and upload the zip to it.

### By hand (all in the browser, about 30 minutes)

You need a paid Claude plan with Claude Code on the web (routines run on Pro, Max, Team and
Enterprise and use your normal plan usage), and a GitHub account.

### 1. Put this folder on GitHub
1. On github.com click **New repository**, name it `portfolio-intel`, choose **Private**, create it.
2. On the empty repo page click **uploading an existing file**, drag in `portfolio-intel.zip`,
   and commit.
3. Open **claude.ai/code**, connect GitHub when asked, start a session on `portfolio-intel` and
   type: *"Unzip portfolio-intel.zip, move everything inside its portfolio-intel folder
   (including the hidden .claude folder) to the repository root, delete the zip and the empty
   folder, run `python3 -m unittest discover -s tests`, and commit and push to main."*
   (Alternative: unzip on your computer and drag the folder's contents in; on a Mac press
   Cmd+Shift+. first so the hidden `.claude` folder is included.)
4. In `config/portfolio.toml` set `repo.url` to your repository's address (pencil icon on GitHub).

### 2. Connect Google Drive and Gmail
At **claude.ai/customize/connectors** connect **Google Drive** and **Gmail**. The Google account
you connect must be able to open the FIDELITY sheet (checked on 2026-10-04: it can). If it ever
cannot, either share the sheet with that account (Viewer is enough) or reconnect using
sgomezo2003@gmail.com. The email is sent from whichever Gmail account is connected.

### 3. Create the cloud environment
In claude.ai/code open the environment menu and add a cloud environment named `portfolio-intel`:
- **Network access:** Custom, tick "Also include default list of common package managers", and
  allow `query1.finance.yahoo.com`, `query2.finance.yahoo.com`, `api.nasdaq.com`, `www.sec.gov`,
  `data.sec.gov` (plus `www.alphavantage.co` if you add a key), and the news and investor-relations
  sites listed in `setup/SETUP_PROMPT.md` Phase 8. Choose **Full** instead if you want
  the researchers to open any news site.
- **Environment variables:** none required. Optional: an Alpha Vantage key as an API credential
  named `ALPHAVANTAGE_API_KEY` (a free backup price source).

### 4. Create the daily routine
At **claude.ai/code/routines** click **New routine**:
- **Name:** Daily portfolio report
- **Instructions:** paste `routines/daily-routine-prompt.md`; pick the model you want (a stronger
  model writes better explanations and uses more of your plan)
- **Repository:** portfolio-intel  -  **Environment:** portfolio-intel
- **Trigger:** Schedule, Daily, **07:07** (a few minutes past the hour starts more reliably)
- **Connectors:** keep Google Drive and Gmail, remove the rest
Click **Create**, then **Run now** for a first test.

### 5. Optional: the weekly deep dive
Create a second routine with `routines/weekly-routine-prompt.md`, weekly on Sundays at 10:07.
Each week one holding gets a full analysis and its thesis file is rebuilt from primary documents.

### 6. Check the first run
Open the run's session: read the summary at the end (a green status only means the session ran,
not that every step worked). Then check `reports/daily/` on GitHub and your inbox.

### 7. Switch off the old versions
Once a run is clean, turn off the Cowork scheduled task "Daily portfolio report" (Claude Desktop,
Cowork, Scheduled), and if you installed the free Apps Script email in your sheet, run its
`deleteDailyTrigger` function. Otherwise you will get two or three emails a day.

### Costs
Routine runs use your normal Claude plan usage. The promotional cloud session credit (claim by
October 7, 2026; expires November 4, 2026) pays for ordinary cloud sessions but not for routines.

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
  your first cloud run, so read that run's summary.
- Routines are a research-preview feature; settings and limits may change. Docs:
  https://code.claude.com/docs/en/routines
