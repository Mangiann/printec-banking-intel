"""Export the whole source master-list (the registry) to ONE human Excel file.

This is THE deliverable a human opens: `deliverables/<one file>.xlsx`. It lists EVERY source we hold, not a
per-run delta, with the run that first added each one — so the file GROWS (is appended) as runs promote new
sources, and a reviewer can sort by 'added_in_run' to see what each run contributed. Read-only view: the
canonical store is the registry (promotion.db); this is its human-readable projection.

Tabs: 'READ ME FIRST' (what the columns mean), 'All sources' (one row per source — the globe's view), one tab
per research (workstream) so each kind of source can be read on its own, and 'Pending - needs access' (durable
sources found but not yet accepted — blocked/held — so nothing is hidden).
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

_SECTOR_LABEL = {"both": "Banking & Payments", "banking": "Banking", "payments": "Payments"}

_PRANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
COLUMNS = [
    ("workstream", "Which research it serves (A1 disclosures · A2 tenders · A3 regulation · A4 stats · A5 jobs · A6 vendors · A8 trends)"),
    ("added_in_run", "Which run first found this source"),
    ("added_on", "Date it entered the list"),
    ("status", "active = we collect it · paused = kept, needs an access/legal OK first"),
    ("priority", "critical / high / medium / low"),
    ("source_name", "Name of the source"),
    ("source_type", "What kind of source it is"),
    ("url", "Where it lives"),
    ("access", "How reachable it is (public / login / paywall / …)"),
    ("legal", "Legal status for collecting it"),
    ("sector", "banking / payments / both"),
    ("topics", "What it covers"),
    ("why_track_it", "Why it is worth monitoring"),
]
_HEADERS = [c[0] for c in COLUMNS]

# One tab per research (workstream) inside each country file — so a reviewer sees "Tenders" separate from
# "Disclosures" without filtering, while the file stays one-per-country for the globe.
WS_LABELS = {
    "A1": "Disclosures", "A2": "Tenders & Procurement", "A3": "Regulation & Deadlines",
    "A4": "Market Statistics", "A5": "Early Intent & Jobs", "A6": "Vendors & Competitors",
    "A8": "Futurist & Trends",
}


def _by_workstream(rows):
    """{workstream_code: [rows]} — a source tagged with several workstreams appears under each."""
    groups = {}
    for r in rows:
        for code in (t.strip() for t in str(r.get("workstream") or "").split(",") if t.strip()):
            groups.setdefault(code, []).append(r)
    return groups


def _norm(u):
    return u.strip().rstrip("/").lower() if isinstance(u, str) else ""


def build_url_run_index(run_files):
    """{normalized canonical_url -> (run_label, run_id)} for the EARLIEST run that saw the url.

    `run_files` is an ordered list of (run_label, run_id, jsonl_path), earliest first."""
    idx = {}
    for label, run_id, path in run_files:
        p = Path(path)
        if not p.exists():
            continue
        for ln in p.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                c = json.loads(ln)
            except ValueError:
                continue
            u = _norm(c.get("canonical_url"))
            if u and u not in idx:                 # earliest run wins (files passed earliest-first)
                idx[u] = (label, run_id)
    return idx


def _registry_rows(registry_db, url_run):
    rows, seen = [], set()
    if not registry_db or not Path(registry_db).exists():
        return rows, seen
    conn = sqlite3.connect(f"file:{Path(registry_db)}?mode=ro", uri=True)
    try:
        docs = [json.loads(d) for (d,) in conn.execute("SELECT doc FROM source")]
    except sqlite3.Error:
        docs = []
    finally:
        conn.close()
    for d in docs:
        url = d.get("canonical_url") or d.get("url_or_endpoint")
        seen.add(_norm(url))
        label, _rid = url_run.get(_norm(url), ("(unknown)", None))
        created = d.get("created_at") or ""
        rows.append({
            "workstream": ", ".join(d.get("workstreams", []) if isinstance(d.get("workstreams"), list) else []),
            "added_in_run": label, "added_on": str(created)[:10],
            "status": d.get("active_status"), "priority": d.get("priority"),
            "source_name": d.get("name"), "source_type": d.get("source_subtype"),
            "url": url, "access": d.get("access_status"), "legal": d.get("legal_status"),
            "sector": d.get("sector"),
            "topics": ", ".join(d.get("topics", []) if isinstance(d.get("topics"), list) else []),
            "why_track_it": d.get("reason_to_track"),
        })
    return rows, seen


def _pending_rows(pending, url_run, in_registry):
    """pending: list of candidate dicts (durable but NOT yet in the registry). Deduped by url (a source
    held across several runs must appear once)."""
    rows, seen = [], set()
    for c in pending or []:
        url = c.get("canonical_url") or c.get("source_url")
        nu = _norm(url)
        if nu in in_registry or nu in seen:
            continue
        seen.add(nu)
        label, _rid = url_run.get(_norm(url), ("(unknown)", None))
        access = c.get("access_status")
        status = "needs access" if access not in ("public", None, "") else "pending review"
        rows.append({
            "workstream": c.get("workstream") or ", ".join(
                c.get("workstreams", []) if isinstance(c.get("workstreams"), list) else []),
            "added_in_run": label, "added_on": "",
            "status": status, "priority": c.get("priority"),
            "source_name": c.get("source_name"), "source_type": c.get("source_subtype"),
            "url": url, "access": access, "legal": c.get("legal_status"),
            "sector": c.get("sector"),
            "topics": ", ".join(c.get("topics", []) if isinstance(c.get("topics"), list) else []),
            "why_track_it": (c.get("discovery_basis") or {}).get("why_relevant"),
        })
    return rows


def _sort_key(r):
    return (str(r.get("added_in_run")), _PRANK.get(r.get("priority"), 9), str(r.get("source_name") or ""))


def _write_sheet(ws, rows):
    hdr_font, hdr_fill = Font(bold=True), PatternFill("solid", fgColor="DDDDDD")
    for i, h in enumerate(_HEADERS, 1):
        c = ws.cell(row=1, column=i, value=h)
        c.font, c.fill = hdr_font, hdr_fill
    for r, row in enumerate(sorted(rows, key=_sort_key), start=2):
        for i, h in enumerate(_HEADERS, 1):
            v = row.get(h)
            ws.cell(row=r, column=i, value=v if isinstance(v, (str, int, float)) or v is None else str(v))
    widths = {"source_name": 40, "url": 52, "why_track_it": 60, "topics": 26, "source_type": 26,
              "status": 12, "added_in_run": 14, "added_on": 12, "access": 16, "legal": 14}
    for i, h in enumerate(_HEADERS, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 13)
    ws.freeze_panes = "A2"


def build_master_workbook(registry_db, run_files, out_path, *, scope_label, pending=None):
    """Write the single master-list workbook. `run_files` = ordered [(label, run_id, jsonl_path)] earliest
    first (for provenance). `pending` = durable candidates not yet in the registry. Returns (out_path, counts)."""
    url_run = build_url_run_index(run_files)
    reg_rows, in_registry = _registry_rows(registry_db, url_run)
    pend_rows = _pending_rows(pending, url_run, in_registry)

    wb = Workbook()
    info = wb.active
    info.title = "READ ME FIRST"
    intro = [
        (scope_label, ""),
        ("What this is", "The full list of information sources we track. It grows as each discovery run "
                         "adds new ones. Sort by 'added_in_run' to see what a run contributed."),
        ("", ""),
        ("'All sources' tab", f"{len(reg_rows)} sources we have accepted into the list."),
        ("Per-research tabs", "One tab per research (A1 Disclosures, A2 Tenders, …) — the same sources, split "
                              "by which research they serve, so you can read one kind at a time."),
        ("'Pending - needs access' tab", f"{len(pend_rows)} good sources found but not yet reachable/accepted."),
        ("", ""),
    ] + [(name, desc) for name, desc in COLUMNS]
    for r, (k, v) in enumerate(intro, 1):
        info.cell(row=r, column=1, value=k).font = Font(bold=True)
        info.cell(row=r, column=2, value=v)
    info.column_dimensions["A"].width = 22
    info.column_dimensions["B"].width = 100

    _write_sheet(wb.create_sheet("All sources"), reg_rows)
    for code, group in sorted(_by_workstream(reg_rows).items()):
        title = f"{code} - {WS_LABELS.get(code, code)}"[:31]      # Excel caps sheet titles at 31 chars
        _write_sheet(wb.create_sheet(title), group)
    _write_sheet(wb.create_sheet("Pending - needs access"), pend_rows)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    counts = {"sources": len(reg_rows), "pending": len(pend_rows)}
    try:
        wb.save(out_path)
    except PermissionError:
        # The file is open in Excel (Windows locks it). This workbook is only a projection of the registry —
        # which is already updated — so DON'T crash the round: leave the file stale, flag it, regenerate later.
        counts["locked"] = True
        print(f"WARNING: could not write {out_path} — it is open in Excel. Registry is updated; the "
              f"deliverable was left stale — re-export it after closing the file.", file=sys.stderr)
    return str(out_path), counts


def _gather_pending(data_root, run_prefix=""):
    """Durable 'keep' candidates from THIS scope's runs (run_prefix like 'dr_gr_') that have LLM role verdicts.
    Empty prefix = all runs. All scopes share data/source_candidates/, so without the prefix a country's file
    would list every other country's pending. Dedup happens by url later."""
    data_root = Path(data_root)
    pending = []
    for cf in sorted((data_root / "source_candidates").glob("*.jsonl")):
        run_id = cf.stem
        if run_prefix and not run_id.startswith(run_prefix):
            continue                                    # a different scope's run -> not this file's pending
        rvp = data_root / "run_logs" / run_id / "agent_inputs" / "role_verdicts.json"
        if not rvp.exists():
            continue
        try:
            # r.get("verdict") (not r["verdict"]): a row missing 'verdict' must drop only THAT row (-> None,
            # never == "keep"), not KeyError out of the comprehension and skip the whole run's pending sources.
            roles = {r["candidate_id"]: r.get("verdict") for r in json.loads(rvp.read_text(encoding="utf-8"))
                     if isinstance(r, dict) and isinstance(r.get("candidate_id"), str)}
        except ValueError:
            continue
        for ln in cf.read_text(encoding="utf-8").splitlines():
            if not ln.strip():
                continue
            try:
                c = json.loads(ln)
            except ValueError:
                continue
            if roles.get(c.get("candidate_id")) == "keep":
                pending.append(c)
    return pending


def deliverable_name(config):
    """A plain-English filename that says what's inside — e.g.
    'Greece - Banking & Payments Sources (Tenders, Procurement).xlsx'."""
    country = config.get("country_name") or config.get("country") or "Sources"
    sector = _SECTOR_LABEL.get(config.get("sector"), "Banking & Payments")
    name = f"{country} - {sector} Sources.xlsx"   # ONE Excel per country; the workstream is a column
    return re.sub(r'[<>:"/\\|?*]', "-", name)     # strip characters Windows forbids in filenames


def export_from_project(data_root, registry_db, out_dir, config):
    """Discover all run files + pending, and write the single master-list deliverable into `out_dir`
    (flat, no per-run subfolder). Returns (path, counts)."""
    data_root = Path(data_root)
    prefix = f"dr_{Path(registry_db).stem.lower()}_"     # GR.db -> dr_gr_ ; EU.db -> dr_eu_ : only this scope
    files = sorted(f for f in (data_root / "source_candidates").glob("*.jsonl")
                   if f.stem.startswith(prefix))         # only THIS scope's runs (no cross-country leak)
    run_files = [(f"Run {i + 1}", f.stem, str(f)) for i, f in enumerate(files)]
    country = config.get("country_name") or config.get("country") or "Sources"
    sector = _SECTOR_LABEL.get(config.get("sector"), "Banking & Payments")
    topics = ", ".join(t for t in (config.get("topics") or []) if isinstance(t, str))
    ws = (config.get("workstreams") or [""])[0]
    scope_label = f"{country} - {sector} - {topics} ({ws})".strip(" -()")
    out_path = Path(out_dir) / deliverable_name(config)
    return build_master_workbook(registry_db, run_files, str(out_path),
                                 scope_label=scope_label, pending=_gather_pending(data_root, prefix))
