#!/usr/bin/env python3
"""make_test_build.py - a TEST-ONLY variant of the artifact for checking the Budget tab in a browser.

It builds the normal single-file artifact into <out>, then embeds the budget payload in PLAIN text as
window.__DASH_BUDGET_PLAIN__ and shims the Admin unlock so the tab opens with an empty password. It also
adds a charset meta tag so a plain static server renders the middle dots correctly.
NEVER publish or share the output: the budget is readable in it.

  python3 make_test_build.py <out.html>
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "printec-dashboard.TEST.html")
subprocess.run([sys.executable, os.path.join(HERE, "build_artifact.py"), out], check=True, cwd=HERE)
h = open(out, encoding="utf-8").read()
bdir = os.path.join(ROOT, "budget")
payload = {}
pst = os.path.join(bdir, "budget_2027_stretch.json")
if os.path.exists(pst):
    payload["budget_2027_stretch"] = json.load(open(pst))
pcat = os.path.join(bdir, "budget_2027_categories.json")
if os.path.exists(pcat):
    payload["budget_2027_categories"] = json.load(open(pcat))
old = "const P=await budgetDecrypt(inp.value);"; assert h.count(old) == 1
h = h.replace(old, "const P=window.__DASH_BUDGET_PLAIN__||await budgetDecrypt(inp.value);")
h = h.replace("<script>\nwindow.__DASH_BUDGET_ENC__", "<script>window.__DASH_BUDGET_PLAIN__=" + json.dumps(payload, ensure_ascii=False) + ";</script>\n<script>\nwindow.__DASH_BUDGET_ENC__", 1)
assert "__DASH_BUDGET_PLAIN__=" in h
if "<meta charset" not in h:
    h = '<meta charset="utf-8">\n' + h
open(out, "w", encoding="utf-8").write(h)
print("TEST build (budget in plain text, do not share): %s  %.2f MB" % (out, len(h.encode()) / 1e6))
