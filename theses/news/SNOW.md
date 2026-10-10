# SNOW news log: what happened, what is coming, and how the stock reacted

Every report that covers SNOW adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/SNOW.md`](../SNOW.md).

This page is rebuilt on every run from `data/news-log/SNOW.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **9** news items and **3** report days logged (first report 2026-10-04, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +8.64% (3 items).
- Average move beyond the market on the reaction day to **bad** news: +0.01% (2 items).
- Biggest reactions so far: 2026-09-03 +15.51% beyond the market (very big) after: Product revenue $1,491.9m (+37%), a third quarter in a row of faster growth; net revenue...; 2026-10-09 +6.82% beyond the market (very big) after: Snowflake said no flaw in its service was involved and no customer action is needed...; 2026-10-08 +3.59% beyond the market (big) after: ASOS said the breach began when an employee was tricked into giving up a login used on....
- Of those biggest moves, 1 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-13 | Court deadline (motion to dismiss) and end of $550m convertible option (approximate) | not confirmed | not recorded |
| 2026-11-03 | EXPEDITION event (to 11-05) | yes | not recorded |
| 2026-12-02 | Q3 FY2027 results (estimated) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | Snowflake said no flaw in its service was involved and no customer action is needed (media statement); whether the stolen login reached ASOS's Snowflake account is unknown. Stock +7.42% with the software rally. | good | medium | 2026-10-09 | +7.42% | +0.60% | +6.82% | very big | n/a | [The Independent via Yahoo Finance UK, 2026-10-09](https://uk.finance.yahoo.com/news/asos-cyber-breach-not-caused-102151192.html), tier 3 |
| 2026-10-08 | ASOS said the breach began when an employee was tricked into giving up a login used on 'third-party platforms'; Snowflake +3.17% that day (company part +3.32). | good | medium | 2026-10-08 | +3.17% | -0.42% | +3.59% | big | n/a | [Irish Examiner (PA), 2026-10-08](https://www.irishexaminer.com/news/arid-41921518.html), tier 2 |
| 2026-10-07 | Co-founder Dageville's trust sold 50,000 shares at $333.42 (about $16.67m) under a 10b5-1 plan. | neutral | low | 2026-10-07 | -0.92% | -0.24% | -0.68% | normal | n/a | [SEC Form 4, 2026-10-08](https://www.sec.gov/Archives/edgar/data/1640147/000182173726000016/xslF345X06/wk-form4_1791497594.xml), tier 1 |
| 2026-10-07 | Co-founder Benoit Dageville filed to sell 50,000 shares (about $16.7m) under a 10b5-1 plan, continuing fortnightly sales since July. | neutral | low | 2026-10-07 | -0.92% | -0.24% | -0.68% | normal | n/a | [SEC Form 144, 2026-10-07](https://www.sec.gov/Archives/edgar/data/1640147/000195917326007302/xsl144X01/primary_doc.xml), tier 1 |
| 2026-10-06 | Hackers claimed to have 'fully compromised the Snowflake instance' of UK retailer ASOS; Snowflake said it found no compromise of its platform and ASOS blamed third-party messaging platforms; the stock lagged software by 2.52 points that day. | bad | medium | 2026-10-06 | -0.90% | +0.55% | -1.45% | normal | n/a | [Reuters via The Globe and Mail, 2026-10-06](https://www.theglobeandmail.com/business/international-business/article-british-retailer-asos-hack-customer-data-breached/), tier 2 |
| 2026-10-05 | Announced EXPEDITION 2026, an online event on 11-03 to 11-05 with Microsoft CEO Satya Nadella. | neutral | low | 2026-10-05 | -0.60% | +0.67% | -1.28% | normal | n/a | [Snowflake, 2026-10-05](https://www.snowflake.com/en/news/press-releases/snowflake-agentic-transformation-expedition-2026-speaker-satya-nadella/), tier 1 |
| 2026-10-02 | Closed the sale of $3.75bn of 0% convertible notes (loans paying no interest that lenders can swap for shares, at about $500.38 and $483.98); a hedge limits dilution up to $820.30. If converted, about 2.2% more shares (up to about 4%). First announced 2026-09-28. | mixed | medium | 2026-10-05 | -0.60% | +0.67% | -1.28% | normal | n/a | [SEC 8-K, 2026-10-02](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000043/snow-20260928.htm), tier 1 |
| 2026-09-02 | Product revenue $1,491.9m (+37%), a third quarter in a row of faster growth; net revenue retention 126%; the stock jumped 22%. Contracted future revenue slipped from $9.21bn to $9.00bn, and the standard (GAAP) loss was $191.7m. | good | high | 2026-09-03 | +16.55% | +1.05% | +15.51% | very big | -7.71% | [Snowflake Q2 FY2027 results, 2026-09-02](https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000033/fy2027q2earnings.htm), tier 1 |
| 2026-02-24 | A securities class action (shareholders saying they were misled) was filed against the former CEO and former CFO; Snowflake's motion to dismiss is due 2026-10-13 (10-Q). | bad | medium | 2026-02-24 | +2.20% | +0.73% | +1.47% | normal | +2.94% | [Snowflake 10-Q, 2026-09-03](https://www.sec.gov/Archives/edgar/data/0001640147/000164014726000037/snow-20260731.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $368.89 | +7.42% | +0.59% | +3.09% | +3.74% | big | Snowflake said no flaw in its service was involved and no customer action is needed (media statement); whether the stolen login reached ASOS's Snowflake account is unknown. Stock +7.42% with the software rally. |
| 2026-10-07 | 2026-10-07 | $332.85 | -0.92% | -0.24% | -1.32% | +0.64% | normal | Co-founder Benoit Dageville filed to sell 50,000 shares (about $16.7m) under a 10b5-1 plan, continuing fortnightly sales since July. |
| 2026-10-04 | 2026-10-02 | $341.04 | -0.28% | +0.76% | -0.78% | -0.26% | normal | Closed the sale of $3.75bn of 0% convertible notes (loans paying no interest that lenders can swap for shares, at about $500.38 and $483.98); a hedge limits dilution up to $820.30. If converted, about 2.2% more shares (up to about 4%). First announced 2026-09-28. |

Informational research and education, not investment advice.
