"""Route a run's candidates into the FINAL right-sized outputs, using grouping (consolidate) + role verdicts.

Deterministic and TOTAL. Every candidate lands in exactly one place - nothing is dropped:
  - durable  : the monitoring list, grouped by ENTITY (each = keep channels + folded endpoints). This is
               the short, analyst-facing source list.
  - evidence : one-off articles / case studies / PDFs -> the evidence ledger (the seed of the Evidence layer).
  - pointers : directories/member-lists to mine ONCE then archive.
  - marginal : low-yield or an endpoint with no kept parent -> flagged for a human cut.

Role vocabulary consumed (the analyst-panel / LLM verdicts): keep, fold_into_parent, evidence_not_source,
pointer_once, marginal. The deterministic classifier's 'durable_source' is treated as 'keep'. Unknown/missing
-> marginal. This module makes NO judgement - it only routes given verdicts.
"""
from consolidate import group_candidates

_KEEP = {"keep", "durable_source"}
# route may be fed EITHER vocabulary: the LLM analyst verdicts (ROLE_VERDICTS: evidence_not_source /
# pointer_once) OR the deterministic fallback prelabel.source_role() (evidence / pointer). Alias the latter
# onto the former so a fallback role can never fall through into NO bucket (route's "nothing is dropped").
_ROLE_ALIASES = {"evidence": "evidence_not_source", "pointer": "pointer_once"}


def _ref(c, g):
    c = c if isinstance(c, dict) else {}
    return {"candidate_id": c.get("candidate_id"), "entity": g["entity"], "entity_name": g["entity_name"],
            "source_name": c.get("source_name"), "canonical_url": c.get("canonical_url"),
            "why_relevant": (c.get("discovery_basis") or {}).get("why_relevant")
            if isinstance(c.get("discovery_basis"), dict) else None}


def route(candidates, role_by_id, groups=None):
    """Return {durable, evidence, pointers, marginal} + summary. `role_by_id` maps candidate_id -> role."""
    groups = groups if groups is not None else group_candidates(candidates)
    roles = role_by_id if isinstance(role_by_id, dict) else {}
    by_id = {c["candidate_id"]: c for c in candidates
             if isinstance(c, dict) and isinstance(c.get("candidate_id"), str)}

    def rol(cid):
        r = roles.get(cid)
        r = r if isinstance(r, str) else "marginal"
        return _ROLE_ALIASES.get(r, r)

    durable, evidence, pointers, marginal = [], [], [], []
    for g in groups:
        members = g["member_ids"]
        keeps = [m for m in members if rol(m) in _KEEP]
        folds = [m for m in members if rol(m) == "fold_into_parent"]
        if keeps:
            primary = g["primary_id"] if g["primary_id"] in (keeps + folds) else (keeps + folds)[0]
            durable.append({"entity": g["entity"], "entity_name": g["entity_name"], "primary_id": primary,
                            "channel_ids": keeps, "endpoint_ids": folds})
        else:
            marginal.extend(_ref(by_id.get(m), g) for m in folds)   # endpoints with no kept parent -> flag
        for m in members:
            r = rol(m)
            if r == "evidence_not_source":
                evidence.append(_ref(by_id.get(m), g))
            elif r == "pointer_once":
                pointers.append(_ref(by_id.get(m), g))
            elif r == "marginal":
                marginal.append(_ref(by_id.get(m), g))

    summary = {
        "durable_entities": len(durable),
        "durable_channels": sum(len(d["channel_ids"]) for d in durable),
        "endpoints_folded": sum(len(d["endpoint_ids"]) for d in durable),
        "evidence": len(evidence),
        "pointers": len(pointers),
        "marginal": len(marginal),
    }
    return {"durable": durable, "evidence": evidence, "pointers": pointers, "marginal": marginal,
            "summary": summary}


def write_ledgers(routed, out_dir):
    """Write the evidence / pointer / marginal ledgers as JSONL (routed, not lost). Returns {key: path}."""
    import json
    import os
    _FILES = {"evidence": "evidence_ledger", "pointers": "pointer_queue", "marginal": "marginal_flagged"}
    paths = {}
    for key, fname in _FILES.items():
        p = os.path.join(out_dir, f"{fname}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for x in routed.get(key, []):
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
        paths[key] = p
    return paths


def write_durable_workbook(routed, candidates, out_path):
    """Write the durable monitoring list to .xlsx: one section per entity (PRIMARY + channels + endpoints)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter

    by_id = {c["candidate_id"]: c for c in candidates
             if isinstance(c, dict) and isinstance(c.get("candidate_id"), str)}
    HEADERS = ["entity", "role", "priority", "source_class", "source_subtype", "source_name",
               "canonical_url", "url_verified", "why_relevant"]
    wb = Workbook(); ws = wb.active; ws.title = "Durable Sources"
    for i, h in enumerate(HEADERS, 1):
        ws.cell(1, i, h).font = Font(bold=True)
    pf, cf = PatternFill("solid", fgColor="D8E4BC"), PatternFill("solid", fgColor="F2F2F2")

    def _c(v):
        return v if v is None or isinstance(v, (str, int, float, bool)) else str(v)

    r = 2
    for d in routed.get("durable", []):
        ids = list(d["channel_ids"]) + list(d["endpoint_ids"])
        for j, cid in enumerate(ids):
            c = by_id.get(cid, {})
            prim = cid == d["primary_id"]
            role = "PRIMARY" if prim else ("channel" if cid in d["channel_ids"] else "endpoint")
            uv = c.get("url_verification"); db = c.get("discovery_basis")
            vals = [d["entity_name"] if j == 0 else "", role, c.get("priority"), c.get("source_class"),
                    c.get("source_subtype"), c.get("source_name"), c.get("canonical_url"),
                    uv.get("status") if isinstance(uv, dict) else None,
                    db.get("why_relevant") if isinstance(db, dict) else None]
            for i, v in enumerate(vals, 1):
                cell = ws.cell(r, i, _c(v))
                cell.fill = pf if prim else cf
                if prim:
                    cell.font = Font(bold=True)
            r += 1
    widths = {"entity": 28, "source_name": 46, "canonical_url": 50, "why_relevant": 50}
    for i, h in enumerate(HEADERS, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 14)
    ws.freeze_panes = "A2"
    wb.save(out_path)
    return out_path
