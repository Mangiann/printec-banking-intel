#!/usr/bin/env python3
"""Page-vision helper for the Printec knowledge base.

Text extraction (extract.py) misses anything that lives in a CHART, GRAPH or image.
This renders the actual PAGES of a document to PNG images so an agent can LOOK at them
with the Read tool (which reads PNG/JPG natively) — the only way to capture figures.

Backed by PyMuPDF (fitz): no external binary, and it opens owner/AES-encrypted PDFs
directly (authenticate("")). PPTX/PPT/DOCX are first converted to PDF (LibreOffice if
present, else Microsoft Office via COM) and then rendered.

Usage:
    python render_pages.py "<doc>" --count                 # -> {"pages": N}
    python render_pages.py "<doc>" --figures               # -> pages that likely hold a chart/figure/table
    python render_pages.py "<doc>" --pages "45-60,72" [--out DIR] [--dpi 140]
        # renders those 1-based pages to PNG, prints {"dir":..., "pages":[{page,path}]}

PNGs go to a TEMP working dir by default (they are transient — the *findings* live in the
digest text, not the images). Re-rendering the same page is skipped if the PNG already exists.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None


def _slug(path):
    base = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(path))[0].lower()).strip("-")
    h = hashlib.sha1(os.path.abspath(path).encode("utf-8")).hexdigest()[:8]
    return (base[:48] or "doc") + "-" + h


def parse_pages(spec, n):
    out = []
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            out += list(range(a, b + 1))
        else:
            out.append(int(part))
    # 1-based, clamp to [1, n], dedupe, keep order
    seen, res = set(), []
    for p in out:
        if 1 <= p <= n and p not in seen:
            seen.add(p); res.append(p)
    return res


# ---- convert Office files to PDF (cached in temp) so fitz can render them ----
def to_pdf(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return path
    cache = os.path.join(tempfile.gettempdir(), "kb-pdf")
    os.makedirs(cache, exist_ok=True)
    pdf = os.path.join(cache, _slug(path) + ".pdf")
    if os.path.isfile(pdf) and os.path.getsize(pdf) > 0:
        return pdf
    # 1) LibreOffice headless (cross-platform, no app needed)
    for exe in ("soffice", "libreoffice"):
        try:
            subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", cache, path],
                           check=True, capture_output=True, timeout=600)
            cand = os.path.join(cache, os.path.splitext(os.path.basename(path))[0] + ".pdf")
            if os.path.isfile(cand):
                if cand != pdf:
                    os.replace(cand, pdf)
                return pdf
        except Exception:
            pass
    # 2) Microsoft Office via COM (Windows; PowerPoint/Word installed on this machine)
    try:
        import win32com.client as win32
        import pythoncom
        pythoncom.CoInitialize()
        if ext in (".pptx", ".ppt"):
            app = win32.Dispatch("PowerPoint.Application")
            pres = app.Presentations.Open(os.path.abspath(path), WithWindow=False)
            pres.SaveAs(os.path.abspath(pdf), 32)   # 32 = ppSaveAsPDF
            pres.Close(); app.Quit()
            return pdf
        if ext in (".docx", ".doc"):
            app = win32.Dispatch("Word.Application")
            doc = app.Documents.Open(os.path.abspath(path))
            doc.SaveAs(os.path.abspath(pdf), FileFormat=17)  # 17 = wdFormatPDF
            doc.Close(); app.Quit()
            return pdf
    except Exception as e:
        raise SystemExit(json.dumps({"error": "could not convert to PDF (need LibreOffice or MS Office): %s" % e}))
    raise SystemExit(json.dumps({"error": "unsupported file type for rendering: %s" % ext}))


def open_doc(path):
    if fitz is None:
        raise SystemExit(json.dumps({"error": "PyMuPDF not installed — run `pip install pymupdf`"}))
    pdf = to_pdf(path)
    d = fitz.open(pdf)
    if d.needs_pass:
        d.authenticate("")
    return d


def figure_pages(d):
    """Pages that likely carry a chart/figure/table (where text extraction falls short):
    a sizeable raster image, a dense vector drawing (chart), or 'Figure/Chart/Exhibit/Table N' text."""
    pages = []
    for i in range(d.page_count):
        pg = d.load_page(i)
        area = abs(pg.rect.width * pg.rect.height) or 1
        big_img = False
        for img in pg.get_images(full=True):
            try:
                rects = pg.get_image_rects(img[0])
                if any(abs(r.width * r.height) / area > 0.04 for r in rects):
                    big_img = True; break
            except Exception:
                big_img = True; break
        txt = pg.get_text("text") or ""
        # a caption near the start of a line ("Figure 4.4 …", "Chart 2 …") signals a real exhibit;
        # plain "table" mentions in prose are ignored (text tables are already captured by extract.py).
        # NB: vector-drawing count is deliberately NOT used — many report PDFs draw gridlines/rules on
        # every page, so it flags ~everything. A figure-dense report is better handled by relevance-
        # targeted deep-read than by this filter.
        fig_txt = bool(re.search(r"(?mi)^\s*(figure|chart|exhibit)\s+\d", txt))
        if big_img or fig_txt:
            pages.append(i + 1)
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--pages")
    ap.add_argument("--out")
    ap.add_argument("--dpi", type=int, default=140)
    args = ap.parse_args()

    if not os.path.isfile(args.path):
        raise SystemExit(json.dumps({"error": "not a file: %s" % args.path}))

    d = open_doc(args.path)
    n = d.page_count

    if args.count:
        print(json.dumps({"pages": n})); return
    if args.figures:
        fp = figure_pages(d)
        print(json.dumps({"total": n, "figure_pages": fp, "n_figure_pages": len(fp)})); return
    if not args.pages:
        raise SystemExit(json.dumps({"error": "give --count, --figures, or --pages"}))

    out = args.out or os.path.join(tempfile.gettempdir(), "kb-pages", _slug(args.path))
    os.makedirs(out, exist_ok=True)
    rendered = []
    for p in parse_pages(args.pages, n):
        png = os.path.join(out, "p%04d.png" % p)
        if not (os.path.isfile(png) and os.path.getsize(png) > 0):
            pix = d.load_page(p - 1).get_pixmap(dpi=args.dpi)
            pix.save(png)
        rendered.append({"page": p, "path": png})
    print(json.dumps({"dir": out, "dpi": args.dpi, "pages": rendered}, ensure_ascii=False))


if __name__ == "__main__":
    main()
