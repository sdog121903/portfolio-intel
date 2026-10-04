---
name: why-analysis
description: Finds and explains the real cause of a price move, an earnings reaction, a valuation drop or any business change. Use whenever the report says something moved, or Santi asks why. Combines the numbers (how much of a move came from the market, the industry and the company; whether profits or the valuation multiple changed) with the Why Ladder (keep asking why until a basic, sourced driver) and macro transmission chains.
---

# Why analysis

"Why" is the question Santi cares about most. A good answer has two halves: the **numbers** that
size each possible cause, and the **story** that links the cause to the effect, with sources.

## Step 1: size the move with numbers

`scripts/move_attribution.py` (run by the pipeline) writes `data/metrics/attribution-<DATE>.json`.
For each holding it fits, on about a year of daily returns,

  stock = alpha + b_market x market + b_industry x (industry - market) + company-specific

and splits the last day and the last 5 days into a **market part**, an **industry part** and a
**company-specific part**, with a z-score saying how unusual the company part is compared with
its normal daily noise. Method and caveats for beginners: `references/move-attribution.md`.

Reading it:
- Company part small (|z| under about 1.5): the market or the industry explains the move.
  Say so and do not hunt for a company story that is not needed.
- Company part large: there is probably company news. Find it (source-hierarchy), date it,
  and check the timing lines up (after-hours news shows up in the next day's move).
- Large company part and no news found: say exactly that, list the plausible candidates
  (an analyst note, a peer's results, options expiry, index rebalancing), and label them as guesses.

## Step 2: profits or excitement?

When a stock re-rates over weeks or months, split the price change into the change in
expected or reported earnings and the change in the multiple (the price paid per dollar of
earnings) with `decompose_price_change(p0, p1, eps0, eps1)` from the same script. "Most of the
fall came from investors paying less for each dollar of profit, not from lower profits" is one of
the most useful sentences a beginner can learn.

## Step 3: climb the Why Ladder

`references/why-ladder.md`. Ask "why?" up to five times, each rung a short sentence with a
source or a confidence label, until you reach a **basic driver**: demand, price, cost,
competition, supply, regulation, interest rates, management decisions, accounting, or
expectations. Stop earlier if the evidence runs out, and say that it did.

## Step 4: connect to the bigger picture

For policy and macro news (interest rates, export controls, tariffs, AI spending plans), use the
transmission chains in `references/macro-drivers.md` and say which holdings are most exposed.

## Output in the report

- A *Market vs company* line with the attribution numbers.
- One to three cited bullets with the cause and why it matters.
- A **How this works** paragraph for the mechanism (with explain-like-a-teacher).
