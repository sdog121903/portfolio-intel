# QQQM news log: what happened, what is coming, and how the stock reacted

Every report that covers QQQM adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/QQQM.md`](../QQQM.md).

This page is rebuilt on every run from `data/news-log/QQQM.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **3** news items and **2** report days logged (first report 2026-10-07, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **bad** news: -0.89% (1 item).
- Biggest reactions so far: 2026-10-08 -0.89% beyond the market (big) after: −1.31% (10-08) and +0.50% (10-09), tracking the Nasdaq-100; it fell three times as much...; 2026-10-09 -0.10% beyond the market (normal) after: Moderna replaced Warner Bros. Discovery in the Nasdaq-100, so QQQM now holds a slice of...; 2026-10-07 -0.02% beyond the market (normal) after: Santi bought 0.100 shares at Tuesday's close ($312.76); the Nasdaq-100 index it copies....
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-14 | ASML (a member) Q3 results | yes | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | Moderna replaced Warner Bros. Discovery in the Nasdaq-100, so QQQM now holds a slice of Moderna. | neutral | low | 2026-10-09 | +0.50% | +0.60% | -0.10% | normal | n/a | [Reuters via Zawya, 2026-10-01](https://www.zawya.com/en/capital-markets/moderna-to-replace-warner-bros-discovery-on-nasdaq-100-1486543), tier 2 |
| 2026-10-08 | −1.31% (10-08) and +0.50% (10-09), tracking the Nasdaq-100; it fell three times as much as the S&P 500 on Thursday because the index is chip-heavy. | bad | low | 2026-10-08 | -1.31% | -0.42% | -0.89% | big | n/a | [Yahoo Finance, 2026-10-08](https://finance.yahoo.com/markets/live/stock-market-today-thursday-october-8-dow-sp-500-nasdaq-080537884.html), tier 3 |
| 2026-10-06 | Santi bought 0.100 shares at Tuesday's close ($312.76); the Nasdaq-100 index it copies adds Moderna on 10-09. | neutral | low | 2026-10-07 | -0.26% | -0.24% | -0.02% | normal | n/a | [Nasdaq, 2026-10-01](https://ir.nasdaq.com/news-releases/news-release-details/moderna-inc-join-nasdaq-100-indexr-beginning-october-9-2026), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $309.39 | +0.50% | +0.60% | -0.10% | +0.01% | normal | Moderna replaced Warner Bros. Discovery in the Nasdaq-100, so QQQM now holds a slice of Moderna. |
| 2026-10-07 | 2026-10-07 | $311.94 | -0.26% | -0.24% | -0.01% | -0.01% | normal | Santi bought 0.100 shares at Tuesday's close ($312.76); the Nasdaq-100 index it copies adds Moderna on 10-09. |

Informational research and education, not investment advice.
