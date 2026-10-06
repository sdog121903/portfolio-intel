# Theses: why you own each stock

One file per holding. The daily report checks each day's news against it; the weekly deep dive
rebuilds the facts from primary documents. The theses for the 16 stocks in the sheet were
approved by Santi on 2026-10-05.

- **Why I own it**: the reason in one sentence, the case with its evidence, what you accept,
  "The numbers behind it" (SEC quarterly trend and price trend, rebuilt on every run by
  `.claude/skills/position-review/scripts/thesis_tools.py`), sourced key trends, and up to three
  theses, each answering *why would I own it for this?*, *what must stay true?* and *what would
  prove me wrong?*. The routine never rewrites your approved reasons; it proposes changes.
- **What must stay true** (pillars) and **Invalidation triggers**: each says why it matters,
  exactly how it is measured or what counts, an early warning, where and when to check, and its
  status now. The routine updates the "Now" and "Status now" lines as facts change.
- **Facts as of** and **Change log**: kept current by every run that brings material news, and
  rebuilt by the weekly deep dive. `thesis_tools.py check` flags any file that falls behind.
- **News and events** live only in `theses/news/<TICKER>.md`: past news with the price reaction,
  and the upcoming calendar (see `theses/news/README.md`).

Copy `TEMPLATE.md` when you add a new stock.
