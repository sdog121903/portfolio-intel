# How it fits together

```
 07:07 Madrid, every day (routine schedule, Anthropic cloud)
        |
        v
 fresh Claude Code session clones this repo  ->  reads CLAUDE.md
        |
        v
 1. Google Drive connector reads the FIDELITY sheet  ->  data/holdings/raw-<DATE>.json
 2. scripts/run_daily_data.py
       holdings -> prices -> metrics -> move attribution -> portfolio risk -> your rules
       -> SEC filings (8-K items, Form 4) -> fundamentals (weekly / after 10-Q)
       ->  data/metrics/*.json, data/filings/, data/fundamentals/, data/snapshots/
 3. holding-researcher subagents, one per stock, in parallel  ->  data/research/<DATE>/
 4. conclusions per stock: why-analysis, earnings-analysis, product-explainer,
    filings-decoder, news-and-events, position-review
 5. portfolio view: portfolio-risk + 14-day calendar
 6. teaching layer: lesson of the day, new words, learning ledger
 7. report from template  ->  challenger -> fact-checker -> plain-english-editor -> linter
 8. commit + push to main  ->  reports/daily/YYYY/MM/<DATE>.md
 9. Gmail connector  ->  email to sgomezo2003@gmail.com
```

Weekly (optional second routine): one holding gets a full `stock-analysis` deep dive, and its
thesis file is refreshed from primary documents.

## Design choices

- **Deterministic numbers, judgement in prose.** Anything that can be computed is computed by a
  tested script (`tests/`), so the language model never does arithmetic from memory.
- **Skills as reference guides.** Each skill folder is self-contained (`SKILL.md` + references +
  scripts) so the agent loads only what a step needs.
- **Primary sources and a linter.** Citations are mandatory and machine-checked; avoid-listed
  sources fail the build.
- **Teaching is a first-class output.** The learning ledger makes explanations deepen over time.
- **No advice.** Rules are the owner's; the system reports evidence and which rules fired.
- **Fail soft.** A failed step becomes a line in "Data quality and sources", never a silent gap.
