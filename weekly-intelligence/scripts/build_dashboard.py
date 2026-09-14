#!/usr/bin/env python3
"""
build_dashboard.py - Compute the Printec weekly intelligence "DASH" payload and render outputs.

Reads the structured cache produced by ingest.py (data/*.json) plus the curated references
(references/*.json), computes the four strategic lenses, and emits:

  1. dashboard-data.json          the DASH payload the live web app renders (published to Vercel)
  2. <assets>/data.json           refreshed bundled snapshot for the web app (optional)

The UI lives ONCE in dashboard-web/ (index.html + styles.css + app.js) — the live web app on
Vercel. That is the only dashboard; there is no offline/single-file build.

All aggregation is arithmetic over values that already exist in the source files. Signal
"strength" is a transparent confidence/agent/likelihood weighting (see ingest.score_signal),
NOT a market size or budget. The dashboard never displays a number that isn't traceable to a
source row.

Usage:
  python build_dashboard.py --data <cache> [--week YYYY-MM-DD]
                            [--refs <refs>] [--assets <dashboard-web dir>]
"""
import argparse, json, os, sys, datetime, re

def load(p, d=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return d

# ---------- evidence-file labelling (findings/NN-topic/<date>.md) ----------
_FINDING_TOPIC = {
    "01-bank-disclosures": "Bank disclosures",
    "02-tenders":          "Tenders & procurement",
    "03-regulation":       "Regulation",
    "04-statistics":       "Market statistics",
    "05-jobs":             "Jobs & leadership",
    "06-vendors":          "Competitors & partners",
}

def evidence_label(path):
    """Human label for a finding file, e.g. 'findings/01-bank-disclosures/..' -> 'Bank disclosures (A1)'."""
    parts = (path or "").split("/")
    folder = parts[1] if len(parts) > 1 else ""
    num = folder[:2]
    agent = ("A" + num.lstrip("0")) if num.isdigit() else ""
    topic = _FINDING_TOPIC.get(folder)
    if not topic:
        t = folder[3:] if (len(folder) > 3 and folder[:2].isdigit() and folder[2] == "-") else folder
        topic = t.replace("-", " ").strip().capitalize() or "Evidence file"
    return topic + (" (" + agent + ")" if agent else "")

_FIT_FIELDS = ("projection", "cagr_pct", "slope_per_year", "r2", "fit_quality", "inflection", "method",
               "projection_to", "extrapolation_years", "horizon_reason", "last_year", "last_value")

def _strip_fit(rows, anchors):
    """Drop every trend-fit field from the baseline rows and attach the row's anchor point."""
    by = {(a["country"], a["metric"]): a for a in anchors}
    out = []
    for r in rows:
        r = {k: v for k, v in r.items() if k not in _FIT_FIELDS}
        # other organisations' projected points are theirs, not a fit; keep them, they are drawn as ×
        a = by.get((r.get("country"), r.get("metric")))
        if a:
            r["anchor"] = {k: a[k] for k in ("year", "value", "n", "points", "provisional")}
        out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", help="Engine folder with references/ (default: this script's parent)")
    ap.add_argument("--refs", help="Reference JSON folder (default: <skill>/references)")
    ap.add_argument("--data", help="Cache folder written by ingest.py (default: <skill>/data)")
    ap.add_argument("--assets", help="dashboard-web folder (default: <root>/dashboard-web)")
    ap.add_argument("--out", help="DEPRECATED, ignored — the offline single-file build was removed; "
                                  "only the live web app is produced.")
    ap.add_argument("--week", default=None)
    args = ap.parse_args()

    skill = args.skill or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    D = os.path.abspath(args.data or os.path.join(skill, "data"))
    R = args.refs or os.path.join(skill, "references")
    # The web assets normally sit beside the cache at <root>/dashboard-web (D = <root>/intel-cache);
    # try one level up too, then fall back to the first candidate for the warning message.
    if args.assets:
        assets = args.assets
    else:
        cands = [os.path.join(os.path.dirname(D), "dashboard-web"),
                 os.path.join(os.path.dirname(os.path.dirname(D)), "dashboard-web")]
        assets = next((c for c in cands if os.path.isdir(c)), cands[0])
    signals     = load(os.path.join(D, "signals.json"), [])
    series      = load(os.path.join(D, "series.json"), {})
    events      = load(os.path.join(D, "events.json"), [])
    patterns    = load(os.path.join(D, "patterns.json"), [])
    cstats      = load(os.path.join(D, "country_stats.json"), [])
    summary     = load(os.path.join(D, "summary.json"), {})
    forecast    = load(os.path.join(D, "forecast.json"), {"forecasts": [], "accuracy": {}, "coverage": []})
    narrative   = load(os.path.join(D, "forecast_narrative.json"), {"outlooks": []})
    verification = load(os.path.join(D, "verification.json"), {"summary": {}, "files": {}})
    outlook_val  = load(os.path.join(D, "outlook_validation.json"), {"validated": []})   # independent traceability audit
    futures_val  = load(os.path.join(D, "futures_validation.json"), {"futures": []})     # independent audit of the Futurist 2-5yr calls
    competitor_series = load(os.path.join(D, "competitor_series.json"), {})              # SEC EDGAR competitor financials
    futures_narr = load(os.path.join(D, "futures_narrative.json"), {"futures": []})       # Agent 8 (Futurist) 3-5yr outlooks
    rbr_series   = load(os.path.join(D, "rbr_series.json"), {})                            # RBR per-country current-trends series (deep-read, internal)
    comp_brief   = load(os.path.join(D, "competition_brief.json"), {})                     # Orchestrator-authored plain-English competitor/partner brief (Overview "Competition & partners — this week")
    competition_brief = comp_brief.get("brief", "") if isinstance(comp_brief, dict) else (comp_brief if isinstance(comp_brief, str) else "")
    atm_market   = load(os.path.join(D, "atm_market.json"), {})                            # deep-read RBR ATM-market series (per-country history + 2028 forecast) for the dedicated Products ATM section
    derived_raw  = load(os.path.join(D, "derived_opportunities.json"), {})                  # INDIRECT opportunities: plays composed from 2+ signals that no single signal states
    proj_lines   = load(os.path.join(D, "projection_lines.json"), {})                     # signals + patterns projection lines (project_lines.py)
    patterns_kb  = load(os.path.join(D, "patterns_kb.json"), [])                          # KB-mined structural patterns (orchestrator-maintained), merged after the hand workbook Patterns sheet
    footprint   = load(os.path.join(R, "footprint.json"), {})
    pmap        = load(os.path.join(R, "product_map.json"), {})
    competitors = load(os.path.join(R, "competitors.json"), {})
    regcal      = load(os.path.join(R, "reg_calendar.json"), {})

    # Fail fast with a clear message if a required reference file is missing/empty (else we'd crash
    # later on a bare KeyError deep in the aggregation).
    missing = []
    if not footprint.get("countries"):   missing.append("footprint.json (countries)")
    if not pmap.get("categories"):       missing.append("product_map.json (categories)")
    if not competitors.get("vendors"):   missing.append("competitors.json (vendors)")
    if not regcal.get("items"):          missing.append("reg_calendar.json (items)")
    if missing:
        sys.exit("ERROR: missing/empty reference data: " + "; ".join(missing) + " (looked in " + R + ")")

    week = args.week or summary.get("week") or datetime.date.today().isoformat()
    try:
        run_date = datetime.date.fromisoformat(week)
    except ValueError:
        sys.exit("ERROR: --week must be a valid YYYY-MM-DD date, got: " + str(week))

    code2name = {c["code"]: c["name"] for c in footprint["countries"]}

    # ---- footprint scope gate -------------------------------------------------
    # footprint.json is the single source of truth for which markets are in scope.
    # A signal whose countries lie ENTIRELY outside it (e.g. Austria, removed
    # 2026-09-02) is dropped here rather than deleted from signals.json, so the
    # historical record survives while nothing out-of-scope is counted, ranked or
    # shown. NOTE: footprint_wide alone does not rescue a signal — a row tagged
    # footprint_wide but carrying only out-of-scope countries is not footprint-wide.
    _INSCOPE = set(code2name)
    # Wording that means "this is not about one market" rather than "the resolver failed".
    _WIDE_WORDS = ("footprint", "emea", "eu-wide", "europe", "european", "sepa", "ssm",
                   "cross-border", "all markets", "region", "global", "worldwide")

    def _in_scope(sig):
        cs = sig.get("countries") or []
        if cs:
            return bool(_INSCOPE.intersection(cs))
        # No resolved code. That used to mean "cross-market, keep it" — but the resolver only knows
        # FOOTPRINT countries, so once Austria left the footprint every Austrian row also stopped
        # resolving and twelve of them came back in through this branch, three of them flagged
        # footprint-wide. A row that NAMES a market the resolver cannot place is naming a market
        # outside the footprint; only genuinely cross-market wording stays.
        raw = (sig.get("country_raw") or "").strip().lower()
        if not raw:
            return True
        return any(w in raw for w in _WIDE_WORDS)
    _n0 = len(signals)
    signals = [x for x in signals if _in_scope(x)]
    if len(signals) != _n0:
        print("scope: dropped %d signal(s) outside the %d-country footprint (kept in signals.json)"
              % (_n0 - len(signals), len(_INSCOPE)))

    prod_label = {c["id"]: c["label"] for c in pmap["categories"]}
    prod_printec = {c["id"]: c["printec"] for c in pmap["categories"]}
    cstat_by_code = {c["code"]: c for c in cstats if c.get("code")}

    # ---------- provenance (trust pass): evidence-base reachability + the actual source trail ----------
    # verify.py already re-fetched every cited URL and snapshotted the reachable ones. Surface that so a
    # reader can click from a signal to its sources: per signal we keep the counts + which finding files it
    # cites; the full per-file source list (url + status + snapshot) is emitted ONCE in `evidence_files`
    # (keyed by finding path) so the dashboard can join without duplicating it onto every signal.
    vfiles = verification.get("files", {})
    evidence_files = {}
    for fp, fi in vfiles.items():
        evidence_files[fp] = {
            "label": evidence_label(fp),
            "total": fi.get("total", 0),
            "reachable": fi.get("reachable", 0),
            "checked": fi.get("checked_at"),
            "sources": [{"url": x.get("url", ""), "status": x.get("status", ""),
                         "code": x.get("code"), "snapshot": x.get("snapshot")}
                        for x in fi.get("sources", [])],
        }
    # Per-signal evidence is CARD-SCOPED, not file-scoped. The trail used to fan each card out to every URL in
    # the whole agent finding files it cited ("159 of 173 reachable") — noise the reader can't triage. Instead
    # we keep only the sources THIS card actually cites: the specific links in its Source cell PLUS any inline
    # [label](url) in the card's own text fields, each with its own reachability (looked up by URL in the
    # verification map). The whole agent files stay as a demoted "working notes" pointer (`cites`), never an
    # expanded dump. `sources`/`reachable` now count the card's OWN cited links (so the badge reads e.g. "7 of 8").
    vurls = verification.get("urls", {})
    checked_date = (verification.get("checked_utc") or "")[:10] or None
    def _src_meta(u):
        r = vurls.get(u) or {}
        return {"status": r.get("status", ""), "code": r.get("code"), "snapshot": r.get("snapshot")}
    # markdown [label](url | findings-ref), or a bare http(s) url not already inside a markdown link
    _LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+|findings/\d\d-[a-z0-9-]+/[A-Za-z0-9._-]+\.md)\)"
                          r"|(?<![\(\w])(https?://[^\s)\]]+)")
    def _card_links(text):
        out = []
        for m in _LINK_RE.finditer(text or ""):
            if m.group(2):   out.append((m.group(1), m.group(2)))
            elif m.group(3): out.append((None, m.group(3)))
        return out
    def _add_src(label, url, cited, cites, seen):
        url = (url or "").rstrip(".,;)")
        if not url or url in seen:
            return
        seen.add(url)
        if url.startswith("findings/"):
            cites.append(url)
        else:
            cited.append({"label": (label or "").strip(), "url": url, **_src_meta(url)})
    for s in signals:
        cited, cites, seen = [], [], set()
        for src in s.get("sources", []):                       # the structured Source cell
            _add_src(src.get("text"), src.get("url"), cited, cites, seen)
        blob = " ".join(str(s.get(k, "") or "") for k in ("signal", "implies", "likelihood", "follow_up"))
        for label, url in _card_links(blob):                   # inline citations in the card's own text
            _add_src(label, url, cited, cites, seen)
        ctot = len(cited)
        creach = sum(1 for c in cited if c.get("status") == "ok")
        status = ("unaudited" if not cited and not cites else
                  "broken"   if ctot and creach == 0 else
                  "strong"   if ctot and creach / ctot >= 0.8 else
                  "thin"     if ctot else
                  "filed")   # specific source links live only in the agent working file(s)
        s["provenance"] = {"cited": cited, "cites": cites, "files": len(cites),
                           "sources": ctot, "reachable": creach,
                           "status": status, "checked": checked_date}

    # ---------- outlook evidence (let a reader trace each reasoned call to its sources) ----------
    # Each outlook is analyst synthesis OF specific signals + agent findings, and already names them inline
    # (e.g. "(A4)"). Attach the REAL supporting signal keys + finding-file paths so the dashboard can render
    # the same clickable evidence trail it shows on signal cards. Prefer explicit citations on the outlook
    # (cite_signals / cite_files / primary_url — written by the orchestrator or the grounding workflow); fall
    # back to the inline agent tags, then to this country's signals, so EVERY outlook gets a source trail.
    finding_by_agent = {}
    for fp in vfiles:
        m = re.match(r"findings/(0\d)-", fp)
        if m:
            finding_by_agent.setdefault(m.group(1), []).append(fp)
    sig_by_key = {s["key"]: s for s in signals}
    name2codes = {}
    for c in footprint["countries"]:
        name2codes.setdefault(c["name"], set()).add(c["code"])
    def _agent_docs(text):
        out = []
        for n in set(re.findall(r"\bA([1-8])\b", text or "") + re.findall(r"Agent\s*([1-8])", text or "")):
            out += finding_by_agent.get("0" + n, [])
        return out
    # the independent validator's verdict (outlook_validation.json), keyed by oid — authoritative over the
    # orchestrator's own self-reported cite_ungrounded when present (an author is a poor proofreader of itself).
    val_by_oid = {v.get("oid"): v for v in outlook_val.get("validated", [])}
    def _enrich_outlook(o):
        skeys = [k for k in (o.get("cite_signals") or o.get("signal_keys") or []) if k in sig_by_key]
        fpaths = [p for p in (o.get("cite_files") or o.get("finding_paths") or []) if p in vfiles]
        if not skeys and not fpaths:                       # fallback 1: parse the inline agent tags
            blob = " ".join([o.get("rationale", "")] + (o.get("drivers") or []))
            fpaths = sorted(set(_agent_docs(blob)))
        for k in skeys:                                    # fold the chosen signals' own finding cites in
            for p in (sig_by_key[k].get("provenance", {}) or {}).get("cites", []):
                if p in vfiles and p not in fpaths:
                    fpaths.append(p)
        if not fpaths:                                     # fallback 2: this country's signals' docs
            codes = name2codes.get(o.get("country"), set())
            for sg in signals:
                if set(sg.get("countries", [])) & codes:
                    for p in (sg.get("provenance", {}) or {}).get("cites", []):
                        if p in vfiles and p not in fpaths:
                            fpaths.append(p)
        # CARD-SCOPED sources (same model as signals): the links the outlook itself cites — inline [label](url)
        # in its projected/rationale/drivers + primary_url + any source_reports — each with reachability; the
        # cited finding files stay as a "working notes" pointer (fpaths), not an expanded per-file dump.
        ocited, oseen = [], set()
        blob = " ".join([o.get("projected", "") or "", o.get("rationale", "") or ""] + [str(x) for x in (o.get("drivers") or [])])
        for lbl, url in _card_links(blob):
            _add_src(lbl, url, ocited, [], oseen)
        if o.get("primary_url"):
            _add_src(None, o["primary_url"], ocited, [], oseen)
        for rep in (o.get("source_reports") or []):
            _add_src(rep.get("label"), rep.get("url"), ocited, [], oseen)
        ctot = len(ocited); creach = sum(1 for c in ocited if c.get("status") == "ok")
        status = ("unaudited" if not ocited and not fpaths else
                  "broken" if ctot and creach == 0 else
                  "strong" if ctot and creach / ctot >= 0.8 else
                  "thin" if ctot else "filed")
        o["evidence"] = {
            "signals": [{"key": k, "bank_theme": sig_by_key[k]["bank_theme"]} for k in skeys],
            "cites": fpaths, "cited": ocited, "primary_url": o.get("primary_url", ""),
            "sources": ctot, "reachable": creach, "checked": checked_date, "status": status,
        }
        # honesty flags (the "⚠ N claim(s) not yet linked to a cited source" caveat): prefer the independent
        # validator's verdict; fall back to the orchestrator's own self-report if the audit didn't run.
        v = val_by_oid.get(o.get("oid"))
        if v is not None:
            o["evidence"]["ungrounded"] = v.get("ungrounded", [])
            o["evidence"]["verdict"]    = v.get("verdict", "")
            o["evidence"]["validated"]  = True
        else:
            o["evidence"]["ungrounded"] = o.get("cite_ungrounded", [])
            o["evidence"]["verdict"]    = o.get("cite_verdict", "")
            o["evidence"]["validated"]  = False
        # lane + recency INHERITED from the cited signals — so the Outlook tab routes owned/incumbent/lost
        # outlooks out of "Biggest near-term opportunities by market" exactly as the signal lanes do, and
        # orders the opportunity outlooks newest development first. An outlook with ANY net-new cited signal
        # stays an opportunity; one citing only owned/incumbent -> installed_base; only competitor-won -> lost.
        lanes = [sig_by_key[k].get("lane") for k in skeys if k in sig_by_key]
        o["lane"] = ("opportunity" if (not lanes or "opportunity" in lanes)
                     else "installed_base" if "installed_base" in lanes
                     else "lost" if "lost" in lanes else "opportunity")
        o["dev_date"] = max((sig_by_key[k].get("dev_date") or sig_by_key[k].get("future_date") or ""
                             for k in skeys if k in sig_by_key), default="")
    # The Outlook tab leads with a PRODUCT-direction layer (one call per Printec line) and shows the per-market
    # calls below; both sets get the identical evidence trail. (product_outlooks: authored by the orchestrator
    # in forecast_narrative.json — see agent-briefs/07-orchestrator.md.)
    outlooks = narrative.get("outlooks", [])
    product_outlooks = narrative.get("product_outlooks", [])
    for o in outlooks + product_outlooks:
        _enrich_outlook(o)
    if not val_by_oid:
        print("warn: no outlook_validation.json — Outlook honesty flags are orchestrator self-reported, NOT "
              "independently validated this run (run weekly-intelligence/workflows/validate-outlooks.workflow.js).")
    else:
        if outlook_val.get("week") and outlook_val.get("week") != week:
            print("warn: outlook_validation.json is for week %s but building %s — validation may be stale."
                  % (outlook_val.get("week"), week))
        miss = [o.get("oid") for o in outlooks + product_outlooks if o.get("oid") not in val_by_oid]
        if miss:
            print("warn: %d outlook(s) not covered by the validator (oids %s) — those fall back to self-report."
                  % (len(miss), miss))

    # ---------- futures (Agent 8 / Futurist 3-5yr outlooks) — same evidence-grounding as the outlooks ----------
    # Authored by the Futurist (futures_narrative.json), rendered in the dashboard's "3-5yr Outlook" tab. Same
    # shape as the orchestrator's outlooks, so reuse the identical trail logic (explicit cites → inline agent
    # tags → the country's signals) and carry the underlying paid/internal reports through as source_reports.
    futures = futures_narr.get("futures", [])
    for o in futures:
        skeys = [k for k in (o.get("cite_signals") or []) if k in sig_by_key]
        fpaths = [p for p in (o.get("cite_files") or []) if p in vfiles]
        if not skeys and not fpaths:
            blob = " ".join([o.get("rationale", "")] + (o.get("drivers") or []))
            fpaths = sorted(set(_agent_docs(blob)))
        for k in skeys:
            for p in (sig_by_key[k].get("provenance", {}) or {}).get("cites", []):
                if p in vfiles and p not in fpaths:
                    fpaths.append(p)
        if not fpaths:
            codes = name2codes.get(o.get("country"), set())
            for sg in signals:
                if set(sg.get("countries", [])) & codes:
                    for p in (sg.get("provenance", {}) or {}).get("cites", []):
                        if p in vfiles and p not in fpaths:
                            fpaths.append(p)
        ocited, oseen = [], set()
        blob = " ".join([o.get("projected", "") or "", o.get("rationale", "") or ""] + [str(x) for x in (o.get("drivers") or [])])
        for lbl, url in _card_links(blob):
            _add_src(lbl, url, ocited, [], oseen)
        if o.get("primary_url"):
            _add_src(None, o["primary_url"], ocited, [], oseen)
        for rep in (o.get("source_reports") or []):
            _add_src(rep.get("label"), rep.get("url"), ocited, [], oseen)
        ctot = len(ocited); creach = sum(1 for c in ocited if c.get("status") == "ok")
        status = ("unaudited" if not ocited and not fpaths else
                  "broken" if ctot and creach == 0 else
                  "strong" if ctot and creach / ctot >= 0.8 else
                  "thin" if ctot else "filed")
        o["evidence"] = {
            "signals": [{"key": k, "bank_theme": sig_by_key[k]["bank_theme"]} for k in skeys],
            "cites": fpaths, "cited": ocited, "primary_url": o.get("primary_url", ""),
            "sources": ctot, "reachable": creach, "checked": checked_date, "status": status,
            "source_reports": o.get("source_reports", []),
        }
    # honesty flags for the futures: an independent auditor (futures_validation.json, keyed by oid) re-read
    # each Futurist call against its cited reports + findings, checked source reachability, and returned a
    # verdict. When present it is authoritative over the unaudited default — same contract as the outlooks.
    fval_by_oid = {f.get("oid"): f for f in futures_val.get("futures", [])}
    for o in futures:
        fv = fval_by_oid.get(o.get("oid"))
        if fv is not None:
            # the validator supplies the honesty verdict only; reachability/sources come from the cited finding
            # files via evidence_files (verify.py snapshots), exactly as for the outlooks — same trail, same DB.
            o["evidence"]["validated"]  = bool(fv.get("validated"))
            o["evidence"]["verdict"]    = fv.get("verdict", "")
            o["evidence"]["ungrounded"] = fv.get("ungrounded", [])
        else:
            o["evidence"]["validated"] = False
    if not fval_by_oid:
        print("warn: no futures_validation.json — the 2-5yr Future-outlook calls are NOT independently "
              "validated this run (run the futures auditor).")

    # ---------- movements (week over week, NOT build over build) ----------
    # _prev_signals_min.json holds the signal set of the last DISTINCT week, the week it represents, and the
    # movements computed for that week. Keying on the week (not just "whatever was built last") means
    # rebuilding/republishing the SAME week does not self-compare to zero or consume the first-week baseline:
    # a same-week rebuild replays the movement it first computed. A genuinely new week compares against the
    # stored prior week, then rolls the snapshot forward.
    prev_path = os.path.join(D, "_prev_signals_min.json")
    stored = load(prev_path, None)
    if isinstance(stored, dict) and "signals" in stored and "week" in stored:
        prev_week = stored.get("week"); prev_sig = stored.get("signals") or {}; prev_moves = stored.get("movements")
    elif isinstance(stored, dict) and stored:
        prev_week = None; prev_sig = stored; prev_moves = None        # legacy flat snapshot (unknown week)
    else:
        prev_week = None; prev_sig = None; prev_moves = None          # no snapshot → first week
    cur_min = {s["key"]: {"confidence": s["confidence"], "bank_theme": s["bank_theme"]} for s in signals}

    def _diff(base):
        mv = {"added": [], "removed": [], "confidence_changed": [], "baseline": False}
        for k, v in cur_min.items():
            if k not in base:
                mv["added"].append(v["bank_theme"])
            elif base[k]["confidence"] != v["confidence"]:
                mv["confidence_changed"].append(
                    {"bank_theme": v["bank_theme"], "from": base[k]["confidence"], "to": v["confidence"]})
        for k, v in base.items():
            if k not in cur_min:
                mv["removed"].append(v["bank_theme"])
        return mv

    if prev_sig is None:
        movements = {"added": [], "removed": [], "confidence_changed": [], "baseline": True}   # first week ever
        snap = {"week": week, "signals": cur_min, "movements": movements}
    elif prev_week == week:
        movements = prev_moves if prev_moves is not None else _diff(prev_sig)   # same-week rebuild → replay
        snap = {"week": week, "signals": cur_min, "movements": movements}        # keep latest signals for next week
    else:
        movements = _diff(prev_sig)                                              # a new distinct week
        snap = {"week": week, "signals": cur_min, "movements": movements}
    json.dump(snap, open(prev_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # ---------- country prioritization (rank by DIRECT in-country opportunity) ----------
    wide_signals = [s for s in signals if s["footprint_wide"]]
    countries = []
    for c in footprint["countries"]:
        code = c["code"]
        direct = [s for s in signals if code in s["countries"]]
        # OBJECTIVE opportunity value (€m): current biddable deals only — excludes held/secured positions
        # (e.g. Cashflex) and threats/macro, so this matches the main dashboard's "opportunity value" bar.
        direct_score = sum(s.get("pot_value", 0) for s in direct if s.get("is_opportunity"))
        prods = {}
        for s in direct:
            if not s.get("is_opportunity"):
                continue
            for p in s["products"]:
                prods[p] = prods.get(p, 0) + s.get("pot_value", 0)
        st = cstat_by_code.get(code, {})
        countries.append({
            "code": code, "name": c["name"], "region": c["region"], "euro": c["euro"],
            "score": round(direct_score, 1),
            "n_signals": len(direct),
            # opportunity COUNT is now tracked alongside the € score: a market whose contests are all
            # value-unscoped scores €0 but is NOT empty, and must stay ranked/clickable.
            "n_opps": sum(1 for s in direct if s.get("is_opportunity")),
            "n_unscoped_opps": sum(1 for s in direct if s.get("unscoped_opp")),
            "n_high": sum(1 for s in direct if s["confidence"] == "High"),
            "n_new": sum(1 for s in direct if s["is_new_this_week"]),
            "top_products": sorted(prods, key=prods.get, reverse=True),   # all products with opportunity value in this market
            "atms": st.get("atms", ""), "branches": st.get("branches", ""),
            "cash_trend": st.get("cash_trend", ""), "instant": st.get("instant_payments", ""),
            "implication": st.get("implication", ""),
            "signal_keys": [s["key"] for s in direct],
        })
    # rank by € value, then by how many live contests sit there — so a market carrying only unscoped
    # contests ranks above one carrying none, instead of tying at €0 with the empty markets.
    countries.sort(key=lambda x: (x["score"], x["n_opps"], x["n_signals"]), reverse=True)

    # ---------- product prioritization ----------
    products = []
    for cat in pmap["categories"]:
        pid = cat["id"]
        tagged = [s for s in signals if pid in s["products"]]
        ccount = {}
        for s in tagged:
            for cc in s["countries"]:
                ccount[cc] = ccount.get(cc, 0) + 1
        products.append({
            "id": pid, "label": cat["label"], "printec": cat["printec"],
            "score": round(sum(s.get("pot_value", 0) for s in tagged if s.get("is_opportunity")), 1), "n_signals": len(tagged),  # OBJECTIVE €m, opportunities only
            "n_opps": sum(1 for s in tagged if s.get("is_opportunity")),
            "n_unscoped_opps": sum(1 for s in tagged if s.get("unscoped_opp")),
            "n_high": sum(1 for s in tagged if s["confidence"] == "High"),
            "top_countries": sorted(ccount, key=ccount.get, reverse=True),   # all markets where this product has signals
            "signal_keys": [s["key"] for s in tagged],
        })
    products.sort(key=lambda x: (x["score"], x["n_opps"]), reverse=True)

    # ---------- competitive & partner risk ----------
    # Detect terms are matched on WORD BOUNDARIES, not raw substrings. Plain containment made
    # short tokens catastrophically greedy — "integra" matched "integration"/"integrating" and put a
    # Low-threat vendor at the top of the competitor chart on 94 phantom mentions; "epay" matched
    # "epayments", "landi" matched "landing", "dias" matched "diaspora". (?<!\w)...(?!\w) is used
    # instead of \b so tokens that start or end with punctuation (e.g. "integra zrt.") still anchor.
    # Blobs are built once and each vendor's terms compiled into one alternation — matching every
    # vendor against every signal is ~50k searches, so rebuilding the blob per vendor is wasteful.
    _blobs = [(s["key"], " ".join([s["bank_theme"], s["signal"], s["implies"], s["follow_up"]]).lower())
              for s in signals]
    for v in competitors["vendors"]:
        _terms = [re.escape(d.lower()) for d in v.get("detect", []) if d]
        if not _terms:
            v["mention_keys"], v["n_mentions"] = [], 0
            continue
        _pat = re.compile(r"(?<!\w)(?:" + "|".join(_terms) + r")(?!\w)")
        mentions = [k for k, b in _blobs if _pat.search(b)]
        v["mention_keys"] = mentions
        v["n_mentions"] = len(mentions)
    competitors["vendors"].sort(key=lambda v: ({"High":0,"Medium":1,"Low":2}.get(v["threat"],3), -v["n_mentions"]))
    threat_rank = {"High": 3, "Medium": 2, "Low": 1}
    # Matrix columns = competitors ACTUALLY PRESENT in this week's signals (data-driven), already
    # threat-ordered above. No fixed cap — the set grows/shrinks with what the data shows. Fallback to
    # the global/regional set only if nothing was detected this week (so the matrix is never empty).
    active_vendors = [v for v in competitors["vendors"]
                      if v["role"] in ("competitor", "both", "oem") and v.get("n_mentions", 0) > 0]
    if not active_vendors:
        active_vendors = [v for v in competitors["vendors"]
                          if v["role"] in ("competitor", "both", "oem") and v.get("tier") in ("global", "regional")]
    sig_ctry = {s["key"]: s["countries"] for s in signals}
    matrix = []
    for c in footprint["countries"]:
        row = {"code": c["code"], "name": c["name"], "cells": {}}
        any_cell = False
        for v in active_vendors:
            present = c["code"] in v["countries"]
            ment = sum(1 for k in v["mention_keys"] if c["code"] in sig_ctry.get(k, []))
            val = (threat_rank[v["threat"]] if present else 0) + ment
            row["cells"][v["name"]] = val
            if val:
                any_cell = True
        if any_cell:
            matrix.append(row)

    # ---------- regulatory timeline ----------
    deadlines = []
    for it in regcal["items"]:
        d = datetime.date.fromisoformat(it["date"])
        days = (d - run_date).days
        bucket = "past" if days < 0 else ("imminent" if days <= 60 else ("soon" if days <= 180 else "later"))
        deadlines.append({**it, "days_until": days, "bucket": bucket,
                          "geo_names": [code2name.get(x, x) for x in it["geography"]]})
    deadlines.sort(key=lambda x: x["date"])

    # ---------- top opportunities, account targets + the re-homed lanes (RECENCY-FIRST; no win term) ----------
    # Ordering is deterministic and NEVER a score: newest development first, with deal-size then evidence-
    # confidence as pure tiebreaks. Only lane=='opportunity' signals are biddable near-term opportunities;
    # owned/incumbent positions and competitor-won scopes are kept but routed to their own subordinate lanes.
    # ---------- INDIRECT (composed) opportunities ----------
    # A derived play is an inference ACROSS signals: it exists only in the intersection, typically of rows the
    # lane model deliberately keeps out of the rankings (threat_macro has no buyer, lost is competitor-held,
    # installed_base is already ours). Because it is inference, the engine — not the author — enforces the
    # honesty rules: components must RESOLVE to real signals in this week's table, they must span >=2
    # independent agents (counted from the components themselves, never self-reported), and confidence is
    # capped at Medium-High no matter what the file claims. Anything failing that is dropped loudly.
    by_key = {s["key"]: s for s in signals}
    derived = []
    for e in (derived_raw.get("derived") or []) if isinstance(derived_raw, dict) else []:
        cites = e.get("cite_signals") or []
        comps = [by_key[k] for k in cites if k in by_key]
        stale = [k for k in cites if k not in by_key]
        agents = sorted({a for c in comps for a in c.get("agents", [])})
        why = []
        if len(comps) < 2:  why.append("only %d of %d component signals resolve to this week's table" % (len(comps), len(cites)))
        if len(agents) < 2: why.append("components span only %d independent agent(s)" % len(agents))
        if why:
            print("derived: DROPPED %r — %s" % (e.get("id", "?"), "; ".join(why)))
            continue
        if stale:
            print("derived: %r cites %d signal(s) no longer in the table (%s) — kept, flagged in the UI"
                  % (e.get("id", "?"), len(stale), ", ".join(stale)))
        conf = e.get("confidence", "Medium")
        if conf not in ("Medium", "Medium-High"):
            print("derived: capped confidence of %r from %s to Medium-High (a composition is inference and "
                  "never inherits its components' confidence)" % (e.get("id", "?"), conf))
            conf = "Medium-High"
        ctry = e.get("countries") or sorted({c for x in comps for c in x.get("countries", [])})
        # a product id that isn't in the taxonomy would render as a raw slug on the board — catch it here
        valid_pids = {c["id"] for c in pmap["categories"]}
        prods_authored = e.get("products") or sorted({p for x in comps for p in x.get("products", [])})
        bad_pids = [p for p in prods_authored if p not in valid_pids]
        if bad_pids:
            print("derived: %r drops unknown product id(s) %s — not in product_map.json"
                  % (e.get("id", "?"), ", ".join(bad_pids)))
        derived.append({
            "id": e.get("id", ""), "title": e.get("title", ""), "claim": e.get("claim", ""),
            "buyer": e.get("buyer", ""), "trigger": e.get("trigger", ""),
            "why_not_visible": e.get("why_not_visible_in_one_signal", ""),
            "falsifier": e.get("falsifier", ""),
            "countries": ctry, "footprint_wide": bool(e.get("footprint_wide")),
            "products": [p for p in prods_authored if p in valid_pids],
            "component_keys": [c["key"] for c in comps], "stale_components": stale,
            "agents": agents, "confidence": conf,
            "size_band": e.get("size_band", "Unscoped"),
            # a derived play is only live while at least one component still is
            "is_current": any(c.get("is_current") for c in comps),
            "n_new_components": sum(1 for c in comps if c.get("is_new_this_week")),
        })
    derived.sort(key=lambda d: ({"Medium-High": 0, "Medium": 1}.get(d["confidence"], 2), -len(d["agents"])))
    if derived:
        print("derived: %d indirect opportunit%s composed from %d distinct signals"
              % (len(derived), "y" if len(derived) == 1 else "ies",
                 len({k for d in derived for k in d["component_keys"]})))

    SIZE_RANK = {"XL": 4, "L": 3, "M": 2, "S": 1}
    CONF_RANK = {"High": 4, "Medium-High": 3, "Medium": 2, "Low": 1}
    def _recency_key(s):
        return (s.get("dev_date") or s.get("future_date") or "",
                SIZE_RANK.get(s.get("size_band"), 0), CONF_RANK.get(s.get("confidence"), 0))
    opps = sorted([s for s in signals if s.get("is_opportunity")], key=_recency_key, reverse=True)
    top_ops = opps[:8]
    NON_ACCOUNT = ("sector", "regulatory", "compliance wave", "branch consolidation", "accessibility")
    account_targets = [s for s in opps if not any(n in s["bank_theme"].lower() for n in NON_ACCOUNT)]
    # the two re-homed lanes — kept visible, never ranked as opportunities; newest development first
    installed_base = sorted([s for s in signals if s.get("lane") == "installed_base"], key=_recency_key, reverse=True)
    lost = sorted([s for s in signals if s.get("lane") == "lost"], key=_recency_key, reverse=True)

    # KB-mined structural patterns REPLACE the hand workbook Patterns when present (the orchestrator now
    # maintains the full set — the sharpened originals + KB additions — from the whole knowledge base);
    # falls back to the workbook sheet if patterns_kb.json is absent. Each: {pattern, evidence, implication, confidence}.
    _pk = patterns_kb if isinstance(patterns_kb, list) else (patterns_kb.get("patterns", []) if isinstance(patterns_kb, dict) else [])
    _pk = [p for p in _pk if isinstance(p, dict) and p.get("pattern")]
    if _pk:
        patterns = [{"#": "", "Pattern": p.get("pattern", ""),
                     "Evidence (see Metrics/Milestones)": p.get("evidence", ""),
                     "What it means for Printec": p.get("implication", ""),
                     "Confidence": p.get("confidence", "Medium"),
                     "Source": p.get("sources", ""),
                     "Citations": p.get("citations", []),
                     "Group": p.get("group", ""),
                     # direction/rate are what the pattern ITSELF claims — the dashboard shows an arrow
                     # and, only where the pattern states one, its rate. Absent until the next patterns
                     # mining run writes them (see agent-briefs/07-orchestrator.md).
                     "Direction": p.get("direction", ""),
                     "Rate": p.get("rate") or ""} for p in _pk]
    for i, p in enumerate(patterns, 1):
        if isinstance(p, dict) and "#" in p:
            p["#"] = i

    kpis = {
        "n_signals": len(signals),
        "n_new": sum(1 for s in signals if s["is_new_this_week"]),
        "n_high": sum(1 for s in signals if s["confidence"] == "High"),
        "n_imminent": sum(1 for d in deadlines if d["bucket"] == "imminent"),
        "n_opps": sum(1 for s in signals if s.get("is_opportunity")),
        "n_unscoped_opps": sum(1 for s in signals if s.get("unscoped_opp")),
        "n_countries_active": sum(1 for c in countries if c["n_signals"] > 0),
        "n_derived": len(derived),
    }

    DASH = {
        "week": week, "generated": summary.get("generated_utc", ""),
        "kpis": kpis, "movements": movements,
        "signals": signals, "countries": countries, "products": products,
        "wide_signals": [s["key"] for s in wide_signals],
        "competitors": competitors["vendors"], "matrix": matrix,
        "active_vendors": [v["name"] for v in active_vendors],
        "competition_brief": competition_brief,
        "atm_market": (atm_market.get("series", []) if isinstance(atm_market, dict) else (atm_market if isinstance(atm_market, list) else [])),
        "deadlines": deadlines, "top_ops": [s["key"] for s in top_ops],
        "account_targets": [s["key"] for s in account_targets],
        "installed_base": [s["key"] for s in installed_base],
        "lost": [s["key"] for s in lost],
        "derived": derived,
        "series": series, "events": events, "patterns": patterns,
        # No trend fit reaches the dashboard (asked 09/09/2026): the rows carry the reported series
        # only, plus their anchor — the last reported point (mean when several) that every line starts from.
        "forecast": _strip_fit(forecast.get("forecasts", []), proj_lines.get("anchors", [])),
        "forecast_accuracy": {},
        "forecast_coverage": forecast.get("coverage", []), "outlook": outlooks,
        "product_outlooks": product_outlooks,
        "outlook_overlays": narrative.get("overlays", []),
        # The 2nd and 3rd baseline projection lines. Kept separate from "forecast" (the statistical
        # line) on purpose: the strategy call asked for three lines that are never fused, so nothing
        # downstream should be able to blend them by accident.
        "projection_lines": proj_lines.get("lines", []),
        # the pooled reading for next year: mean and spread of every projection on the chart
        # (project_lines.py consensus). The map and the Charts table read this, not the fit alone.
        "projection_consensus": proj_lines.get("consensus", []),
        "projection_gaps": proj_lines.get("gaps", []),
        "futures": futures,
        "futures_board": futures_narr.get("board_view", {}),
        "rbr_series": rbr_series.get("countries", {}),
        "provenance": verification.get("summary", {}),
        "evidence_files": evidence_files,
        "prod_label": prod_label, "prod_printec": prod_printec,
        "competitor_series": competitor_series,
        "code2name": code2name, "summary": summary,
    }

    # scope sweep: no out-of-scope country code may survive anywhere in the payload
    # country-NAME keyed structures (baselines, coverage, per-market series) — the code
    # sweep below only catches 2-letter codes, so drop out-of-scope names here too.
    _NAMES = set(code2name.values())
    _ALLNAMES_SEEN = _NAMES | {'Austria'}   # names we know are markets (in- or out-of-scope)
    for _k in ("forecast", "forecast_coverage", "projection_lines", "projection_gaps", "projection_consensus"):
        _v = DASH.get(_k)
        if isinstance(_v, list):
            _n = len(_v)
            DASH[_k] = [r for r in _v if not (isinstance(r, dict) and r.get("country")
                                              and r["country"] not in _NAMES)]
            if len(DASH[_k]) != _n:
                print("scope: dropped %d out-of-footprint row(s) from %s" % (_n - len(DASH[_k]), _k))
    if isinstance(DASH.get("series"), dict):
        _drop = [k for k in DASH["series"] if (k not in _NAMES and k in _ALLNAMES_SEEN)
                 or (len(k) == 2 and k.isupper() and k not in _INSCOPE)]
        for k in _drop: DASH["series"].pop(k, None)
        if _drop: print("scope: dropped series for %s" % ", ".join(_drop))
    # the RBR datasets are keyed by code and fed every ATM chart on Products; Austria left the
    # footprint and must not be drawn anywhere (asked 10/09/2026)
    if isinstance(DASH.get("rbr_series"), dict):
        _drop = [k for k in DASH["rbr_series"] if k not in _INSCOPE]
        for k in _drop: DASH["rbr_series"].pop(k, None)
        if _drop: print("scope: dropped rbr_series for %s" % ", ".join(_drop))
    if isinstance(DASH.get("atm_market"), list):
        _n = len(DASH["atm_market"])
        DASH["atm_market"] = [r for r in DASH["atm_market"] if not (isinstance(r, dict) and r.get("country") not in _INSCOPE)]
        if len(DASH["atm_market"]) != _n:
            print("scope: dropped %d out-of-footprint atm_market series" % (_n - len(DASH["atm_market"])))

    # Rows keyed by a SCALAR country code. _strip_scope below only cleans list-valued country fields,
    # and the name-based drop above only catches rows keyed by a country NAME — so a reasoned outlook,
    # which carries country: "AT", slipped through both and kept two Austrian cards on the tab.
    # "EU" is not a market: it is the pseudo-code the orchestrator uses for footprint-wide calls.
    _PSEUDO = {"EU"}
    for _k in ("outlook", "product_outlooks"):
        _v = DASH.get(_k)
        if isinstance(_v, list):
            _n = len(_v)
            DASH[_k] = [r for r in _v
                        if not (isinstance(r, dict) and isinstance(r.get("country"), str)
                                and len(r["country"]) == 2 and r["country"].isupper()
                                and r["country"] not in _INSCOPE and r["country"] not in _PSEUDO)]
            if len(DASH[_k]) != _n:
                print("scope: dropped %d out-of-footprint row(s) from %s" % (_n - len(DASH[_k]), _k))

    def _strip_scope(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("countries", "geography", "markets") and isinstance(v, list) \
                   and v and all(isinstance(x, str) for x in v):
                    o[k] = [x for x in v if x in _INSCOPE or len(x) != 2]
                else:
                    _strip_scope(v)
        elif isinstance(o, list):
            for v in o: _strip_scope(v)
    _strip_scope(DASH)

    # ---- the 2026 group budget beside the market (budget/budget_clean.xlsx; see budget_actions.py) ----
    # Computed on the finished payload so every cell joins the same signals, deadlines and outlooks the
    # tabs show. The result is NOT put into the payload: it is written to budget/ (git-ignored) and the
    # artifact build encrypts it behind the admin password (decision of 14/09/2026). No budget file -> nothing.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import budget_actions as _ba, budget_2027 as _b27
        _root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        _bud = _ba.compute(_root, DASH)
        if _bud:
            _bdir = os.path.join(_root, "budget"); os.makedirs(_bdir, exist_ok=True)
            with open(os.path.join(_bdir, "budget_actions.json"), "w", encoding="utf-8") as _fh:
                json.dump(_bud, _fh, ensure_ascii=False, indent=1)
            print(_ba.summary_line(_bud))
            _p27 = _b27.compute(_root, DASH, _bud)
            if _p27:
                with open(os.path.join(_bdir, "budget_2027.json"), "w", encoding="utf-8") as _fh:
                    json.dump(_p27, _fh, ensure_ascii=False, indent=1)
                _t = _p27["totals"]
                print("budget 2027: base EUR %.1fm (%+.1f%%), stretch EUR %.1fm (%+.1f%%)" % (_t["base"] / 1e6, _t["base_growth_pct"], _t["stretch"] / 1e6, _t["stretch_growth_pct"]))
    except Exception as _e:
        print("warn: budget join skipped:", _e)

    dash_str = json.dumps(DASH, ensure_ascii=False)

    # ---- 1. dashboard-data.json (the artifact the orchestrator publishes) ----
    data_json = os.path.join(D, "dashboard-data.json")
    with open(data_json, "w", encoding="utf-8") as f:
        f.write(dash_str)

    # ---- 2. refresh the web app's bundled snapshot (optional) ----
    if os.path.isdir(assets):
        try:
            with open(os.path.join(assets, "data.json"), "w", encoding="utf-8") as f:
                f.write(dash_str)
        except Exception as e:
            print("warn: could not refresh web data.json:", e)

    print("Wrote", data_json)
    print("KPIs:", json.dumps(kpis))


if __name__ == "__main__":
    main()
