# LITE news log: what happened, what is coming, and how the stock reacted

Every report that covers LITE adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/LITE.md`](../LITE.md).

This page is rebuilt on every run from `data/news-log/LITE.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **7** news items and **2** report days logged (first report 2026-10-04, latest 2026-10-05).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +3.93% (4 items).
- Biggest reactions so far: 2026-08-12 +13.38% beyond the market (very big) after: Q4 revenue doubled to $1.01bn (+109%); next quarter guided to $1.225-1.275bn; management...; 2026-10-01 +7.49% beyond the market (big) after: Bernstein started covering optical stocks at Outperform; Lumentum jumped 7.7% as the...; 2026-07-29 -6.07% beyond the market (big) after: Signed a six-year deal reserving production at AXT (wafer maker for lasers), backed by....
- Of those biggest moves, 2 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-05)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-12 to 10-15 | OCP Global Summit (data-center hardware conference); Lumentum talks 2026-10-14 | yes | not recorded |
| 2026-11-05 | Q1 FY2027 results after the close; call 5:00 p.m. New York time (guidance $1.225-1.275bn) | yes | [Lumentum via Business Wire (Yahoo Finance), 2026-10-05](https://finance.yahoo.com/markets/stocks/articles/lumentum-announces-reporting-date-fiscal-120000373.html), tier 3 |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | Set Q1 FY2027 results for Thursday 2026-11-05 after the close, with a call at 5:00 p.m. New York time. | neutral | low | 2026-10-05 | +0.58% | +0.67% | -0.10% | normal | n/a | [Lumentum via Business Wire (Yahoo Finance), 2026-10-05](https://finance.yahoo.com/markets/stocks/articles/lumentum-announces-reporting-date-fiscal-120000373.html), tier 3 |
| 2026-10-02 | Record close of $1,085.42 (+3.79%), mostly because chip stocks rose. After the close a filing showed the CFO sold 24,542 shares (about $25.7m, roughly a quarter of his stake) under a pre-planned 10b5-1 plan. | neutral | medium | 2026-10-05 | +0.58% | +0.67% | -0.10% | normal | n/a | [SEC Form 4, 2026-10-02](https://www.sec.gov/Archives/edgar/data/1633978/000156110026000008/xslF345X06/form4-10022026_081041.xml), tier 1 |
| 2026-10-01 | Bernstein started covering optical stocks at Outperform; Lumentum jumped 7.7% as the group rallied. | good | medium | 2026-10-01 | +7.67% | +0.18% | +7.49% | big | n/a | [Yahoo Finance, 2026-10-01](https://finance.yahoo.com/markets/stocks/article/coherent-lumentum-and-ciena-stocks-surge-on-bullish-wall-street-call-182906439.html), tier 2 |
| 2026-09-15 | US senators introduced a bill to keep Chinese optical transceivers out of US national-security systems, which could help US makers. Not law. | good | low | 2026-09-15 | +0.47% | -0.46% | +0.93% | normal | +12.72% | [Sen. McCormick, 2026-09-15](https://www.mccormick.senate.gov/news/press-releases/senators-mccormick-gallego-cornyn-fetterman-introduce-bill-to-keep-chinese-transceivers-out-of-u-s-national-security-systems/), tier 1 |
| 2026-08-14 | The annual report (10-K) showed Lumentum swapped convertible bonds for about 10.6 million new shares, about 13% more shares in the quarter: less debt, but each owner's slice is smaller. | mixed | medium | 2026-08-14 | +5.19% | -0.20% | +5.39% | normal | -6.42% | [Lumentum 10-K, 2026-08-14](https://www.sec.gov/Archives/edgar/data/0001633978/000162828026057358/lite-20260627.htm), tier 1 |
| 2026-08-11 | Q4 revenue doubled to $1.01bn (+109%); next quarter guided to $1.225-1.275bn; management said it is still shipping behind customer demand for its lasers. | good | high | 2026-08-12 | +13.63% | +0.25% | +13.38% | very big | -11.25% | [Lumentum Q4 FY2026 results, 2026-08-11](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results/default.aspx), tier 1 |
| 2026-07-29 | Signed a six-year deal reserving production at AXT (wafer maker for lasers), backed by two $43.5m deposits, securing a scarce input. | good | low | 2026-07-29 | -7.61% | -1.54% | -6.07% | big | +37.17% | [AXT 8-K, 2026-07-29](https://www.sec.gov/Archives/edgar/data/0001051627/000143774926024883/axti20260715_8k.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | 2026-10-05 | $1,091.67 | +0.58% | +0.33% | -0.26% | +0.50% | normal | Record close of $1,085.42 (+3.79%), mostly because chip stocks rose. After the close a filing showed the CFO sold 24,542 shares (about $25.7m, roughly a quarter of his stake) under a pre-planned 10b5-1 plan. |
| 2026-10-04 | 2026-10-02 | $1,085.42 | +3.79% | +0.37% | +2.29% | +1.13% | normal | Record close of $1,085.42 (+3.79%), mostly because chip stocks rose. After the close a filing showed the CFO sold 24,542 shares (about $25.7m, roughly a quarter of his stake) under a pre-planned 10b5-1 plan. |

Informational research and education, not investment advice.
