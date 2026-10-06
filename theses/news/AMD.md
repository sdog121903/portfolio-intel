# AMD news log: what happened, what is coming, and how the stock reacted

Every report that covers AMD adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/AMD.md`](../AMD.md).

This page is rebuilt on every run from `data/news-log/AMD.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **6** news items and **2** report days logged (first report 2026-10-04, latest 2026-10-05).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: -2.10% (3 items).
- Biggest reactions so far: 2026-08-05 -6.84% beyond the market (very big) after: Q2 revenue $11.5bn (+50%), data center $6.7bn (+107%); Q3 guided to about $13.0bn (+41%)....; 2026-09-28 -2.86% beyond the market (normal) after: Agreed to buy World Labs, Fei-Fei Li's AI lab, for about $8.2bn paid only in AMD shares...; 2026-09-10 -2.76% beyond the market (normal) after: CEO Lisa Su sold about $48.1m of shares under a pre-planned 10b5-1 plan..
- Of those biggest moves, 3 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-05)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-12 | Lisa Su keynote at the OCP Global Summit | yes | not recorded |
| about 2026-11-03 | Q3 2026 results (guidance about $13.0bn) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | Stifel raised its price target to $700 from $635 (Buy), expecting results above forecasts and a higher outlook. | good | low | 2026-10-05 | -0.34% | +0.67% | -1.02% | normal | n/a | [Investing.com, 2026-10-05](https://www.investing.com/news/analyst-ratings/stifel-raises-amd-stock-price-target-to-700-on-server-strength-93CH-4932133), tier 3 |
| 2026-10-02 | Rose 2.95% to a record close, almost all because the market and chip stocks rose. | neutral | low | 2026-10-02 | +2.95% | +0.74% | +2.21% | normal | n/a | [24/7 Wall St., 2026-10-02](https://247wallst.com/investing/2026/10/02/amd-climbs-3-as-chip-stocks-extend-their-run-arm-jumps-8-nvidia-rises-2/), tier 3 |
| 2026-09-28 | Agreed to buy World Labs, Fei-Fei Li's AI lab, for about $8.2bn paid only in AMD shares (about 0.8% more shares, researcher's calculation); the stock fell 3.6% that day. | mixed | medium | 2026-09-28 | -3.61% | -0.74% | -2.86% | normal | +3.93% | [SEC 8-K, 2026-09-28](https://www.sec.gov/Archives/edgar/data/2488/000000248826000182/amd-20260926.htm), tier 1 |
| 2026-09-10 | CEO Lisa Su sold about $48.1m of shares under a pre-planned 10b5-1 plan. | neutral | low | 2026-09-10 | -3.36% | -0.60% | -2.76% | normal | +8.24% | [SEC Form 4, 2026-09-10](https://www.sec.gov/Archives/edgar/data/2488/000000248826000178/), tier 1 |
| 2026-08-04 | Q2 revenue $11.5bn (+50%), data center $6.7bn (+107%); Q3 guided to about $13.0bn (+41%). The stock still fell 7% afterwards. | good | high | 2026-08-05 | -7.04% | -0.20% | -6.84% | very big | +0.18% | [AMD Q2 2026 results, 2026-08-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000121/q22026991.htm), tier 1 |
| 2026-07-22 | Anthropic agreed to deploy up to 2 gigawatts of AMD GPUs in AMD's Helios racks, first gigawatt from the first half of 2027; AMD committed to invest up to $5bn in Anthropic. (Anthropic makes Claude, which wrote this file.) | good | high | 2026-07-22 | +1.45% | -0.12% | +1.57% | normal | -22.23% | [CNBC, 2026-07-22](https://www.cnbc.com/2026/07/22/amd-anthropic-ai-chip-investment.html), tier 2 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | 2026-10-05 | $631.75 | -0.34% | +0.81% | -0.22% | -0.93% | normal | Stifel raised its price target to $700 from $635 (Buy), expecting results above forecasts and a higher outlook. |
| 2026-10-04 | 2026-10-02 | $633.91 | +2.95% | +0.89% | +1.94% | +0.12% | normal | Rose 2.95% to a record close, almost all because the market and chip stocks rose. |

Informational research and education, not investment advice.
