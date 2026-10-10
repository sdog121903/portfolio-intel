# PANW news log: what happened, what is coming, and how the stock reacted

Every report that covers PANW adds its news here, newest first. Nothing is deleted, so over months this page shows how the stock tends to react to each kind of news. Thesis file: [`theses/PANW.md`](../PANW.md).

This page is rebuilt on every run from `data/news-log/PANW.json` by `.claude/skills/news-and-events/scripts/news_log.py`; edits made here by hand are lost.

**How to read the reaction columns.** *Reaction day* is the first trading day the news could move the price (the next day if it came out after the 4 p.m. New York close). *Stock* is the price change that day; *Market* is the S&P 500 fund (SPY) the same day; *Beyond market* is the difference, the part the market does not explain. *Size* compares that difference with a normal day for this stock over the year before (measured so that one extreme day cannot distort it): normal (under one typical day), big (one to two), very big (two or more). *Next 5 days* shows whether the move held or faded.

## What the log shows so far

- **14** news items and **4** report days logged (first report 2026-10-04, latest 2026-10-09).
- **Too early to draw conclusions:** fewer than 20 items. Read this page as a diary for now, not as a rule about how the stock behaves.
- Average move beyond the market on the reaction day to **good** news: +3.53% (6 items).
- Average move beyond the market on the reaction day to **bad** news: -0.62% (3 items).
- Biggest reactions so far: 2026-09-14 +13.54% beyond the market (very big) after: Security stocks jumped (PANW about +13%) after AI-lab leaders warned about the risks of...; 2026-09-02 -9.73% beyond the market (very big) after: Q4 revenue $3.41bn (+34%), above forecasts; next-generation security ARR $9.10bn (+63%)....; 2026-10-09 +4.49% beyond the market (very big) after: Rose 5.09%, almost entirely the cybersecurity group (industry part +4.41) as software led....
- Of those biggest moves, 2 partly reversed over the next five trading days.
- Report days with a very big company-specific move and no news found: 0.
- Several items can share one reaction day, so their reactions are not independent.

## Coming up (calendar as of 2026-10-09)

Dated events that could move the stock. When one happens, it moves into the news table below.

| Date | Event | Confirmed? | Source |
|---|---|---|---|
| 2026-11-18 | Q1 FY2027 results (estimated) | not confirmed | not recorded |

## News, newest first

| Date | What happened | Good or bad for the stock | Importance | Reaction day | Stock | Market | Beyond market | Size | Next 5 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | Rose 5.09%, almost entirely the cybersecurity group (industry part +4.41) as software led Friday's rebound; no cybersecurity-specific reason published. | good | medium | 2026-10-09 | +5.09% | +0.60% | +4.49% | very big | n/a | [Yahoo Finance, 2026-10-09](https://finance.yahoo.com/markets/live/stock-market-today-friday-october-9-dow-sp-500-nasdaq-080148117.html), tier 3 |
| 2026-10-09 | Director Bawa's trust sold 250 shares (about $103k) outside a plan, after unplanned sales on 09-14, 09-15 and 09-24: four in 30 days by one person. | bad | low | 2026-10-09 | +5.09% | +0.60% | +4.49% | very big | n/a | [SEC Form 4, 2026-10-09](https://www.sec.gov/Archives/edgar/data/1327567/000119312526419277/ownership.xml), tier 1 |
| 2026-10-08 | Named one of 11 founding partners of Anthropic's Critical Infrastructure Defense Program; no money terms. | good | low | 2026-10-08 | -1.74% | -0.42% | -1.32% | normal | n/a | [Anthropic, 2026-10-08](https://www.anthropic.com/news/anthropic-cyber-mission), tier 1 |
| 2026-10-08 | Klarich's trust gave 60,000 shares to a charity he controls, which filed notice to sell them (about $23.9m), no plan listed; proceeds go to the charity. | neutral | low | 2026-10-08 | -1.74% | -0.42% | -1.32% | normal | n/a | [SEC Form 144, 2026-10-08](https://www.sec.gov/Archives/edgar/data/1327567/000195824426000652/xsl144X01/primary_doc.xml), tier 1 |
| 2026-10-07 | Fell 3.42% with the cybersecurity group; no company news. | bad | low | 2026-10-07 | -3.42% | -0.24% | -3.17% | big | n/a | [Yahoo Finance, 2026-10-07](https://finance.yahoo.com/markets/live/stock-market-today-wednesday-october-7-dow-sp-500-nasdaq-080241833.html), tier 3 |
| 2026-10-06 | Rose 3.23% to a record close of $419.91 with the software rally. | good | medium | 2026-10-06 | +3.23% | +0.55% | +2.68% | big | n/a | [Reuters via Investing.com, 2026-10-06](https://www.investing.com/news/stock-market-news/us-software-stocks-scale-fresh-2026-highs-as-ai-disruption-worries-fade-4934831), tier 2 |
| 2026-10-02 | TD Cowen raised its price target to $440 from $400 and kept a Buy rating (an opinion, not new facts). | good | low | 2026-10-02 | +1.76% | +0.74% | +1.02% | normal | +3.85% | [Investing.com, 2026-10-02](https://investing.com/news/analyst-ratings/td-cowen-raises-palo-alto-networks-stock-price-target-on-ai-tailwinds-93CH-4929302), tier 3 |
| 2026-10-01 | Chief accounting officer Josh Paul sold 400 shares at $395.70 under a 10b5-1 plan; 1,308 shares were withheld for tax on vesting stock. | neutral | low | 2026-10-01 | -0.27% | +0.18% | -0.45% | normal | +0.57% | [SEC Form 4, 2026-10-05](https://www.sec.gov/Archives/edgar/data/1327567/000188228526000027/xslF345X06/ownership.xml), tier 1 |
| 2026-10-01 | Lee Klarich gave away 25,000 shares as a gift, not a sale. | neutral | low | 2026-10-02 | +1.76% | +0.74% | +1.02% | normal | +3.85% | [SEC Form 4, 2026-10-01](https://www.sec.gov/Archives/edgar/data/1327567/000168226026000006/xslF345X06/ownership.xml), tier 1 |
| 2026-09-22 | Launched new AI-security services such as Unit 42 Frontier AI Defense. | good | low | 2026-09-22 | +0.76% | -0.02% | +0.77% | normal | +3.69% | [Palo Alto Networks via Nasdaq, 2026-09-22](https://www.nasdaq.com/press-release/palo-alto-networks-delivers-anthropics-mythos-and-openais-gpt-56-customers-unit-42), tier 1 |
| 2026-09-18 | Bernstein lowered its rating, saying the stock had run past fair value. | bad | medium | 2026-09-18 | -3.06% | +0.13% | -3.19% | big | +3.07% | [Motley Fool, 2026-09-18](https://www.fool.com/investing/2026/09/18/why-palo-alto-networks-stock-dropped-today/), tier 3 |
| 2026-09-14 | Security stocks jumped (PANW about +13%) after AI-lab leaders warned about the risks of powerful AI, which investors read as more security spending ahead. | good | medium | 2026-09-14 | +13.09% | -0.45% | +13.54% | very big | -0.58% | [Forbes, 2026-09-14](https://www.forbes.com/sites/antoniopequenoiv/2026/09/14/crowdstrike-skyrockets-14-as-ai-fears-send-cybersecurity-stocks-surging/), tier 2 |
| 2026-09-01 | Q4 revenue $3.41bn (+34%), above forecasts; next-generation security ARR $9.10bn (+63%). Next year's forecast $14.10-14.20bn means growth slows to 23-24% as the CyberArk boost fades; standard (GAAP) loss of $0.35 a share. | mixed | high | 2026-09-02 | -9.28% | +0.44% | -9.73% | very big | +3.05% | [PANW Q4 FY2026 results, 2026-09-01](https://www.sec.gov/Archives/edgar/data/0001327567/000132756726000019/ex991q426earningsrelease.htm), tier 1 |
| 2026-02-11 | Completed the purchase of CyberArk (logins and passwords for people and AI agents) for $21.1bn, paid partly with 112 million new shares. | mixed | high | 2026-02-11 | -0.13% | -0.02% | -0.10% | normal | -8.66% | [Palo Alto Networks, 2026-02-11](https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-cyberark-to-secure-the-ai-era), tier 1 |

## Price on each report day, newest first

The day's move split into the part from the whole market, the part from its industry and the part that is the company's own (from the report's move attribution).

| Report | Trading day | Close | Day move | Market part | Industry part | Company part | Size of company part | Main news that day |
|---|---|---|---|---|---|---|---|---|
| 2026-10-09 | 2026-10-09 | $418.78 | +5.09% | +0.61% | +4.41% | +0.07% | normal | Rose 5.09%, almost entirely the cybersecurity group (industry part +4.41) as software led Friday's rebound; no cybersecurity-specific reason published. |
| 2026-10-07 | 2026-10-07 | $405.57 | -3.42% | -0.24% | -1.78% | -1.40% | normal | Fell 3.42% with the cybersecurity group; no company news. |
| 2026-10-05 | 2026-10-05 | $406.76 | +0.87% | +0.68% | +0.85% | -0.66% | normal | no news found |
| 2026-10-04 | 2026-10-02 | $403.24 | +1.76% | +0.75% | +0.22% | +0.80% | normal | TD Cowen raised its price target to $440 from $400 and kept a Buy rating (an opinion, not new facts). |

Informational research and education, not investment advice.
