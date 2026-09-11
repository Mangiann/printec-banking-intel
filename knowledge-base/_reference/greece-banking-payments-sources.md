---
source_file: "Greece - Banking & Payments Sources.xlsx"
type: xlsx
processed: 2026-07-23
agents: ["agent-1-bank-disclosures", "agent-2-tenders", "agent-3-regulation", "agent-4-statistics", "agent-5-jobs", "agent-6-vendors", "_reference"]
tags: ["greece", "banking", "payments", "source-registry", "information-sources", "monitoring", "workstreams", "market-intelligence"]
original: "../processed/Greece - Banking & Payments Sources.xlsx"
---

> **Original document:** [Greece - Banking & Payments Sources.xlsx](../processed/Greece - Banking & Payments Sources.xlsx) — full file in `knowledge-base/processed/`.

# Greece – Banking & Payments source registry (overview)

**What it is:** a tabular **registry of the information sources we track** for the Greece banking & payments market intelligence programme. It is *not* a report — it is the master list of *where to look*. It grows as each discovery run adds new sources; sort by `added_in_run` to see what a run contributed. Source file: **`Greece - Banking & Payments Sources.xlsx`** (in `knowledge-base/processed/`).

**Size:** 1928 accepted sources on the master **"All sources"** sheet, plus **99** good-but-not-yet-reachable sources on **"Pending – needs access"**.

## Per-workstream counts (accepted sources)

| Workstream | Sheet | Serves agent | Sources | critical | high | medium | low |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 — Disclosures | A1 - Disclosures | agent-1-bank-disclosures | 298 | 27 | 124 | 110 | 37 |
| A2 — Tenders & Procurement | A2 - Tenders & Procurement | agent-2-tenders | 892 | 96 | 385 | 335 | 76 |
| A3 — Regulation & Deadlines | A3 - Regulation & Deadlines | agent-3-regulation | 231 | 31 | 95 | 91 | 14 |
| A4 — Market Statistics | A4 - Market Statistics | agent-4-statistics | 164 | 15 | 67 | 66 | 16 |
| A5 — Early Intent & Jobs | A5 - Early Intent & Jobs | agent-5-jobs | 242 | 19 | 79 | 113 | 31 |
| A6 — Vendors & Competitors | A6 - Vendors & Competitors | agent-6-vendors | 101 | 6 | 44 | 39 | 12 |
| **Total** | All sources | (all) | **1928** | **194** | **794** | **754** | **186** |

_No A8 / trends sources are present in this registry._

## Columns in every sheet
`workstream` · `added_in_run` · `added_on` · `status` (active = collected / paused = kept, needs access-or-legal OK first) · `priority` (critical/high/medium/low) · `source_name` · `source_type` · `url` · `access` (public / login / paywall / …) · `legal` (allowed / requires_review / unclear / restricted) · `sector` (banking / payments / both) · `topics` · `why_track_it`.

## Access / legal picture (all sources)
- **Status:** 1418 active · 510 paused.
- **Access:** 1732 public · 160 unknown · 10 requires_free_account · 9 blocked · 8 requires_paid_subscription · 7 requires_legal_review · 2 requires_credentials.
- **Legal:** 1601 allowed · 188 requires_review · 139 unclear — review the requires_review / unclear / restricted ones before automated collection.
- **Pending – needs access (99):** sources found but not yet reachable (mostly requires_credentials / paid subscription / free account); priority mix 4 critical · 44 high · 29 medium · 22 low. Re-check for access before relying on them.

## How to use it
- Each research agent has a **per-workstream digest** (in its own KB folder) listing that workstream's critical & high sources with URLs and why-track notes — start there.
- Need the long tail (medium/low) or extra columns (source_type, topics, added_on)? Open the master file and read the matching **"A# – …"** sheet, or filter the **"All sources"** sheet by the `workstream` column.
- Respect the `status`, `access` and `legal` columns: **paused / requires_review / paywall / login** sources need a green light before collection.

---
> **Source of truth:** `Greece - Banking & Payments Sources.xlsx` in `knowledge-base/processed/`. Never treat this digest as the full list — it is a navigational index over the registry.
