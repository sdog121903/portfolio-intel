---
name: news-and-events
description: Classifies news and events for the holdings by materiality, filters noise, de-duplicates stories, and builds the upcoming-catalyst calendar. Use while researching the daily news window, when deciding what deserves space in the report, and when listing what is coming up in the next 14-30 days.
---

# News and events

Most headlines about a stock are noise. The report earns trust by covering the few items that
change what a company will earn, or what investors believe it will earn, and by saying
"nothing material happened" on quiet days.

## For every candidate item, record
- **What**: one sentence, with the date and time (before or after market hours).
- **Type and materiality**: from `references/event-taxonomy.md` (high / medium / low).
- **New or rehash?** Many articles repeat old news; only new information counts.
- **Direction for the thesis**: supports, weakens, or neutral; and why in one sentence.
- **Source tier** and link; a second source for anything high-materiality.
- **Market reaction**: did the company-specific part of the move line up with it?

## Rules
- De-duplicate: one event, many articles -> cite the best primary source plus one tier-2 report.
- Price-movement articles ("stock jumps 5%") are not causes; find what they are reacting to.
- Lists ("3 stocks to buy now"), predictions and promotional pieces are noise.
- An analyst note is an opinion; it matters when it contains new facts (channel checks, a model change).
- Peer news counts when it is about shared customers, suppliers or demand (a big cloud company's
  capex plan matters to all the AI hardware holdings).

## Catalyst calendar
List dated upcoming events across all holdings: earnings (confirmed or estimated), investor days,
product launches, major industry conferences, lock-up expiries, index changes, regulatory
decisions. Confirm dates on company investor-relations pages.

## The news log (one running record per stock)
Every run adds its fact-checked items to each stock's log, so over months Santi can see how the
stock tends to react to each kind of news (results, downgrades, share sales, contracts, policy).

- **Input**: after the quality gates, write `data/research/<DATE>/news-log.json`
  (`{"date", "fact_checked": true, "tickers": {"<TICKER>": [items]}}`). Each item:
  `key` (stable id, e.g. `lite-2026-08-11-q4-results`; reuse it when the same event comes back),
  `date` (the event's own date, `YYYY-MM-DD`), `timing` (before open / during / after close /
  unknown), `type`, `materiality`, `direction` (good / bad / neutral / mixed for the stock),
  `what` (one plain-English sentence, with the numbers exactly as the final report states
  them) and `source` (`name`, `date`, `url`, `tier`). Only items that made it into the report.
  Add `"upcoming": {"<TICKER>": [{date, event, confirmed, source}]}` with the 14-day-plus calendar for
  each stock: the log page shows it under "Coming up". Past news and upcoming events live **only**
  in the news log, never as tables in the thesis files.
- **Run**: `python3 .claude/skills/news-and-events/scripts/news_log.py update --date <DATE>`.
  It merges the items into `data/news-log/<TICKER>.json` (the record; nothing is deleted, repeat
  items are not added twice), calculates each item's price reaction from `data/prices/`
  (stock vs S&P 500 on the first trading day the news could affect, its size against a normal
  day, and the next five days), adds one row per report day from the move attribution, and
  rebuilds `theses/news/<TICKER>.md`, newest first.
- If `news-log.json` is missing, the script falls back to the researcher files and marks every
  item "not fact-checked". Fix that on the next run by writing the curated file with the same keys.
- The "What the log shows so far" section is arithmetic, not a forecast. Under 20 items it says
  so; never turn a pattern into a buy or sell call.
