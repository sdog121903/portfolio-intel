# CRDO news log: what happened, what is coming, and how the stock reacted

Every report that covers CRDO adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/CRDO.md`](../CRDO.md).

This page is rebuilt on every run from `data/news-log/CRDO.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **5** news items and **2** report days logged (first report 2026-10-04, latest 2026-10-05).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: -0.17% (1 item).
- Average move beyond the market on the reaction day to **bad** news: -6.38% (2 items).
- Biggest reactions so far: 2026-09-02 -20.48% beyond the market (very big) after: After the results, BofA (to $275 from $340) and JPMorgan (to $310 from $335) cut their...; 2026-09-02 -20.48% beyond the market (very big) after: Q1 revenue $479.0m (+114.7%), above forecasts; next quarter guided to $525-535m and...; 2026-10-01 +7.72% beyond the market (big) after: Chief Legal Officer James Laufman sold 5,000 shares at $205.00 (about $1.03m, about 3% of....
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-05)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| about 2026-12-02 | Q2 FY2027 results (guidance $525-535m; not confirmed) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 | The chief operating officer sold 50,000 shares (about $10.3m) under a pre-planned 10b5-1 plan; insiders sold about $41.5m from 2026-09-23 to 10-02, all flagged as pre-planned, and bought nothing. | neutral | low | 2026-10-05 | -2.82% | +0.67% | -3.49% | normal | n/a | [SEC Form 4, 2026-10-02](https://www.sec.gov/Archives/edgar/data/1807794/000162828026064627/xslF345X06/wk-form4_1790974671.xml), tier 1 |
| 2026-10-01 | Chief Legal Officer James Laufman sold 5,000 shares at $205.00 (about $1.03m, about 3% of his holding) without the 10b5-1 box checked; one person, so not the 'several insiders' breaker. | bad | low | 2026-10-01 | +7.90% | +0.18% | +7.72% | big | n/a | [SEC Form 4, 2026-10-05](https://www.sec.gov/Archives/edgar/data/1807794/000162828026064939/xslF345X06/wk-form4_1791231688.xml), tier 1 |
| 2026-09-02 | After the results, BofA (to $275 from $340) and JPMorgan (to $310 from $335) cut their price targets, and Mizuho did too later in September; none lowered its rating. | bad | medium | 2026-09-02 | -20.04% | +0.44% | -20.48% | very big | -2.97% | [Benzinga, 2026-09-02](https://www.benzinga.com/analyst-stock-ratings/price-target/26/09/61572886/these-analysts-revise-their-forecasts-on-credo-technology-group-following-q1-results), tier 3 |
| 2026-09-01 | Q1 revenue $479.0m (+114.7%), above forecasts; next quarter guided to $525-535m and full-year growth above 85%. But the standard gross margin fell to 64.5% from 68.2%, and the stock fell about 20% the next day (margin drop the likely cause, inference). | mixed | high | 2026-09-02 | -20.04% | +0.44% | -20.48% | very big | -2.97% | [Credo Q1 FY2027 results, 2026-09-01](https://www.sec.gov/Archives/edgar/data/1807794/000162828026059795/credoq12027ex-991.htm), tier 1 |
| 2026-05-27 | Completed its purchase of DustPhotonics, expanding into optical chips. | good | medium | 2026-05-27 | -0.18% | -0.02% | -0.17% | normal | -3.00% | [Credo via Business Wire, 2026-05-27](https://www.businesswire.com/news/home/20260527239270/en/Credo-Completes-Acquisition-of-DustPhotonics), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 | 2026-10-05 | $212.48 | -2.82% | +0.70% | -0.25% | -3.27% | normal | The chief operating officer sold 50,000 shares (about $10.3m) under a pre-planned 10b5-1 plan; insiders sold about $41.5m from 2026-09-23 to 10-02, all flagged as pre-planned, and bought nothing. |
| 2026-10-04 | 2026-10-02 | $218.64 | +4.03% | +0.78% | +2.21% | +1.04% | normal | The chief operating officer sold 50,000 shares (about $10.3m) under a pre-planned 10b5-1 plan; insiders sold about $41.5m from 2026-09-23 to 10-02, all flagged as pre-planned, and bought nothing. |

Informational research and education, not investment advice.
