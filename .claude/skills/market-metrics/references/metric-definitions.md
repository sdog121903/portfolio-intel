# Metric definitions (formula, plain English, pitfalls)

| Metric | Formula (as computed) | Plain English | Pitfall |
|---|---|---|---|
| Daily return | close today / close yesterday - 1 | How much it moved today | Splits distort unadjusted prices; adjusted closes are used |
| 1w/1m/3m/6m/1y return | price now / price N calendar days ago - 1 (adjusted) | How it did over the period | One period says little; compare with the market |
| YTD return | price now / last close of last year - 1 | Since January 1 | Early in the year it is noise |
| 52-week high/low | max high / min low over 252 trading days | The year's range | A stock near its high is not "due" to fall |
| Position in range | (price - low) / (high - low) | 0% = at the low, 100% = at the high | Ignores how it got there |
| SMA 20/50/200 | average close of the last N days | The recent "normal" price | Lags; it describes, it does not predict |
| Trend state | uptrend: price > SMA50 > SMA200; downtrend: the reverse | Direction of the longer move | Mixed states are common and normal |
| RSI (14) | Wilder's average gain / average loss over 14 days, scaled 0-100 | Speed of recent moves | Strong stocks can stay above 70 for months |
| ATR (14) | Wilder average of daily true range (high-low incl. gaps) | A typical day's swing in dollars | Rises after big news days |
| Volatility (20d/60d) | stdev of daily returns x sqrt(252) | How bumpy, as a yearly % | Not the same as risk of permanent loss |
| Max drawdown (1y) | worst fall from a peak to a later low | The worst ride in the last year | Backward-looking |
| Relative volume | today's volume / average of the previous 20 days | Unusual interest when far above 1 | Index rebalancing days inflate it |
| Beta (1y) | cov(stock, market) / var(market), daily returns | Moves about beta% per 1% market move | Changes over time; low correlation makes it unreliable |
| Correlation (60d) | Pearson correlation of daily returns | How in-step with the market (-1 to 1) | Rises in sell-offs, when diversification is needed most |
| Excess return | stock return - benchmark return, same window | Better or worse than the market / industry | Benchmark choice matters (`[sector_etf]`) |
| P&L | sign x (value - invested) - fees | Money made or lost since buying | Uses the estimated entry when no fill price is entered |
| Drawdown since entry | price / highest close since buying - 1 | How far below the best point since you bought | Feeds the optional trailing rule |

Plain-English templates:
- "NVDA is in an uptrend: above its 50-day ($X) and 200-day ($Y) averages."
- "LITE has risen fast (RSI 78). That describes the past few weeks; it does not mean it must fall."
- "CRWD's beta is 1.3: when the market moves 1%, CRWD has tended to move about 1.3%."
