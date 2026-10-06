# SNOW news log: what happened, what is coming, and how the stock reacted

Every report that covers SNOW adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/SNOW.md`](../SNOW.md).

This page is rebuilt on every run from `data/news-log/SNOW.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **3** news items and **1** report days logged (first report 2026-10-04, latest 2026-10-04).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +15.51% (1 item).
- Average move beyond the market on the reaction day to **bad** news: +1.47% (1 item).
- Biggest reactions so far: 2026-09-03 +15.51% beyond the market (very big) after: Product revenue $1,491.9m (+37%), a third quarter in a row of faster growth; net revenue...; 2026-02-24 +1.47% beyond the market (normal) after: A securities class action (shareholders saying they were misled) was filed against the....
- Of those biggest moves, 1 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-04)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-13 | Court deadline: Snowflake's motion to dismiss the 2026 class action | yes | [Snowflake 10-Q, 2026-09-03](https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000037/snow-20260731.htm), tier 1 |
| 2026-12-02 | Q3 FY2027 results (guidance product revenue $1,588-1,593m) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 | Closed the sale of $3.75bn of 0% convertible notes (loans paying no interest that lenders can swap for shares, at about $500.38 and $483.98); a hedge limits dilution up to $820.30. If converted, about 2.2% more shares (up to about 4%). First announced 2026-09-28. | mixed | medium | n/a | n/a | n/a | n/a | n/a | n/a | [SEC 8-K, 2026-10-02](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000043/snow-20260928.htm), tier 1 |
| 2026-09-02 | Product revenue $1,491.9m (+37%), a third quarter in a row of faster growth; net revenue retention 126%; the stock jumped 22%. Contracted future revenue slipped from $9.21bn to $9.00bn, and the standard (GAAP) loss was $191.7m. | good | high | 2026-09-03 | +16.55% | +1.05% | +15.51% | very big | -7.71% | [Snowflake Q2 FY2027 results, 2026-09-02](https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000033/fy2027q2earnings.htm), tier 1 |
| 2026-02-24 | A securities class action (shareholders saying they were misled) was filed against the former CEO and former CFO; Snowflake's motion to dismiss is due 2026-10-13 (10-Q). | bad | medium | 2026-02-24 | +2.20% | +0.73% | +1.47% | normal | +2.94% | [Snowflake 10-Q, 2026-09-03](https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000037/snow-20260731.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-04 | 2026-10-02 | $341.04 | -0.28% | +0.76% | -0.78% | -0.26% | normal | Closed the sale of $3.75bn of 0% convertible notes (loans paying no interest that lenders can swap for shares, at about $500.38 and $483.98); a hedge limits dilution up to $820.30. If converted, about 2.2% more shares (up to about 4%). First announced 2026-09-28. |

Informational research and education, not investment advice.
