# Portfolio report: <DATE>

*Prices as of the <LAST CLOSE DATE> close (US Eastern). News window: <WINDOW>.*
<!-- If holdings came from the fallback file, put a WARNING line here. -->

## The bottom line

- <One sentence per point, conclusion first: the biggest thing that happened, why, and whether it matters.>
- <Portfolio change today in $ and %, and the main driver.>
- <Any RETREAT, TARGET or THESIS ALERT, or "No rule fired and no thesis alert today.">

## Your rules today

*These are your own rules from `config/rules.toml` and your sheet. The report shows which fired and
the evidence both ways, never a buy or sell call: the decision, and the knowledge of your whole
situation, are yours.*

| Stock | Status | Why |
|---|---|---|
| <TICKER> | <No rule fired / WATCH / RETREAT RULE HIT / TARGET REACHED / THESIS ALERT> | <one plain sentence with the numbers> |

## Position: <TICKER> (<Company name>)

**Bottom line:** <the move, its main cause, and the thesis status, in one or two sentences>

**Where it stands** <shares> shares, entry $<entry> (<source of entry price>), now $<price>,
worth $<value>, <+/-$P&L (+/-x.x%)> since you bought; today <+/-x.x%>.
<One plain sentence on trend and how unusual today's move was.>

**What happened, and why**
*Market vs company:* <from attribution-<DATE>.json: "Of today's -3.1%, about -2.7 points came from the market, ~0 from the industry, -0.4 from the company itself (normal size).">
- <Event in one sentence, then why it matters in one sentence.> [<Source>, <YYYY-MM-DD>](<url>)
- <If nothing material: "No material news in the window; the move matches the market.">

**How this works** <The mechanism or product behind today's news, in everyday words, then one
step more precise. Include how much it sells, or say it is not disclosed.>

**Case to stay**
1. <strongest sourced point>
2. <...>
3. <...>

**Case to retreat**
1. <strongest sourced point>
2. <...>
3. <...>

**Thesis check** <Intact / Watch / Challenged / Broken> - <why, referring to theses/<TICKER>.md>.

**Coming up** <next dated event: earnings date (confirmed or estimated), product launch, conference>.

## Your portfolio as a whole

<Total invested, value, P&L. Biggest weights. Theme concentration in plain words ("about $X of
every $10 rides on AI data-center spending"). How much the holdings move together. A typical
bad day in dollars. What a 5% market drop or 10% industry drop would roughly mean.>

**Against your goals** <from goals_check: "You want to diversify beyond tech; today X% of your
money is in technology companies and Y% rides on AI data centers. Volatility: ... High movers: ...".
Use portfolio_volatility_ann_pct, portfolio_beta_vs_market and high_movers_beta_1_5_plus; name
any unclassified_tickers as not yet set up in config/portfolio.toml. Facts only, no suggestions.>

**Next 14 days:** <calendar of earnings dates and events>

## Lesson of the day

**<Question as title>**
<120-250 words using one of his holdings, a worked mini-example, then:>
*Check yourself:* <one question>. (Answer at the end.)

## New words today

- **<Term>**: <plain one-line definition, with an everyday comparison if it helps>.

## Data quality and sources

- <What worked, what failed (from the pipeline status), which figures are estimates.>
- Prices: <provider>. Filings: SEC EDGAR. Fundamentals: SEC XBRL company facts.
- *Answer to "check yourself":* <answer>.

Informational research and education, not investment advice. The decisions are yours.
