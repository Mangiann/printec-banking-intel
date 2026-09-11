# deliverables/ — the human folder

**One file.** A single Excel that lists **every source** we track, named in plain English
(e.g. `Greece - Banking & Payments Sources (tenders, procurement).xlsx`). No per-run subfolders, no versions.
"Go to this folder and review the sources" = open the one file.

The file grows as each discovery run **appends** its new sources. Three tabs:
- **READ ME FIRST** — what each column means.
- **All sources** — every source we've accepted, one per row, with `added_in_run` (which run found it),
  `status` (active = we collect it / paused = kept but needs an access or legal OK first), and the facts
  (name, type, url, access, why we track it). Sort by `added_in_run` to see what a run contributed.
- **Pending - needs access** — good sources found but not yet reachable/accepted, so nothing is hidden.

Everything else a run produces (per-run review sheets, ledgers, grouped detail, the durable list) is
**machine output** under `data/run_logs/<run_id>/artifacts/` — never in this folder.

The file is regenerated automatically at the end of every `run_pipeline.py` run and every
`sync_registry.py`, so it always reflects the current master list.
