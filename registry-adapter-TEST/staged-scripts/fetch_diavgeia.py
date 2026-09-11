#!/usr/bin/env python3
"""
fetch_diavgeia.py — Tier-0 sub-threshold procurement sweep (registry-driven).

Sweeps a national OpenData transparency portal (default: Greek ΚΗΜΔΗΣ/Diavgeia) for below-TED-threshold
procurement decisions in the banking/self-service/payments space, filling the F2 gap. Public API, no auth.

Built to EXTRACTION_PLAYBOOK standard:
- §6.6 country/host/terms live in a REGISTRY CONFIG (references/diavgeia_config.json), never in this code.
- §1   uses the PROVEN filter param `subject=` (q=/query= are decoration); param name comes from config.
- §6.2 a positive control (a common term that MUST return >0) runs first; a false zero ABORTS instead of
        overwriting the cache with an empty file.
- §6.4 paginates and ANNOUNCES every drop: per term it prints fetched N of TOTAL (dropped M); a global
        cap is announced too. No silent truncation.
- §6.3 counts what LANDED (stored, after de-dup + relevance exclusion), not what was requested.
- §2   is a good citizen: ~1 req/sec per host, identifies itself, retries a transient error once.

Usage: python fetch_diavgeia.py --data <intel-cache> [--week YYYY-MM-DD] [--months 12]
       [--config <path>] [--per-term-cap 300] [--page-size 100]
"""
import argparse, json, os, time, datetime, urllib.request, urllib.error, urllib.parse

UA = "Mozilla/5.0 (compatible; PrintecIntel/1.0; tender-floor; +opendata)"
RATE_SLEEP = 1.0   # §2: ~1 request/second per host

DEFAULT_CONFIG = {   # used only if the registry config is missing — and we ANNOUNCE the fallback
    "opendata_base": "https://diavgeia.gov.gr/luminapi/opendata", "host": "diavgeia.gov.gr",
    "country": "GR", "filter_param": "subject",
    "terms": ["ATM", "τερματικά POS", "καταμέτρησης χαρτονομισμάτων"],
    "control_term": "προμήθεια", "exclude_subject_contains": [],
}

def _get_json(url, timeout=30, retry=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace")), None
    except Exception as e:
        if retry:                                   # §2: retry a transient failure ONCE
            time.sleep(2.0)
            return _get_json(url, timeout, retry=False)
        return None, f"{type(e).__name__}"

def _page(base, param, term, page, size):
    q = urllib.parse.urlencode({param: term, "page": page, "size": size})
    return _get_json(f"{base}/search.json?{q}")

def _total_and_hits(d):
    info = d.get("info", {}) if isinstance(d, dict) else {}
    total = info.get("total")
    for key in ("decisions", "results", "items"):
        if isinstance(d, dict) and isinstance(d.get(key), list):
            return total, d[key]
    return total, (d if isinstance(d, list) else [])

def _date_of(dec):
    """Diavgeia dates are epoch MILLIS — convert to ISO YYYY-MM-DD."""
    for k in ("issueDate", "submissionTimestamp", "publishTimestamp", "date"):
        v = dec.get(k)
        if v in (None, ""):
            continue
        try:
            n = int(v)
            if n > 10_000_000_000:
                n //= 1000
            return datetime.datetime.utcfromtimestamp(n).date().isoformat()
        except (ValueError, TypeError, OSError, OverflowError):
            return str(v)[:10]
    return ""

def _org_label(base, org_id, cache):
    if not org_id:
        return ""
    if org_id in cache:
        return cache[org_id]
    d, _ = _get_json(f"{base}/organizations/{urllib.parse.quote(str(org_id))}.json")
    label = (d.get("label") or d.get("name") or "") if isinstance(d, dict) else ""
    cache[org_id] = label
    time.sleep(RATE_SLEEP)
    return label

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    ap.add_argument("--months", type=int, default=12)
    ap.add_argument("--config", default=None)
    ap.add_argument("--per-term-cap", type=int, default=300)   # §6.4: bounded, and the drop is announced
    ap.add_argument("--page-size", type=int, default=100)
    args = ap.parse_args()
    os.makedirs(args.data, exist_ok=True)
    out_path = os.path.join(args.data, "greek_tenders_diavgeia.json")

    cfg_path = args.config or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "diavgeia_config.json")
    if os.path.exists(cfg_path):
        cfg = json.load(open(cfg_path, encoding="utf-8"))
    else:
        cfg = DEFAULT_CONFIG
        print(f"fetch_diavgeia: WARN registry config not found at {cfg_path} — using built-in fallback "
              f"({len(cfg['terms'])} terms). Add references/diavgeia_config.json (PLAYBOOK §6.6).")

    base = cfg["opendata_base"]; param = cfg.get("filter_param", "subject")
    terms = cfg.get("terms", []); excludes = cfg.get("exclude_subject_contains", [])
    control = cfg.get("control_term", "προμήθεια")

    # §6.2 POSITIVE CONTROL — a false zero here means the API/param is broken; abort, don't write empty.
    d, err = _page(base, param, control, 0, 5)
    ctotal, _ = _total_and_hits(d or {})
    if err or not ctotal:
        print(f"fetch_diavgeia: ABORT — positive control '{param}={control}' returned total={ctotal} "
              f"(err={err}). API/param may be broken; keeping any cached file, not writing an empty one.")
        return
    print(f"fetch_diavgeia: positive control OK ('{param}={control}' -> {ctotal} total); sweeping {len(terms)} terms.")

    try:
        cutoff = (datetime.date.fromisoformat(args.week) -
                  datetime.timedelta(days=30 * args.months)).isoformat()
    except Exception:
        cutoff = "0000-00-00"

    seen, items, org_cache = set(), [], {}
    per_term, dropped_cap, dropped_excl, dropped_old = {}, 0, 0, 0
    for term in terms:
        total, fetched_this = None, 0
        page = 0
        while True:
            d, e = _page(base, param, term, page, args.page_size)
            time.sleep(RATE_SLEEP)
            if e or not isinstance(d, dict):
                per_term[term] = {"total": total, "fetched": fetched_this, "error": e}
                break
            total, hits = _total_and_hits(d)
            if not hits:
                break
            for dec in hits:
                fetched_this += 1
                ada = dec.get("ada") or dec.get("id")
                subj = (dec.get("subject") or "").strip()
                if not ada or ada in seen:
                    continue
                if any(x in subj for x in excludes):        # §6.4 relevance drop (announced below)
                    dropped_excl += 1; continue
                date = _date_of(dec)
                if date and date < cutoff:
                    dropped_old += 1; continue
                seen.add(ada)
                org_id = dec.get("organizationId") or dec.get("organizationUid")
                items.append({"ada": ada, "subject": subj[:300],
                              "org": _org_label(base, org_id, org_cache), "org_id": org_id,
                              "date": date, "matched_term": term,
                              "doc_url": f"https://{cfg['host']}/doc/{urllib.parse.quote(str(ada))}"})
            page += 1
            if fetched_this >= min(total or 0, args.per_term_cap):
                break
        # §6.4 ANNOUNCE the drop for this term
        drop = (total - fetched_this) if (total and total > fetched_this) else 0
        dropped_cap += drop
        per_term.setdefault(term, {"total": total, "fetched": fetched_this})
        print(f"  {param}={term!r:32} total={total} fetched={fetched_this}"
              + (f"  DROPPED {drop} (per-term cap {args.per_term_cap})" if drop else ""))

    items.sort(key=lambda x: x["date"], reverse=True)
    out = {"generated_week": args.week, "source": f"{cfg['host']} OpenData ({param}= free-text)",
           "country": cfg.get("country"), "months_window": args.months, "terms": terms,
           "landed": len(items),                                    # §6.3 what LANDED, not attempted
           "dropped": {"per_term_cap": dropped_cap, "relevance_excluded": dropped_excl,
                       "older_than_window": dropped_old},
           "per_term": per_term, "items": items}
    if not items and os.path.exists(out_path):
        print(f"fetch_diavgeia: 0 landed — keeping cached file (PLAYBOOK §6.1: a real 0 is a question).")
        return
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"fetch_diavgeia: LANDED {len(items)} decisions "
          f"(dropped: cap={dropped_cap}, noise={dropped_excl}, old={dropped_old}) -> {out_path}")

if __name__ == "__main__":
    main()
