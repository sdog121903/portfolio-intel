# STRL news log: what happened, what is coming, and how the stock reacted

Every report that covers STRL adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/STRL.md`](../STRL.md).

This page is rebuilt on every run from `data/news-log/STRL.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **8** news items and **4** report days logged (first report 2026-10-04, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **bad** news: -2.96% (4 items).
- Biggest reactions so far: 2026-08-04 -13.23% beyond the market (very big) after: Q2 revenue $1.168bn (+90%), backlog $4.33bn (+116%), 2026 outlook raised to $4.00-4.15bn;...; 2026-10-06 +7.16% beyond the market (very big) after: Jumped 7.71% with no company news: AI data-center builders rallied (MYR Group +7.5%,...; 2026-10-07 -5.00% beyond the market (big) after: Fell 5.24% with no company news: infrastructure stocks fell 2.49% on a day the 10-year US....
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-27 | Fed rate decision (10-27/28) | yes | [Federal Reserve, 2026-10-07](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm), tier 1 |
| 2026-11-02 | Q3 2026 results (estimated, after close) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-08 | Fell 2.94% with data-center builders (eight-peer average −1.60%) after the OpenAI revenue report; −1.04% on 10-09 with no published cause. | bad | low | 2026-10-08 | -2.94% | -0.42% | -2.52% | normal | n/a | [Motley Fool, 2026-10-08](https://fool.com/coverage/stock-market-today/2026/10/08/stock-market-midday-oct-8-stocks-edge-lower-on-growing-ai-caution/), tier 3 |
| 2026-10-08 | Stifel cut its target to $742 from $804 and kept Buy; no reason published. | bad | low | 2026-10-08 | -2.94% | -0.42% | -2.52% | normal | n/a | [GuruFocus, 2026-10-08](https://www.gurufocus.com/news/9115929/strl-maintained-by-stifel-price-target-lowered-to-742), tier 3 |
| 2026-10-07 | Fell 5.24% with no company news: infrastructure stocks fell 2.49% on a day the 10-year US bond rate touched its highest since 2002 in the morning (it closed almost unchanged); Sterling moves about 3.3 times the market. | bad | medium | 2026-10-07 | -5.24% | -0.24% | -5.00% | big | n/a | [CNBC, 2026-10-07](https://www.cnbc.com/amp/2026/10/07/treasury-yields-auction-fomc-minutes.html), tier 2 |
| 2026-10-06 | Jumped 7.71% with no company news: AI data-center builders rallied (MYR Group +7.5%, Comfort Systems +4.7%) on a record day for the S&P 500 and cooler bond yields; most of Sterling's 'own' 5 points was probably that group (inference, medium). | neutral | medium | 2026-10-06 | +7.71% | +0.55% | +7.16% | very big | n/a | [StockStory via Yahoo Finance, 2026-10-06](https://finance.yahoo.com/markets/stocks/articles/rocket-lab-myr-group-ameresco-205634892.html), tier 3 |
| 2026-10-05 | Appointed Katherine Hargis as Senior Vice President, General Counsel, Chief Compliance Officer and Corporate Secretary. | neutral | low | 2026-10-05 | -1.89% | +0.67% | -2.57% | normal | n/a | [SEC 8-K, 2026-10-05](https://www.sec.gov/Archives/edgar/data/874238/000087423826000110/strl-20261005.htm), tier 1 |
| 2026-10-02 | Jumped 5.6% with no company news: the whole market and construction stocks rose after a weak jobs report made an interest-rate rise less likely, and STRL usually moves about three times as much as the market. | neutral | low | 2026-10-02 | +5.60% | +0.74% | +4.86% | big | -3.83% | [Motley Fool, 2026-10-02](https://www.fool.com/coverage/stock-market-today/2026/10/02/stock-market-midday-oct-2-stocks-rally-as-weak-jobs-data-cools-fed-rate-hike-bets/), tier 3 |
| 2026-08-03 | Q2 revenue $1.168bn (+90%), backlog $4.33bn (+116%), 2026 outlook raised to $4.00-4.15bn; yet the stock fell 13% after hours, possibly because the extra revenue comes at lower margins (inference, medium confidence). | mixed | high | 2026-08-04 | -11.42% | +1.80% | -13.23% | very big | -1.64% | [Sterling Q2 2026 results, 2026-08-03](https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/), tier 1 |
| 2026-05-12 | Filed a shelf registration (S-3) that lets it sell new shares quickly whenever it chooses; none sold so far, but the stock fell 8.3% that week. | bad | medium | 2026-05-12 | -1.94% | -0.15% | -1.79% | normal | -14.45% | [QuiverQuant, 2026-05-18](https://www.quiverquant.com/news/Sterling+Infrastructure+falls+8.3%25+as+investors+react+to+shelf+filing+and+post-rally+profit-taking), tier 3 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $513.00 | -1.04% | +1.82% | -0.52% | -2.34% | normal | no news found |
| 2026-10-07 | 2026-10-07 | $534.13 | -5.24% | -0.73% | -5.24% | +0.72% | normal | Fell 5.24% with no company news: infrastructure stocks fell 2.49% on a day the 10-year US bond rate touched its highest since 2002 in the morning (it closed almost unchanged); Sterling moves about 3.3 times the market. |
| 2026-10-05 | 2026-10-05 | $523.33 | -1.89% | +2.04% | -0.57% | -3.36% | normal | Appointed Katherine Hargis as Senior Vice President, General Counsel, Chief Compliance Officer and Corporate Secretary. |
| 2026-10-04 | 2026-10-02 | $533.42 | +5.60% | +2.25% | +1.96% | +1.39% | normal | Jumped 5.6% with no company news: the whole market and construction stocks rose after a weak jobs report made an interest-rate rise less likely, and STRL usually moves about three times as much as the market. |

Informational research and education, not investment advice.
