# AAOI news log: what happened, what is coming, and how the stock reacted

Every report that covers AAOI adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/AAOI.md`](../AAOI.md).

This page is rebuilt on every run from `data/news-log/AAOI.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **13** news items and **4** report days logged (first report 2026-10-04, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +2.60% (3 items).
- Average move beyond the market on the reaction day to **bad** news: -1.53% (5 items).
- Biggest reactions so far: 2026-10-08 -13.16% beyond the market (big) after: SVP Shu-Hua Yeh's planned sale executed: 6,000 shares on 10-05 at $120.03 (about $0.72m)...; 2026-10-08 -13.16% beyond the market (big) after: Fell 13.58% with no company news: optical stocks fell from the open (oil, high rates,...; 2026-08-07 +8.57% beyond the market (big) after: The 10-Q showed shares outstanding rose from 75.0m to 84.4m in six months; top 10....
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-11-05 | Q3 2026 results (estimated; date announcement expected mid-October) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | Rose 3.53% (opened +6.4%, faded) as optical stocks bounced after Lumentum's CEO said its parts are sold out until almost 2029. | good | low | 2026-10-09 | +3.53% | +0.60% | +2.93% | normal | n/a | [24/7 Wall St, 2026-10-09](https://247wallst.com/investing/2026/10/09/optics-stocks-rally-on-sold-out-optical-capacity-through-early-2029-applied-optoelectronics-and-lumentum-surge-7-coherent-climbs-5/), tier 3 |
| 2026-10-08 | Fell 13.58% with no company news: optical stocks fell from the open (oil, high rates, profit-taking) and the sell-off deepened after a Financial Times report that OpenAI's revenue pace was about $50bn, not $70bn; chipmakers −3.4%. | bad | medium | 2026-10-08 | -13.58% | -0.42% | -13.16% | big | n/a | [Reuters via Yahoo Finance, 2026-10-08](https://finance.yahoo.com/news/p-500-nasdaq-end-lower-203227225.html), tier 2 |
| 2026-10-07 | Fell 5.85% with no company news as chip and optical stocks fell together on a day of a morning rate spike; it had risen 29% in five sessions. | bad | medium | 2026-10-07 | -5.85% | -0.24% | -5.61% | normal | n/a | [Yahoo Finance, 2026-10-07](https://finance.yahoo.com/markets/live/stock-market-today-wednesday-october-7-dow-sp-500-nasdaq-080241833.html), tier 3 |
| 2026-10-07 | SVP Shu-Hua Yeh's planned sale executed: 6,000 shares on 10-05 at $120.03 (about $0.72m) under a 10b5-1 plan; he keeps 371,498 shares. | neutral | low | 2026-10-08 | -13.58% | -0.42% | -13.16% | big | n/a | [SEC Form 4, 2026-10-07](https://www.sec.gov/Archives/edgar/data/1158114/000168316826007698/xslF345X06/ownership.xml), tier 1 |
| 2026-10-06 | Rose 7.07% with no new company news: the morning gain was AOI's own (the share-sale completion it was credited to came out a day earlier), the afternoon matched an optics rally on the day Marvell raised its outlook (inference, medium). | neutral | medium | 2026-10-06 | +7.07% | +0.55% | +6.52% | normal | n/a | [24/7 Wall St, 2026-10-06](https://247wallst.com/investing/2026/10/06/applied-optoelectronics-surges-6-as-600m-share-sale-program-closes-lumentum-sits-out-the-rally-corning-edges-higher/), tier 3 |
| 2026-10-05 | Confirmed its $600m at-the-market share sale (announced 2026-08-21) is complete: 5,694,845 new shares at an average $105.36, $588.0m after fees, about 6.7% more shares; shares are up about 12.5% in five months, meeting AAOI trigger 6 read literally (THESIS ALERT). The stock still rose 5.17%: the end of the selling may have helped, or the optical rally simply continued (inference, low-to-medium confidence). | mixed | high | 2026-10-05 | +5.17% | +0.67% | +4.50% | normal | n/a | [PR Newswire, 2026-10-05](https://www.prnewswire.com/news-releases/applied-optoelectronics-announces-completion-of-previously-announced-at-the-market-offering-302897857.html), tier 1 |
| 2026-10-05 | Officer Shu-Hua (Joshua) Yeh filed notice to sell 6,000 shares (about $0.72m) under a 10b5-1 plan dated 2026-03-19; about 0.007% of shares. | neutral | low | 2026-10-06 | +7.07% | +0.55% | +6.52% | normal | n/a | [SEC Form 144, 2026-10-05](https://www.sec.gov/Archives/edgar/data/1158114/000197407826000376/xsl144X01/primary_doc.xml), tier 1 |
| 2026-10-02 | Jumped 7.71% on Friday (and 8.1% on Thursday) with no company news, as optical-networking stocks rose together. | neutral | low | 2026-10-02 | +7.71% | +0.74% | +6.97% | normal | -5.15% | [24/7 Wall St., 2026-10-02](https://247wallst.com/investing/2026/10/02/applied-optoelectronics-is-unstoppable-up-8-today-and-231-this-year-is-aaoi-stock-too-hot-to-handle-now/), tier 3 |
| 2026-09-10 | September 8-Ks (missed earlier): two more Houston buildings leased, a Houston building bought for $26,783,472 in cash, and a 10-year factory lease in Ningbo, China. | good | low | 2026-09-10 | -4.30% | -0.60% | -3.70% | normal | -5.06% | [AOI 8-K, 2026-09-10](https://www.sec.gov/Archives/edgar/data/1158114/000168316826007057/aaoi_8k.htm), tier 1 |
| 2026-09-08 | Found 2026-10-07 (missed earlier): SVP Hung-Lun (Fred) Chang sold 32,172 shares at $110.21 (about $3.55m, about 11% of his stake) without a 10b5-1 plan. | bad | low | 2026-09-08 | +5.70% | -0.55% | +6.25% | normal | -14.58% | [SEC Form 4, 2026-09-10](https://www.sec.gov/Archives/edgar/data/1158114/000168316826007059/xslF345X06/ownership.xml), tier 1 |
| 2026-08-21 | Set up a program to sell up to $600m of new shares over time, its third this year; the stock fell 13.8% the next trading day. | bad | high | 2026-08-21 | -3.32% | +0.41% | -3.72% | normal | -14.89% | [AOI 8-K, 2026-08-21](https://www.sec.gov/Archives/edgar/data/1158114/000110465926099688/tm2623389d2_8k.htm), tier 1 |
| 2026-08-06 | The 10-Q showed shares outstanding rose from 75.0m to 84.4m in six months; top 10 customers are 99% of revenue; customers owe $314.0m, $211.0m of it from one distributor; GAAP net loss $22.8m. | bad | medium | 2026-08-07 | +9.19% | +0.61% | +8.57% | big | +10.80% | [AOI 10-Q, 2026-08-06](https://www.sec.gov/Archives/edgar/data/1158114/000143774926026278/aaoi20260630_10q.htm), tier 1 |
| 2026-08-06 | Record Q2 revenue $191.9m (+86.4%), data centers 56.1%, first adjusted profit; Q3 guided to $255-290m; building capacity for about 650,000 high-speed units a month by end-2026. | good | high | 2026-08-07 | +9.19% | +0.61% | +8.57% | big | +10.80% | [AOI Q2 2026 results, 2026-08-06](https://www.sec.gov/Archives/edgar/data/1158114/000168316826006055/aaoi_ex9901.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $109.64 | +3.53% | +0.99% | -2.39% | +4.93% | normal | Rose 3.53% (opened +6.4%, faded) as optical stocks bounced after Lumentum's CEO said its parts are sold out until almost 2029. |
| 2026-10-07 | 2026-10-07 | $122.54 | -5.85% | -0.39% | -1.80% | -3.67% | normal | Fell 5.85% with no company news as chip and optical stocks fell together on a day of a morning rate spike; it had risen 29% in five sessions. |
| 2026-10-05 | 2026-10-05 | $121.57 | +5.17% | +1.06% | -0.29% | +4.41% | normal | Confirmed its $600m at-the-market share sale (announced 2026-08-21) is complete: 5,694,845 new shares at an average $105.36, $588.0m after fees, about 6.7% more shares; shares are up about 12.5% in five months, meeting AAOI trigger 6 read literally (THESIS ALERT). The stock still rose 5.17%: the end of the selling may have helped, or the optical rally simply continued (inference, low-to-medium confidence). |
| 2026-10-04 | 2026-10-02 | $115.59 | +7.71% | +1.15% | +2.60% | +3.96% | normal | Jumped 7.71% on Friday (and 8.1% on Thursday) with no company news, as optical-networking stocks rose together. |

Informational research and education, not investment advice.
