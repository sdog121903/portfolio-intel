# Sources and credits

This folder system was built after reviewing the skills Santi pointed to. What was used, and how:

| Repository | License | How it is used here |
|---|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills/tree/main/finance/skills) `finance/skills/stock-analysis` | MIT | **Vendored unchanged** (minus its evals) as `.claude/skills/stock-analysis` for weekly deep dives: sector playbooks, earnings quality, valuation and reverse DCF, forensic red flags, scoring, the challenge pass, the report linter. Its "analysis, not advice" rule matches ours |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | MIT | **Vendored** its SEC EDGAR and FRED API references into `source-hierarchy/references/`. Its statistical-analysis approach informed the metrics and tests |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | MIT | The research-lead / subagent / citations pattern shaped the parallel holding researchers and the fact-checker; the financial-statement and financial-modeling skills informed the earnings and valuation guidance. Not copied |
| [quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research) | MIT | Its catalyst analysis, bull/base/bear framing, insider-signal and technical-context sections informed the report structure. Its buy/sell ratings, price targets and position sizing were deliberately **not** adopted |
| [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) | MIT | Indicator definitions (RSI, ATR, moving averages) and risk metrics informed `market-metrics`; its trading-signal generation was not adopted |
| [liangdabiao/claude-data-analysis](https://github.com/liangdabiao/claude-data-analysis) | none found | Its pattern of specialised subagents plus a quality-assurance step informed `.claude/agents/`. Nothing copied |
| [coffeefuelbump/csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | none found | Reviewed; the sheet is small and structured, so a dedicated loader was written instead. Nothing copied |
| [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) | none found | Reviewed; reports are markdown and email, so not needed. Nothing copied |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | MIT | Used as a catalog for discovery; nothing copied |
| [Snyk: top Claude skills for finance](https://snyk.io/articles/top-claude-skills-finance-quantitative-developers/) | article | Guidance followed: precise skill descriptions, progressive disclosure, and vetting third-party skills before use (only reviewed, MIT-licensed files were vendored; nothing is downloaded at run time) |

Full license texts for vendored files are in `LICENSES/`.
