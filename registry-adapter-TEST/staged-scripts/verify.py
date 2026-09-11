#!/usr/bin/env python3
"""
verify.py — Trust / provenance pass (Phase 3).  [STAGED TEST COPY — registry-aware self-heal]

Same as production verify.py PLUS one change (marked `# REGISTRY-AWARE`): when a cited URL is dead
(http_error / unreachable), look its domain up in source_access_registry.json and retry the registry's
corrected `final_url` / `best_resource_url`. If that resolves, the record is annotated with a
`repaired_url` + `repair_status` so the dashboard can show a live replacement instead of a dead link.
Evidence for this change: the Greece pilot cited a Worldline URL that 404'd; the registry already holds
corrected URLs, so verification is exactly where the registry pays off (NOT the discovery-agent briefs).

Usage (same as prod, plus optional --registry):
  python verify.py --root <BANKING_folder> --data <intel-cache> [--week YYYY-MM-DD]
                   [--timeout 6] [--workers 16] [--registry <path to source_access_registry.json>]
Default --registry: <root>/weekly-intelligence/references/source_access_registry.json, else skip repair.
"""
import argparse, json, os, re, glob, hashlib, datetime, ssl, urllib.request, urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (compatible; PrintecIntel/1.0; provenance-check)"
URL_RE = re.compile(r'https?://[^\s)\]\}>"\'<]+')
SKIP = ("printec-market-research.vercel.app",)
# PLAYBOOK §2: detect bot walls by POSITIVE EVIDENCE (named markers).
# HARD markers are wall infrastructure that never appears on a normal content page -> block at ANY size.
HARD_MARKERS = ("sgcaptcha", "/cdn-cgi/challenge", "__cf_chl", "_incapsula_resource", "distil", "px-captcha")
# SOFT markers (reCAPTCHA/hCaptcha widgets, challenge phrases) ALSO appear on real pages that embed a
# captcha on a form -> block ONLY when the page is THIN (little real content), else it's genuine content.
SOFT_MARKERS = ("recaptcha", "hcaptcha", "just a moment...", "verifying you are human", "attention required")
THIN_TEXT = 2000   # visible (de-tagged) chars below this + a soft marker = a challenge page, not content

def _visible_len(text):
    t = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', text)
    t = re.sub(r'(?s)<[^>]+>', ' ', t)
    return len(re.sub(r'\s+', ' ', t).strip())

def _dom(u):
    try:
        d = urlparse(u).netloc.lower()
        return d[4:] if d.startswith("www.") else d
    except Exception:
        return ""

def load_registry(path):                                             # REGISTRY-AWARE
    """domain -> corrected URL (final_url or best_resource_url), for repairing dead citations."""
    if not path or not os.path.exists(path):
        return {}
    try:
        reg = json.load(open(path, encoding="utf-8"))
    except Exception:
        return {}
    m = {}
    for dom, r in reg.items():
        alt = (r.get("final_url") or r.get("best_resource_url") or "").strip()
        if alt.startswith("http"):
            m[dom] = alt
    return m

def extract_urls_by_file(root):
    by_file = {}
    files = glob.glob(os.path.join(root, "findings", "**", "*.md"), recursive=True)
    mt = os.path.join(root, "master-signal-table.md")
    if os.path.exists(mt):
        files.append(mt)
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                txt = fh.read()
        except Exception:
            continue
        rel = os.path.relpath(f, root).replace("\\", "/")
        us = set()
        for u in URL_RE.findall(txt):
            u = u.rstrip('.,);\'"')
            if any(s in u for s in SKIP):
                continue
            us.add(u)
        by_file[rel] = sorted(us)
    return by_file

def _get(url, timeout, snap_dir, week, snapshot=True):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    rec = {"url": url, "fetched_at": week}
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            data = r.read(500_000)
            code = r.getcode()
            try:
                text = data.decode("utf-8", "replace")
            except Exception:
                text = ""
            # PLAYBOOK §2: hard marker (or 202) = wall at any size; soft marker = wall only if page is thin.
            low = text.lower()
            hard = next((m for m in HARD_MARKERS if m in low), None)
            soft = next((m for m in SOFT_MARKERS if m in low), None)
            if hard or code == 202:
                blk_marker = hard or f"HTTP {code}"
            elif soft and _visible_len(text) < THIN_TEXT:
                blk_marker = f"{soft} (thin {_visible_len(text)}c)"
            else:
                blk_marker = None
            if blk_marker:
                rec.update({"status": "blocked", "code": code, "bytes": len(data),
                            "block_marker": blk_marker})
            else:
                rec.update({"status": "ok", "code": code, "bytes": len(data),
                            "content_sha1": hashlib.sha1(data).hexdigest()[:16]})
                if snapshot:
                    name = hashlib.sha1(url.encode()).hexdigest()[:16] + ".txt"
                    with open(os.path.join(snap_dir, name), "w", encoding="utf-8") as fh:
                        fh.write(f"URL: {url}\nFETCHED: {week}\nHTTP: {code}\n\n{text[:200_000]}")
                    rec["snapshot"] = name
    except urllib.error.HTTPError as e:
        rec.update({"status": "http_error", "code": e.code})
    except Exception as e:
        rec.update({"status": "unreachable", "error": type(e).__name__})
    return rec

def fetch(url, timeout, snap_dir, week, registry):
    rec = _get(url, timeout, snap_dir, week)
    if rec.get("status") != "ok" and registry:                       # REGISTRY-AWARE self-heal
        alt = registry.get(_dom(url))
        if alt and alt.rstrip("/") != url.rstrip("/"):
            rep = _get(alt, timeout, snap_dir, week)
            rec["repaired_url"] = alt
            rec["repair_status"] = rep.get("status")
            if rep.get("status") == "ok":
                rec["repair_snapshot"] = rep.get("snapshot")
                rec["repair_code"] = rep.get("code")
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    ap.add_argument("--timeout", type=int, default=6)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--registry", default=None)                      # REGISTRY-AWARE
    args = ap.parse_args()

    reg_path = args.registry or os.path.join(
        args.root, "weekly-intelligence", "references", "source_access_registry.json")
    registry = load_registry(reg_path)

    snap_dir = os.path.join(args.data, "snapshots")
    os.makedirs(snap_dir, exist_ok=True)
    by_file = extract_urls_by_file(args.root)
    all_urls = sorted({u for us in by_file.values() for u in us})

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(fetch, u, args.timeout, snap_dir, args.week, registry): u for u in all_urls}
        for fu in as_completed(futs):
            r = fu.result()
            results[r["url"]] = r

    def st(u): return results.get(u, {}).get("status")
    files = {}
    for rel, us in by_file.items():
        files[rel] = {"total": len(us), "reachable": sum(1 for u in us if st(u) == "ok"),
                      "checked_at": args.week,
                      "sources": [{"url": u, **{k: results.get(u, {}).get(k)
                                   for k in ("status", "code", "fetched_at", "snapshot",
                                             "block_marker", "repaired_url", "repair_status")}} for u in us]}
    repaired = sum(1 for u in all_urls if results.get(u, {}).get("repair_status") == "ok")
    summary = {"total": len(all_urls),
               "reachable":   sum(1 for u in all_urls if st(u) == "ok"),
               "http_error":  sum(1 for u in all_urls if st(u) == "http_error"),
               "unreachable": sum(1 for u in all_urls if st(u) == "unreachable"),
               "blocked":     sum(1 for u in all_urls if st(u) == "blocked"),      # PLAYBOOK §2
               "repaired_via_registry": repaired}                    # REGISTRY-AWARE
    out = {"generated_week": args.week,
           "checked_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
           "registry_used": bool(registry), "summary": summary, "files": files, "urls": results}
    with open(os.path.join(args.data, "verification.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"verify: {summary['total']} sources | {summary['reachable']} reachable, "
          f"{summary['http_error']} http-error, {summary['unreachable']} unreachable, "
          f"{summary['blocked']} bot-blocked | {repaired} repaired via registry | snapshots in {snap_dir}")

if __name__ == "__main__":
    main()
