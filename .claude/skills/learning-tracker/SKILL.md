---
name: learning-tracker
description: Tracks what Santi has already been taught so explanations grow with him: new terms get full explanations, familiar ones a one-line reminder, known ones none, and old lessons come back for spaced review. Use before writing any report (to check term levels), after writing one (to record what was taught), and when choosing the Lesson of the day from learning/curriculum.md.
---

# Learning tracker

The goal is that Santi becomes an expert, so the report should get more sophisticated as he
does, without ever leaving him behind.

## The ledger: `learning/concepts.json`

`scripts/concept_ledger.py` manages it:
```bash
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py status guidance beta "free cash flow"
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py taught "guidance" --one-liner "the company's own forecast"
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py due     # concepts worth a refresher today
python3 .claude/skills/learning-tracker/scripts/concept_ledger.py list
```
Levels: **new** (never explained: full explanation), **learning** (explained before: one-line
reminder in brackets), **known** (seen on 5 or more days: no definition). Refreshers follow
spaced repetition: 2, 7, 21 and 60 days after a concept was taught.

## The curriculum: `learning/curriculum.md`

A path from basics to expert topics. Each day's Lesson of the day picks the next unchecked topic
that today's news makes concrete (a guidance cut is the perfect day to teach guidance). Tick it
when taught. If a "due" concept fits today's news, weave a two-sentence refresher into the report.

## Lessons archive: `learning/lessons/YYYY-MM-DD.md`

Each lesson is saved so Santi can reread them as a growing textbook. Format: title as a
question, explanation, worked example with his holdings, check-yourself question and answer.
