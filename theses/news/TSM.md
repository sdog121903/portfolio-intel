# TSM news log: what happened, what is coming, and how the stock reacted

Every report that covers TSM adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/TSM.md`](../TSM.md).

This page is rebuilt on every run from `data/news-log/TSM.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **7** news items and **4** report days logged (first report 2026-10-04, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: -1.30% (6 items).
- Biggest reactions so far: 2026-10-08 -2.59% beyond the market (big) after: September sales NT$511.86bn (−0.6% m/m, +54.6% y/y); Q3 NT$1,494.24bn, about US$46.70bn...; 2026-10-08 -2.59% beyond the market (big) after: GlobalFoundries signed a five-year US$2bn deal to make silicon interposers for TSMC's...; 2026-10-02 +2.22% beyond the market (big) after: Bloomberg reported TSMC is weighing a multi-factory campus near Dallas, each factory....
- Of those biggest moves, 1 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-12 | Taiwan market reopens after National Day | not confirmed | not recorded |
| 2026-10-15 | Q3 2026 results, 14:00 Taipei (08:00 Madrid) | yes | [TSMC, 2026-10-09](https://investor.tsmc.com/english/financial-calendar), tier 1 |
| 2026-11-10 | October 2026 revenue | yes | [TSMC, 2026-10-09](https://investor.tsmc.com/english/financial-calendar), tier 1 |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-08 | September sales NT$511.86bn (−0.6% m/m, +54.6% y/y); Q3 NT$1,494.24bn, about US$46.70bn at NT$32, about 2% above the top of guidance. US shares still fell 3.01% with chips. | good | high | 2026-10-08 | -3.01% | -0.42% | -2.59% | big | n/a | [TSMC 6-K, 2026-10-08](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000680/tsm-revenue20261008.htm), tier 1 |
| 2026-10-08 | GlobalFoundries signed a five-year US$2bn deal to make silicon interposers for TSMC's CoWoS packaging in New York, volume from 2028. | good | low | 2026-10-08 | -3.01% | -0.42% | -2.59% | big | n/a | [GlobalFoundries, 2026-10-08](https://gf.com/news-and-events/news/globalfoundries-reaches-agreement-to-establish-us-based-supply-of-silicon-interposers-for-advanced-ai-packaging/), tier 1 |
| 2026-10-07 | Citi said it expects TSMC to beat its own Q3 forecast and AI revenue to nearly double next year; the US shares fell 2.09% with chip stocks. | good | low | 2026-10-07 | -2.09% | -0.24% | -1.85% | normal | n/a | [Yahoo Finance, 2026-10-07](https://finance.yahoo.com/markets/stocks/article/tsmc-stock-just-hit-a-record--and-the-gains-may-be-only-starting-113728917.html), tier 3 |
| 2026-10-03 | Elon Musk confirmed early talks about TSMC helping his Texas Terafab chip-factory project ("Just discussions, but something may come of it"); no TSMC comment. TSM rose 2.75% on Monday (+2.08 points company-specific), possibly partly on this, while AI-chip leaders also rallied; no single cause confirmed (tier-3 reports). | good | medium | 2026-10-05 | +2.75% | +0.67% | +2.08% | big | n/a | [Motley Fool, 2026-10-05](https://www.fool.com/investing/2026/10/05/elon-musk-confirmed-terafab-talks-with-tsmc-intel-has-been-its-only-named-chip-partner/), tier 3 |
| 2026-10-01 | Bloomberg reported TSMC is weighing a multi-factory campus near Dallas, each factory costing at least $20bn; early stage, and TSMC said "no comment on market rumors". | mixed | medium | 2026-10-02 | +2.96% | +0.74% | +2.22% | big | -4.12% | [Bloomberg, 2026-10-01](https://www.bloomberg.com/news/articles/2026-10-01/tsmc-mulls-multibillion-dollar-texas-campus-for-more-ai-chips), tier 2 |
| 2026-09-10 | August sales were a record NT$514.81bn (New Taiwan dollars), up 53.3% from a year earlier, driven by AI chips. | good | medium | 2026-09-10 | -1.68% | -0.60% | -1.08% | normal | +0.79% | [TSMC, 2026-09-10](https://pr.tsmc.com/english/news/3340), tier 1 |
| 2026-07-16 | Q2 revenue US$40.20bn (+36%) with a 67.7% gross margin; Q3 guided to US$44.6-45.8bn, with margin guided slightly lower (65-67%) because new 2-nanometre factories cost more at first. | good | high | 2026-07-16 | -2.32% | -0.54% | -1.78% | normal | +1.43% | [TSMC Q2 2026 results, 2026-07-16](https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $453.31 | -1.02% | +0.69% | -0.92% | -0.79% | normal | no news found |
| 2026-10-07 | 2026-10-07 | $472.20 | -2.09% | -0.28% | -0.70% | -1.12% | normal | Citi said it expects TSMC to beat its own Q3 forecast and AI revenue to nearly double next year; the US shares fell 2.09% with chip stocks. |
| 2026-10-05 | 2026-10-05 | $485.80 | +2.75% | +0.79% | -0.11% | +2.08% | big | Elon Musk confirmed early talks about TSMC helping his Texas Terafab chip-factory project ("Just discussions, but something may come of it"); no TSMC comment. TSM rose 2.75% on Monday (+2.08 points company-specific), possibly partly on this, while AI-chip leaders also rallied; no single cause confirmed (tier-3 reports). |
| 2026-10-04 | 2026-10-02 | $472.78 | +2.96% | +0.85% | +0.98% | +1.12% | normal | Bloomberg reported TSMC is weighing a multi-factory campus near Dallas, each factory costing at least $20bn; early stage, and TSMC said "no comment on market rumors". |

Informational research and education, not investment advice.
