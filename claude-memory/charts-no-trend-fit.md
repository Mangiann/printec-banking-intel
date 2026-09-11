---
name: charts-no-trend-fit
description: Printec dashboard Charts tab — no statistical trend fit anywhere; projections start from the last reported point (mean if several in a year); outlook % = mean ± std of patterns and signals readings for next year
metadata: 
  node_type: memory
  type: project
  originSessionId: 9a51b16c-1ba3-43e8-aabe-9882bfb8346d
  modified: 2026-09-10T08:23:55.839Z
---

Decision of 10/09/2026 for the BANKING dashboard (`~/Downloads/BANKING`): the Charts tab must not calculate, use or show any statistical trend fit. `build_dashboard.py` strips the fit fields from the baseline rows (`_strip_fit`), and `project_lines.py` no longer reads `f.projection`.

- Every projection line (patterns, analyst signals line, rule-based signals point) starts from the row's **anchor**: the last year with any reported point, measured or provisional, from the row's own series or another organisation's readings (`alt_series`), never a projected point. Several readings in that year → their mean (`anchor_point()` in `project_lines.py`).
- The map and table "outlook /yr" = mean ± sample std of the patterns and signals readings for next year (`consensus` in `project_lines.py`, passed as `DASH.projection_consensus`). No fit reading.
- Product tags on signals come from the LLM critic (`product_critic.py`, `product_review.json`, Agent 10); keyword matching is only a hint.

**Why:** the user said the trend fit is a single source and asked for the pooled verdict of all projections; and that projections must start from the last reported point, not from a projected one.
**How to apply:** never reintroduce `cagr_pct`, `fit_quality` or `f.projection` in the front end; keep `forecast.py` output as history + alt_series only in the dashboard payload. See [[printec-dashboard-artifact]] and [[plain-english-everywhere]].
