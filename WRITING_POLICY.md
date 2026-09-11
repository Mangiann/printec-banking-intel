# Writing policy — all user-facing text

This is the single writing standard for the Printec market-intelligence system. It applies to everything a
reader sees: the dashboard's own text, text the application generates, and every output written by an
agent, sub-agent, research agent, summariser or other AI component — titles, section introductions,
summaries, findings, recommendations, cards, tables, tooltips, reports and generated analysis.

The goal is simple, professional, easy-to-read business English. Clarity matters more than style.
Preserve the analysis; make it easier to understand. Never shorten by deleting useful information.

## 1. Plain English

- Write in plain English. Prefer a clear explanation over clever, dramatic or journalistic wording.
- Do not write headline-style statements inside normal paragraphs.
  - Not: "Demand is inverting, and the calendar explains why."
  - Write: "Regulatory deadlines are changing where demand is likely to come from."
- Do not use dramatic expressions. State the actual fact instead. Banned examples: "the endgame",
  "the plumbing has moved", "the sharper change", "the story is…", "the real prize", "the clock is
  ticking", "the market is exploding", "the opportunity is hiding", "the winner will be…",
  "what nobody is watching", "keeps it honest", "the loudest voice".

## 2. Capitalisation and emphasis

- Do not use ALL CAPS for emphasis inside sentences.
  - Not: "Both the money and the BUYERS are moving."
  - Write: "Both spending and the types of buyers are changing."
- Do not capitalise words such as BUYERS, OPERATES, ACCEPTANCE, DEMAND or GROWTH unless normal grammar
  requires it (proper names, acronyms, the start of a sentence).
- Use bold sparingly, only where emphasis is genuinely necessary — usually the one most important figure
  or conclusion in a passage.

## 3. Sentences

- One main idea per sentence.
- Usually no more than 20–25 words per sentence.
- Split any sentence that carries several dates, regulations, statistics or conclusions.
- Avoid long chains joined by commas, semicolons and dashes.
- A reader should not have to read a sentence twice to understand it.

## 4. Paragraphs

- Keep paragraphs short: 2–4 sentences.
- If a paragraph holds several independent facts, split it into separate paragraphs or use bullets.
- Do not turn an analysis into one dense block of text. Do not solve this by creating dozens of tiny
  headline fragments either — use normal prose, well divided.

## 5. Technical terms

- The first time an acronym or specialist term appears, explain it briefly in normal language.
  - "Hardware security modules (HSMs), which are secure devices used to store payment encryption keys, …"
- Do not remove the technical term itself. Do not assume the reader knows regulatory or technical jargon.

## 6. Facts before interpretation

- First say what happened. Then say why it matters. Then, if relevant, what it means commercially.
  - "FIDA does not yet have an agreed final text. This means its implementation timetable remains uncertain."
- Do not fold the fact, the interpretation and the sales conclusion into one complicated sentence.

## 7. Dates and regulations

- Never put several regulatory deadlines in one sentence. Use a short list, a table or separate sentences,
  then give the commercial implication separately.
  - "Several important deadlines are approaching:
    - Non-euro instant payments: 9 January 2027
    - Verification of Payee: 9 July 2027
    - AML Regulation: 10 July 2027
    - EUDI wallet acceptance: 24 December 2027"

## 8. Numbers

- Do not overload a sentence with statistics. Give the important number first, then say what it means.
- Round when exact precision adds nothing: "about 15% a year", "roughly $29 billion by 2030".
- Do not pack several unrelated market forecasts into one sentence.

## 9. Tone

Clear, calm, professional, analytical, factual, commercially useful, easy for a senior business reader to
scan. Not journalistic, dramatic, academic, promotional, cryptic, headline-heavy or overly clever. Do not
try to make every paragraph memorable.

## 10. Headings

- A heading describes what the section contains. It helps navigation; it does not create suspense.
  - Good: "Regulatory deadlines", "New buyer groups", "Core banking changes", "Market outlook".
  - Bad: "Demand is inverting", "The buyer is changing", "The endgame", "The plumbing has moved",
    "What nobody is watching".

## 11. Conclusions

- Make conclusions explicit and plain.
  - "This creates an opportunity for vendors that provide integration services."
    not "Fragmentation is exactly what creates integration revenue."
  - "Cash and ATM services remain a stable source of recurring revenue, but they are unlikely to be the
    main source of market growth."
    not "Cash and ATMs stay a defensible managed-services annuity, but they are the legacy base to
    optimise, never the growth spine."

## 12. Screen readability

Before text is shown, shape it for the screen: short paragraphs; bullets for several facts; tables for
comparisons and dates; descriptive headings; highlight only the most important figure or conclusion; no
walls of text.

## 13. What must never change

Numbers, dates, company names, regulatory names, citations, links and factual claims stay exactly as they
are, unless there is a factual reason to correct them. Wording changes; facts do not.

## 14. Where this policy is enforced

- Every agent brief in `agent-briefs/` and every scheduled agent task references this file and follows it
  when writing anything a reader will see.
- The final formatting stage — Agent 9, the plain-English editor (`agent-briefs/09-plain-english-editor.md`)
  — rewrites new content to this standard before the dashboard is built.
- `weekly-intelligence/scripts/plain_lint.py` checks every user-facing text against the measurable rules
  (banned phrases, ALL-CAPS emphasis, sentence and paragraph length) after each build and reports what
  still fails. `plain_check.py` guarantees no figure, date or link is lost in a rewrite.
