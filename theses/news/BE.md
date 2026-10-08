# BE news log: what happened, what is coming, and how the stock reacted

Every report that covers BE adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/BE.md`](../BE.md).

This page is rebuilt on every run from `data/news-log/BE.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **7** news items and **2** report days logged (first report 2026-10-04, latest 2026-10-07).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +2.18% (3 items).
- Average move beyond the market on the reaction day to **bad** news: +10.89% (2 items).
- Biggest reactions so far: 2026-07-30 +24.81% beyond the market (very big) after: Shareholders filed a securities class action after a Hunterbrook report on Chinese...; 2026-10-02 +3.43% beyond the market (normal) after: Barclays raised its target to $308 and kept a neutral rating, citing a second factory in...; 2026-10-02 +3.43% beyond the market (normal) after: Virginia's 2026 Energy Plan named fuel cells as a near-term clean-power option (Bloom not....
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-07)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-10-27 | Q3 2026 results (estimated 10-26 to 10-29) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-07 | Bernstein kept Market Perform ($282 target), seeing a 10-20 GW behind-the-meter market by 2030 and utilities as a second group of buyers. | neutral | low | 2026-10-07 | -1.52% | -0.24% | -1.28% | normal | n/a | [Investing.com, 2026-10-07](https://www.investing.com/news/analyst-ratings/bernstein-reiterates-bloom-energy-stock-rating-on-utility-demand-93CH-4936717), tier 3 |
| 2026-10-07 | Fuel-cell stocks fell after FuelCell Energy's CFO stepped down (FuelCell -12%); Bloom fell far less (-1.52%). | neutral | low | 2026-10-07 | -1.52% | -0.24% | -1.28% | normal | n/a | [24/7 Wall St, 2026-10-07](https://247wallst.com/investing/2026/10/07/fuelcell-tumbles-12-as-its-finance-chief-of-15-years-steps-down-bloom-energy-dips-plug-power-slides-3/), tier 3 |
| 2026-10-02 | Barclays raised its target to $308 and kept a neutral rating, citing a second factory in Fremont, California, and utility demand (Ameren plans 500 megawatts of fuel cells). | good | low | 2026-10-02 | +4.17% | +0.74% | +3.43% | normal | n/a | [Investing.com, 2026-10-02](https://www.investing.com/news/stock-market-news/barclays-lifts-bloom-energy-target-to-308-on-factory-expansion-utility-shift-4927314), tier 3 |
| 2026-10-01 | Virginia's 2026 Energy Plan named fuel cells as a near-term clean-power option (Bloom not named); fuel-cell stocks rallied the next day and BE rose 4.17%. | good | low | 2026-10-02 | +4.17% | +0.74% | +3.43% | normal | n/a | [Cardinal News, 2026-10-01](https://cardinalnews.org/2026/10/01/spanberger-unveils-energy-plan-with-focus-on-achieving-a-net-zero-power-sector-by-2050/), tier 3 |
| 2026-09-24 | Oracle invoked force majeure (a claim that events outside its control excuse a delay) on Project Jupiter in New Mexico, which may use up to 2.45 gigawatts of Bloom fuel cells, because the gas pipeline slipped to February 2027. All sides say the contract stands. | bad | high | 2026-09-24 | -3.10% | -0.08% | -3.02% | normal | +4.10% | [CNBC, 2026-09-24](https://www.cnbc.com/2026/09/24/oracle-data-center-force-majeure.html), tier 2 |
| 2026-07-30 | Shareholders filed a securities class action after a Hunterbrook report on Chinese scandium (a rare metal) in Bloom's supply chain, which Bloom calls false. | bad | medium | 2026-07-30 | +26.49% | +1.68% | +24.81% | very big | +10.54% | [D&O Diary, 2026-08-02](https://www.dandodiary.com/2026/08/articles/geopolitical-risk/geopolitical-issues-lead-to-securities-suit-against-fuel-cell-company/), tier 3 |
| 2026-07-28 | Q2 revenue $1,065.4m (+165.5%) with $226.4m of operating cash flow; 2026 outlook raised to $3.9-4.2bn. | good | high | 2026-07-29 | -1.85% | -1.54% | -0.31% | normal | +43.10% | [Bloom Q2 2026 results, 2026-07-28](https://www.sec.gov/Archives/edgar/data/0001664703/000162828026050150/ex991_q226financialresults.htm), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-07 | 2026-10-07 | $291.29 | -1.52% | -0.53% | -3.38% | +2.40% | normal | Bernstein kept Market Perform ($282 target), seeing a 10-20 GW behind-the-meter market by 2030 and utilities as a second group of buyers. |
| 2026-10-04 | 2026-10-02 | $289.15 | +4.17% | +1.65% | +4.23% | -1.71% | normal | Barclays raised its target to $308 and kept a neutral rating, citing a second factory in Fremont, California, and utility demand (Ameren plans 500 megawatts of fuel cells). |

Informational research and education, not investment advice.
