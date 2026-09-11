#!/usr/bin/env python3
"""STEP 1 of URL recovery: re-check every HEAD-failed URL with a REAL GET.

Why: `runner.HttpUrlVerifier` only does a HEAD request and treats `reachable = 200 <= code < 400`, so a
403 (bot-defended but LIVE), a 405 (server refuses HEAD but serves GET), a 429 (we were impolite) and a
transient timeout all get recorded as `url_verification.status = "failed"`. The safety gate then refuses to
ACTIVATE a source whose URL is unverified, and the decision pre-labeller sees "URL dead" and defers it. Net
effect: live sources are silently locked out of the registry. The dev log measured the HEAD check
over-reporting "dead" by ~5x; a 25-URL sample of the Greece failures found 36% returning 200 on a plain GET.

This step is the CHEAP rung of the recovery ladder — deterministic, no browser, no agent, no LLM:

    verified   GET 200 and the final URL is the one we asked for
    repaired   GET 200 but the server redirected us elsewhere -> adopt the corrected URL
    (anything else is NOT decided here)

Fail-closed and deliberately conservative: this script NEVER emits `dead`. A 403 / 404 / 429 / timeout is
left UNRESOLVED and written to `remaining_failures.json` for the browser-ladder step, because "a failed
fetch is a hypothesis, not a verdict" (routine_prompt.md) and a 404 usually means MOVED, not gone. Only the
browser ladder (which reads the rendered page) may propose `dead`.

Output per run, consumed by the already-tested `recovery.apply_url_recovery`:
    data/run_logs/<run>/agent_inputs/recovery_results.json   (verified/repaired ONLY)
    data/run_logs/<run>/agent_inputs/remaining_failures.json (the browser step's queue)

    python scripts/recheck_failed_urls.py                 # all runs
    python scripts/recheck_failed_urls.py --only GR       # one country
    python scripts/recheck_failed_urls.py --dry-run
"""
import argparse
import json
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))
import runner  # noqa: E402  (for normalize_url)

# A browser UA: many WAFs 403 anything that doesn't look like a browser. We are not hiding — we are simply
# not being punished for using urllib. The scout's own UA is what earned most of these 403s.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA,
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "el,en;q=0.9",
           "Accept-Encoding": "identity"}     # no brotli in stdlib; keep it simple

_host_lock = defaultdict(threading.Lock)
_host_next = defaultdict(float)
_HOST_DELAY = 1.5          # seconds between two requests to the SAME host


def _polite(host):
    """Serialize per host and keep >= _HOST_DELAY between requests to it."""
    with _host_lock[host]:
        wait = _host_next[host] - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _host_next[host] = time.monotonic() + _HOST_DELAY


def check(url, timeout=12):
    """TOTAL: never raises. -> (outcome, http_status, final_url, note)."""
    host = (urlsplit(url).hostname or "").lower()
    _polite(host)
    ctx = ssl.create_default_context()
    try:
        req = urllib.request.Request(url, method="GET", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            code = getattr(r, "status", None) or r.getcode()
            final = r.geturl()
            r.read(4096)                                   # touch the body: a real GET, not a HEAD
        if not (200 <= code < 300):
            return "unresolved", code, final, f"http {code}"
        same = runner.normalize_url(final) == runner.normalize_url(url)
        if same:
            return "verified", code, final, "GET 200"
        return "repaired", code, final, "GET 200 after redirect"
    except urllib.error.HTTPError as e:
        # 403/405/429 = almost certainly LIVE but defended. 404/410 = usually MOVED. Neither is our call.
        return "unresolved", e.code, None, f"http {e.code}"
    except Exception as e:                                  # noqa: BLE001 - timeouts, DNS, TLS, resets
        return "unresolved", None, None, f"{type(e).__name__}"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Re-check HEAD-failed URLs with a real GET.")
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--only", default=None, help="restrict to one country (e.g. GR)")
    ap.add_argument("--run-id", default=None, help="restrict to a single run (e.g. dr_gr_a2_live_008)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=12)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    data_root = Path(args.data_root)

    jobs = []          # (run_id, candidate_id, url)
    for f in sorted((data_root / "run_logs").glob("dr_*/agent_inputs/failed_urls.json")):
        run = f.parts[-3]
        if args.run_id and run != args.run_id:
            continue
        if args.only and run.split("_")[1].upper() != args.only.upper():
            continue
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for r in rows if isinstance(rows, list) else []:
            cid, url = r.get("candidate_id"), r.get("source_url")
            if isinstance(cid, str) and isinstance(url, str) and url:
                jobs.append((run, cid, url))

    print(f"[recheck] {len(jobs)} failed URLs across "
          f"{len({j[0] for j in jobs})} runs (workers={args.workers}, per-host delay={_HOST_DELAY}s)")
    if args.dry_run:
        print(json.dumps({"would_check": len(jobs)}, indent=2))
        return 0

    results = {}
    done = [0]
    lock = threading.Lock()

    def work(job):
        run, cid, url = job
        outcome, code, final, note = check(url, timeout=args.timeout)
        with lock:
            done[0] += 1
            if done[0] % 200 == 0:
                print(f"[recheck]   {done[0]}/{len(jobs)} checked")
        return (run, cid, url, outcome, code, final, note)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for run, cid, url, outcome, code, final, note in ex.map(work, jobs):
            results.setdefault(run, []).append(
                {"candidate_id": cid, "source_url": url, "outcome": outcome,
                 "http_status": code, "corrected_url": final if outcome == "repaired" else None,
                 "method": "http_get", "ladder_step": "get_recheck", "evidence": note})

    # write per-run artifacts
    tot = defaultdict(int)
    for run, rows in sorted(results.items()):
        ai = data_root / "run_logs" / run / "agent_inputs"
        ai.mkdir(parents=True, exist_ok=True)
        # recovery.apply_url_recovery COERCES an unknown outcome to "dead" -> pass ONLY the decided ones.
        decided = [r for r in rows if r["outcome"] in ("verified", "repaired")]
        remaining = [r for r in rows if r["outcome"] == "unresolved"]
        (ai / "recovery_results.json").write_text(
            json.dumps(decided, ensure_ascii=False, indent=1), encoding="utf-8")
        (ai / "remaining_failures.json").write_text(
            json.dumps(remaining, ensure_ascii=False, indent=1), encoding="utf-8")
        for r in rows:
            tot[r["outcome"]] += 1
        tot["_runs"] += 1

    v, rp, un = tot["verified"], tot["repaired"], tot["unresolved"]
    n = v + rp + un
    print()
    print(f"[recheck] RESULT over {n} URLs the HEAD check called dead:")
    print(f"[recheck]   verified  (live, same URL)     : {v}")
    print(f"[recheck]   repaired  (live, moved)        : {rp}")
    print(f"[recheck]   unresolved (-> browser ladder) : {un}")
    print(f"[recheck]   => {v + rp} of {n} ({100 * (v + rp) / max(1, n):.0f}%) were FALSE DEADS")
    print(f"[recheck] wrote recovery_results.json + remaining_failures.json for {tot['_runs']} runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
