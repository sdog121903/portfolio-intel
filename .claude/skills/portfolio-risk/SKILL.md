---
name: portfolio-risk
description: Looks at the portfolio as a whole: position weights, how concentrated it is in one stock or one theme, how much the holdings move together, typical bad-day losses in dollars, and simple market and industry shock scenarios. Use for the "Your portfolio as a whole" section and whenever Santi asks how risky or diversified his portfolio is.
---

# Portfolio risk

Several stocks can behave like one if they all ride the same story. This section shows Santi how
much of his money depends on a single idea and what a normal bad day looks like, in dollars.

## Where the numbers come from

`scripts/portfolio_risk.py` (run by the pipeline) writes `data/metrics/portfolio-<DATE>.json`:
- **weights_pct**: each position's share of the portfolio value.
- **concentration**: the Herfindahl index and the "effective number of positions" (1 / sum of
  squared weights). Five equal positions = 5; one big position and four tiny ones is closer to 1-2.
- **theme_exposure_pct**: from `[themes]` in config; one stock can count in several themes.
- **correlation_60d**: how similarly each pair moved over about three months (1 = in lockstep).
- **volatility, value at risk (VaR) and expected shortfall**: from a year of daily returns at
  today's weights. "On 1 day in 20, the portfolio lost at least $X" is the plain version of 95% VaR.
- **beta_vs_market** and **shocks**: rough estimates of what a 5% or 10% market fall would mean.
- **sector_exposure_pct** and **goals_check**: how much of the money sits in technology and in the
  biggest theme, to compare with his own goals in `config/portfolio.toml` `[goals]`.

## Against his goals
Santi's stated goals are to diversify beyond tech, keep the portfolio reasonably safe, and still
hold some high movers. Each report states the facts against those goals in one or two plain
sentences: the technology share, the biggest theme's share, the volatility and a typical bad day,
and how many of his holdings are the fast-moving kind (high volatility or beta). Then stop.
Describe, never prescribe: no suggestions of what to buy or sell, no "you should diversify".

## How to write it
- Lead with the plain picture: "About $X of every $10 you have invested rides on AI data-center
  spending."
- Translate every statistic into dollars for his actual portfolio size.
- Say what correlation means for him: "when one of your AI stocks falls, the others usually fall too,
  so owning several of them spreads less risk than it looks".
- State the limits: estimates use the past year; correlations jump in sell-offs; scenarios are
  rough, not forecasts.
- Describe; never prescribe. No "you should diversify"; he can draw that conclusion himself.
