#!/usr/bin/env python3
"""Campaign driver — hand out ONE pending (scope, workstream) set at a time, and track progress.

The scheduled task calls `--next` to get the next set to scout (fully resolved: discovery args + the exact
commands to run), scouts it, then calls `--complete <scope> <ws>`. Progress lives in a durable state file, so
each fresh scheduled run knows exactly what's left. First pass = one round per set (research_plan.yaml).

    python scripts/campaign.py --next               # -> JSON descriptor for the next set (or {"done_all": true})
    python scripts/campaign.py --complete GR A2      # mark a set done
    python scripts/campaign.py --status              # progress summary

ASSIGNMENT — the ownership fence. This machine may only work the scopes named in
`data/campaign_assignment.json`: {"owner": "<name>", "scopes": ["CZ", "HU", ...]}. Two people can therefore
split the SAME plan by giving each machine a different, non-overlapping list — neither driver can hand out,
or tick off, the other's countries, so unattended overnight runs cannot collide or duplicate work.
A MISSING or EMPTY assignment file STOPS the campaign with an explanation. It never falls back to "run
everything": an unbounded default is precisely the silent-skip failure this project exists to prevent
(CLAUDE.md rule 2 — a stage that cannot run stops the pipeline; rule 7 — a silent bound may not exist).
"""
import argparse
import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "scripts"))
sys.path.insert(0, str(_ROOT / "review"))
import scout_config  # noqa: E402

PLAN = _ROOT / "research_plan.yaml"
STATE = _ROOT / "data" / "campaign_state.json"
ASSIGNMENT = _ROOT / "data" / "campaign_assignment.json"
_SET_RE = re.compile(r"scope:\s*([A-Za-z]+).*?workstream:\s*(A\d).*?runs:\s*(\d+)")


def parse_plan():
    """[(scope, workstream, seeded_runs)] from research_plan.yaml's `sets:` block (no PyYAML needed)."""
    out, in_sets = [], False
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "sets:":
            in_sets = True
            continue
        if in_sets:
            if s and not s.startswith("-") and not s.startswith("#") and ":" in s and not s.startswith("{"):
                break                                  # left the sets block
            m = _SET_RE.search(line)
            if m:
                out.append((m.group(1), m.group(2), int(m.group(3))))
    return out


def _key(s, w):
    return f"{s}:{w}"


def _fail(message, **extra):
    """Stop LOUDLY: a machine-readable line on stdout AND a non-zero exit, so neither a scheduled agent nor a
    human can mistake a refusal for 'nothing left to do'."""
    print(json.dumps({"error": message, **extra}, ensure_ascii=False))
    raise SystemExit(2)


def load_assignment(path=None):
    """(owner, {scopes}) that THIS machine owns. Missing/empty/unreadable/unknown-scope => stop, never 'all'."""
    p = Path(path) if path else ASSIGNMENT
    if not p.exists():
        _fail("No assignment file at {0}. This machine has not been told which countries it owns, so the "
              "campaign will not hand out any work. Create it as: "
              '{{"owner": "<your name>", "scopes": ["CZ", "HU"]}} — ISO-2 country codes, or a region code '
              "(GLOBAL, EU, CEE, US, APAC), exactly as they appear in research_plan.yaml.".format(p),
              assignment_path=str(p))
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        _fail("Assignment file {0} could not be read: {1}".format(p, exc), assignment_path=str(p))
    if not isinstance(d, dict):
        _fail("Assignment file {0} must be a JSON object with a 'scopes' list.".format(p),
              assignment_path=str(p))
    scopes = {str(s).strip().upper() for s in (d.get("scopes") or []) if str(s).strip()}
    if not scopes:
        _fail("Assignment file {0} names no scopes. Add at least one country code to 'scopes' — with an empty "
              "list this machine has nothing to work on.".format(p), assignment_path=str(p))
    unknown = sorted(scopes - {s for s, _w, _r in parse_plan()})
    if unknown:
        _fail("Assignment file {0} names scopes that are not in research_plan.yaml: {1}. Fix the codes (or add "
              "those sets to the plan) — a typo here would silently do nothing.".format(p, ", ".join(unknown)),
              assignment_path=str(p), unknown_scopes=unknown)
    return (d.get("owner") or "unnamed"), scopes


def _ip_tuple(ip):
    """(scope, workstream, run_id|None) from in_progress — a dict (current) or a legacy [scope, ws] list."""
    if isinstance(ip, dict):
        return (ip.get("scope"), ip.get("workstream"), ip.get("run_id"))
    if isinstance(ip, list) and len(ip) >= 2:
        return (ip[0], ip[1], ip[2] if len(ip) > 2 else None)
    return None


_PRIORITY = _ROOT / "data" / "campaign_priority.json"


def _priority_sets():
    """(scope, workstream) sets to run BEFORE normal plan order — e.g. finish one country first. [] if none.

    File `data/campaign_priority.json`: {"priority": [["GR","A1"], ...]}. Done sets are skipped automatically,
    so the list self-clears; delete or empty the file to drop back to pure plan order."""
    if not _PRIORITY.exists():
        return []
    try:
        d = json.loads(_PRIORITY.read_text(encoding="utf-8"))
        items = d.get("priority") if isinstance(d, dict) else d
        return [(x[0], x[1]) for x in (items or []) if isinstance(x, (list, tuple)) and len(x) >= 2]
    except (ValueError, OSError, TypeError):
        return []


def _priority_stop():
    """True if the priority file asks the campaign to PAUSE once the priority block is done (don't roll on)."""
    if not _PRIORITY.exists():
        return False
    try:
        d = json.loads(_PRIORITY.read_text(encoding="utf-8"))
        return bool(isinstance(d, dict) and d.get("stop_when_done"))
    except (ValueError, OSError, TypeError):
        return False


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    # first time: sets the plan already marks as seeded (runs>0, e.g. GR/A2) count as done
    done = [[s, w] for s, w, r in parse_plan() if r > 0]
    return {"done": done, "in_progress": None}


def save_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=2), encoding="utf-8")


def _descriptor(scope, ws, run_id=None):
    cfg = scout_config.build(iso=scope, workstream=ws, run_id=run_id)   # resolves name/languages/run_id/db/topics
    dr, run = cfg["data_root"], cfg["run_id"]
    q = lambda p: f'"{p}"'
    return {
        "scope": scope, "workstream": ws, "workstream_label": cfg["workstream_label"], "run_id": run,
        "discovery_args": {
            "country": cfg["country"], "country_name": cfg["country_name"], "sector": "both",
            "workstreams": [ws], "topics": cfg["topics"], "languages": cfg["languages"],
            "run_id": run, "data_root": dr, "min_cells": 10, "max_cells": 16,
        },
        "ingest_cmd": f'python scripts/round_ingest.py --run-id {run} --config {q(cfg["config_path"])} --promotion-db {q(cfg["promotion_db"])}',
        "label_batch_dir": f'{dr}/run_logs/{run}/agent_inputs/label_batches',
        "labeling_scope": f'{cfg["country_name"]} {ws} {cfg["workstream_label"]}',
        "finalize_cmd": f'python scripts/round_finalize.py --run-id {run} --config {q(cfg["config_path"])} --promotion-db {q(cfg["promotion_db"])}',
        "complete_cmd": f'python scripts/campaign.py --complete {scope} {ws}',
        "deliverable": cfg["deliverable_name"],
    }


def cmd_next():
    owner, mine = load_assignment()                # stops here if this machine has not been given any scopes
    st = load_state()
    done = {_key(*d) for d in st.get("done", [])}
    ip = _ip_tuple(st.get("in_progress"))
    if ip and ip[0] in mine and _key(ip[0], ip[1]) not in done:   # left mid-run -> RESUME it with its OWN run_id
        print(json.dumps({**_descriptor(ip[0], ip[1], run_id=ip[2]), "resumed": True, "owner": owner},
                         ensure_ascii=False))
        return 0
    prio = [(s, w) for s, w in _priority_sets() if s in mine]     # never jump the queue into another machine's work
    for s, w in prio:                              # jump the queue: finish these first (e.g. all of Greece)
        if _key(s, w) in done:
            continue
        desc = _descriptor(s, w)
        st["in_progress"] = {"scope": s, "workstream": w, "run_id": desc["run_id"]}
        save_state(st)
        print(json.dumps({**desc, "priority": True, "owner": owner}, ensure_ascii=False))
        return 0
    if prio and _priority_stop() and all(_key(s, w) in done for s, w in prio):
        print(json.dumps({"paused_after_priority": True, "owner": owner,   # priority block done + pause requested
                          "message": "Priority block complete (e.g. Greece); campaign PAUSED as requested. "
                                     "Delete or empty data/campaign_priority.json to resume broad coverage."}))
        return 0
    for s, w, _r in parse_plan():
        if s not in mine or _key(s, w) in done:     # someone else's scope, or already done
            continue
        desc = _descriptor(s, w)                    # mints the run_id...
        st["in_progress"] = {"scope": s, "workstream": w, "run_id": desc["run_id"]}   # ...remembered, so a resume
        save_state(st)                              # continues this same run instead of re-discovering from scratch
        print(json.dumps({**desc, "owner": owner}, ensure_ascii=False))
        return 0
    print(json.dumps({"done_all": True, "owner": owner, "scopes": sorted(mine),
                      "completed": len([d for d in st.get("done", []) if d[0] in mine]),
                      "message": "Every set assigned to this machine ({0}) is done. The other scopes in "
                                 "research_plan.yaml belong to another machine and are deliberately not "
                                 "picked up.".format(", ".join(sorted(mine)))}, ensure_ascii=False))
    return 0


def cmd_complete(scope, ws):
    owner, mine = load_assignment()
    scope = scope.upper()
    if scope not in mine:                          # code decides, not the agent (CLAUDE.md rule 8)
        _fail("{0} is not assigned to this machine — {1} owns: {2}. Refusing to mark it done: that set belongs "
              "to another machine's run, and ticking it off here would hide work that was never done."
              .format(scope, owner, ", ".join(sorted(mine))),
              scope=scope, workstream=ws, owner=owner, scopes=sorted(mine))
    st = load_state()
    if [scope, ws] not in st["done"]:
        st["done"].append([scope, ws])
    ip = _ip_tuple(st.get("in_progress"))
    if ip and ip[0] == scope and ip[1] == ws:
        st["in_progress"] = None
    save_state(st)
    total = len([1 for s, _w, _r in parse_plan() if s in mine])
    mine_done = len([d for d in st["done"] if d[0] in mine])
    print(json.dumps({"completed": [scope, ws], "owner": owner, "done": mine_done, "total": total,
                      "remaining": total - mine_done}))
    return 0


def cmd_status():
    owner, mine = load_assignment()
    st = load_state()
    plan = parse_plan()
    my_sets = [(s, w) for s, w, _r in plan if s in mine]
    done_keys = {_key(*d) for d in st.get("done", [])}
    my_left = [f"{s}/{w}" for s, w in my_sets if _key(s, w) not in done_keys]
    print(json.dumps({
        "owner": owner, "scopes": sorted(mine),
        "done": len(my_sets) - len(my_left), "total": len(my_sets), "remaining": len(my_left),
        "remaining_sets": my_left, "in_progress": st.get("in_progress"),
        "plan_total_all_machines": len(plan),
        "note": "Counts cover THIS machine's assigned scopes only; the rest of research_plan.yaml belongs to "
                "another machine (see data/campaign_assignment.json).",
    }, indent=2, ensure_ascii=False))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Source-scouting campaign driver.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--next", action="store_true", help="descriptor for the next pending set")
    g.add_argument("--complete", nargs=2, metavar=("SCOPE", "WS"), help="mark a set done")
    g.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)
    if args.next:
        return cmd_next()
    if args.complete:
        return cmd_complete(args.complete[0], args.complete[1].upper())
    return cmd_status()


if __name__ == "__main__":
    raise SystemExit(main())
