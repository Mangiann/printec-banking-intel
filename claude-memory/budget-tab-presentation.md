---
name: budget-tab-presentation
description: "Colleague feedback on the Budget 2027 tab (14/09/2026) — only a very simple executive summary on top, then the moves grid with the details of each move underneath; the long board report goes behind a fold"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0bb1fab0-f44e-4aec-8f89-37f3eb288af0
  modified: 2026-09-14T13:45:11.554Z
---

On 14/09/2026 colleagues reviewed the Budget 2027 tab with the board's executive report and said (in Greek): "probably better, but the presentation is not good; it says a lot and again you understand nothing. We want only an executive summary in very simple English, and then the table it had before with the moves, with the details for each move appearing below, like before."

Second round of feedback the same day: the executive summary must be a ONE-PAGER in the same form as the competitors summary and the 2030 outlook summary (flowing prose, key figures in bold), and the English must be simple but written for executives, not dumbed down. Implemented as `report.executive_summary_md` (markdown, ~800 words, seven bold-led paragraphs) rendered through `mdToHtml` in a `.news.bg-onepager` block; the sentence list `executive_summary` is only the fallback. The chair brief asks for both.

Third round (14/09/2026): (a) remove ANY reference to the agentic board from what readers see (keep the explanations) — done with `board_2027.py publicize`, which applies `round4/texts_public.json` (a neutral third-person rewrite of every text, made by an agent under strict rules: no board/chair/seat/vote/sceptic/agent/adviser words, no first person, every figure kept), maps seats to "views" (Finance view, Risk view, Outside view, Commercial view, line and market views, "the review", "delivery check") and drops the votes (kept in `budget_2027_board.internal.json`); (b) the four estimate cards (2026 budget / lowest acceptable / 2027 budget / most the evidence supports) are clickable and switch the moves grid's numbers and percentages; (c) formatting like the Future outlook tab: cyan `.bl-hero` with kicker + thesis, `.bl-kpi` cards, `.bl-shead` icon-chip section headers, full-width prose, the full explanation as a `.bl-panel` fold with tiles for levers, conditions and the lower views. Run order after a board sitting: finalize → publicize → build_artifact.

Fourth round (14/09/2026): the ranked list "The moves, ranked by the money behind them" was removed — it repeated the grid. The tab is now two things only: the executive summary (hero + estimate cards + sections, full explanation folded) and the moves grid with the drill-down.

Fifth round (14/09/2026): clicking an estimate card must scroll the reader down to the moves grid (smooth scroll + a short cyan flash on the card), otherwise nobody sees what the click changed.

Sixth round (15/09/2026): the mandate's ladder cards (floor with actions landed / budget with actions landed / maximum) are clickable like the estimate cards and switch the moves grid; per-cell values = board floor/target + the mandate's per-cell action euros (`MdA` in app.js), group totals anchored on the ladder's own euros. Artifact v64.

**Why:** the readers are a mixed management team; a ten-section report with evidence chips reads as noise. The earlier layout (moves grid coloured by action → click → reasons, dated items, signals) was what they liked.

**How to apply:** `renderBudget` in app.js now has three cards: (1) "Budget 2027 in short": four tiles + eight to ten one-idea sentences from `report.executive_summary` (the chair writes it; brief updated), with the full report inside a closed `<details class="bg-fullreport">`; (2) "The moves, market by market": the 2026 action grid (budget_actions.json) showing the board's 2027 number per cell, drill-down = board block + `bgCellBody`; (3) [removed 14/09/2026] the ranked moves list. Do not put the long report back on top. Keep this shape for any future budget content: summary first, moves grid second, everything else folded. See [[plain-english-everywhere]] and [[budget-board-2027]].

**Selectable blocks (user, 18/09/2026):** no black frames anywhere on the Budget tab. Estimate cards: unselected are muted (saturate .7, opacity .88), hover restores colour and lifts, selected (`.on`) switches from the soft tint to the full colour of its tone (k-green → var(--green) etc.) with a white-ish blob; grid cells highlight with an inset shade instead of an outline; the drivers card has the normal 1px card border; driver chips tint with their colour on hover (color-mix). The `.bg-flash` animation is a background fade, not an outline. Artifact v89 (18/09/2026 17:51).

**Euro formatting (user, 23/09/2026):** never show a non-zero amount as "€0.0m". `bgM` in app.js (and the chart/category formatters that now alias it) shows one decimal, two below €0.05m, three below €0.005m; a true zero still reads €0.0m. Artifact v96, build 23/09/2026 13:13.
