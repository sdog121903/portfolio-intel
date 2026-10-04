# Running the reports (tap to run, paid by cloud-session credits)

**Decision (2026-10-04):** no automatic routine. The promotional cloud-session credit does not cover
Routines (verified: support.claude.com/en/articles/17152539, "What doesn't the credit cover?
Projects and Routines"), and there is no supported way to start an ordinary cloud session on a
timer. So each run is an ordinary cloud session that you start with one word, which the credit
pays for until it runs out or expires (claim by **Oct 7, 11:59 PM PT**; expires **Nov 4, 11:59 PM
PT**). After that, cloud sessions count toward your normal plan usage.

| When (Madrid) | Type this | Result |
|---|---|---|
| Every day, 07:07 | `daily report` | `reports/daily/YYYY/MM/<DATE>.md` and `reports/pdf/<DATE>.pdf` |
| Sundays, 10:07 | `deep dive` | `reports/deep-dives/<TICKER>-<DATE>.md` and `reports/pdf/deep-dive-<TICKER>-<DATE>.pdf` |

## One-time setup (signed in to the Claude account that holds the credit)

1. **Claim the credit** before Oct 7, 11:59 PM PT: run `/claim-credit` in Claude Code, or use the
   banner in the Claude app; the balance shows in Settings, Usage. You can claim it without
   turning on usage credits (pay-as-you-go).
2. **GitHub:** open **claude.ai/code**, connect GitHub as **sdog121903**, and give the Claude app
   access to `portfolio-intel`. (Terminal alternative: `claude`, `/login`, `/web-setup`; the GitHub
   CLI on the Mac is already logged in as sdog121903.)
3. **Google Drive:** at **claude.ai/customize/connectors** connect Google Drive with
   **sgomezo2003@gmail.com** (owner of the FIDELITY sheet). No Gmail needed: email is off.
4. **Environment:** in claude.ai/code open the environment menu, **Add environment**, name
   `portfolio-intel`, **Network access: Custom**, tick **Also include default list of common package
   managers**, and paste these domains, one per line:

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

   No environment variables, no setup script.

## Each run (about 10 seconds of your time)

1. Open **claude.ai/code** (or the Claude app, Code).
2. Repository **sdog121903/portfolio-intel**, environment **portfolio-intel**, model **Opus 5.5**.
3. Type `daily report` (Sundays at 10:07: `deep dive`) and send. You can close the page; the
   session keeps running in the cloud and pushes the report and PDF to `main`.

## First run checks

- The session's final summary lists no failed steps.
- `reports/daily/2026/10/<date>.md` and `reports/pdf/<date>.pdf` are on GitHub (main branch).
- No "FALLBACK" warning at the top of the report (it would mean the sheet was not read; check the
  Google Drive connector).
- No blocked downloads (403 or "host_not_allowed") in the session; if there are, fix step 4.

## After the first clean run

Pause the old Cowork task "Daily portfolio report" (07:50 daily) on the account where it lives
(santiago@hobetu.ai): Claude Desktop, Cowork, Scheduled, turn it off. If you installed the Apps
Script email in the sheet, run its `deleteDailyTrigger` function too.

## If you later want it fully automatic

Create a routine with the same instructions (`routines/daily-routine-prompt.md`) at
claude.ai/code/routines: it runs with your laptop closed but is billed to normal plan usage, not
the credit. Schedules: `CRON_TZ=Europe/Madrid 7 7 * * *` and `CRON_TZ=Europe/Madrid 7 10 * * 0`.
