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

# ---- the budget, encrypted behind the admin password (14/09/2026) -------------------------------
# One app, one file. The budget payload (budget/budget_actions.json + budget/budget_2027.json +
# budget/budget_2027_board.json when the board has sat) is
# encrypted with AES-256-GCM under a key derived from the password in budget/budget.password
# (PBKDF2-HMAC-SHA256, 200,000 rounds). The page holds only the ciphertext; the Admin link in the
# sidebar asks for the password and decrypts in the browser (WebCrypto). No file, no budget block.
def strip_stretch(cat):
    """The category file carries a 'stretch' scenario; the plain copy must not (the stretch is behind the password)."""
    c = json.loads(json.dumps(cat))
    c["scenarios"] = [x for x in c.get("scenarios", []) if x != "stretch"]
    for k in ("stretch", "rp_stretch", "total_stretch"):
        c.get("group", {}).pop(k, None)
    for k in ("waterfall", "by_source"):
        (c.get("group", {}).get(k) or {}).pop("stretch", None) if k == "waterfall" else (c.get(k) or {}).pop("stretch", None)
    for C in c.get("countries", []):
        for k in ("stretch", "rp_stretch", "total_stretch"):
            C.pop(k, None)
        (C.get("waterfall") or {}).pop("stretch", None)
        for x in C.get("subs", []):
            x.pop("stretch", None)
        for cell in C.get("cells", []):
            (cell.get("scen") or {}).pop("stretch", None)
    for cell in c.get("cells", []):
        (cell.get("scen") or {}).pop("stretch", None)
    (c.get("checks") or {}).pop("stretch", None)
    c.pop("_stretch", None)
    return c

def budget_block():
    """Since 24/09/2026 the base budget (EUR 180.0m) is embedded in PLAIN text and visible to every viewer
    (window.__DASH_BUDGET__); only the stretched budget (EUR 200.0m) and the category file's stretch scenario
    are encrypted behind the admin password (window.__DASH_BUDGET_ENC__, PBKDF2-HMAC-SHA256 200,000 rounds +
    AES-256-GCM, decrypted in the browser with WebCrypto)."""
    bdir = os.path.join(ROOT, "budget")
    p26, p27 = os.path.join(bdir, "budget_actions.json"), os.path.join(bdir, "budget_2027.json")
    if not os.path.exists(p26):
        return "", "", "no budget data (budget/budget_actions.json missing)"
    plain = {"budget": json.loads(rd(p26))}
    if os.path.exists(p27):
        p = json.loads(rd(p27)); p.pop("rows", None); plain["budget_2027"] = p
    pbd = os.path.join(bdir, "budget_2027_board.json")     # the plan (board_2027.py target)
    if os.path.exists(pbd):
        plain["budget_2027_board"] = json.loads(rd(pbd))
    pcat = os.path.join(bdir, "budget_2027_categories.json")   # the plan in the Excel's HW/SW/SV/OUT categories
    cat_full = json.loads(rd(pcat)) if os.path.exists(pcat) else None
    if cat_full:
        plain["budget_2027_categories"] = strip_stretch(cat_full)
    secret = {}
    pst = os.path.join(bdir, "budget_2027_stretch.json")   # the stretch to EUR 200.0m (board_2027.py stretch)
    if os.path.exists(pst):
        secret["budget_2027_stretch"] = json.loads(rd(pst))
        if cat_full:
            secret["budget_2027_categories"] = cat_full
    plain_js = "window.__DASH_BUDGET__ = " + json.dumps(plain, ensure_ascii=False) + ";"
    if not secret:
        return plain_js, "", "base budget in plain text; no stretch to encrypt"
    pw_path = os.path.join(bdir, "budget.password")
    if os.path.exists(pw_path):
        password = rd(pw_path).strip()
    else:
        import secrets, string
        password = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(14))
        with open(pw_path, "w", encoding="utf-8") as f:
            f.write(password + "\n")
        os.chmod(pw_path, 0o600)
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt, iv, iters = os.urandom(16), os.urandom(12), 200_000
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters).derive(password.encode("utf-8"))
    ct = AESGCM(key).encrypt(iv, json.dumps(secret, ensure_ascii=False).encode("utf-8"), None)
    blob = {"v": 1, "kdf": "PBKDF2-SHA256", "iter": iters, "salt": base64.b64encode(salt).decode(),
            "iv": base64.b64encode(iv).decode(), "ct": base64.b64encode(ct).decode()}
    return plain_js, "window.__DASH_BUDGET_ENC__ = " + json.dumps(blob) + ";", "base budget in plain text; stretch encrypted (password in %s)" % os.path.relpath(pw_path, ROOT)

def main():
    data = rd(os.path.join(WEB, "data.json")).strip()
    dash = json.loads(data)
    docs = collect_docs(dash)

    logo = base64.b64encode(open(os.path.join(WEB, "printec-logo.svg"), "rb").read()).decode()
    idx  = rd(os.path.join(WEB, "index.html"))
    body = idx[idx.index('<div class="layout">'):idx.index("</div>\n<script defer") + len("</div>")]
    body = body.replace('src="printec-logo.svg"', 'src="data:image/svg+xml;base64,%s"' % logo)

    app = patch_artifact.apply(rd(os.path.join(WEB, "app.js")))
    # the chat lives inside app.js's own function scope (it needs DASH, sigByKey, mdToHtml ...): insert it
    # before the closing "})();" of the renderer
    _tail = "\n})();"
    assert app.rstrip().endswith("})();"), "app.js no longer ends with the renderer's closing })();"
    _i = app.rstrip().rfind(_tail)
    import datetime as _dt
    app = app[:_i] + "\n" + patch_artifact.ASK_JS.replace("__ASK_BUILD__", _dt.datetime.now().strftime("%d/%m/%Y %H:%M")) + app[_i:]

    parts = [
        "<title>Printec Intelligence Dashboard</title>",
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">',
        "<style>", rd(os.path.join(WEB, "styles.css")).rstrip("\n"),
        # single-file build: no architecture sub-page to link to, and paint the canvas explicitly
        "\n/* single-file build */\n.archbtn{display:none !important}\nhtml,body{background:var(--bg)}\n",
        patch_artifact.CSS, patch_artifact.ASK_CSS, "</style>",
        body,
        "<script>", rd(os.path.join(HERE, "chart.umd.min.js")).rstrip("\n"), "</script>",
        "<script>", "window.__DASH_DATA__ = " + data + ";", "</script>",
        "<script>", "window.__DASH_DOCS__ = " + json.dumps(docs, ensure_ascii=False) + ";", "</script>",
    ]
    plain_js, enc_js, budget_note = budget_block()
    if plain_js:
        parts += ["<script>", plain_js, "</script>"]
    if enc_js:
        parts += ["<script>", enc_js, "</script>"]
    for js in ("atm-sources.js", "product-outlooks.js", "footprint-map.js"):
        parts += ["<script>", "/* %s */" % js, rd(os.path.join(WEB, js)).rstrip("\n"), "</script>"]
    parts += ["<script>", "/* app.js */", app, "</script>"]

    html = "\n".join(parts) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  %.2f MB  (embedded docs: %s)"
          % (OUT, len(html.encode()) / 1e6, ", ".join(docs) or "none"))
    print("budget: %s" % budget_note)

if __name__ == "__main__":
    main()
