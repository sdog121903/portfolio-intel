---
name: position-review
description: The Stay-or-Retreat evidence review for each holding, without giving advice. Checks the owner's own rules (config/rules.toml) and thesis (theses/<TICKER>.md) against today's evidence, assigns a thesis status (Intact, Watch, Challenged, Broken), lists the three strongest sourced reasons to stay and to retreat, and flags thesis-breaking events. Use for every holding in the daily report and whenever Santi asks "should I stay in this?".
---

# Position review: Stay or Retreat, decided by Santi

Santi asked for a Stay or Retreat call. Telling him to hold or sell would be personal investment
advice, which this system never gives. Instead it makes his own decision fast and well-informed:
his rules are checked mechanically, his thesis is tested against evidence, and the strongest
arguments on both sides are laid out with sources. The decision stays his.

## 1. His rules (mechanical)

`scripts/check_rules.py` (run by the pipeline) applies `config/rules.toml` and writes
`data/metrics/rules-<DATE>.json`: per holding, every rule that fired, the numbers and a
plain-English sentence. Status words: **RETREAT RULE HIT**, **TARGET REACHED**, **WATCH**,
**No rule fired**. Report them exactly; never add rules of your own. If a rule is close to
firing (price within about 3% of his stop or target), mention it as information.

## 2. Thesis breakers (judgement, from evidence)

`config/rules.toml` `[thesis_breakers]` lists events he wants to know about (guidance cut,
CEO/CFO departure, restatement, dilution, clustered unplanned insider selling...). Check each
against the research output and the filings file. Any confirmed hit = **THESIS ALERT** in "Your
rules today", explained in plain words with its source.

## 3. Thesis status (use `references/thesis-status-rubric.md`)

Compare today's evidence with "What must stay true" and "Invalidation triggers" in
`theses/<TICKER>.md`:
- **Intact**: nothing material contradicts the thesis.
- **Watch**: one pillar is weaker or uncertain, but the cause looks temporary or unconfirmed.
- **Challenged**: a pillar is contradicted by tier-1/2 evidence.
- **Broken**: an invalidation trigger has clearly happened.
Status changes need a sentence explaining what changed. If the thesis file is empty, say
"No written thesis yet: add your reasons to theses/<TICKER>.md" and judge against the company's
own stated strategy.
If "Why I own it" is still TODO but the file has a "Draft thesis" (statements Santi has not yet
approved), judge against the draft's "(Proposed)" pillars and triggers and say so plainly:
"judged against the draft thesis, not yet approved by you". A draft trigger that happens is
reported as a THESIS ALERT on the draft, never as his thesis breaking.

## 4. The two cases

Three points each, strongest first, each sourced or labelled as inference with confidence.
Write the case to retreat as seriously as the case to stay; a weak bear case is worse than none.
Good points are specific and checkable ("guidance implies growth slowing from 50% to 30%"),
not generic ("competition is a risk").

## What never appears
"You should", "I recommend", "time to sell", a price target of our own, position sizing.
Analyst ratings and price targets may be reported as other people's opinions, with dates.
