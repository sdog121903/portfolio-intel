---
name: filings-decoder
description: Reads and explains SEC filings for the holdings: 8-K event reports (by item number), 10-Q and 10-K reports, Form 4 insider trades, Form 144 planned sales, S-3 and 424B share sales, 13D/13G large holders, proxy statements. Use when the pipeline finds new filings, when news mentions a filing, or when Santi asks what a filing means.
---

# Filings decoder

A filing is the company speaking under legal obligation, so it is the most reliable source
there is. It is also written in legal language. Your job: find what is new, say what it means
in plain English, and judge whether it matters.

## Where the data comes from

`scripts/fetch_edgar.py` (run by the pipeline) writes `data/filings/<DATE>.json`: every filing
in the last `run.filings_window_days`, with plain-English form names, 8-K items decoded and
rated by materiality, and Form 4 insider trades parsed from the raw XML (who, role, buy or
sell, shares, price, dollar value, shares still owned, 10b5-1 plan flag). Open the actual
document (the `url` field) for anything rated high before explaining it.

## How to explain a filing

1. **What it is**, in one line ("an 8-K is the form a company must file within four business
   days when something important happens").
2. **What is new in it**, quoting numbers from the document itself.
3. **Why it matters**, or why it does not ("Item 9.01 just means exhibits are attached").
4. **Materiality**: high / medium / low, using `references/sec-filings-guide.md`.
5. **Link** `[SEC Form 8-K, YYYY-MM-DD](url)`.

## Insider trades: read them carefully

- Code **S** (open-market sale) and **P** (open-market purchase) are the ones that carry
  information. **F** (shares withheld for tax), **A** (grants), **M** (option exercises) and
  **G** (gifts) are mostly routine.
- Sales under a **10b5-1 plan** were scheduled months in advance and say little about today's
  view. Unplanned sales by several insiders in a short period are a thesis breaker in
  `config/rules.toml`. Open-market purchases with personal money are rarer and more telling.
- Always give size in context: "sold 24,542 shares worth about $25.7 million, about X% of the
  shares they held".
- A **Form 144** is a notice of a planned sale, not the sale itself.

## Reference

`references/sec-filings-guide.md`: every common form and every 8-K item in plain English, with
materiality ratings and what to look for in 10-Q and 10-K sections.
