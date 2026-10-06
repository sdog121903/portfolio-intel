# MRNA news log: what happened, what is coming, and how the stock reacted

Every report that covers MRNA adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/MRNA.md`](../MRNA.md).

This page is rebuilt on every run from `data/news-log/MRNA.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **8** news items and **2** report days logged (first report 2026-10-04, latest 2026-10-05).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +87.83% (2 items).
- Average move beyond the market on the reaction day to **bad** news: -5.61% (2 items).
- Biggest reactions so far: 2026-08-19 +176.76% beyond the market (very big) after: Moderna and Merck's personalised melanoma vaccine (intismeran) plus Keytruda met its main...; 2026-09-01 +10.61% beyond the market (very big) after: Raised $3.0bn with convertible bonds: they could become about 14 million new shares...; 2026-10-05 +6.27% beyond the market (big) after: Rose 6.95% with no company news; biotech stocks rose, and one market-news site (citing no....
- Of those biggest moves, 2 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-05)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-08 | Index funds expected to buy at the close, before the Nasdaq-100 entry | not confirmed | not recorded |
| 2026-10-09 | Joins the Nasdaq-100 index before the open | yes | [Nasdaq, 2026-10-01](https://ir.nasdaq.com/news-releases/news-release-details/moderna-inc-join-nasdaq-100-indexr-beginning-october-9-2026), tier 1 |
| 2026-10-24 | Full Phase 3 melanoma data, ESMO Presidential Symposium, 10:30 a.m. New York time; webcast 1:00 p.m. | yes | [Moderna via ACCESS Newswire, 2026-09-21](https://finance.yahoo.com/healthcare/articles/moderna-announces-breaking-data-presented-141200784.html), tier 3 |
| about 2026-10-29 | Q3 2026 results | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | Rose 6.95% with no company news; biotech stocks rose, and one market-news site (citing no evidence) pointed to buying ahead of the Nasdaq-100 entry and the 10-24 data; against its last 20 trading days the move was about one and a half typical days. | neutral | medium | 2026-10-05 | +6.95% | +0.67% | +6.27% | big | n/a | [TradingKey, 2026-10-05](https://www.tradingkey.com/news/market-movers/262200511-market-movers-mrna-20261005), tier 3 |
| 2026-10-01 | Nasdaq said Moderna joins the Nasdaq-100 index before the open on 2026-10-09; index funds must buy shares, but the business is unchanged. | neutral | medium | 2026-10-02 | +0.57% | +0.74% | -0.17% | normal | n/a | [Nasdaq, 2026-10-01](https://ir.nasdaq.com/news-releases/news-release-details/moderna-inc-join-nasdaq-100-indexr-beginning-october-9-2026), tier 1 |
| 2026-09-30 | Citi downgraded to Sell and sees the stock at $80, arguing the price already assumes about $13bn a year of cancer-vaccine sales. | bad | medium | 2026-09-30 | -5.35% | -0.21% | -5.15% | big | n/a | [CNBC, 2026-09-30](https://www.cnbc.com/2026/09/30/moderna-has-been-on-a-tear-since-mid-august-citi-now-sees-it-plunging-60percent.html), tier 2 |
| 2026-09-30 | Named Juan Andres to a new Chief Operating Officer role from 2026-10-05; the chief technical operations and quality officer will retire. The CEO and CFO stay. | neutral | low | 2026-09-30 | -5.35% | -0.21% | -5.15% | big | n/a | [SEC Form 8-K, 2026-09-30](https://www.sec.gov/Archives/edgar/data/1682852/000119312526408289/d18337d8k.htm), tier 1 |
| 2026-09-01 | Raised $3.0bn with convertible bonds: they could become about 14 million new shares (about 3.6% more) above about $210.58; a capped-call hedge offsets that up to about $392.62. | mixed | medium | 2026-09-01 | +9.93% | -0.69% | +10.61% | very big | -12.10% | [SEC 8-K, 2026-09-01](https://www.sec.gov/Archives/edgar/data/1682852/000119312526378505/d108896d8k.htm), tier 1 |
| 2026-08-19 | Moderna and Merck's personalised melanoma vaccine (intismeran) plus Keytruda met its main goal in a Phase 3 trial (the final round of patient testing before approval). The stock rose 177% that day. | good | high | 2026-08-19 | +176.97% | +0.21% | +176.76% | very big | -14.18% | [Moderna/Merck, 2026-08-19](https://news.modernatx.com/merck-and-moderna-announce-phase-3-interpath-001-trial-of-intismeran-plus-keytruda-met-endpoints-of-rfs-and-dmfs-in-melanoma), tier 1 |
| 2026-08-05 | The FDA approved mFLUSIVA, Moderna's mRNA flu vaccine, for adults 50 and over. | good | medium | 2026-08-05 | -1.29% | -0.20% | -1.09% | normal | +13.18% | [NBC News, 2026-08-05](https://www.nbcnews.com/health/health-news/fda-approves-1st-mrna-flu-shot-moderna-rcna590599), tier 2 |
| 2026-07-31 | Q2 revenue $145m and a net loss of $0.8bn: today's business (mostly COVID vaccines) is small and loss-making. | bad | medium | 2026-07-31 | -5.35% | +0.72% | -6.07% | very big | +7.94% | [Moderna Q2 2026 results, 2026-07-31](https://www.sec.gov/Archives/edgar/data/0001682852/000168285226000147/exhibit9912026q2pressrelea.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | 2026-10-05 | $203.21 | +6.95% | +1.25% | +1.42% | +4.28% | normal | Rose 6.95% with no company news; biotech stocks rose, and one market-news site (citing no evidence) pointed to buying ahead of the Nasdaq-100 entry and the 10-24 data; against its last 20 trading days the move was about one and a half typical days. |
| 2026-10-04 | 2026-10-02 | $190.01 | +0.57% | +1.36% | -2.41% | +1.61% | normal | Nasdaq said Moderna joins the Nasdaq-100 index before the open on 2026-10-09; index funds must buy shares, but the business is unchanged. |

Informational research and education, not investment advice.
