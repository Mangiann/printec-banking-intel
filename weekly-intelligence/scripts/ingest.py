#!/usr/bin/env python3
"""
ingest.py - Build the structured data cache for the Printec weekly intelligence dashboard.

Reads (from the Banking research folder):
  - master-signal-table.md             -> signals.json (+ maintains _ledger.json for week-over-week)
  - history/bank-history-*.xlsx        -> timeseries.json, series.json, events.json, patterns.json
  - findings/04-statistics/<latest>.md -> country_stats.json
Writes a run summary to summary.json.

Nothing here invents numbers: every value is copied from a source file. The only "analysis" is
classification (mapping text to Printec product categories / countries) and arithmetic over values
that already exist (YoY %, a transparent signal-strength weighting).

Usage:
  python ingest.py --root <BANKING_folder> [--skill <engine_dir>] [--refs <dir>] [--data <dir>] [--week YYYY-MM-DD]
Defaults: --skill = this script's parent's parent; --refs = <skill>/references; --data = <skill>/data;
--week = today (UTC). For the first seed run pass the master table's last-triangulation date.
"""
import argparse, json, re, os, glob, datetime

# ---------- helpers ----------
def load_json(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else {}

def slug(s):
    s = re.sub(r"\*\*", "", s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]

def strip_md(s):
    return "" if s is None else s.replace("**", "").strip()

def md_links(s):
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", s or "")

def yoy_from_text(s):
    if not s: return None
    m = re.search(r"([-+]?\d+(?:\.\d+)?)\s*%", s)
    return float(m.group(1)) if m else None

# ---------- country normalization ----------
def build_country_resolver(footprint):
    alias_to_code = {}
    for code, names in footprint["aliases"].items():
        for n in names:
            alias_to_code[n.lower()] = code
    for c in footprint["countries"]:
        alias_to_code[c["name"].lower()] = c["code"]
    markers = [m.lower() for m in footprint["footprint_wide_markers"]]
    iso2 = [c["code"] for c in footprint["countries"]]
    iso2_re = re.compile(r"(?<![A-Za-z])(" + "|".join(iso2) + r")(?![A-Za-z])")
    def resolve(text):
        raw = text or ""
        t = raw.lower()
        codes = []
        for name, code in alias_to_code.items():
            if re.search(r"\b" + re.escape(name) + r"\b", t) and code not in codes:
                codes.append(code)
        for m in iso2_re.findall(raw):           # uppercase ISO2 shorthand e.g. "Greece, BG, RO"
            if m not in codes:
                codes.append(m)
        wide = any(mk in t for mk in markers) or len(codes) >= 5
        return codes, wide
    return resolve

# ---------- product classification (word-boundary aware; trailing '*' = stem) ----------
def compile_product_patterns(product_map):
    compiled = []
    for cat in product_map["categories"]:
        pats = []
        for kw in cat["keywords"]:
            k = kw.lower().strip()
            left = r"(?<![a-z0-9])"
            if k.endswith("*"):
                pats.append(re.compile(left + re.escape(k[:-1])))
            else:
                pats.append(re.compile(left + re.escape(k) + r"(?![a-z0-9])"))
        compiled.append((cat["id"], pats))
    return compiled

def classify_products(text, compiled):
    t = (text or "").lower()
    return [cid for cid, pats in compiled if any(p.search(t) for p in pats)]

CONF_WEIGHT = {"High": 3.0, "Medium-High": 2.5, "Medium": 2.0, "Medium-Low": 1.5, "Low": 1.0, "": 1.0}

def norm_conf(s):
    head = strip_md(s).split("(")[0].strip().lower()
    if "medium-high" in head or ("medium" in head and "high" in head): return "Medium-High"
    if "high" in head: return "High"
    if "medium" in head: return "Medium"
    if "low" in head: return "Low"
    return ""

def score_signal(s):
    w = CONF_WEIGHT.get(s["confidence"], 1.0)
    agent_bonus = min(len(s["agents"]), 3) * 0.4
    like = (s.get("likelihood") or "").lower()
    like_bonus = 0.6 if "high" in like else (0.0 if "medium" in like else -0.2)
    return round(w + agent_bonus + like_bonus, 2)

# ---------- opportunity SIZE band ----------
def norm_size(s):
    head = re.split(r"[\s(/]", strip_md(s), 1)[0].upper()
    return head if head in ("XL", "L", "M", "S") else "Unscoped"

# ---------- contest-type lanes (REPLACES the old win-probability / expected-value model) ----------
# The dashboard NEVER asserts the odds of winning a deal — that is the sales teams' judgement, not
# market intelligence's. Instead every signal is routed to exactly ONE lane; only the 'opportunity'
# lane is shown as a biddable near-term opportunity. contest_type is AUTHORED by the orchestrator in
# the master-table 'Type' column (authoritative). A CONSERVATIVE keyword fallback fires only when the
# Type cell is blank, so legacy tables / a first run still classify; it never INFERS incumbent_renewal
# or lost (those facts are often absent from the prose, and an incumbency ANCHOR inside a net-new row
# must not demote it) — an unauthored row defaults to net_new_contest and is never silently hidden.
CONTEST_TYPES = ("net_new_contest", "incumbent_renewal", "owned_asset", "lost", "threat_macro")
CONTEST_LANE  = {"net_new_contest": "opportunity", "incumbent_renewal": "installed_base",
                 "owned_asset": "installed_base", "lost": "lost", "threat_macro": "context"}

def norm_contest_type(cell):
    h = strip_md(cell).strip().lower().replace("-", "_").replace(" ", "_")
    for t in CONTEST_TYPES:
        if t in h:
            return t
    return {"netnew": "net_new_contest", "net_new": "net_new_contest", "contest": "net_new_contest",
            "open": "net_new_contest", "renewal": "incumbent_renewal", "incumbent": "incumbent_renewal",
            "owned": "owned_asset", "secured": "owned_asset", "macro": "threat_macro",
            "threat": "threat_macro", "driver": "threat_macro"}.get(h, "")

def classify_contest(s):
    """Deterministic fallback used ONLY when the Type cell is blank. Conservative by design: owned_asset
    from a SECURED status, threat_macro from a footprint-wide driver with no named market, else
    net_new_contest — so a genuine contest is never hidden by a guess.
    NOTE (2026-08): a MISSING deal size is no longer evidence of a macro driver. Poor financial disclosure
    is the norm in this footprint (most SEE/CEE tenders never publish a value), so an unsized row is
    classified on its SHAPE (is there a discrete buyer + scope?), never on whether a euro figure exists.
    Unsized rows therefore fall through to net_new_contest and stay visible as value-unscoped
    opportunities; only a driver with no addressable market at all is demoted to threat_macro."""
    if s.get("status") == "SECURED":
        return "owned_asset"
    if s.get("footprint_wide") and not s.get("countries"):
        return "threat_macro"
    return "net_new_contest"

# A market name as the theme's head ("Romania — ...") means the row is about a MARKET, not about a
# counterparty anyone can call. Aliases cover the short forms the agents write.
_MARKET_HEAD_ALIAS = {"czechia": "czech republic", "bosnia": "bosnia & herzegovina",
                      "macedonia": "north macedonia", "herzegovina": "bosnia & herzegovina"}


def has_named_counterparty(s, market_names):
    """Does this row name someone who could actually buy — a bank, a post, a ministry, an agency?

    The master table's convention is "<counterparty> — <what happened>", so a head that is just a
    market name is a market-level observation with no addressable buyer.
    """
    head = (s.get("bank_theme") or "").split("—")[0].split(" - ")[0].strip().lower().rstrip(",")
    head = _MARKET_HEAD_ALIAS.get(head, head)
    return bool(head) and head not in market_names


def is_biddable(s, market_names):
    """The stricter opportunity test (strategy call, 04/09/2026 — "πιο αυστηρό").

    Until now anything shaped like a contest and still current counted as an opportunity, and the
    fallback classifier defaults an unrecognised Type to net_new_contest — so market-level conditions
    with nobody to call and no date to work to were ranked beside named, dated tenders and inflated
    the pipeline. A row now has to offer the sales team a handle on it: either somebody to approach,
    or a date to work back from. A row with NEITHER is real and stays visible, but as market context —
    a reason to sell, not a thing to bid for. Returns (ok, reason_if_not).
    """
    named = has_named_counterparty(s, market_names)
    dated = bool(s.get("has_future_trigger") or s.get("future_date"))
    if named or dated:
        return True, ""
    return False, ("no named buyer and no deadline — a market condition, not a deal anyone can bid for")


# ---------- master table parser (header-driven: columns found by name, so order can change) ----------
def _col(header, *keys):
    for i, h in enumerate(header):
        if any(k in h for k in keys):
            return i
    return -1

# ---------- recency gate (deterministic, Tier-0) ----------
# Parse the signal's free-text date string, find the most-recent PAST development and the nearest FUTURE
# trigger, and classify how fresh the signal really is. This guarantees that a row whose only datable
# anchor is an old standing fact (an incumbency/deal from 2017-2025) can NEVER be silently shown as a
# fresh "NEW" finding — it is flagged stale_new and the dashboard tags it as standing context instead.
_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

def _parse_dates(s):
    """All concrete dates found in a free-text date string (DD/MM/YYYY, Mon YYYY, Qn YYYY, bare/End/FY YYYY)."""
    s = s or ""
    out = []
    for d, m, y in re.findall(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})", s):
        try: out.append(datetime.date(int(y), int(m), int(d)))
        except ValueError: pass
    for mon, y in re.findall(r"([A-Za-z]{3,9})[ \-/]+(\d{4})", s):
        mm = _MONTHS.get(mon[:3].lower())
        if mm: out.append(datetime.date(int(y), mm, 15))
    for q, y in re.findall(r"[Qq]([1-4])[ \-/]*(\d{4})", s):
        out.append(datetime.date(int(y), min(int(q) * 3, 12), 15))
    yrs = {d.year for d in out}
    for y in re.findall(r"(?<!\d)(\d{4})(?!\d)", s):
        yi = int(y)
        if 2000 <= yi <= 2099 and yi not in yrs:
            if re.search(r"(end[\- ]?%d|fy[\- ]?%d|%d[\- ]?end)" % (yi, yi, yi), s.lower()):
                out.append(datetime.date(yi, 12, 31))
            else:
                out.append(datetime.date(yi, 6, 30))
            yrs.add(yi)
    return out

def recency_fields(date_str, week, status):
    try: wk = datetime.date.fromisoformat(week)
    except Exception: wk = datetime.date.today()
    ds = _parse_dates(date_str)
    past = [d for d in ds if d <= wk]
    fut  = [d for d in ds if d > wk]
    dev, nf = (max(past) if past else None), (min(fut) if fut else None)
    age = (wk - dev).days if dev else None
    rec = "undated" if dev is None else ("fresh" if age <= 92 else ("recent" if age <= 183 else "standing"))
    has_fut = nf is not None and (nf - wk).days <= 550          # a deadline within ~18 months keeps it current
    current = rec in ("fresh", "recent") or has_fut
    return {
        "dev_date": dev.isoformat() if dev else "", "age_days": age, "recency": rec,
        "future_date": nf.isoformat() if nf else "", "has_future_trigger": has_fut,
        "is_current": current,
        "stale_new": (rec == "standing" and not has_fut) or ((status in ("NEW", "UPDATED")) and not current),
    }

_STATUS_WORDS = ("NEW", "UPDATED", "UNCHANGED", "SECURED", "LOST")

def _is_status_cell(cell):
    return strip_md(cell).strip().upper() in _STATUS_WORDS

def apply_primary_overrides(rows, overrides):
    """Re-file the lead product where a human has said the automatic choice is wrong.

    `primary_product` is products[0], and `products` comes back in product_map.json's own category
    order — so every row that mentions an ATM at all leads on atm_recycling, whatever it is really
    about. Fixing that ranking would move the lead product on roughly 120 of ~295 signals, which is
    a call for the team, not a silent change. Until then this handles the rows where the result is
    plainly wrong. An override naming a product the row never matched is refused, loudly: it would
    otherwise invent a classification rather than correct one.
    """
    if not overrides:
        return 0
    n = 0
    for r in rows:
        ov = overrides.get(r["key"])
        if not ov:
            continue
        want = ov.get("primary_product") if isinstance(ov, dict) else ov
        if want not in (r.get("products") or []):
            print("WARNING primary-product override ignored for %s: %r is not among its matched "
                  "products %r" % (r["key"], want, r.get("products")))
            continue
        if r.get("primary_product") == want:
            continue
        r["products"] = [want] + [p for p in r["products"] if p != want]
        r["primary_product"] = want
        n += 1
    return n


def _critic_hash(row):
    """The same text hash product_critic.py stores beside a verdict, so 'stale' means the same thing here."""
    try:
        from product_critic import text_hash
        return text_hash(row)
    except Exception:
        return None


def apply_product_reviews(rows, reviews, valid_ids):
    """Replace the keyword-matched product list with the critic's verdict (decision of 09/09/2026).

    The keyword matcher tags a signal with every category whose words appear anywhere in its text,
    so a long row lands in six or seven lines it is not about. product_critic.py has an LLM read
    each row and keep only the lines it is really about; the verdicts sit in product_review.json.
    A verdict is applied even when the signal text has changed since it was made (a slightly stale
    verdict still beats the keyword spray); such rows are counted so the critic can re-judge them.
    The keyword list is kept on the row as `products_keyword` for reference.
    """
    if not reviews:
        return 0, 0
    applied = stale = 0
    for r in rows:
        v = reviews.get(r["key"])
        if not v:
            continue
        prods = [p for p in (v.get("products") or []) if p in valid_ids]
        if not prods:
            print("WARNING product review ignored for %s: no valid taxonomy id in %r" % (r["key"], v.get("products")))
            continue
        r["products_keyword"] = list(r.get("products") or [])
        r["products"] = prods
        r["primary_product"] = prods[0]
        r["product_review_why"] = v.get("why") or ""
        applied += 1
        if v.get("text_hash") and _critic_hash(r) != v["text_hash"]:
            stale += 1
    return applied, stale


def parse_master_table(path, resolve, compiled):
    """Parse the Active-signals table into signal dicts.

    HARDENED (2026-08): parsing is now SECTION-SCOPED, not position-fragile. The old parser stopped at
    the first blank line or non-status row and silently ignored everything after it, so a row appended in
    the wrong spot (e.g. after a `---` separator) just vanished with no error — a real hazard for an
    unattended routine run. Now we ingest every signal-shaped row inside the `## Active signals` section
    regardless of intervening blanks/separators, and RECONCILE at the end: any signal-shaped row that was
    seen but not parsed, or that sits outside Active-signals/Archive, is reported LOUDLY instead of lost.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rows, header, section = [], None, None
    seen_by_section = {}                     # count of full (>=10-col) signal-shaped rows, per section
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## "):              # a new section cancels any table header in force
            section = s[3:].strip().lower(); header = None; continue
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        low = [c.lower() for c in cells]
        # tally anything that looks like a real signal row (>=10 cols + status keyword), wherever it is
        if len(cells) >= 10 and cells and _is_status_cell(cells[0]):
            seen_by_section[section] = seen_by_section.get(section, 0) + 1
        if section is None or "active signals" not in section:   # only Active signals is ingested
            continue
        if low and low[0] == "status":       # the active-signals header row
            header = low; continue
        if set("".join(cells)) <= set("-: "):                    # markdown separator row → skip, don't stop
            continue
        if header is None or len(cells) < 10 or not _is_status_cell(cells[0]):
            continue                          # blank line, sub-note, or malformed row → skip, don't stop
        status = strip_md(cells[0])
        def g(*keys, default=""):
            i = _col(header, *keys)
            return cells[i] if 0 <= i < len(cells) else default
        bank_theme   = strip_md(g("bank", "theme"))
        country_cell = g("country")
        signal       = g("signal")
        source       = g("source")
        date         = strip_md(g("date"))
        implies      = g("implies", "what it")
        likelihood   = strip_md(g("likelihood"))
        confidence   = norm_conf(g("confidence"))
        follow_up    = g("recommended", "follow")
        size_band    = norm_size(g("opp", "size"))
        contest_type = norm_contest_type(g("type", "contest"))
        blob = " ".join([bank_theme, country_cell, signal, implies, follow_up])
        codes, wide = resolve(country_cell + " " + bank_theme)
        agents = sorted(set(re.findall(r"A[1-6]", source)))
        products = classify_products(blob, compiled)
        rows.append({
            "key": slug(bank_theme), "status": status.upper(), "bank_theme": bank_theme,
            "country_raw": strip_md(country_cell), "countries": codes, "footprint_wide": wide,
            "signal": signal,
            "sources": [{"text": t, "url": u} for t, u in md_links(source)] or [{"text": strip_md(source), "url": ""}],
            "agents": agents, "date": date, "implies": implies, "likelihood": likelihood,
            "confidence": confidence, "follow_up": follow_up,
            "size_band": size_band, "contest_type": contest_type,
            "products": products, "primary_product": products[0] if products else None,
        })
    # ---- reconciliation: never let a signal row vanish silently ----
    active_seen = sum(n for sec, n in seen_by_section.items() if sec and "active signals" in sec)
    if active_seen != len(rows):
        print("WARNING master-table: %d signal-shaped rows in the Active-signals section but %d parsed "
              "(%d dropped) — a row is malformed (wrong column count?). FIX before trusting this build."
              % (active_seen, len(rows), active_seen - len(rows)))
    orphan = {sec: n for sec, n in seen_by_section.items()
              if not (sec and ("active signals" in sec or "archive" in sec))}
    if orphan:
        where = ", ".join("%s:%d" % (k or "(no section)", v) for k, v in orphan.items())
        print("WARNING master-table: %d signal-shaped row(s) sit OUTSIDE Active-signals/Archive (%s) and were "
              "NOT ingested — move them into '## Active signals' or they stay invisible on the dashboard."
              % (sum(orphan.values()), where))
    return rows

# ---------- xlsx parsers ----------
def parse_xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ts, events, patterns = [], [], []
    if "Metrics" in wb.sheetnames:
        ws = wb["Metrics"]; hdr = [c.value for c in ws[1]]
        for r in ws.iter_rows(min_row=2, values_only=True):
            if not r[0]: continue
            rec = dict(zip(hdr, r))
            ts.append({"country": rec.get("Country"), "scope": rec.get("Bank / Scope"),
                       "metric": rec.get("Metric"), "unit": rec.get("Unit"),
                       "period": str(rec.get("Period")) if rec.get("Period") is not None else None,
                       "value": rec.get("Value"), "source": rec.get("Source"), "url": rec.get("URL"),
                       "source_date": str(rec.get("Source date") or ""),
                       "confidence": rec.get("Confidence"), "notes": rec.get("Notes")})
    for sheet, bucket in [("Milestones", events), ("Patterns", patterns)]:
        if sheet in wb.sheetnames:
            ws = wb[sheet]; hdr = [c.value for c in ws[1]]
            for r in ws.iter_rows(min_row=2, values_only=True):
                if not r[0]: continue
                bucket.append({k: (str(v) if v is not None else "") for k, v in dict(zip(hdr, r)).items()})
    return ts, events, patterns

def build_series(timeseries):
    KEY = {"ATMs": "atms", "Bank branches": "branches", "Branches": "branches",
           "POS terminals": "pos", "Payment terminals": "pos"}
    series = {}
    for rec in timeseries:
        scope = rec.get("scope") or ""
        if "Sector" not in scope and "benchmark" not in scope.lower(): continue
        metric = rec.get("metric")
        if metric not in KEY: continue
        per = (rec.get("period") or "").strip()
        if not re.fullmatch(r"(19|20)\d{2}", per): continue
        v = rec.get("value")
        if not isinstance(v, (int, float)): continue
        series.setdefault(rec.get("country"), {}).setdefault(KEY[metric], []).append({"year": int(per), "value": v})
    for c in series:
        for k in series[c]:
            series[c][k].sort(key=lambda p: p["year"])
    return series

# ---------- statistics findings country-trends parser ----------
def parse_country_stats(findings_dir, resolve):
    files = sorted(glob.glob(os.path.join(findings_dir, "04-statistics", "*.md")))
    files = [f for f in files if re.search(r"\d{4}-\d{2}-\d{2}", f)]
    if not files:
        return [], None
    # Walk newest -> oldest and use the most recent file that ACTUALLY carries the table. A statistics
    # cycle that skipped the Country-trends section used to blank the whole Countries table (the newest
    # file won unconditionally); now the last good figures survive and we say how old they are.
    for path in sorted(files, reverse=True):
        out, m = _country_stats_from(path, resolve)
        if out:
            if path != sorted(files)[-1]:
                print("country-stats: newest statistics file %s carries no Country-trends table; fell back "
                      "to %s (figures are that old — surface as a coverage gap)."
                      % (os.path.basename(sorted(files)[-1]), os.path.basename(path)))
            return out, os.path.basename(path)
    print("country-stats: NO statistics findings file carries a Country-trends table — the Countries "
          "table will show only ECB-derived rows.")
    return [], os.path.basename(sorted(files)[-1])


def _country_stats_from(path, resolve):
    text = open(path, encoding="utf-8").read()
    # Tolerant heading match: "Country trends summary", "Country-trends summary", any case — so a
    # small wording/punctuation drift in the harness render can never silently empty country_stats.
    m = re.search(r"##\s*country[\s-]?trends\s+summary.*?\n(.*?)(\n##\s|\Z)", text, re.S | re.I)
    out = []
    if m:
        lines = [l for l in m.group(1).splitlines() if l.strip().startswith("|")]
        header = None
        for l in lines:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]; continue
            if set("".join(cells)) <= set("-: "): continue
            rec = dict(zip(header, cells))
            cname = rec.get("country", "")
            codes, _ = resolve(cname)
            out.append({"country_name": cname, "code": codes[0] if codes else None,
                        "atms": rec.get("atms", ""), "branches": rec.get("branches", ""),
                        "cash_trend": rec.get("cash trend", ""),
                        "instant_payments": rec.get("instant payments", ""),
                        "implication": rec.get("implication for printec", "") or rec.get("implication", ""),
                        "atms_yoy": yoy_from_text(rec.get("atms", "")),
                        "branches_yoy": yoy_from_text(rec.get("branches", ""))})
    return out, m

# ---------- structural series merge (fetch_ecb.py EU output + researched non-EU output) ----------
SERIES_MNAME = {"atms": "ATMs", "pos": "POS terminals", "branches": "Bank branches",
                "cash": "Cash withdrawals", "cards": "Payment cards"}

def merge_structural(series, timeseries, data, footprint,
                     fname="structural_series.json", default_source="ECB Data Portal", notes_tag="ECB"):
    """Fold a structural-series JSON into series.json (charts) + timeseries.json (forecast).
    Used twice: structural_series.json (EU, scripted by fetch_ecb.py) and structural_series_noneu.json
    (non-EU, researched by Agent 4's harness and written by its SKILL). The hand-curated workbook series
    win where present (Greece ATMs/branches); these fill everything else. A non-EU file may carry per-point
    `source`/`url`/`unit` (one source per country differs: NBS, NBU, CBK...), so points override file-meta."""
    ext = load_json(os.path.join(data, fname), {})
    if not ext.get("series"):
        return 0, 0
    code2name = {c["code"]: c["name"] for c in footprint.get("countries", [])}
    meta = ext.get("meta", {})
    src_label = ext.get("source", default_source)
    added_series = added_rows = 0
    for cc, metrics in ext["series"].items():
        name = code2name.get(cc, cc)
        for mkey, pts in metrics.items():
            if not pts or series.get(name, {}).get(mkey):     # workbook/EU already has it -> keep it
                continue
            series.setdefault(name, {})[mkey] = [
                {"year": p["year"], "value": p["value"], **({"provisional": True} if p.get("provisional") else {})}
                for p in pts]
            added_series += 1
            m = meta.get(mkey, {})
            for p in pts:
                timeseries.append({"country": name, "scope": "Sector", "metric": SERIES_MNAME.get(mkey, mkey),
                                   "unit": p.get("unit") or m.get("unit", ""), "period": str(p["year"]), "value": p["value"],
                                   "source": p.get("source") or src_label, "url": p.get("url") or m.get("source_url", ""),
                                   "source_date": p.get("source_date") or ext.get("generated", ""),
                                   "confidence": "Low" if p.get("provisional") else "",
                                   "notes": (p.get("notes") or notes_tag) + (" (provisional)" if p.get("provisional") else "")})
                added_rows += 1
    return added_series, added_rows

# ---------- EU country-stats derived from the scripted ECB series (so the dashboard per-country card
# stays full-footprint even when the findings file's Country-trends table holds only the researched
# non-EU rows). Numbers + YoY come from structural_series.json; the slow-changing qualitative cells
# (instant-payments scheme status, Printec implication) come from references/eu_country_notes.json. ----
def _fmt_count(v):
    try:
        return f"{int(round(float(v))):,}"
    except Exception:
        return str(v)

def _latest_two(pts):
    pts = sorted([p for p in (pts or []) if isinstance(p.get("value"), (int, float))], key=lambda p: p["year"])
    if not pts:
        return None, None
    return pts[-1], (pts[-2] if len(pts) >= 2 else None)

def _yoy(last, prev):
    if last and prev and prev.get("value"):
        return round((last["value"] - prev["value"]) / prev["value"] * 100.0, 1)
    return None

def derive_structural_country_stats(data, footprint, present_codes, eu_notes,
                                    fname="structural_series.json", mark="◇"):
    ext = load_json(os.path.join(data, fname), {})
    if not ext.get("series"):
        return []
    code2name = {c["code"]: c["name"] for c in footprint.get("countries", [])}
    gen = ext.get("generated", "")
    out = []
    for cc, metrics in ext["series"].items():
        if cc in present_codes:                       # findings file already supplies this country -> keep richer row
            continue
        a_last, a_prev = _latest_two(metrics.get("atms"))
        b_last, b_prev = _latest_two(metrics.get("branches"))
        c_last, c_prev = _latest_two(metrics.get("cash"))
        a_yoy, b_yoy, c_yoy = _yoy(a_last, a_prev), _yoy(b_last, b_prev), _yoy(c_last, c_prev)
        def cell(last, yoy):
            if not last:
                return ""
            m = mark + " " if last.get("provisional") else ""
            y = f", {'+' if (yoy or 0) >= 0 else ''}{yoy}% y/y" if yoy is not None else ""
            return f"{_fmt_count(last['value'])} {m}{last['year']}{y} (ECB)"
        if c_yoy is None:
            cash_trend = ""
        elif c_yoy < 0:
            cash_trend = f"↓ cash withdrawals falling ({c_yoy}% y/y)"
        elif c_yoy > 0:
            cash_trend = f"↑ cash withdrawals rising (+{c_yoy}% y/y)"
        else:
            cash_trend = "→ cash withdrawals flat y/y"
        note = eu_notes.get(cc, {})
        out.append({"country_name": code2name.get(cc, cc), "code": cc,
                    "atms": cell(a_last, a_yoy), "branches": cell(b_last, b_yoy),
                    "cash_trend": cash_trend or note.get("cash_trend", ""),
                    "instant_payments": note.get("instant_payments", ""),
                    "implication": note.get("implication", ""),
                    "atms_yoy": a_yoy, "branches_yoy": b_yoy,
                    "source": "ECB Data Portal (scripted)", "source_date": gen})
    return out

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Banking research folder")
    ap.add_argument("--skill", help="Engine folder with references/ (default: this script's parent's parent)")
    ap.add_argument("--refs", help="Reference JSON folder (default: <skill>/references)")
    ap.add_argument("--data", help="Writable cache folder (default: <skill>/data)")
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    skill = args.skill or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ref = args.refs or os.path.join(skill, "references")
    data = args.data or os.path.join(skill, "data")
    os.makedirs(data, exist_ok=True)

    footprint = load_json(os.path.join(ref, "footprint.json"))
    product_map = load_json(os.path.join(ref, "product_map.json"))
    resolve = build_country_resolver(footprint)
    compiled = compile_product_patterns(product_map)

    overrides = (load_json(os.path.join(ref, "primary_product_overrides.json"), {}) or {}).get("overrides", {})

    master = os.path.join(args.root, "master-signal-table.md")
    signals = parse_master_table(master, resolve, compiled)
    # the critic's product verdicts go on first; the hand overrides below still win the lead product
    _reviews = (load_json(os.path.join(ref, "product_review.json"), {}) or {}).get("reviews", {})
    _valid = {c["id"] for c in product_map["categories"]}
    _a, _stale = apply_product_reviews(signals, _reviews, _valid)
    if _a:
        print("product lines set by the critic on %d signal(s) (product_review.json)%s"
              % (_a, ("; %d made on older text - run product_critic.py batches to re-judge" % _stale) if _stale else ""))
    _unrev = [x["key"] for x in signals if x["key"] not in _reviews]
    if _reviews and _unrev:
        print("%d signal(s) still carry keyword-only product tags - run the product critic on them" % len(_unrev))
    _n = apply_primary_overrides(signals, overrides)
    if _n:
        print("re-filed the lead product on %d signal(s) from primary_product_overrides.json" % _n)
    _market_names = {c["name"].strip().lower() for c in footprint.get("countries", [])}
    ledger = load_json(os.path.join(data, "_ledger.json"), {})
    new_count = stale_new_count = demoted = 0
    for s in signals:
        k = s["key"]
        if k in ledger and ledger[k]:
            s["week_first_seen"] = ledger[k]
        else:
            s["week_first_seen"] = args.week; ledger[k] = args.week
        s["week_last_confirmed"] = args.week
        s["table_new"] = (s["week_first_seen"] == args.week) or s["status"] == "NEW"   # new TO THE TABLE
        s.update(recency_fields(s.get("date", ""), args.week, s["status"]))             # recency gate
        # "new this week" now means: new to the table AND a genuinely current development (recent or a
        # near-future trigger) — NOT an old standing fact added to the table for the first time.
        s["is_new_this_week"] = s["table_new"] and s["is_current"]
        if s["is_new_this_week"]: new_count += 1
        if s["stale_new"]: stale_new_count += 1
        s["strength"] = score_signal(s)
        # objective deal-size value (€m) from the size band — anchored to tender/capex figures where known.
        # Shown as factual CONTEXT only; never combined with any win/probability term (which we don't compute).
        s["pot_value"] = {"XL": 7.5, "L": 3.0, "M": 0.6, "S": 0.1}.get(s.get("size_band", ""), 0)
        # contest_type (authored Type cell, else a conservative fallback) routes each signal to ONE lane.
        # Only lane=='opportunity' is a biddable near-term opportunity. owned assets + incumbent renewals ->
        # 'installed_base' (own & defend, certain revenue, NOT a contest); competitor-won scopes -> 'lost'
        # (competitive intel); macro/threats -> 'context'. We do NOT estimate win-probability.
        if not s.get("contest_type"):
            s["contest_type"] = classify_contest(s)
        s["lane"] = CONTEST_LANE.get(s["contest_type"], "opportunity")
        s["held"] = (s["lane"] == "installed_base")   # owned or incumbent-renewal: defend, not a contest
        # An opportunity is defined by CONTEST SHAPE + CURRENCY only — deliberately NOT by whether we have a
        # euro figure. Most tenders in this footprint never publish a value, so requiring pot_value>0 was
        # silently deleting real net-new contests for the sin of poor disclosure (changed 2026-08). Unsized
        # opportunities are carried as 'value unscoped': they appear in every opportunity list and count, and
        # contribute €0 to the value bars (we never invent a number to make a chart look complete).
        # stricter gate: an opportunity needs a handle — a counterparty or a date (see is_biddable)
        s["biddable"], s["not_biddable_why"] = (True, "")
        if s["lane"] == "opportunity":
            ok, why = is_biddable(s, _market_names)
            if not ok:
                s["biddable"], s["not_biddable_why"] = False, why
                s["lane"] = "context"
                s["held"] = False
                demoted += 1
        s["is_opportunity"] = bool(s["lane"] == "opportunity" and s["is_current"] and not s["stale_new"])
        s["unscoped_opp"] = bool(s["is_opportunity"] and (s.get("pot_value") or 0) <= 0)
        if s["held"]:
            s["is_new_this_week"] = False
    if demoted:
        print("opportunity gate: %d row(s) re-lane'd to context — no named counterparty and no dated "
              "trigger (still visible everywhere, just not ranked as opportunities)" % demoted)
    if stale_new_count:
        print("recency: %d signal(s) badged NEW/UPDATED but anchored only on standing facts (>6mo, no "
              "near-future trigger) -> flagged stale_new; the dashboard tags them as standing context." % stale_new_count)
    json.dump(ledger, open(os.path.join(data, "_ledger.json"), "w", encoding="utf-8"), indent=2)
    json.dump(signals, open(os.path.join(data, "signals.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    xlsx = sorted(glob.glob(os.path.join(args.root, "history", "*.xlsx")))
    timeseries, events, patterns = ([], [], [])
    if xlsx:
        timeseries, events, patterns = parse_xlsx(xlsx[-1])
    series = build_series(timeseries)
    n_s, n_r = merge_structural(series, timeseries, data, footprint)        # EU (scripted, fetch_ecb.py)
    if n_s:
        print(f"merged ECB structural series: +{n_s} series, +{n_r} annual points")
    n_s2, n_r2 = merge_structural(series, timeseries, data, footprint,      # non-EU (researched, Agent 4)
                                  fname="structural_series_noneu.json",
                                  default_source="National central banks (researched)", notes_tag="national CB")
    if n_s2:
        print(f"merged non-EU structural series: +{n_s2} series, +{n_r2} annual points")
    for name, obj in [("timeseries.json", timeseries), ("series.json", series),
                      ("events.json", events), ("patterns.json", patterns)]:
        json.dump(obj, open(os.path.join(data, name), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # country_stats: researched rows from the findings Country-trends table (non-EU) + EU rows derived
    # deterministically from the scripted ECB series, so the dashboard card stays full-footprint.
    eu_notes = load_json(os.path.join(ref, "eu_country_notes.json"), {})
    country_stats, stats_src = parse_country_stats(os.path.join(args.root, "findings"), resolve)
    present = {r["code"] for r in country_stats if r.get("code")}
    derived = derive_structural_country_stats(data, footprint, present, eu_notes)
    if derived:
        print(f"derived EU country-stats from scripted ECB series: +{len(derived)} countries "
              f"({', '.join(d['code'] for d in derived)})")
    country_stats = country_stats + derived
    json.dump(country_stats, open(os.path.join(data, "country_stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    summary = {"week": args.week,
               "generated_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
               "n_signals": len(signals), "n_new_this_week": new_count,
               "n_stale_new": stale_new_count,
               "n_fresh": sum(1 for s in signals if s.get("recency") == "fresh"),
               "n_standing": sum(1 for s in signals if s.get("recency") == "standing"),
               "n_high_conf": sum(1 for s in signals if s["confidence"] == "High"),
               "n_opportunities": sum(1 for s in signals if s.get("is_opportunity")),
               "n_unscoped_opps": sum(1 for s in signals if s.get("unscoped_opp")),
               "n_timeseries_points": len(timeseries), "n_events": len(events),
               "n_patterns": len(patterns), "n_country_stats": len(country_stats),
               "stats_source_file": stats_src, "master_table": os.path.basename(master)}
    json.dump(summary, open(os.path.join(data, "summary.json"), "w", encoding="utf-8"), indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
