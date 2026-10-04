# Routine setup on your personal Claude account

Everything in this repository is ready. What is left belongs to a Claude account, not to the
repository: the routines, the connectors, the cloud environment, and whose plan pays for each run.
Do these steps **signed in to your personal Claude account** at claude.ai. About 10 minutes.

You need a paid plan (Pro or Max) on that account: routines need Claude Code on the web.

## 1. Let the cloud open the repository (GitHub account sdog121903)

1. Open **claude.ai/code**. If it asks you to connect GitHub, sign in to GitHub as **sdog121903**.
2. When GitHub asks where to install the Claude app, choose **sdog121903**, then **Only select
   repositories** -> `portfolio-intel` (or all repositories, your choice), then **Install**.

Terminal alternative: run `claude`, type `/login` and choose the personal account, then type
`/web-setup`. The GitHub CLI on your Mac is already logged in as sdog121903, so it copies that login.

## 2. Connect Google Drive and Gmail

1. Open **claude.ai/customize/connectors**.
2. Connect **Google Drive** and **Gmail** with **sgomezo2003@gmail.com**. That account owns the
   FIDELITY sheet, and the report email is sent from the connected Gmail account to the same address.

## 3. Create the cloud environment

1. In claude.ai/code, open the environment menu and choose **Add environment**.
2. Name: `portfolio-intel`.
3. **Network access: Custom.** Tick **Also include default list of common package managers**.
   Allowed domains, one per line:

```
query1.finance.yahoo.com
query2.finance.yahoo.com
api.nasdaq.com
www.sec.gov
data.sec.gov
www.reuters.com
www.cnbc.com
apnews.com
www.businesswire.com
www.prnewswire.com
www.globenewswire.com
www.nasdaq.com
finance.yahoo.com
ir.crowdstrike.com
www.crowdstrike.com
investors.credosemi.com
credosemi.com
investor.lumentum.com
www.lumentum.com
www.strlco.com
investors.modernatx.com
www.modernatx.com
investor.tsmc.com
pr.tsmc.com
www.tsmc.com
ir.amd.com
www.amd.com
investors.paloaltonetworks.com
www.paloaltonetworks.com
investor.bloomenergy.com
www.bloomenergy.com
investors.snowflake.com
www.snowflake.com
investor.agilent.com
www.agilent.com
```

   Custom keeps the run from talking to unknown sites. If a run's log shows many blocked pages,
   add those domains or switch to Full.
4. Environment variables: none. Setup script: leave empty. Save.

## 4. Create the daily routine

Open **claude.ai/code/routines** -> **New routine**:

| Field | Value |
|---|---|
| Name | Daily portfolio report |
| Instructions | Everything in `routines/daily-routine-prompt.md` from "You are running..." to the end |
| Model | Opus 5.5 |
| Repository | sdog121903/portfolio-intel |
| Environment | portfolio-intel |
| Trigger | Schedule, daily, **07:07**, time zone **Europe/Madrid** |
| Connectors | **Only** Google Drive and Gmail. Remove every other one: a routine can use every tool of every connector it has, without asking |

Click **Create**.

## 5. Create the weekly deep dive

Same as step 4, except: Name `Weekly deep dive`; Instructions = everything in
`routines/weekly-routine-prompt.md` after its first line; Trigger weekly, **Sunday 10:07**, Europe/Madrid.

## 6. First test

1. Open the daily routine and click **Run now**.
2. When it finishes, read the summary at the end of the run (a green status only means the session
   ran, not that every step worked). Then check:
   - `reports/daily/2026/10/<date>.md` exists on GitHub (main branch).
   - No "FALLBACK" warning at the top of the report (that would mean the sheet was not read).
   - The email reached sgomezo2003@gmail.com.
   - No blocked downloads (403 or "host_not_allowed") in the run log; if there are, fix step 3.

## 7. Switch off the old version (only after a clean test run)

The old Cowork task "Daily portfolio report" (07:50 daily) lives on your **other** Claude account
(santiago@hobetu.ai). Pause it there: Claude Desktop -> Cowork -> Scheduled -> turn it off, or ask
Claude in a session signed in to that account. If you installed the Apps Script email in the
sheet, run its `deleteDailyTrigger` function too.

## If you use Claude Code instead of the browser

In Terminal: `cd ~/portfolio/portfolio-intel && claude`, `/login` with the personal account, then
`/web-setup`, then ask: "Read setup/ROUTINE_SETUP.md and create both routines with /schedule,
attaching only the Google Drive and Gmail connectors". Schedules in that form:
`CRON_TZ=Europe/Madrid 7 7 * * *` (daily) and `CRON_TZ=Europe/Madrid 7 10 * * 0` (Sundays).
The environment (step 3) is still created in the browser.
