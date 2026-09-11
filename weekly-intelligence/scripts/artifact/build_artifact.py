#!/usr/bin/env python3
"""Build the single-file Printec Intelligence Dashboard for publishing as a Claude Artifact.

Concatenates the dashboard-web assets into one self-contained HTML file. app.js already
supports this offline mode natively (it reads window.__DASH_DATA__ instead of fetching).

Layout of the produced file — the artifact platform wraps it in <!doctype>/<head>/<body>
and injects charset + viewport, so no such tags are emitted here:
    <title> · Google-Fonts <link> · <style>styles.css + build CSS</style>
    · body markup from index.html (logo inlined as a data: URI)
    · Chart.js UMD (vendored beside this script)
    · window.__DASH_DATA__  = data.json
    · window.__DASH_DOCS__  = the findings documents cited by the outlook/futures cards
    · atm-sources.js · product-outlooks.js · footprint-map.js · app.js (patched)

Patches live in patch_artifact.py and are applied at build time only — dashboard-web/app.js
is never modified, so the live Vercel app is unaffected. Revert = stop calling them.

Usage:  python build_artifact.py [out.html]
"""
import base64, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))     # …/BANKING
WEB  = os.path.join(ROOT, "dashboard-web")
sys.path.insert(0, HERE)
import patch_artifact

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "printec-dashboard.html")
MAX_DOC = 400_000          # per embedded document, characters

def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def collect_docs(dash):
    """Embed the findings documents the reasoned cards cite, so the evidence viewer works offline."""
    # Only the Futurist's own report: it is the document the 3-5yr cards are read against, and
    # embedding every agent's findings would roughly treble the file for evidence few readers open.
    want = []
    for row in dash.get("futures") or []:
        for fp in (row.get("cite_files") or []):
            if fp not in want:
                want.append(fp)
    docs = {}
    for fp in want:
        full = os.path.join(ROOT, fp)
        if os.path.isfile(full):
            try:
                docs[fp] = rd(full)[:MAX_DOC]
            except Exception:
                pass
    return docs

def main():
    data = rd(os.path.join(WEB, "data.json")).strip()
    dash = json.loads(data)
    docs = collect_docs(dash)

    logo = base64.b64encode(open(os.path.join(WEB, "printec-logo.svg"), "rb").read()).decode()
    idx  = rd(os.path.join(WEB, "index.html"))
    body = idx[idx.index('<div class="layout">'):idx.index("</div>\n<script defer") + len("</div>")]
    body = body.replace('src="printec-logo.svg"', 'src="data:image/svg+xml;base64,%s"' % logo)

    app = patch_artifact.apply(rd(os.path.join(WEB, "app.js")))

    parts = [
        "<title>Printec Intelligence Dashboard</title>",
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">',
        "<style>", rd(os.path.join(WEB, "styles.css")).rstrip("\n"),
        # single-file build: no architecture sub-page to link to, and paint the canvas explicitly
        "\n/* single-file build */\n.archbtn{display:none !important}\nhtml,body{background:var(--bg)}\n",
        patch_artifact.CSS, "</style>",
        body,
        "<script>", rd(os.path.join(HERE, "chart.umd.min.js")).rstrip("\n"), "</script>",
        "<script>", "window.__DASH_DATA__ = " + data + ";", "</script>",
        "<script>", "window.__DASH_DOCS__ = " + json.dumps(docs, ensure_ascii=False) + ";", "</script>",
    ]
    for js in ("atm-sources.js", "product-outlooks.js", "footprint-map.js"):
        parts += ["<script>", "/* %s */" % js, rd(os.path.join(WEB, js)).rstrip("\n"), "</script>"]
    parts += ["<script>", "/* app.js */", app, "</script>"]

    html = "\n".join(parts) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  %.2f MB  (embedded docs: %s)"
          % (OUT, len(html.encode()) / 1e6, ", ".join(docs) or "none"))

if __name__ == "__main__":
    main()
