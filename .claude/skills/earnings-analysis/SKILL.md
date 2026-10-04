---
name: earnings-analysis
description: Previews and reviews quarterly earnings for the holdings: what was expected, what was delivered, the forecast (guidance), the business metrics that matter for each industry, the quality of the result, and why the stock reacted the way it did. Use when a holding reports results in the news window, has results due within 14 days, or when Santi asks about a company's numbers.
---

# Earnings analysis

An earnings report is four questions: What did investors expect? What happened? What does
management now expect? Do the details make the result more or less believable? The stock's
reaction depends mostly on the gap between expectations and the new forecast.

## Before results (preview, when due within 14 days)

- **Date and time** (before the open or after the close), confirmed on the company's
  investor-relations page; say "estimated" if not confirmed.
- **Consensus** revenue and EPS (analysts' average forecast), and the company's own guidance
  from last quarter.
- **The one or two numbers that will decide the reaction** for this business
  (`references/sector-kpis.md`), and what last quarter's trend was.
- **What is priced in**: how far the stock ran into the report (1-month and 3-month returns
  from the metrics file) and what that implies about expectations.

## After results (review)

Follow `references/earnings-checklist.md`. In short:
1. Revenue and EPS versus consensus (beat or miss, by how much, in %).
2. Guidance versus consensus and versus the previous guidance (raised, kept, cut).
3. The industry's key metrics (ARR for software, data-center revenue for chips, backlog for
   builders), with year-over-year change.
4. Quality: growth from more customers or volume, or from one-offs, a lower tax rate, fewer
   shares, or accounting changes? GAAP versus non-GAAP gap?
5. Cash: did cash from operations follow profit?
6. Management's explanation of the "why", from the release and the call transcript.
7. The reaction, sized with the attribution numbers, and the reason given by tier 1-2 sources.

Primary numbers come from the release and the 10-Q (`data/fundamentals/<TICKER>.json` holds the
quarterly series from SEC XBRL, including a derived Q4 when only the annual figure was filed).

## Explaining it to Santi

Use the earnings pattern in `explain-like-a-teacher/references/explanation-patterns.md`. Always
answer "why did it go up/down?" in one plain sentence, and teach the idea underneath
(guidance matters more than the past quarter, because a share price is a bet on the future).
