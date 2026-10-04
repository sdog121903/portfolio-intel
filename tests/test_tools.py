"""Offline tests for the toolbox. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
SK = ROOT / ".claude" / "skills"
sys.path.insert(0, str(ROOT / "scripts"))


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fp = load(SK / "market-metrics/scripts/fetch_prices.py", "fetch_prices")
mm = load(SK / "market-metrics/scripts/market_metrics.py", "market_metrics")
ma = load(SK / "why-analysis/scripts/move_attribution.py", "move_attribution")
ed = load(SK / "filings-decoder/scripts/fetch_edgar.py", "fetch_edgar")
ff = load(SK / "earnings-analysis/scripts/fetch_fundamentals.py", "fetch_fundamentals")
cr = load(SK / "position-review/scripts/check_rules.py", "check_rules")
pr = load(SK / "portfolio-risk/scripts/portfolio_risk.py", "portfolio_risk")
cl = load(SK / "learning-tracker/scripts/concept_ledger.py", "concept_ledger")
lr = load(SK / "portfolio-daily-report/scripts/lint_report.py", "lint_report")
re_ = load(SK / "portfolio-daily-report/scripts/render_email.py", "render_email")
lh = load(SK / "portfolio-daily-report/scripts/load_holdings.py", "load_holdings")


class TestPriceParsers(unittest.TestCase):
    def test_yahoo_skips_null_rows(self):
        rows = fp.parse_yahoo_chart((FIX / "yahoo_chart.json").read_bytes())
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[-1]["close"], 270.04)
        self.assertEqual(rows[-1]["adj_close"], 270.04)

    def test_nasdaq_dates_dollars_and_order(self):
        rows = fp.parse_nasdaq((FIX / "nasdaq.json").read_bytes())
        self.assertEqual([r["date"] for r in rows], ["2026-10-01", "2026-10-02"])  # N/A row dropped
        self.assertAlmostEqual(rows[-1]["close"], 233.95)
        self.assertAlmostEqual(rows[-1]["volume"], 162e6)

    def test_alphavantage_sorted(self):
        rows = fp.parse_alphavantage((FIX / "alphavantage.json").read_bytes())
        self.assertEqual([r["date"] for r in rows], ["2026-10-01", "2026-10-02"])

    def test_nasdaq_unknown_symbol(self):
        with self.assertRaises(ValueError):
            fp.parse_nasdaq(b'{"data":null,"status":{"rCode":400,"bCodeMessage":[{"errorMessage":"Symbol not exists."}]}}')


class TestEdgar(unittest.TestCase):
    def setUp(self):
        self.subs = json.loads((FIX / "submissions.json").read_text())

    def test_recent_filings_and_items(self):
        f = ed.recent_filings(self.subs, "2026-09-20", 1633917)
        self.assertEqual([x["form"] for x in f], ["4", "8-K", "144"])
        eightk = f[1]
        self.assertEqual(eightk["materiality"], "high")
        self.assertEqual(eightk["items"][0]["item"], "5.02")
        self.assertIn("officer", eightk["items"][0]["meaning"])
        self.assertTrue(eightk["url"].startswith("https://www.sec.gov/Archives/edgar/data/1633917/000163391726000099/"))

    def test_form4_url_and_parse(self):
        url = ed.form4_xml_url("https://www.sec.gov/Archives/edgar/data/1/0001/xslF345X05/wk-form4.xml")
        self.assertEqual(url, "https://www.sec.gov/Archives/edgar/data/1/0001/wk-form4.xml")
        p = ed.parse_form4((FIX / "form4.xml").read_bytes())
        self.assertEqual(p["owner"], "Example Officer")
        self.assertIn("officer", p["roles"])
        self.assertFalse(p["under_10b5_1_plan"])
        sale = p["transactions"][0]
        self.assertEqual(sale["code"], "S")
        self.assertAlmostEqual(sale["value_usd"], 1048500.0)
        s = ed.summarise_insiders([p])
        self.assertEqual(s["open_market_sells"], 1)
        self.assertEqual(s["sellers_not_under_10b5_1_plan"], ["Example Officer"])


class TestEdgarExtras(unittest.TestCase):
    def test_foreign_filer_forms_are_decoded(self):
        for form in ("6-K", "20-F", "40-F"):
            self.assertIn(form, ed.FORMS)

    def test_not_pursuant_to_a_plan_is_not_a_plan(self):
        xml = (FIX / "form4.xml").read_bytes()
        neg = xml.replace(b"</ownershipDocument>", b"<footnotes><footnote id='F9'>These sales were not made pursuant "
                                                    b"to a Rule 10b5-1 trading plan.</footnote></footnotes></ownershipDocument>")
        pos = xml.replace(b"</ownershipDocument>", b"<footnotes><footnote id='F9'>Sold under a Rule 10b5-1 trading "
                                                    b"plan adopted in May.</footnote></footnotes></ownershipDocument>")
        self.assertFalse(ed.parse_form4(neg)["under_10b5_1_plan"])
        self.assertTrue(ed.parse_form4(pos)["under_10b5_1_plan"])
        # an unrelated "not" in another footnote must not cancel a real plan
        mixed = xml.replace(b"</ownershipDocument>", b"<footnotes><footnote id='F8'>Includes units that have not yet "
                                                      b"vested</footnote><footnote id='F9'>Sold pursuant to a Rule 10b5-1 "
                                                      b"trading plan.</footnote></footnotes></ownershipDocument>")
        self.assertTrue(ed.parse_form4(mixed)["under_10b5_1_plan"])
        outside = xml.replace(b"</ownershipDocument>", b"<footnotes><footnote id='F9'>Sold outside of any Rule 10b5-1 "
                                                       b"plan.</footnote></footnotes></ownershipDocument>")
        self.assertFalse(ed.parse_form4(outside)["under_10b5_1_plan"])

    def test_failed_ticker_fails_the_step(self):
        """The pipeline marks a step failed only from its exit code, so SEC failures must not exit 0."""
        import pilib
        tmp = Path(tempfile.mkdtemp())
        old_data, old_get = pilib.DATA, pilib.http_get
        try:
            pilib.DATA = tmp
            pilib.write_json(tmp / "filings" / "company_tickers.json",
                             {"0": {"cik_str": 2488, "ticker": "AMD", "title": "Advanced Micro Devices"}})

            def blocked(*a, **k):
                raise RuntimeError("GET failed: HTTP Error 403: Forbidden")
            pilib.http_get = blocked
            self.assertEqual(ed.main(["--date", "2026-10-04", "--tickers", "AMD"]), 1)
            self.assertIn("error", json.loads((tmp / "filings" / "2026-10-04.json").read_text())["tickers"]["AMD"])
        finally:
            pilib.DATA, pilib.http_get = old_data, old_get
            shutil.rmtree(tmp, ignore_errors=True)


class TestSecrets(unittest.TestCase):
    def test_api_keys_are_redacted_from_errors(self):
        import pilib
        msg = pilib.redact("GET failed for https://www.alphavantage.co/query?symbol=SPY&apikey=SECRET123&x=1: 429")
        self.assertNotIn("SECRET123", msg)
        self.assertIn("apikey=REDACTED&x=1", msg)


class TestFundamentals(unittest.TestCase):
    def test_build_derives_q4_and_growth(self):
        out = ff.build(json.loads((FIX / "companyfacts.json").read_text()))
        qs = {q["period_end"]: q for q in out["latest_quarters"]}
        q4 = qs["2025-12-31"]
        self.assertAlmostEqual(q4["revenue"], 130e6)
        self.assertTrue(q4["source"]["derived"])
        self.assertAlmostEqual(qs["2026-03-31"]["revenue"], 151e6)  # later-filed restatement wins
        self.assertAlmostEqual(qs["2026-03-31"]["revenue_yoy_pct"], 51.0)
        self.assertAlmostEqual(qs["2026-06-30"]["revenue_yoy_pct"], 50.0)
        self.assertAlmostEqual(qs["2026-06-30"]["gross_margin_pct"], 62.0)
        self.assertAlmostEqual(out["ttm"]["revenue"], 566e6)
        self.assertAlmostEqual(out["ttm"]["eps_diluted"], 5.65)

    def test_most_recent_tag_wins(self):
        """A company that switched revenue tags must not report the abandoned tag's old quarters."""
        old = [{"start": "2019-10-28", "end": "2020-01-26", "val": 3.1e9, "form": "10-K", "filed": "2020-02-20"}]
        new = [{"start": "2026-05-01", "end": "2026-07-31", "val": 4.0e10, "form": "10-Q", "filed": "2026-08-27"}]
        facts = {"facts": {"us-gaap": {
            "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": old}},
            "Revenues": {"units": {"USD": new}}}}}
        tag, entries = ff.pick_series(facts, "revenue")
        self.assertIn("Revenues", tag)
        self.assertEqual(ff.quarterly(entries)[-1]["end"], "2026-07-31")

    def test_quarters_and_annual_split_across_tags(self):
        """LITE files its quarters under one tag and the annual total under both; Q4 must still be derived."""
        def e(start, end, val, form):
            return {"start": start, "end": end, "val": val, "form": form, "filed": "2026-08-17", "fy": 2026}
        annual = e("2025-06-29", "2026-06-27", 1000.0, "10-K")
        facts = {"facts": {"us-gaap": {
            "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [annual]}},
            "RevenueFromContractWithCustomerIncludingAssessedTax": {"units": {"USD": [
                e("2025-06-29", "2025-09-27", 200.0, "10-Q"), e("2025-09-28", "2025-12-27", 250.0, "10-Q"),
                e("2025-12-28", "2026-03-28", 260.0, "10-Q"), annual]}}}}}
        q = ff.quarterly(ff.pick_series(facts, "revenue")[1])
        self.assertEqual(q[-1]["end"], "2026-06-27")
        self.assertAlmostEqual(q[-1]["value"], 290.0)
        self.assertTrue(q[-1]["derived"])

    def test_staleness_warning(self):
        out = {"latest_quarters": [{"period_end": "2026-03-31"}]}
        self.assertIn("2026-03-31", ff.staleness(out, "2026-10-04"))
        self.assertIsNone(ff.staleness({"latest_quarters": [{"period_end": "2026-06-30"}]}, "2026-10-04"))

    def test_total_revenue_preferred_and_labels_from_first_filing(self):
        def e(tag_val, end, fy, fp, filed, form="10-Q", start=None):
            return {"start": start, "end": end, "val": tag_val, "fy": fy, "fp": fp, "filed": filed, "form": form}
        facts = {"facts": {"us-gaap": {
            "Revenues": {"units": {"USD": [
                e(751.0, "2026-03-31", 2026, "Q1", "2026-04-29", start="2026-01-01"),
                e(322.0, "2025-03-31", 2025, "Q1", "2025-04-30", start="2025-01-01"),
                e(322.0, "2025-03-31", 2026, "Q1", "2026-04-29", start="2025-01-01")]}},   # comparative, newer fy
            "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [
                e(746.0, "2026-03-31", 2026, "Q1", "2026-04-29", start="2026-01-01")]}},
            "NetIncomeLoss": {"units": {"USD": [e(-10.0, "2026-03-31", 2026, "Q1", "2026-04-29", start="2026-01-01")]}},
            "ProfitLoss": {"units": {"USD": [e(-12.0, "2026-03-31", 2026, "Q1", "2026-04-29", start="2026-01-01"),
                                             e(-30.0, "2025-03-31", 2025, "Q1", "2025-04-30", start="2025-01-01")]}}}}}
        out = ff.build(facts)
        qs = {q["period_end"]: q for q in out["latest_quarters"]}
        self.assertEqual(qs["2026-03-31"]["revenue"], 751.0)            # total, not contract-only
        self.assertEqual(qs["2025-03-31"]["fiscal"], "2025 Q1")          # not the comparative's 2026
        self.assertEqual(out["tags_used"]["net_income"], "NetIncomeLoss")
        self.assertEqual(qs["2026-03-31"]["net_income"], -10.0)
        self.assertIsNone(qs["2025-03-31"]["net_income"])                # ProfitLoss not mixed in

    def test_derived_q4_eps_is_not_shown(self):
        out = ff.build(json.loads((FIX / "companyfacts.json").read_text()))
        q4 = {q["period_end"]: q for q in out["latest_quarters"]}["2025-12-31"]
        self.assertTrue(q4["eps_derived"])
        self.assertIsNone(q4["eps_diluted"])
        self.assertAlmostEqual(out["ttm"]["eps_diluted"], 5.65)  # TTM still uses the derived value

    def test_ifrs_filer_is_explained(self):
        out = ff.build({"entityName": "Foreign Co", "facts": {"ifrs-full": {"Revenue": {}}}})
        self.assertEqual(out["latest_quarters"], [])
        self.assertIn("IFRS", out["notes"][0])


class TestMetrics(unittest.TestCase):
    def test_rsi_extremes(self):
        self.assertEqual(mm.rsi_wilder([float(i) for i in range(1, 40)]), 100.0)
        alt = [100 + (1 if i % 2 else -1) for i in range(60)]
        self.assertAlmostEqual(mm.rsi_wilder(alt), 50.0, delta=6)

    def test_drawdown_and_sma(self):
        self.assertAlmostEqual(mm.max_drawdown([100, 120, 90, 95]), -25.0)
        self.assertEqual(mm.sma([1, 2, 3, 4], 2), 3.5)
        self.assertIsNone(mm.sma([1, 2], 3))

    def test_atr_constant_range(self):
        rows = [{"high": 11.0, "low": 9.0, "close": 10.0} for _ in range(30)]
        self.assertAlmostEqual(mm.atr_wilder(rows), 2.0)

    def test_trend_states(self):
        self.assertTrue(mm.trend_state(110, 100, 90).startswith("uptrend"))
        self.assertTrue(mm.trend_state(80, 90, 100).startswith("downtrend"))


def synthetic(n=300, seed=7, beta_m=1.5, beta_s=0.5):
    rng = random.Random(seed)
    dates, m, s, st = [], [100.0], [100.0], [100.0]
    import datetime as dt
    d = dt.date(2025, 6, 2)
    while len(dates) < n:
        if d.weekday() < 5:
            dates.append(d.isoformat())
        d += dt.timedelta(days=1)
    for _ in range(n - 1):
        rm = rng.gauss(0.0005, 0.01)
        rs = rm + rng.gauss(0, 0.008)
        rstock = beta_m * rm + beta_s * (rs - rm) + rng.gauss(0, 0.004)
        m.append(m[-1] * (1 + rm)); s.append(s[-1] * (1 + rs)); st.append(st[-1] * (1 + rstock))
    mk = lambda xs: [{"date": d_, "open": x, "high": x * 1.01, "low": x * 0.99, "close": x, "adj_close": x, "volume": 1e6}
                     for d_, x in zip(dates, xs)]
    return mk(st), mk(m), mk(s)


class TestAttribution(unittest.TestCase):
    def test_fit_recovers_betas_and_parts_add_up(self):
        stock, market, sector = synthetic()
        obs = ma.aligned(stock, market, sector)
        alpha, bm, bs, sd = ma.fit_two_factor(obs)
        self.assertAlmostEqual(bm, 1.5, delta=0.1)
        self.assertAlmostEqual(bs, 0.5, delta=0.1)
        a = ma.attribute(obs[-5:], (alpha, bm, bs, sd))
        self.assertAlmostEqual(a["market_part_pct"] + a["industry_part_pct"] + a["company_specific_pct"], a["actual_pct"], delta=0.02)

    def test_price_change_decomposition(self):
        d = ma.decompose_price_change(100, 120, 5.0, 5.5)
        self.assertTrue(d["ok"])
        self.assertAlmostEqual(d["eps_change_pct"], 10.0)
        self.assertAlmostEqual(d["share_of_move_from_earnings_pct"] + d["share_of_move_from_valuation_pct"], 100.0, delta=0.2)
        self.assertFalse(ma.decompose_price_change(100, 90, -1, 2)["ok"])


class TestRulesAndRisk(unittest.TestCase):
    def test_rules(self):
        rules = {"rule": [
            {"id": "stop", "type": "stop_loss_from_sheet", "action": "retreat", "enabled": True},
            {"id": "tgt", "type": "target_from_sheet", "action": "target", "enabled": True},
            {"id": "move", "type": "abs_day_move_pct", "threshold": 5, "action": "watch", "enabled": True},
            {"id": "off", "type": "loss_from_entry_pct", "threshold": 1, "action": "retreat", "enabled": False},
            {"id": "w", "type": "position_weight_pct", "threshold": 35, "action": "watch", "enabled": True}]}
        holdings = {"positions": [
            {"ticker": "CRWD", "side": "Long", "stop_loss": 280.0, "target": None},
            {"ticker": "NVDA", "side": "Long", "stop_loss": None, "target": 230.0},
            {"ticker": "LITE", "side": "Long", "stop_loss": None, "target": None}]}
        metrics = {"positions": {
            "CRWD": {"close": 270.04, "day_change_pct": 1.0, "position": {"pnl_pct": -5}},
            "NVDA": {"close": 233.95, "day_change_pct": -6.2, "position": {}},
            "LITE": {"close": 1085.42, "day_change_pct": 0.5, "position": {}}}}
        out = cr.run(holdings, metrics, rules, {"LITE": 40.0})
        self.assertEqual(out["CRWD"]["status"], "RETREAT RULE HIT")
        self.assertEqual(out["NVDA"]["status"], "TARGET REACHED")
        self.assertEqual({f["id"] for f in out["NVDA"]["fired"]}, {"tgt", "move"})
        self.assertEqual(out["LITE"]["status"], "WATCH")

    def test_portfolio_compute(self):
        stock, market, _ = synthetic()
        s1 = pr.returns_by_date(stock)
        s2 = {d: r * 2 for d, r in s1.items()}
        out = pr.compute({"A": 75.0, "B": 25.0}, {"A": s1, "B": s2}, {"A": 1.5, "B": 3.0},
                         {"A": ["AI"], "B": ["AI", "Chips"]})
        self.assertAlmostEqual(out["weights_pct"]["A"], 75.0)
        self.assertAlmostEqual(out["correlation_60d"]["A"]["B"], 1.0, places=6)
        self.assertAlmostEqual(out["theme_exposure_pct"]["AI"], 100.0)
        self.assertAlmostEqual(out["beta_vs_market"], 1.875, delta=0.01)
        self.assertIsNotNone(out["var_95_1d_pct"])
        self.assertAlmostEqual(out["concentration"]["effective_number_of_positions"], 1.6, delta=0.01)


class TestLedger(unittest.TestCase):
    def test_levels_and_due(self):
        d = {"concepts": {}}
        self.assertEqual(cl.status(d, "Guidance"), "new")
        cl.taught(d, "Guidance", "The company's own forecast", "2026-10-05")
        cl.taught(d, "guidance", "", "2026-10-05")
        self.assertEqual(d["concepts"]["guidance"]["days_seen"], 1)
        self.assertEqual(cl.status(d, "GUIDANCE"), "learning")
        self.assertEqual([c["term"] for c in cl.due(d, "2026-10-07")], ["Guidance"])
        for day in ("2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09"):
            cl.taught(d, "Guidance", "", day)
        self.assertEqual(cl.status(d, "guidance"), "known")


GOOD = """# Portfolio report: 2026-10-05

## The bottom line
- CRWD rose because the whole market rose.

## Your rules today
No rule fired.

## Position: CRWD (CrowdStrike)
**Bottom line:** CRWD rose with the market.
**Where it stands** 0.074 shares.
**What happened, and why**
- CrowdStrike raised its yearly forecast [Reuters, 2026-08-27](https://www.reuters.com/x)
**How this works** Revenue is ...
**Case to stay** ...
**Case to retreat** ...
**Thesis check** Intact.
**Coming up** Results on 2026-12-02 (estimated).

## Your portfolio as a whole
Five stocks.

## Lesson of the day
What guidance is.

## New words today
- **Guidance**: the company's own forecast.

## Data quality and sources
Prices from Yahoo. Research and education, not investment advice.
"""


class TestLintAndRender(unittest.TestCase):
    def setUp(self):
        import pilib
        self.tiers = pilib.load_toml(ROOT / "config/sources.toml")  # tomllib on 3.11+, tomli before

    def test_good_report_passes(self):
        errors, warnings, counts = lr.lint(GOOD, self.tiers, {"concepts": {}}, ["guidance", "beta"])
        self.assertEqual(errors, [])
        self.assertEqual(counts["tier2"], 1)

    def test_bad_report_fails(self):
        bad = GOOD.replace("## The bottom line\n- CRWD rose because the whole market rose.\n", "") \
                  .replace("[Reuters, 2026-08-27](https://www.reuters.com/x)", "(https://coincodex.com/x)") \
                  .replace("Five stocks.", "You should sell NVDA. Its beta is high.")
        errors, _, _ = lr.lint(bad, self.tiers, {"concepts": {}}, ["beta"])
        text = " | ".join(errors)
        self.assertIn("missing section: '## The bottom line'", text)
        self.assertIn("citation", text)
        self.assertIn("advice language", text)
        self.assertIn("jargon 'beta'", text)

    def test_position_contract_and_coverage(self):
        no_parts = GOOD.replace("**Bottom line:** CRWD rose with the market.\n", "").replace("**Coming up**", "**Later**")
        text = " | ".join(lr.lint(no_parts, self.tiers, {"concepts": {}}, [])[0])
        self.assertIn("missing 'Bottom line'", text)
        self.assertIn("missing 'Coming up'", text)
        errors, warnings, _ = lr.lint(GOOD, self.tiers, {"concepts": {}}, [], open_tickers=["CRWD", "NVDA"])
        self.assertEqual(errors, ["open holding NVDA has no '## Position: NVDA' section"])
        _, warnings, _ = lr.lint(GOOD, self.tiers, {"concepts": {}}, [], open_tickers=[])
        self.assertTrue(any("not an open holding" in w for w in warnings))

    def test_cited_analyst_opinion_allowed_paraphrased_advice_caught(self):
        cited = GOOD.replace("Five stocks.", "- Morgan Stanley kept its buy rating with a price target of $500 "
                                             "[Reuters, 2026-10-04](https://www.reuters.com/y)")
        self.assertEqual(lr.lint(cited, self.tiers, {"concepts": {}}, [])[0], [])
        uncited = GOOD.replace("Five stocks.", "Our price target of $500 looks fair.")
        self.assertIn("without a citation", " | ".join(lr.lint(uncited, self.tiers, {"concepts": {}}, [])[0]))
        for phrase in ("You should consider selling CRWD.", "Consider trimming NVDA.", "I would sell here."):
            errs = lr.lint(GOOD.replace("Five stocks.", phrase), self.tiers, {"concepts": {}}, [])[0]
            self.assertTrue(any("advice language" in e for e in errs), phrase)

    def test_new_word_must_be_a_whole_word(self):
        report = GOOD.replace("Five stocks.", "EPS rose.").replace("- **Guidance**: the company's own forecast.",
                                                                   "- **Guidance**: the next steps.")
        self.assertIn("jargon 'eps'", " | ".join(lr.lint(report, self.tiers, {"concepts": {}}, ["eps"])[0]))

    def test_render(self):
        html = re_.convert("# Title\n\n**Bold** and [link](https://x.com)\n\n- a\n- b\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")
        for frag in ("<h1>Title</h1>", "<strong>Bold</strong>", '<a href="https://x.com">link</a>', "<ul><li>a</li>", "<table"):
            self.assertIn(frag, html)


class TestHoldings(unittest.TestCase):
    def test_merge_and_estimates(self):
        rows = [
            {"ticker": "nvda", "shares": "0.043", "fill_price": "$230.00", "open_date": "5 Oct 2026"},
            {"ticker": "NVDA", "shares": 0.01, "fill_price": 240, "open_date": "2026-10-06", "stop_loss_alert": 200},
            {"ticker": "CRWD", "shares": 0.074, "entry_price_estimate": 270.04},
            {"ticker": "AMD", "shares": 1, "fill_price": 150, "exit_date": "2026-09-20", "exit_price": 160},
            {"ticker": "", "shares": 1},
        ]
        out = lh.normalise(rows, "test", "2026-10-05")
        pos = {p["ticker"]: p for p in out["positions"]}
        mixed = lh.normalise([{"ticker": "X", "shares": 1, "entry_price_estimate": 10},
                              {"ticker": "X", "shares": 1, "fill_price": 12}], "test", "2026-10-05")
        self.assertEqual(mixed["positions"][0]["entry_price_source"], "mixed")
        self.assertAlmostEqual(pos["NVDA"]["shares"], 0.053)
        self.assertAlmostEqual(pos["NVDA"]["entry_price"], (230 * 0.043 + 240 * 0.01) / 0.053, places=3)
        self.assertEqual(pos["NVDA"]["open_date"], "2026-10-05")
        self.assertEqual(pos["NVDA"]["stop_loss"], 200)
        self.assertEqual(pos["CRWD"]["entry_price_source"], "sheet-estimate")
        self.assertEqual(len(out["closed"]), 1)
        self.assertTrue(any("in the future" in w for w in out["warnings"]))


class TestEndToEndOffline(unittest.TestCase):
    """Copies the repo to a temp folder, writes synthetic prices, and runs the offline tools in order."""

    def test_pipeline(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            repo = tmp / "repo"
            shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", "__pycache__", "data"))
            (repo / "data").mkdir()
            for i, t in enumerate(["CRWD", "NVDA", "SPY", "QQQ", "CIBR", "SMH"]):
                st, mk, sc = synthetic(seed=11 + i)
                with open(repo / "data" / "prices" / f"{t}.csv" if (repo / "data" / "prices").exists() else _mk(repo, t), "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=["date", "open", "high", "low", "close", "adj_close", "volume"])
                    w.writeheader()
                    for r in (mk if t in ("SPY", "QQQ") else st):
                        w.writerow(r)
            csvp = repo / "config" / "holdings_test.csv"
            csvp.write_text("open_date,ticker,side,order_type,shares,fill_price,stop_loss_alert,target_price,exit_date,exit_price,fees,notes\n"
                            "2026-01-05,CRWD,Long,Market,0.074,90,500,,,,0,\n2026-01-05,NVDA,Long,Market,0.043,80,,,,,0,\n")
            env = dict(os.environ, RUN_DATE="2026-07-31")
            S = repo / ".claude" / "skills"
            cmds = [
                [S / "portfolio-daily-report/scripts/load_holdings.py", "--from-csv", str(csvp), "--date", "2026-07-31"],
                [S / "market-metrics/scripts/market_metrics.py", "--date", "2026-07-31"],
                [S / "why-analysis/scripts/move_attribution.py", "--date", "2026-07-31"],
                [S / "portfolio-risk/scripts/portfolio_risk.py", "--date", "2026-07-31"],
                [S / "position-review/scripts/check_rules.py", "--date", "2026-07-31"],
            ]
            for c in cmds:
                p = subprocess.run([sys.executable, *map(str, c)], capture_output=True, text=True, env=env, cwd=repo)
                self.assertEqual(p.returncode, 0, msg=f"{c[0].name}: {p.stdout}\n{p.stderr}")
            metrics = json.loads((repo / "data/metrics/2026-07-31.json").read_text())
            self.assertIn("CRWD", metrics["positions"])
            pos = metrics["positions"]["CRWD"]["position"]
            self.assertIsNotNone(pos["pnl"])
            self.assertIsNotNone(metrics["positions"]["NVDA"]["beta_1y_vs_market"])
            rules = json.loads((repo / "data/metrics/rules-2026-07-31.json").read_text())
            self.assertIn("CRWD", rules["positions"])
            port = json.loads((repo / "data/metrics/portfolio-2026-07-31.json").read_text())
            self.assertAlmostEqual(sum(port["weights_pct"].values()), 100.0, delta=0.2)
            att = json.loads((repo / "data/metrics/attribution-2026-07-31.json").read_text())
            self.assertIn("last_day", att["CRWD"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestEntryEstimate(unittest.TestCase):
    def test_weekend_and_future_dates(self):
        rows = [{"date": "2026-10-01", "open": 100.0, "high": 101, "low": 99, "close": 100.5, "adj_close": 100.5, "volume": 1},
                {"date": "2026-10-02", "open": 101.0, "high": 102, "low": 100, "close": 101.5, "adj_close": 101.5, "volume": 1},
                {"date": "2026-10-05", "open": 103.0, "high": 104, "low": 102, "close": 103.5, "adj_close": 103.5, "volume": 1}]
        self.assertEqual(mm.estimate_entry("2026-10-02", rows)[0], 101.5)          # trading day -> close
        price, src = mm.estimate_entry("2026-10-03", rows)                         # Saturday -> Monday open
        self.assertEqual(price, 103.0)
        self.assertIn("next trading day", src)
        price, src = mm.estimate_entry("2026-10-07", rows)                         # future -> latest close, flagged
        self.assertEqual(price, 103.5)
        self.assertIn("may not be filled", src)
        pos = mm.position_metrics({"shares": 0.074, "side": "Long", "entry_price": None, "open_date": "2026-10-03"}, rows)
        self.assertAlmostEqual(pos["pnl"], 0.074 * (103.5 - 103.0), places=2)  # dollars, rounded to cents


class TestGoalsLens(unittest.TestCase):
    def test_sector_exposure_and_goals_check(self):
        stock, market, _ = synthetic()
        s1 = pr.returns_by_date(stock)
        out = pr.compute({"NVDA": 60.0, "STRL": 40.0}, {"NVDA": s1, "STRL": s1}, {"NVDA": 1.8, "STRL": 1.2},
                         {"NVDA": ["AI data centers"], "STRL": ["AI data centers", "construction"]},
                         {"NVDA": "Technology", "STRL": "Industrials"}, ["Diversify beyond tech"])
        self.assertAlmostEqual(out["sector_exposure_pct"]["Technology"], 60.0)
        self.assertAlmostEqual(out["goals_check"]["technology_share_pct"], 60.0)
        self.assertEqual(out["goals_check"]["largest_theme"], "AI data centers")
        self.assertAlmostEqual(out["goals_check"]["largest_theme_share_pct"], 100.0)
        self.assertEqual(out["goals_check"]["high_movers_beta_1_5_plus"], ["NVDA"])
        self.assertAlmostEqual(out["goals_check"]["high_movers_share_pct"], 60.0)
        self.assertEqual(out["goals_check"]["unclassified_tickers"], [])

    def test_unknown_ticker_never_becomes_the_largest_theme(self):
        stock, _, _ = synthetic()
        s1 = pr.returns_by_date(stock)
        out = pr.compute({"NEW": 70.0, "NVDA": 30.0}, {"NEW": s1, "NVDA": s1}, {"NEW": 1.0, "NVDA": 1.8},
                         {"NVDA": ["AI data centers"]}, {"NVDA": "Technology"}, [])
        self.assertEqual(out["goals_check"]["largest_theme"], "AI data centers")
        self.assertEqual(out["goals_check"]["unclassified_tickers"], ["NEW"])


def _mk(repo, t):
    (repo / "data" / "prices").mkdir(parents=True, exist_ok=True)
    return repo / "data" / "prices" / f"{t}.csv"


if __name__ == "__main__":
    unittest.main()
