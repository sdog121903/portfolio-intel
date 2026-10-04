# Move attribution, explained for beginners

**The idea.** On any day, three things push a stock: the whole market (most stocks rise and
fall together), its industry (chip stocks often move together), and news about the company
itself. If we know how strongly the stock usually follows the market and its industry, we can
estimate how much of today's move those two explain. Whatever is left is about the company.

**How it is computed.** Over roughly the last 252 trading days the script fits

  stock return = alpha + b_m x market return + b_s x (industry return - market return) + residual

using the S&P 500 fund (SPY) as "the market" and the holding's industry fund from
`[sector_etf]` (SMH for chips, CIBR for cybersecurity, PAVE for infrastructure). For a given day:

- market part = b_m x market return
- industry part = b_s x (industry return - market return)
- company-specific part = actual return - market part - industry part
- z-score = company part / typical size of the daily residual

**Example.** CRWD falls 3.0% on a day the market falls 2.0%. With b_m = 1.3, the market part is
-2.6%. Cybersecurity stocks did the same as the market, so the industry part is about 0. The
company part is -0.4%, smaller than CRWD's normal daily noise (z about -0.4). Conclusion: "most of
today's fall was the market".

**Caveats to say out loud when they matter.**
- Betas drift; a year of data smooths over regime changes.
- The industry fund is a proxy. Lumentum is compared with a chip fund because no liquid
  optical-components fund exists.
- Big news days are part of the history and inflate the "normal noise".
- A small company part does not prove there was no news, only that the move did not need it.
