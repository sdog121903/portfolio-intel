# Free data endpoints used by the pipeline

| Data | Endpoint | Key? | Notes |
|---|---|---|---|
| Daily prices (1st choice) | `https://query1.finance.yahoo.com/v8/finance/chart/<T>?range=2y&interval=1d` | No | Unofficial; can rate-limit or change. Adjusted closes included |
| Daily prices (2nd) | `https://stooq.com/q/d/l/?s=<t>.us&i=d` | No | CSV; split-adjusted closes |
| Daily prices (3rd) | `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=<T>` | Yes (free) | Set `ALPHAVANTAGE_API_KEY` as an API credential; compact output is about 100 days |
| Ticker -> SEC CIK | `https://www.sec.gov/files/company_tickers.json` | No | Needs a User-Agent with an email |
| Filings list | `https://data.sec.gov/submissions/CIK##########.json` | No | Includes 8-K item numbers |
| Filing documents | `https://www.sec.gov/Archives/edgar/data/<cik>/<accession>/<doc>` | No | Form 4 raw XML parsed by `filings-decoder` |
| Reported financials | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` | No | Quarterly values; Q4 derived from the annual figure |

SEC asks automated users to identify themselves (name and email in the User-Agent) and to stay
under 10 requests per second; the scripts send the owner's name and email and pause between calls.

## Network allowlist for the cloud environment

The routine's environment must allow these hosts (Custom network access, plus the default
package-manager list):

```
query1.finance.yahoo.com
query2.finance.yahoo.com
stooq.com
www.alphavantage.co
www.sec.gov
data.sec.gov
```

Reading full news articles with a fetch tool needs their domains too. If the session log shows
many blocked fetches, either add the domains you need or switch the environment to Full access.
Connectors (Google Drive, Gmail) do not need allowlist entries.
