# Search playbook

Query patterns that reliably surface primary and top-tier sources. Replace <Company> with the
short common name (CrowdStrike, NVIDIA, Credo, Lumentum, Sterling Infrastructure) and <TICKER>.

## What happened in the window
- `<Company> news` with the search tool's recency filter if available; then add the date:
  `<Company> October 5 2026`.
- `<Company> press release`, `<Company> announces` (company newsroom, Business Wire, PR Newswire, GlobeNewswire).
- `<Company> site:reuters.com`, `<Company> Reuters`, `<Company> Bloomberg` for reporting.
- `why is <Company> stock down` / `up` only to find candidate explanations; confirm each against
  tier 1-2 before using it.

## Earnings
- `<Company> fourth quarter fiscal 2027 results` (use the company's fiscal naming).
- `<Company> earnings call transcript` (company IR site or a reputable transcript host).
- `<Company> earnings date` -> confirm on the company's investor-relations events page.
- Consensus: the earnings release coverage in tier 2 usually states "analysts expected ...".

## Products and customers
- `<Company> <product name> launch`, `<Company> <product> shipping`, `<Company> <product> customers`.
- Sales figures: the latest 10-Q or 10-K (business and segment sections), the earnings call
  transcript, the investor presentation. If not disclosed, say so.

## Analysts and investors
- `<Company> price target raised` / `cut`, `<Company> upgrade` / `downgrade` (tier 2/3; opinions).
- Insider trades: use `data/filings/<DATE>.json` (Form 4 parsed from SEC) rather than articles.

## Disconfirming evidence (always run at least two)
- `<Company> risk`, `<Company> lawsuit`, `<Company> investigation`, `<Company> delay`,
  `<Company> customer loss`, `<Company> short seller report`, `<Company> competition <competitor>`.

## Industry and macro (when relevant to a thesis)
- Customer spending: `Microsoft capex`, `Meta capital expenditures 2026`, `hyperscaler capex`.
- Policy: `chip export controls <month year>`, `tariffs semiconductors`, `Fed decision <month year>`.
