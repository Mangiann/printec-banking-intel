"""Excel review round-trip — export a run's review DELTA to a reviewer, import their decisions.

EXPORT: writes the run's *new* candidates (from crossrun) to an .xlsx "Review" sheet with four column
bands — MACHINE (locked, read-only reference), AGENT-SUGGESTION (pre-labeled by the assistant agent),
HUMAN-DECISION (a dropdown decision + owner + notes), and ACCESS (a `can_access` dropdown + `access_note`
where the reviewer corrects what the scout got wrong about reachability). A "Run Info" sheet carries the run
id + counts + instructions.

IMPORT: reads the returned .xlsx and extracts ONLY the human-decision + access columns keyed by
`candidate_id`. Edits to machine columns are IGNORED — the canonical data stays the JSONL; the sheet is just
a UI. Decisions are validated (allowed vocab; an `approve` must name an owner; `can_access` in the allowed
set; `yes`/`do_not_collect` need an access_note). Produces a structured decisions list + an errors list. It
does NOT promote — feeding decisions into the promotion workflow is `promotion/apply.py`.
"""
import json
from collections import Counter
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

import crossrun
from _safe import dget

MACHINE = ["candidate_id", "novelty", "priority", "source_class", "source_subtype", "source_name",
           "canonical_url", "access_status", "legal_status", "url_verified", "why_relevant"]
SUGGEST = ["suggested_decision", "suggested_priority", "rationale"]
DECISION = ["decision", "owner", "notes"]
# ACCESS band: reviewer feedback on whether we can actually reach the source (feeds the promotion mapping).
ACCESS = ["can_access", "access_note"]
HEADERS = MACHINE + SUGGEST + DECISION + ACCESS
EDITABLE = set(SUGGEST + DECISION + ACCESS)
DECISIONS = {"approve", "reject", "needs_access", "defer"}
CAN_ACCESS = {"yes", "no", "do_not_collect"}
_PRANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
_SHEET = "Review"


def _machine_row(c, novelty):
    return {
        "candidate_id": c.get("candidate_id"), "novelty": novelty, "priority": c.get("priority"),
        "source_class": c.get("source_class"), "source_subtype": c.get("source_subtype"),
        "source_name": c.get("source_name"), "canonical_url": c.get("canonical_url"),
        "access_status": c.get("access_status"), "legal_status": c.get("legal_status"),
        "url_verified": dget(c.get("url_verification"), "status"),
        "why_relevant": dget(c.get("discovery_basis"), "why_relevant"),
    }


def _prank(c):
    p = c.get("priority")
    return _PRANK.get(p, 9) if isinstance(p, str) else 9


def _scalar(v):
    """Excel cells accept only scalars; coerce a malformed non-scalar (dict/list) to a string so a bad
    record degrades the cell rather than crashing the whole export."""
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    return json.dumps(v, ensure_ascii=False)


def new_candidates(data_root, run_id, *, registry_db=None, only_ids=None):
    """Return (reviewable_candidates_sorted_by_priority, summary) — the run's review delta. If `only_ids` is
    given, the returned rows are restricted to that set (e.g. the DURABLE sources), so the review sheet that
    feeds the registry holds monitoring sources — not one-off evidence/pointers. `summary` stays the full delta.

    A candidate is REVIEWABLE unless the registry ALREADY holds its URL. It used to be selected on
    `novelty == "new"`, which ALSO suppressed `seen_prior_run` — and that silently dropped sources:
    `crossrun.build_prior_index` indexes every OTHER run (later ones, and other countries' runs too — not
    just "an earlier run" as its doc says), so a URL found by two runs was `seen_prior_run` in BOTH and
    therefore appeared in NEITHER review sheet — no run ever filed it. "Another run also saw it" is not
    "we already have it"; only `in_registry` is. Suppressing on that alone is the only safe rule, and the
    promotion layer's UNIQUE(canonical_url) gate + per-run sequencing stop any double-filing.
    """
    cands = crossrun.load_run_candidates(data_root, run_id)
    prior = crossrun.build_prior_index(data_root, run_id)
    registry = crossrun.build_registry_index(registry_db)
    classification = crossrun.classify(cands, prior, registry)   # 1:1 with cands, in candidate order
    summary = crossrun.summarize(classification)
    # Select rows by POSITION (zip), never by candidate_id — duplicate ids must not drop a new row.
    new = [c for c, cl in zip(cands, classification)
           if cl["novelty"] != "in_registry" and (only_ids is None or c.get("candidate_id") in only_ids)]
    new.sort(key=_prank)
    return new, summary


def export_review_workbook(data_root, run_id, out_path, *, registry_db=None, suggestions=None, only_ids=None):
    """Write the run's NEW candidates (the delta, optionally restricted to `only_ids`) to `out_path`, with
    optional pre-filled agent suggestions ({candidate_id -> {suggested_decision, ...}}). Returns
    (out_path, summary)."""
    new, summary = new_candidates(data_root, run_id, registry_db=registry_db, only_ids=only_ids)
    _build_workbook(out_path, run_id, summary, new, suggestions or {})
    return out_path, summary


_SUGGEST_SET = set(SUGGEST)


def _build_workbook(out_path, run_id, summary, new_cands, suggestions):
    wb = Workbook()

    # --- Sheet 1: plain-language instructions (the workbook OPENS here) ---
    info = wb.active
    info.title = "READ ME FIRST"
    intro = [
        ("HOW TO REVIEW THESE SOURCES", ""),
        ("What this is", f"A list of new information sources we found (run {run_id}). "
                         "Your job: decide which ones we should keep and track."),
        ("", ""),
        ("Step 1", "Open the 'Review' tab (the second tab, next to this one)."),
        ("Step 2", "For each row, fill the yellow 'decision' box with ONE of: "
                   "approve / reject / needs_access / defer."),
        ("Step 3", "For every 'approve', also type your name in the yellow 'owner' box."),
        ("Step 4", "The grey columns are information only — you cannot and need not change them."),
        ("Step 5 (optional)", "'can_access' tells us if we can actually reach the source: "
                              "yes = we can (say how in 'access_note'); no = it's blocked; "
                              "do_not_collect = we must not collect it."),
        ("Step 6", "Save the file and send it back. Only your decision + access columns are read; "
                   "everything else is ignored."),
        ("", ""),
        ("Sources to review (in the Review tab)", summary["new"]),
        ("Already seen in an earlier run (not shown)", summary["seen_prior_run"]),
        ("Already in our source list (not shown)", summary["in_registry"]),
        ("Total found in this run", summary["total"]),
    ]
    for r, (k, v) in enumerate(intro, 1):
        info.cell(row=r, column=1, value=k).font = Font(bold=True)
        info.cell(row=r, column=2, value=v)
    info.column_dimensions["A"].width = 40
    info.column_dimensions["B"].width = 96

    # --- Sheet 2: the sources to review ---
    ws = wb.create_sheet(_SHEET)
    hdr_font, hdr_fill = Font(bold=True), PatternFill("solid", fgColor="DDDDDD")
    edit_fill = PatternFill("solid", fgColor="FFF7CC")   # tint the columns the reviewer edits

    for i, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=i, value=h)
        cell.font = hdr_font
        cell.fill = edit_fill if h in EDITABLE else hdr_fill

    for r, c in enumerate(new_cands, start=2):
        mr = _machine_row(c, "new")
        cid = c.get("candidate_id")
        # isinstance(cid, str) guard: an unhashable id (list/dict) would raise in suggestions.get(cid)
        sug = suggestions.get(cid, {}) if (isinstance(suggestions, dict) and isinstance(cid, str)) else {}
        for i, h in enumerate(HEADERS, 1):
            val = sug.get(h) if h in _SUGGEST_SET else mr.get(h)   # agent-suggestion cols from `suggestions`
            cell = ws.cell(row=r, column=i, value=_scalar(val))
            if h in EDITABLE:
                cell.protection = Protection(locked=False)
                cell.fill = edit_fill

    if new_cands:
        last = len(new_cands) + 1
        for col_name, vocab in (("decision", DECISIONS), ("can_access", CAN_ACCESS)):
            col = get_column_letter(HEADERS.index(col_name) + 1)
            dv = DataValidation(type="list", formula1='"%s"' % ",".join(sorted(vocab)), allow_blank=True)
            ws.add_data_validation(dv)
            dv.add(f"{col}2:{col}{last}")

    widths = {"source_name": 34, "canonical_url": 48, "why_relevant": 52, "rationale": 40, "notes": 30,
              "can_access": 16, "access_note": 40}
    for i, h in enumerate(HEADERS, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 15)
    ws.freeze_panes = "B2"
    ws.protection.sheet = True     # locks the machine columns in Excel (advisory; import also ignores them)

    wb.save(out_path)


def _counts(decisions):
    c = Counter(d["decision"] for d in decisions)
    return {k: c.get(k, 0) for k in sorted(DECISIONS)}


def _open_review_sheet(xlsx_path):
    """Load a review sheet -> (idx {header:col}, data_rows, header_errors), or (None, None, error_result) if
    the file is unreadable / empty / not a review sheet. TOTAL: never raises."""
    try:
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        ws = wb[_SHEET] if _SHEET in wb.sheetnames else wb.active
        rows = list(ws.iter_rows(values_only=True))
        wb.close()
    except Exception as ex:  # noqa: BLE001
        return None, None, {"decisions": [], "errors": [{"error": f"unreadable workbook: {ex}"}], "counts": _counts([])}
    if not rows:
        return None, None, {"decisions": [], "errors": [{"error": "empty sheet"}], "counts": _counts([])}
    headers = [str(h).strip() if h is not None else "" for h in rows[0]]
    idx, dup = {}, []
    for i, h in enumerate(headers):
        if not h:
            continue
        if h in idx:
            dup.append(h)        # first occurrence wins; a duplicate key column is surfaced as an error
        else:
            idx[h] = i
    header_errors = []
    key_dups = sorted({h for h in dup if h in ("candidate_id", "decision", "owner", "notes",
                                               "can_access", "access_note")})
    if key_dups:
        header_errors.append({"error": f"duplicate header column(s) {key_dups}; using the first of each"})
    if "candidate_id" not in idx or "decision" not in idx:
        return None, None, {"decisions": [], "counts": _counts([]),
                            "errors": header_errors + [{"error": "unrecognized sheet (missing candidate_id/decision)"}]}
    return idx, rows[1:], header_errors


def _cell_getter(idx):
    def g(row, name):
        i = idx.get(name)
        v = row[i] if (i is not None and i < len(row)) else None
        return str(v).strip() if v is not None else ""
    return g


def _access_fields(g, row, errors, cid):
    """Read + validate the access columns; append any error and return (can_access, access_note, ok)."""
    ca = g(row, "can_access").lower()
    an = g(row, "access_note")
    if ca and ca not in CAN_ACCESS:
        errors.append({"candidate_id": cid, "error": f"invalid can_access {ca!r}"})
        return None, None, False
    if ca in ("yes", "do_not_collect") and not an:
        errors.append({"candidate_id": cid, "error": f"can_access={ca} requires an access_note"})
        return None, None, False
    return ca or None, an or None, True


def import_review_decisions(xlsx_path):
    """Read a returned review workbook -> {decisions, errors, counts}. Only candidate_id + the human decision
    columns are trusted; a blank decision = undecided (skipped)."""
    idx, data_rows, header = _open_review_sheet(xlsx_path)
    if idx is None:
        return header
    errors, g = list(header), _cell_getter(idx)
    decisions, seen = [], set()
    for row in data_rows:
        cid = g(row, "candidate_id")
        if not cid:
            continue
        dec = g(row, "decision").lower()
        if not dec:
            continue   # undecided -> not a decision
        if cid in seen:   # a second decision row for the same candidate is a conflict, not a silent 2nd vote
            errors.append({"candidate_id": cid, "error": "duplicate candidate_id (multiple decision rows)"})
            continue
        seen.add(cid)
        if dec not in DECISIONS:
            errors.append({"candidate_id": cid, "error": f"invalid decision {dec!r}"})
            continue
        owner, notes = g(row, "owner"), g(row, "notes")
        if dec == "approve" and not owner:
            errors.append({"candidate_id": cid, "error": "approve requires an owner"})
            continue
        ca, an, ok = _access_fields(g, row, errors, cid)
        if not ok:
            continue
        decisions.append({"candidate_id": cid, "decision": dec, "owner": owner or None, "notes": notes or None,
                          "can_access": ca, "access_note": an})
    return {"decisions": decisions, "errors": errors, "counts": _counts(decisions)}


def import_effective_decisions(xlsx_path, *, default_owner="auto:pipeline"):
    """Human review is OPTIONAL: for each candidate use the HUMAN's decision if they filled one, else fall
    back to the LLM's `suggested_decision`. So the registry stays current with or without a human. A HUMAN
    approve still needs a human owner; an LLM-DEFAULT approve is attributed to `default_owner` (the pipeline is
    accountable). Each decision is tagged `decided_by` = human|llm. TOTAL. This is the auto-sync's reader —
    the human just edits the Excel; the machine applies the effective decisions with no human-run script."""
    idx, data_rows, header = _open_review_sheet(xlsx_path)
    if idx is None:
        return header
    errors, g = list(header), _cell_getter(idx)
    decisions, seen = [], set()
    for row in data_rows:
        cid = g(row, "candidate_id")
        if not cid:
            continue
        human = g(row, "decision").lower()
        if human and human not in DECISIONS:
            errors.append({"candidate_id": cid, "error": f"invalid decision {human!r}"})
            continue
        llm = g(row, "suggested_decision").lower()
        dec = human if human in DECISIONS else (llm if llm in DECISIONS else None)
        if not dec:
            continue   # neither a human nor a valid LLM decision -> nothing to apply
        if cid in seen:
            errors.append({"candidate_id": cid, "error": "duplicate candidate_id (multiple rows)"})
            continue
        seen.add(cid)
        from_human = human in DECISIONS
        owner, notes = g(row, "owner"), g(row, "notes")
        if dec == "approve" and not owner:
            if from_human:
                errors.append({"candidate_id": cid, "error": "human approve requires an owner"})
                continue
            owner = default_owner   # LLM-default approve -> the pipeline is the accountable owner
        ca, an, ok = _access_fields(g, row, errors, cid)
        if not ok:
            continue
        decisions.append({"candidate_id": cid, "decision": dec, "owner": owner or None, "notes": notes or None,
                          "can_access": ca, "access_note": an, "decided_by": "human" if from_human else "llm"})
    return {"decisions": decisions, "errors": errors, "counts": _counts(decisions)}


def write_decisions_jsonl(out_path, decisions):
    Path(out_path).write_text("".join(json.dumps(d, sort_keys=True, ensure_ascii=False) + "\n" for d in decisions),
                              encoding="utf-8")
    return str(out_path)
