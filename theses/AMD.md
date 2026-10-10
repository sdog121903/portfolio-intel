# AMD: Advanced Micro Devices

**Last deep dive:** never  |  **Sector playbook:** semiconductors  |  **Industry fund:** SMH

**Thesis approved:** 2026-10-05 (justification prefilled by Claude from the 2026-10-04 research; approved by Santi)  |  **News and events:** [`theses/news/AMD.md`](news/AMD.md): every report's news, the upcoming calendar and how the price reacted, newest first.

## Why I own it (approved by Santi, 2026-10-05)

**In one sentence:** I hold AMD because it is the main alternative to NVIDIA for AI chips, and the biggest AI labs are signing multi-year deals with it.

AI labs and cloud companies do not want to depend on a single chip supplier, and AMD is the main alternative to NVIDIA for the graphics processors (GPUs) that train and run AI. That is now visible in contracts: OpenAI agreed to 6 gigawatts of AMD GPUs in 2025, and Anthropic up to 2 gigawatts in 2026 (Anthropic makes Claude, which wrote this file) [CNBC, 2026-07-22; research file], and data-center revenue more than doubled to $6.7bn last quarter (+107%) [AMD Q2 2026 results, 2026-08-04]. AMD is also moving from selling single chips to selling complete AI server racks (Helios), which are worth much more per customer, and it still sells the CPUs (general-purpose processors) that every server needs.

**What I accept (the risks):** the stock is up 191% in six months and about 69% above its 200-day average, so expectations are high; it fell 7% after a strong report in August; AMD has pledged up to $5bn of investment in Anthropic, one of its own customers; Helios only starts ramping in late 2026; and paying for World Labs in shares adds about 0.8% more shares.

### The numbers behind it

<!-- numbers:start (rebuilt by thesis_tools.py from data as of 2026-10-09; edits inside this block are lost) -->

**The business, last five quarters** (SEC filings via `data/fundamentals/`; Q4 figures marked * are the annual total minus the three other quarters)

| Quarter (period end) | Revenue | vs a year earlier | Gross margin | Operating margin | Net income |
|---|---|---|---|---|---|
| 2026 Q2 (2026-06-27) | $11.54bn | +50.1% | 53.8% | 17.2% | $2.30bn |
| 2026 Q1 (2026-03-28) | $10.25bn | +37.9% | 52.8% | 14.4% | $1.38bn |
| 2025 Q4* (2025-12-27) | $10.27bn | +34.1% | 54.3% | 17.1% | $1.51bn |
| 2025 Q3 (2025-09-27) | $9.25bn | +35.6% | 51.7% | 13.7% | $1.24bn |
| 2025 Q2 (2025-06-28) | $7.68bn | +31.7% | 39.8% | -1.7% | $872.0m |

*What the trend says:*
- Revenue: $11.54bn in the latest quarter, +50.1% from a year earlier; it has grown 1 quarter in a row. Growth is speeding up (from +35.6% to +50.1% over the last four quarters).
- Gross margin (share of each sale left after making the product): rising (51.7% to 53.8%, +2.1 points) over the last four quarters.
- Operating margin (share left after all running costs): rising (13.7% to 17.2%, +3.5 points).
- Profit: positive net income in 4 of the last 4 quarters.

**The stock** (to 2026-10-09, `data/metrics/`)

| 1 month | 3 months | 6 months | 1 year | vs its 200-day average | Worst fall in the past year | Typical day |
|---|---|---|---|---|---|---|
| +16.7% | +9.0% | +148.2% | +161.1% | +57.8% | -27.8% | 3.9% |

*Price trend:* uptrend (price above its 50- and 200-day averages, and the 50 is above the 200). (The 200-day average is the average closing price over about the last ten months; trading above it usually means a longer uptrend.)

<!-- numbers:end -->

**Key trends from company reports** (sourced; refreshed when new results come out)

- Data-center revenue $6.7bn, +107%; total $11.5bn, +50%; Q3 guided about $13.0bn, +41% [AMD Q2 2026 results]
- Stock up 191% in six months; about 69% above its 200-day average (data/metrics)

### Thesis 1: "AMD is the main alternative to NVIDIA for AI chips, and big AI labs are signing multi-year deals with it."

1. **Why would I own it for this?** Data-center revenue more than doubled (+107%) to $6.7bn [AMD Q2 2026 results]; OpenAI (6 gigawatts, 2025) and Anthropic (2 gigawatts, 2026) signed multi-year deals [CNBC, 2026-07-22; research file].
2. **What must stay true?** Data-center revenue keeps growing, and the big AI deals are delivered on schedule. *(pillars 1, 2 and 3 below)*
3. **What would prove me wrong?** Any one of these *(triggers 1 and 2 below)*:
   - Data-center revenue shrinks for two quarters in a row.
   - A big AI customer cuts or cancels its deal.

### Thesis 2: "AMD is moving from selling single chips to selling complete AI systems (Helios racks), which are worth much more per customer."

1. **Why would I own it for this?** Helios racks (complete cabinets of AI servers) start ramping in late 2026, and the Q2 release lists customers including Anthropic, Meta, Microsoft, OpenAI and Oracle (research file).
2. **What must stay true?** Helios ships on time and shows up as a clear jump in data-center revenue in 2027. *(pillar 4 below)*
3. **What would prove me wrong?** Any one of these *(triggers 3 and 4 below)*:
   - Helios is delayed.
   - Customers order AMD chips but not complete racks.

## What the company does (plain English, 3 sentences)
AMD designs processors: CPUs, the general-purpose "brains" of computers, and GPUs, chips that do many small calculations at once, which is what AI needs. It does not make chips itself; TSMC manufactures them. Data-center revenue was $6.7 billion last quarter, up 107%, because AI companies are buying its GPUs under large multi-year deals [AMD Q2 2026 results, 2026-08-04].

## How it makes money
Chip sales grouped into segments such as data center, PCs, gaming and embedded chips. The deep
dive will add each segment's share of revenue, with sources.

## Metrics that matter
- Data center segment revenue and its growth
- AI accelerator (data-center GPU) sales, or 'not disclosed'
- Gross margin
- Server CPU market share, from a named source
- Guidance for the next quarter

## What must stay true (checkable pillars)
Each pillar says why it matters, how it is measured, where it stands now and when it is next checked. The daily report tests every one; when a "Now" line changes, the change log records it.

1. **Data-center revenue keeps growing.** *(Thesis 1)*
   - *Why it matters:* Data center is where the AI chips are sold; its growth is the AI case in one number.
   - *Measured by:* Data-center segment revenue against a year earlier, every quarter.
   - *Now (as of 2026-10-04):* $6.7bn, +107% [AMD Q2 2026 results].
   - *Next check:* Q3 results, about 2026-11-03 (estimated).
2. **Revenue meets guidance.** *(Thesis 1)*
   - *Why it matters:* Guidance of about $13.0bn (+41%) is AMD's own view of near-term demand.
   - *Measured by:* Quarterly revenue against guidance.
   - *Now (as of 2026-10-04):* Q2 $11.5bn (+50%); Q3 guided about $13.0bn [AMD Q2 2026 results].
   - *Next check:* About 2026-11-03.
3. **The big AI deals are delivered on schedule.** *(Thesis 1)*
   - *Why it matters:* Multi-year deals only count when chips ship and customers deploy them.
   - *Measured by:* Company and customer updates on deployments (Anthropic: first gigawatt from H1 2027).
   - *Now (as of 2026-10-04):* OpenAI 6 GW (2025); Anthropic up to 2 GW, first GW from H1 2027 (research file).
   - *Next check:* Earnings calls; news in daily reports.
4. **Helios racks ship on time.** *(Thesis 2)*
   - *Why it matters:* Selling whole racks raises how much AMD earns per customer.
   - *Measured by:* Management updates on Helios timing and first revenue.
   - *Now (as of 2026-10-04):* Ramping from late 2026; customers include Anthropic, Meta, Microsoft, OpenAI and Oracle (research file).
   - *Next check:* OCP keynote 2026-10-12; Q3 results.
5. **Dilution and investments in customers stay small.** *(whole position; added 2026-10-05)*
   - *Why it matters:* Paying in shares and investing in customers can quietly reduce what each share earns.
   - *Measured by:* Share count in each 10-Q; size of investments in customers.
   - *Now (as of 2026-10-09):* World Labs adds about 0.8% more shares; up to $5bn pledged to Anthropic (research file). Also, from the 10-Q: warrants for OpenAI and Meta could add up to 320 million shares (about 19.6%) if all milestones are met; none vested as of 2026-06-27 [AMD 10-Q, 2026-08-05](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm).
   - *Next check:* Next 10-Q.

## Invalidation triggers (what would prove the thesis wrong)
Each trigger says why it matters, exactly what counts, the early warning that usually comes first, where to look and its status now. A trigger that fires becomes a THESIS ALERT in the daily report: a reason to re-read this file, not an instruction to sell. An early warning is reported as "Watch".

1. **Data-center revenue shrinks for two quarters in a row.** *(Thesis 1)*
   - *Why it matters:* It would mean AMD is losing ground or AI spending is slowing.
   - *Counts if:* Data-center revenue below the previous quarter's, two quarters in a row.
   - *Early warning:* One quarter below the previous one.
   - *Where and when to check:* Quarterly results; next about 2026-11-03.
   - *Status now (2026-10-04):* Not hit.
2. **A big AI customer cuts or cancels its deal.** *(Thesis 1)*
   - *Why it matters:* The multi-year deals are the proof AMD is a real alternative to NVIDIA.
   - *Counts if:* OpenAI, Anthropic or another large customer cuts, delays or cancels its commitment (company or tier-1/2 source).
   - *Early warning:* Reports that a big customer is shifting back to NVIDIA or to its own chips.
   - *Where and when to check:* News in every daily report.
   - *Status now (2026-10-04):* Not hit.
3. **Helios is delayed.** *(Thesis 2)*
   - *Why it matters:* Racks are the step-up in value per customer; a delay pushes that revenue out.
   - *Counts if:* AMD moves the Helios ramp beyond its stated timing.
   - *Early warning:* Reports of supply or engineering problems with the racks.
   - *Where and when to check:* OCP keynote 2026-10-12; earnings calls.
   - *Status now (2026-10-04):* Not hit.
4. **Customers order AMD chips but not complete racks.** *(Thesis 2)*
   - *Why it matters:* Then the systems part of my reason did not work.
   - *Counts if:* By the end of 2027 management reports no meaningful rack revenue, or says customers prefer chips only.
   - *Early warning:* Few new Helios customers announced after the first ones.
   - *Where and when to check:* Earnings calls.
   - *Status now (2026-10-09):* Not hit. Note: AMD's 10-Q says it does not sell completed Helios racks, so "no meaningful rack revenue" cannot be tested as written (see Proposed below).
5. **Revenue misses company guidance.** *(whole position; added 2026-10-05)*
   - *Why it matters:* With expectations high after a 191% rise, a miss would show demand is not keeping up with the story.
   - *Counts if:* Quarterly revenue below the guided range.
   - *Early warning:* Next-quarter guidance below what analysts expected.
   - *Where and when to check:* Quarterly results.
   - *Status now (2026-10-04):* Not hit.

## Facts as of 2026-10-09 (every figure sourced)
- AMD's 10-Q: AMD does "not manufacture or sell the completed Helios rack systems"; it licenses the design and supplies components [AMD 10-Q, 2026-08-05](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm)
- Warrants to OpenAI and Meta for up to 320 million AMD shares at $0.01, vesting in tranches tied to purchase and share-price milestones; none vested as of 2026-06-27; about 19.6% of 1.632bn shares if all were issued (our calculation) [AMD 10-Q, 2026-08-05](https://www.sec.gov/Archives/edgar/data/2488/000000248826000123/amd-20260627.htm)
- Stock −3.90% (10-08) and −2.03% (10-09), almost all chip-sector moves after a Financial Times report that OpenAI's revenue pace was about $50bn, not $70bn (data/metrics; [TechCrunch, 2026-10-08](https://techcrunch.com/2026/10/08/openais-revenue-is-reportedly-20-billion-less-than-previously-projected/))
- Lisa Su OCP keynote 2026-10-12, 4:15 p.m. Pacific [AMD media alert (page as read), 2026-10-09](https://newsroom.amd.com/news/media-alert-ceo-lisa-su-keynote-2026-ocp/)
- Q2 2026 revenue $11.5bn (+50%); data center $6.7bn (+107%); Q3 guidance about $13.0bn (+41%) [AMD Q2 2026 results, 2026-08-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000121/q22026991.htm)
- Anthropic: up to 2 GW of AMD GPUs in Helios racks, first GW from H1 2027; AMD to invest up to $5bn in Anthropic [CNBC, 2026-07-22](https://www.cnbc.com/2026/07/22/amd-anthropic-ai-chip-investment.html)
- World Labs purchase for about $8.2bn in AMD shares (about 0.8% dilution, researcher's calculation) [SEC 8-K, 2026-09-28](https://www.sec.gov/Archives/edgar/data/2488/000000248826000182/amd-20260926.htm)
- CEO Lisa Su sold about $48.1m on 2026-09-10 under a pre-planned 10b5-1 plan [SEC Form 4](https://www.sec.gov/Archives/edgar/data/2488/000000248826000178/)
- Record close $633.91 on 2026-10-02; up 191% in six months; about 69% above its 200-day average (data/metrics)
- Q3 results 2026-11-03 after the close (confirmed) [AMD, 2026-10-06](https://ir.amd.com/news-events/press-releases/detail/1300/amd-to-report-fiscal-third-quarter-2026-financial-results)
- CEO Lisa Su (Taipei, 2026-10-06): demand exceeds supply; AMD will 'substantially increase our supply in 2027' and plans capacity three to five years ahead [Taipei Times, 2026-10-07](https://www.taipeitimes.com/News/biz/archives/2026/10/07/2003865507)
- Record close $649.42 on 2026-10-06; $645.86 on 2026-10-07 (data/metrics)

## Change log
- 2026-10-04: Created when the holding appeared in the FIDELITY sheet.
- 2026-10-05: Added the draft thesis (up to three statements, each with why / what must stay true / what would prove it wrong), the 3-sentence company summary, the recent-news table and the link to the news log. Replaced the earlier starting points in "What must stay true" and "Invalidation triggers" with items from the draft, marked "(Proposed)". "Why I own it" untouched.
- 2026-10-05: Santi approved the theses. "Why I own it" filled with the justification (one-sentence reason, the case, what I accept), a numbers block (SEC quarterly trend and price trend, rebuilt each run) and key trends; the news and upcoming-events tables now live only in the news log. Pillars and triggers strengthened: each has why it matters, how it is measured (or exactly what counts), an early warning, where and when to check, and its status. All approved triggers kept; new ones are marked "added 2026-10-05". Facts as of 2026-10-04 filled.
- 2026-10-07 (daily report): Facts updated (results date confirmed; CEO supply comments). No trigger status changed. No change to the reasons, pillars or triggers.
- 2026-10-09 (daily report, covering Thu 10-08 and Fri 10-09): Facts updated (10-Q: Helios racks not sold by AMD; OpenAI/Meta warrants). Pillar 5 'Now' and trigger 4 status refreshed. Proposed (waiting for Santi's approval, nothing changed): (1) re-word Thesis 2 ("selling complete AI systems") to match the 10-Q (AMD licenses the Helios design and sells the chips); (2) re-word trigger 4 so it can be tested (for example, Helios-related data-center revenue or customer count); (3) add the warrants to pillar 5's measure.
