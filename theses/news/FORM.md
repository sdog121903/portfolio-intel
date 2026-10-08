# FORM news log: what happened, what is coming, and how the stock reacted

Every report that covers FORM adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/FORM.md`](../FORM.md).

This page is rebuilt on every run from `data/news-log/FORM.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **7** news items and **3** report days logged (first report 2026-10-04, latest 2026-10-07).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +11.21% (3 items).
- Average move beyond the market on the reaction day to **bad** news: -5.07% (1 item).
- Biggest reactions so far: 2026-07-30 +24.60% beyond the market (very big) after: Record Q2 revenue $258.2m (+31.9%) and adjusted gross margin 53.3%; Q3 guided to $270m...; 2026-09-30 +9.79% beyond the market (very big) after: Deutsche Bank began coverage positively, saying FormFactor is now a second approved...; 2026-10-06 -5.07% beyond the market (big) after: Fell 4.52% with no company news as chip-equipment and test stocks fell together (median....
- Of those biggest moves, 1 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-07)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-08 | Samsung preliminary Q3 results (memory read-across) | yes | not recorded |
| 2026-10-13 | Management at CEO Investor Summit | yes | not recorded |
| 2026-10-27 | SK hynix Q3 results (largest customer) | not confirmed | not recorded |
| 2026-10-28 | Q3 2026 results (estimated) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-06 | Fell 4.52% with no company news as chip-equipment and test stocks fell together (median of eight peers -3.52%) and memory stocks slid before results. | bad | medium | 2026-10-06 | -4.52% | +0.55% | -5.07% | big | n/a | [Korea JoongAng Daily, 2026-10-07](https://www.koreajoongangdaily.com/business/kospi-drops-nearly-2-percent-as-bond-yield-worries-hit-tech-stocks/12909800), tier 2 |
| 2026-10-05 | About 13.9 million shares traded (about 11 times normal) as index funds rebalanced before its move into the S&P MidCap 400 on 10-06 (inference, high confidence); the price barely moved (-0.78%). | neutral | low | 2026-10-05 | -0.78% | +0.67% | -1.45% | normal | n/a | [S&P Dow Jones Indices, 2026-10-01](https://press.spglobal.com/2026-10-01-Vylor-Added-to-the-S-P-500-Twilio-Set-to-Join-S-P-500-Others-to-Join-S-P-MidCap-400-and-S-P-SmallCap-600), tier 1 |
| 2026-10-02 | Barely moved (+0.48%) while chip stocks rose; its own small dip was normal noise and no reason was published. | neutral | low | 2026-10-02 | +0.48% | +0.74% | -0.26% | normal | n/a | Pipeline attribution, 2026-10-04, tier 1 |
| 2026-10-01 | S&P moves FormFactor from the SmallCap 600 into the MidCap 400 index before the open on 2026-10-06; index funds rebalance, but the business is unchanged. | neutral | medium | 2026-10-02 | +0.48% | +0.74% | -0.26% | normal | n/a | [S&P Dow Jones Indices, 2026-10-01](https://press.spglobal.com/2026-10-01-Vylor-Added-to-the-S-P-500-Twilio-Set-to-Join-S-P-500-Others-to-Join-S-P-MidCap-400-and-S-P-SmallCap-600), tier 1 |
| 2026-09-30 | Deutsche Bank began coverage positively, saying FormFactor is now a second approved supplier of test cards for NVIDIA graphics chips; the stock rose 9.6%. | good | medium | 2026-09-30 | +9.59% | -0.21% | +9.79% | very big | -6.37% | [Investing.com, 2026-09-30](https://www.investing.com/news/stock-market-news/why-is-formfactor-stock-surging-today-93CH-4925395), tier 3 |
| 2026-09-30 | Memory maker Micron reported quarterly revenue of $54.23bn against $51.07bn expected, a sign the AI-memory boom (FormFactor's main market) continues. | good | medium | 2026-10-01 | -0.58% | +0.18% | -0.76% | normal | n/a | [Micron 8-K, 2026-09-30](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm), tier 1 |
| 2026-07-29 | Record Q2 revenue $258.2m (+31.9%) and adjusted gross margin 53.3%; Q3 guided to $270m plus or minus $10m. Management said about a third of the margin gain was one-off. | good | high | 2026-07-30 | +26.28% | +1.68% | +24.60% | very big | +9.33% | [FormFactor Q2 2026 results, 2026-07-29](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000030/ex9901-earningsreleasexq226.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-07 | 2026-10-07 | $139.80 | -1.06% | +0.01% | -1.93% | +0.86% | normal | no news found |
| 2026-10-05 | 2026-10-05 | $147.99 | -0.78% | -0.01% | -0.31% | -0.46% | normal | About 13.9 million shares traded (about 11 times normal) as index funds rebalanced before its move into the S&P MidCap 400 on 10-06 (inference, high confidence); the price barely moved (-0.78%). |
| 2026-10-04 | 2026-10-02 | $149.15 | +0.48% | -0.00% | +2.72% | -2.24% | normal | S&P moves FormFactor from the SmallCap 600 into the MidCap 400 index before the open on 2026-10-06; index funds rebalance, but the business is unchanged. |

Informational research and education, not investment advice.
