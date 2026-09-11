#!/usr/bin/env python3
"""STEP 1b of URL recovery: the WAF-handshake rung — still deterministic, still no browser, no agent.

`recheck_failed_urls.py` (a plain browser-UA GET) settled 619 of 2,189. The residue is dominated by
403 (679) and timeouts (400) — and most 403s are not "forbidden", they are a WAF that refused a request
which did not look like a browser SESSION: no cookies, no Sec-Fetch-* headers, no Referer, arriving cold at
a deep URL. A real browser never does that; it lands on the site, picks up a cookie, then follows a link.

So: warm up on the site ROOT (collecting cookies), then retry the deep URL with the full browser header set
and a Referer. This is the cheap rung BELOW the browser ladder, and it must be exhausted first — the project
rule is that code does whatever code can do, and an agent-driven Chrome pass over 1,000 URLs costs hours.

Conservative, exactly like step 1: emits ONLY `verified` / `repaired`. Never `dead`. Whatever is still
unsettled stays in remaining_failures.json for the browser ladder, because a failed fetch is a hypothesis.

    python scripts/recheck_tier2.py            # all runs
    python scripts/recheck_tier2.py --only GR
"""
import argparse
import http.cookiejar
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
from urllib.parse import urlsplit, urlunsplit

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "routines" / "source_discovery_scout"))
import runner  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")
# The header set a real Chrome actually sends. WAFs fingerprint on the ABSENCE of these.
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
               "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"),
    "Accept-Language": "el-GR,el;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "identity",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Connection": "keep-alive",
}

_host_lock = defaultdict(threading.Lock)
_host_next = defaultdict(float)
_HOST_DELAY = 2.5                     # gentler than step 1: we already annoyed some of these hosts
_warm = {}                            # host -> opener (with its cookie jar), built once per host
_warm_lock = threading.Lock()


def _opener_for(host, scheme):
    """One opener + cookie jar per host, warmed on the site root so we arrive holding a session cookie."""
    with _warm_lock:
        if host in _warm:
            return _warm[host]
        cj = http.cookiejar.CookieJar()
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        op.addheaders = list(BROWSER_HEADERS.items())
        _warm[host] = op
    root = urlunsplit((scheme, host, "/", "", ""))
    try:                                                    # warm-up: collect cookies, ignore the outcome
        op.open(urllib.request.Request(root, headers=BROWSER_HEADERS), timeout=12).read(2048)
    except Exception:                                       # noqa: BLE001 - warm-up failure is not fatal
        pass
    return op


def _polite(host):
    with _host_lock[host]:
        wait = _host_next[host] - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _host_next[host] = time.monotonic() + _HOST_DELAY


def check(url, timeout=25):
    """TOTAL. -> (outcome, http_status, final_url, note)."""
    parts = urlsplit(url)
    host, scheme = (parts.hostname or ""), (parts.scheme or "https")
    if not host:
        return "unresolved", None, None, "no host"
    op = _opener_for(host, scheme)
    _polite(host)
    root = urlunsplit((scheme, host, "/", "", ""))
    hdrs = dict(BROWSER_HEADERS)
    hdrs["Referer"] = root                                   # arrive as if we followed a link from the site
    try:
        r = op.open(urllib.request.Request(url, headers=hdrs), timeout=timeout)
        code = getattr(r, "status", None) or r.getcode()
        final = r.geturl()
        r.read(4096)
        r.close()
        if not (200 <= code < 300):
            return "unresolved", code, final, f"http {code}"
        same = runner.normalize_url(final) == runner.normalize_url(url)
        return ("verified" if same else "repaired"), code, final, "browser-handshake GET 200"
    except urllib.error.HTTPError as e:
        return "unresolved", e.code, None, f"http {e.code}"
    except Exception as e:                                   # noqa: BLE001
        return "unresolved", None, None, type(e).__name__


def main(argv=None):
    ap = argparse.ArgumentParser(description="WAF-handshake retry over the URLs a plain GET could not settle.")
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--run-id", default=None, help="restrict to a single run")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=25)
    args = ap.parse_args(argv)
    data_root = Path(args.data_root)

    jobs = []
    for f in sorted((data_root / "run_logs").glob("dr_*/agent_inputs/remaining_failures.json")):
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
            if r.get("candidate_id") and r.get("source_url"):
                jobs.append((run, r))

    print(f"[tier2] {len(jobs)} unresolved URLs, {len({urlsplit(j[1]['source_url']).hostname for j in jobs})} hosts "
          f"(workers={args.workers}, per-host delay={_HOST_DELAY}s)")
    done = [0]
    lock = threading.Lock()

    def work(job):
        run, r = job
        outcome, code, final, note = check(r["source_url"], timeout=args.timeout)
        with lock:
            done[0] += 1
            if done[0] % 150 == 0:
                print(f"[tier2]   {done[0]}/{len(jobs)}")
        return run, {"candidate_id": r["candidate_id"], "source_url": r["source_url"], "outcome": outcome,
                     "http_status": code, "corrected_url": final if outcome == "repaired" else None,
                     "method": "http_get_browser_handshake", "ladder_step": "waf_handshake",
                     "evidence": note}

    out = defaultdict(list)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for run, res in ex.map(work, jobs):
            out[run].append(res)

    from collections import Counter
    tot = Counter()
    for run, rows in sorted(out.items()):
        ai = data_root / "run_logs" / run / "agent_inputs"
        won = [r for r in rows if r["outcome"] in ("verified", "repaired")]
        left = [r for r in rows if r["outcome"] == "unresolved"]
        if won:                                              # MERGE into the existing recovery artifact
            p = ai / "recovery_results.json"
            prev = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
            seen = {x["candidate_id"] for x in prev}
            prev += [w for w in won if w["candidate_id"] not in seen]
            p.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
        (ai / "remaining_failures.json").write_text(
            json.dumps(left, ensure_ascii=False, indent=1), encoding="utf-8")
        for r in rows:
            tot[r["outcome"]] += 1

    v, rp, un = tot["verified"], tot["repaired"], tot["unresolved"]
    n = v + rp + un
    print()
    print(f"[tier2] RESULT over {n} URLs a plain GET could not settle:")
    print(f"[tier2]   verified (WAF handshake worked) : {v}")
    print(f"[tier2]   repaired (moved)                : {rp}")
    print(f"[tier2]   still unresolved -> browser     : {un}")
    print(f"[tier2]   => {v + rp} more false deads recovered WITHOUT a browser")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
