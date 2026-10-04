# Explanation patterns

Each pattern is the skeleton for one kind of event. Fill every line; if a line cannot be filled,
say what is missing and why ("Credo does not disclose sales by product").

---

## 1. "Why did my stock move?" (price move)

- **What happened:** "CRWD fell 6.2% today, while the S&P 500 rose 0.4%."
- **How much was the market, the industry, the company?** From `move_attribution.py`:
  "About 0.6 points came from the market, 1.1 from cybersecurity stocks falling, and 5.7 points
  were specific to CrowdStrike, an unusually large company-specific move (about 2.5 times its
  normal daily noise)."
- **The trigger:** the dated event that lines up with the move, cited. If none: say so.
- **Why that trigger matters:** the chain down to a basic driver (see why-analysis).
- **Profits or excitement?** Is the market changing its view of future profits, or just how much
  it is willing to pay for them (the multiple)? Use the earnings-vs-valuation split when possible.
- **How unusual is this?** Compare with its typical daily move (the ATR or volatility figure).
- **What would change the picture:** the next fact that would confirm or reverse the story.

## 2. Earnings result

- **Expected vs delivered:** revenue and earnings per share (EPS) vs the analysts' average
  forecast (the consensus), with the size of the beat or miss in %.
- **The forecast for next quarter (guidance)** vs what analysts expected. Explain that guidance
  usually matters more than the past quarter, because a stock price is a bet on the future.
- **The one or two numbers that matter most for this business** (sector-kpis.md), and why they
  matter: "Annual recurring revenue (ARR) is the yearly value of subscriptions; it shows sales
  that will repeat next year, which makes future revenue more predictable."
- **Quality of the beat:** was it from selling more, or from one-offs, a lower tax rate or fewer shares?
- **The market's reaction and why:** "The stock fell even though results beat, because the
  guidance was below what investors had hoped for: the price already assumed something better."
- **Plain-English summary:** one sentence a friend would understand.

## 3. Product or technology launch

Use the product-explainer skill. The written explanation always covers:
- **What it is**, in one sentence with an everyday analogy.
- **What problem it solves**, and for whom.
- **How it works**, one level deeper than the analogy.
- **Who pays for it and roughly what it costs** (cited, or "price not disclosed").
- **How much it sells or is expected to sell**: units, revenue, backlog or orders, with the source.
  If the company does not disclose it, say so, then give the best proxy (segment revenue,
  management comments, a cited industry estimate), clearly labelled as a proxy.
- **Stage:** announced, sampling to customers, shipping, or ramping in volume. Announcements are
  promises; shipments are revenue.
- **Why investors care:** how big it could be relative to the company's current revenue.
- **Competition:** who else sells something similar and how this one differs.

## 4. Guidance change

- What the company said it now expects (range), what it said before, what analysts expected.
- Why management changed it (their stated reason, cited) and whether that reason is believable.
- Explain: guidance is the company's own forecast; investors trust it because management sees
  orders before anyone else does.

## 5. Analyst rating or price-target change

- Who (firm), what changed (rating, target), the date, their stated reason.
- Explain that analysts are professionals giving opinions, often several disagree, and a change
  matters mostly when it brings new information (for example channel checks or a model change),
  not because of the rating itself.
- Context: how many analysts cover it and where most of them stand, if a reliable source has it.

## 6. Insider trade (Form 4) or planned sale (Form 144)

- Who traded (role), what (bought, sold, received, tax withholding), how many shares, at what
  price, and the dollar value relative to what they still own.
- Was it under a pre-planned 10b5-1 plan? Explain: executives often schedule sales months in
  advance to avoid accusations of trading on secret information, so planned sales usually say
  little. Open-market *purchases* with their own money are rarer and more informative.

## 7. Share sale or dilution (S-3, 424B prospectus, convertible notes)

- What is being sold, how much, at what price, and why the company says it needs the money.
- Explain dilution with the pizza analogy: the same pizza cut into more slices, so each existing
  slice is a smaller share, unless the new money grows the pizza.

## 8. Macro or policy event (interest rates, tariffs, export rules, AI spending)

- What changed, who announced it, when.
- The transmission chain to this company: "Higher interest rates -> future profits are worth less
  today -> fast-growing companies whose profits are far in the future fall more."
- Which of his holdings are more exposed and why (use macro-drivers.md).

## 9. Lesson of the day

- Title as a question ("Why can a stock fall after good news?").
- The idea in one sentence, then the explanation (120-250 words) using one of his holdings.
- A worked mini-example with simple numbers.
- One "check yourself" question, with the answer hidden at the end of the report.
