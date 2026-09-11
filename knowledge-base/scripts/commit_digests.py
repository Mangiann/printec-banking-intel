#!/usr/bin/env python3
"""Commit step of the knowledge-base pipeline (deterministic).

Takes the LLM digest+routing output (the same shape the nightly processor / the
digest workflow produces) and does the reliable file plumbing:
  * writes each per-target digest .md (consistent YAML frontmatter + a clickable
    relative link back to the original),
  * moves each original document out of the drop-inbox into processed/,
  * maintains _manifest.json (dedup by sha256 so a re-dropped file is recognised).

Records JSON may be a bare list, or {"result": [...]} / {"results": [...]}.
Each record: {slug, original_filename, file_type, tags[], digests:[{folder, markdown}]}.
Folder "_reference" -> knowledge-base/_reference; anything else -> knowledge-base/by-agent/<folder>.

Usage:
    python commit_digests.py --records <json> --dump "<Data dump>" --kb "<knowledge-base>" [--date YYYY-MM-DD]
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import shutil


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_records(path):
    data = json.loads(open(path, encoding="utf-8").read())
    if isinstance(data, list):
        return data
    for k in ("result", "results", "records"):
        v = data.get(k)
        if isinstance(v, list):
            return v
    raise SystemExit("could not find a records list in " + path)


def target_dir(kb, folder):
    return os.path.join(kb, "_reference") if folder == "_reference" \
        else os.path.join(kb, "by-agent", folder)


def fm_list(items):
    return "[" + ", ".join(json.dumps(str(x), ensure_ascii=False) for x in items) + "]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--dump", required=True)
    ap.add_argument("--kb", required=True)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    kb, dump = args.kb, args.dump
    processed = os.path.join(kb, "processed")
    os.makedirs(processed, exist_ok=True)
    manifest_path = os.path.join(kb, "_manifest.json")
    manifest = {"updated": "", "documents": []}
    if os.path.isfile(manifest_path):
        try:
            manifest = json.load(open(manifest_path, encoding="utf-8"))
        except Exception:
            pass
    by_sha = {d.get("sha256"): d for d in manifest.get("documents", []) if d.get("sha256")}

    records = load_records(args.records)
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    written, moved, problems = [], [], []

    for r in records:
        orig = r["original_filename"]
        slug = r["slug"]
        src_in_dump = os.path.join(dump, orig)
        dst_in_proc = os.path.join(processed, orig)
        # hash the original wherever it currently lives
        src = src_in_dump if os.path.isfile(src_in_dump) else (dst_in_proc if os.path.isfile(dst_in_proc) else None)
        sha = sha256_of(src) if src else ""
        size = os.path.getsize(src) if src else 0
        routed = [d["folder"] for d in r["digests"]]

        digest_paths = []
        for d in r["digests"]:
            tdir = target_dir(kb, d["folder"])
            os.makedirs(tdir, exist_ok=True)
            md_path = os.path.join(tdir, slug + ".md")
            rel_to_original = os.path.relpath(dst_in_proc, tdir).replace(os.sep, "/")
            body = html.unescape(d["markdown"]).strip()
            fm = (
                "---\n"
                f'source_file: {json.dumps(orig, ensure_ascii=False)}\n'
                f"type: {r.get('file_type','')}\n"
                f"processed: {args.date}\n"
                f"agents: {fm_list(routed)}\n"
                f"tags: {fm_list(r.get('tags', []))}\n"
                f'original: {json.dumps(rel_to_original, ensure_ascii=False)}\n'
                "---\n\n"
                f"> **Original document:** [{orig}]({rel_to_original}) — full file in `knowledge-base/processed/`.\n\n"
            )
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(fm + body + "\n")
            rel = os.path.relpath(md_path, kb).replace(os.sep, "/")
            digest_paths.append("knowledge-base/" + rel)
            written.append(rel)

        # move the original into processed/ (idempotent; tolerate a locked file)
        if os.path.isfile(src_in_dump):
            try:
                shutil.move(src_in_dump, dst_in_proc)
                moved.append(orig)
            except Exception as e:
                problems.append(f"could not move {orig}: {e}")

        entry = {
            "file": orig, "slug": slug, "type": r.get("file_type", ""),
            "sha256": sha, "bytes": size, "processed_utc": now,
            "routed": routed, "digests": digest_paths, "tags": r.get("tags", []),
        }
        if sha in by_sha:
            by_sha[sha].update(entry)
        else:
            manifest["documents"].append(entry)
            by_sha[sha] = entry

    manifest["updated"] = now
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(json.dumps({
        "digests_written": written,
        "originals_moved": moved,
        "problems": problems,
        "manifest_documents": len(manifest["documents"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
