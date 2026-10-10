# QQQM: Invesco NASDAQ 100 ETF

**Last deep dive:** never  |  **Sector playbook:** none (an index fund, not a company)  |  **Industry fund:** QQQ (tracks the same index)

**Thesis approved:** draft: not yet approved (prefilled by Claude on 2026-10-07, the day after you bought it; nothing here is official until you approve or rewrite it)  |  **News and events:** [`theses/news/QQQM.md`](news/QQQM.md): every report's news, the upcoming calendar and how the price reacted, newest first.

## Why I own it (DRAFT for Santi to approve or rewrite)

**In one sentence (draft):** I hold QQQM because one cheap fund gives me about 100 of the largest Nasdaq companies at once, so this part of my money depends on no single company.

QQQM is an exchange-traded fund (ETF) [a fund that trades on the stock exchange like a share] that copies the Nasdaq-100 index: about 100 of the largest non-financial companies listed on the Nasdaq exchange [Invesco, 2026-10-07](https://www.invesco.com/qqq-etf/en/about.html). It costs 0.15% a year (15 cents for every $100 held) [Pensions & Investments ETF data, 2026-10-07](https://etf.pionline.com/fund/QQQM). Its biggest holdings on 2026-10-05 were NVIDIA 8.43%, Apple 7.28%, Microsoft 5.75%, Micron 5.01% and AMD 4.27% [StockAnalysis, 2026-10-05](https://stockanalysis.com/etf/qqqm/holdings/). Over the past year its worst fall was 12.0%, against 22.2% for your whole portfolio; its volatility over the last 60 days was 18.3%, against 41.6% for your portfolio over the past year (different windows, a rough comparison) (`data/metrics/2026-10-07.json`, `portfolio-2026-10-07.json`).

**What I accept (the risks, draft):** it is still mostly technology (about 67% by one data provider's count [Pensions & Investments ETF data, 2026-10-07](https://etf.pionline.com/fund/QQQM)), so it does less for "diversify beyond tech" than its 100 names suggest. It already owns some of your single stocks (AMD 4.27%, Palo Alto Networks 1.36%, CrowdStrike 1.14% on 2026-10-05 [StockAnalysis, 2026-10-05](https://stockanalysis.com/etf/qqqm/holdings/)), and Moderna joins the index on 2026-10-09 [Nasdaq, 2026-10-01](https://ir.nasdaq.com/news-releases/news-release-details/moderna-inc-join-nasdaq-100-indexr-beginning-october-9-2026). A fund falls with the market: it cannot beat the index it copies.

### The numbers behind it

<!-- numbers:start (rebuilt by thesis_tools.py from data as of 2026-10-09; edits inside this block are lost) -->

*No quarterly SEC figures for this company (it files as a foreign company); see the key trends below, taken from its own results releases.*

**The stock** (to 2026-10-09, `data/metrics/`)

| 1 month | 3 months | 6 months | 1 year | vs its 200-day average | Worst fall in the past year | Typical day |
|---|---|---|---|---|---|---|
| +5.0% | +3.7% | +23.2% | +23.7% | +11.8% | -12.0% | 1.2% |

*Price trend:* uptrend (price above its 50- and 200-day averages, and the 50 is above the 200). (The 200-day average is the average closing price over about the last ten months; trading above it usually means a longer uptrend.)

<!-- numbers:end -->

**Key trends** (sourced; refreshed when they change)

- Price: +26.0% over the past year to 2026-10-07, close $311.94, 0.7% below its 52-week high of $314.11 (`data/metrics/2026-10-07.json`).

### Thesis 1 (draft): "A low-cost, broad core that moves less than my single stocks"

1. **Why would I own it for this?** About 100 companies in one fund, for 0.15% a year; its worst fall in the past year (12.0%) was about half of my portfolio's (22.2%).
2. **What must stay true?** The fund keeps tracking the Nasdaq-100 closely at low cost *(pillar 1 below)*, and it stays steadier than my single stocks *(pillar 2 below)*.
3. **What would prove me wrong?** Any one of these *(triggers 1-2 below)*.

## What the company does (plain English, 3 sentences; here, the fund)
QQQM pools investors' money and buys the shares of the companies in the Nasdaq-100 index, in the same proportions as the index. When those companies rise or fall on average, the fund does the same, minus its small yearly fee. Invesco, the fund manager, earns that 0.15% fee; you earn (or lose) whatever the 100 companies do together.

## How it makes money
- For you: price changes of the ~100 companies, plus small dividends passed through (about 0.4% a year by one tier-3 estimate; not verified with Invesco).
- For Invesco: the 0.15% yearly fee, taken from the fund's assets.

## Metrics that matter
- How closely it follows the Nasdaq-100 (the gap between the fund and its index each year).
- Its fee (0.15% now).
- How much of it is technology, and how much overlaps with your single stocks.
- Its volatility and worst fall compared with your whole portfolio.

## What must stay true (checkable pillars)
1. **The fund tracks the Nasdaq-100 closely and cheaply** *(Thesis 1)*
   - *Why it matters:* a fund is only as good as its copying; a big gap or a fee rise eats your return.
   - *Measured by:* QQQM's daily return vs QQQ (same index), and the fee on Invesco's page.
   - *Now (as of 2026-10-07):* over the past month QQQM did 5.47% and QQQ 5.50% (`data/metrics/2026-10-07.json`); fee 0.15% [Pensions & Investments ETF data, 2026-10-07](https://etf.pionline.com/fund/QQQM).
   - *Next check:* every report (automatic), and Invesco's page yearly.
2. **It stays steadier than my single stocks** *(Thesis 1)*
   - *Why it matters:* if the "calm core" swings like everything else, it no longer does the job.
   - *Measured by:* its 60-day volatility and its worst fall in the past year, vs the whole portfolio (`data/metrics/`).
   - *Now (as of 2026-10-07):* 18.3% volatility over 60 days vs 41.6% for the portfolio over a year (different windows); worst fall 12.0% vs 22.2%.
   - *Next check:* every report.

## Invalidation triggers (what would prove the thesis wrong)
1. **The fund stops tracking its index or its fee rises** *(Thesis 1)*
   - *Why it matters:* the whole reason for a fund is cheap, faithful copying.
   - *Counts if:* QQQM trails QQQ by more than 0.5 points over a year, or Invesco raises the fee.
   - *Early warning:* a gap of more than 0.2 points in one month.
   - *Where and when to check:* `data/metrics/` (each report); Invesco's page.
   - *Status now (2026-10-07):* Not hit.
2. **It behaves like one more tech stock** *(Thesis 1)*
   - *Why it matters:* you bought a broad fund, not another AI bet.
   - *Counts if:* its 60-day volatility rises above 30%, or its 60-day correlation with your AI holdings rises above 0.8.
   - *Early warning:* volatility above 25%.
   - *Where and when to check:* `data/metrics/` and `portfolio-<DATE>.json`, each report.
   - *Status now (2026-10-07):* Not hit (60-day volatility 18.3%).

## Facts as of 2026-10-07 (every figure sourced)
- Bought 0.100 shares on 2026-10-06; entry $312.76 (the sheet's estimate, Tuesday's close); worth $31.19 at Wednesday's close, the largest position in your portfolio at 13.7% (`data/metrics/portfolio-2026-10-07.json`).
- Index: Nasdaq-100; fee 0.15% a year [Pensions & Investments ETF data, 2026-10-07](https://etf.pionline.com/fund/QQQM).
- Top holdings on 2026-10-05: NVIDIA 8.43%, Apple 7.28%, Microsoft 5.75%, Micron 5.01%, AMD 4.27% [StockAnalysis, 2026-10-05](https://stockanalysis.com/etf/qqqm/holdings/).

## Change log
- 2026-10-07: Draft created after the 2026-10-06 purchase. Everything above "Facts as of" is a proposal for Santi to approve, rewrite or reject.
- 2026-10-09 (daily report, covering Thu 10-08 and Fri 10-09): Draft still awaiting Santi's approval. Both draft pillars hold (one-year tracking QQQM +23.51% vs QQQ +23.45%; 60-day volatility 18.2%). Early warning on the draft correlation trigger: 60-day correlation with TSMC 0.79 (draft trigger 0.8). Moderna joined the Nasdaq-100 on 2026-10-09. No edits to the draft.
