# News logs: how each stock reacted to its news

One page per stock (`<TICKER>.md`), rebuilt on every report run, newest first. Each page has:

- **What the log shows so far**: simple arithmetic over everything logged (average move beyond
  the market after good and after bad news, the biggest reactions, moves nobody explained).
  Under 20 items it says it is too early to draw conclusions.
- **News, newest first**: every fact-checked item from the reports, with its source and how the
  price reacted: the stock against the S&P 500 on the first trading day the news could affect,
  how big that was for this stock, and what happened over the next five days.
- **Price on each report day**: the day's move split into market, industry and company parts.

The record behind each page is `data/news-log/<TICKER>.json`; the pages are rebuilt from it by
`.claude/skills/news-and-events/scripts/news_log.py`, so edits made here by hand are lost.
Both are committed and pushed with each report.

Informational research and education, not investment advice.
