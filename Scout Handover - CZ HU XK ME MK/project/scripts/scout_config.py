#!/usr/bin/env python3
"""Assemble a runnable scout config from a (country, workstream) request — the fixed research taxonomy.

The `/printec-market-research` skill maps the user's free text to a COUNTRY (any country) and one of the fixed
WORKSTREAMS (project description sec.16: A1-A6, A8). This script assembles that into what a run needs. Storage
is PER COUNTRY (the globe reads one DB per country): the registry is `data/registries/<ISO>.db` and the Excel
is one per country, with the sources TAGGED by workstream. The run_id carries the workstream so rounds are
distinct.

    python scripts/scout_config.py --iso GR --country-name Greece --languages el --workstream A2
"""
import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "review"))
import master_export  # noqa: E402

# The 7 fixed source-discovery researches. code -> (label, canonical topics that guide the scout's search).
# These topics ARE the workstream's definition (sec.16) — not a hidden default; the user picks the workstream.
WORKSTREAMS = {
    "A1": ("Disclosures", ["disclosures", "annual reports", "investor relations", "press releases", "earnings"]),
    "A2": ("Tenders & Procurement", ["tenders", "procurement", "public contracts", "award notices"]),
    "A3": ("Regulation & Deadlines", ["regulation", "supervision", "consultations", "deadlines"]),
    "A4": ("Market Statistics", ["market statistics", "payment statistics", "card statistics", "cash usage", "ATM POS data"]),
    "A5": ("Early Intent & Jobs", ["jobs", "hiring", "leadership moves", "organization changes"]),
    "A6": ("Vendors & Competitors", ["vendors", "competitors", "case studies", "partnerships"]),
    "A8": ("Futurist & Trends", ["trends", "forecasts", "analyst reports", "technology outlook"]),
}

# SCOPE lookup: a scope is a COUNTRY (Printec operates there) or a REGION/GLOBAL lens (for trends A8, EU
# regulation A3, global vendors A6). NOT a restriction — any country works via --iso + --languages. English
# is always added. Region/global scopes stamp records with country=ZZ (the finer geo is an analysis-layer tag).
KNOWN = {
    # Printec operating countries
    "AL": ("Albania", ["sq"]), "AT": ("Austria", ["de"]), "BA": ("Bosnia & Herzegovina", ["bs", "hr", "sr"]),
    "BG": ("Bulgaria", ["bg"]), "HR": ("Croatia", ["hr"]), "CY": ("Cyprus", ["el"]),
    "CZ": ("Czech Republic", ["cs"]), "GR": ("Greece", ["el"]), "HU": ("Hungary", ["hu"]),
    "XK": ("Kosovo", ["sq", "sr"]), "ME": ("Montenegro", ["sr"]), "MK": ("North Macedonia", ["mk"]),
    "RO": ("Romania", ["ro"]), "RS": ("Serbia", ["sr"]), "SK": ("Slovakia", ["sk"]),
    "SI": ("Slovenia", ["sl"]), "UA": ("Ukraine", ["uk"]),
    # regional / global lenses (mostly A8 trends; English-dominant source ecosystems)
    "US": ("United States", ["en"]), "EU": ("Europe", ["en"]),
    "CEE": ("Central & Eastern Europe", ["en"]), "APAC": ("Asia-Pacific", ["en"]),
    "GLOBAL": ("Global", ["en"]), "ZZ": ("Global", ["en"]),
}
# scopes whose records are stamped country=ZZ (they are regions/global, not a single ISO country).
REGION_SCOPES = {"EU", "CEE", "APAC", "GLOBAL", "ZZ"}
_NAME_TO_ISO = {name.lower(): iso for iso, (name, _l) in KNOWN.items()}


def resolve_country(country=None, iso=None, name=None, languages=None):
    """(iso2, name, [local_langs]) from whatever was given. Explicit iso+languages ALWAYS win (any country)."""
    langs = [l.strip() for l in (languages or []) if l and l.strip()]
    if iso and langs:
        known_name = KNOWN.get(iso.upper(), (None,))[0]     # a known ISO keeps its display name (ZZ -> Global)
        return iso.upper(), (name or known_name or iso.upper()), langs
    key = (country or iso or name or "").strip().lower()
    hit = None
    if key.upper() in KNOWN:
        hit = key.upper()
    elif key in _NAME_TO_ISO:
        hit = _NAME_TO_ISO[key]
    else:
        for nm, iso2 in _NAME_TO_ISO.items():
            if nm in key or (key and key in nm):
                hit = iso2
                break
    if hit:
        nm, ls = KNOWN[hit]
        return hit, (name or nm), (langs or ls)
    if iso:
        return iso.upper(), (name or iso.upper()), langs
    return None


def _next_run_id(data_root, iso, ws):
    prefix = f"dr_{iso.lower()}_{ws.lower()}_live_"
    folder = Path(data_root) / "source_candidates"
    seq = 0
    if folder.exists():
        for f in folder.glob(f"{prefix}*.jsonl"):
            tail = f.stem[len(prefix):]
            if tail.isdigit():
                seq = max(seq, int(tail))
    return f"{prefix}{seq + 1:03d}"


def _write_config(path, iso, name, sector, workstream, topics, languages):
    path.parent.mkdir(parents=True, exist_ok=True)
    label = WORKSTREAMS.get(workstream, (workstream, []))[0]
    path.write_text("\n".join([
        f"# Auto-generated: {name} / {workstream} {label} / sector={sector}.",
        f"country: {iso}", f"country_name: {name}", f"sector: {sector}",
        f"workstreams: [{workstream}]", f"topics: [{', '.join(topics)}]",
        f"languages: [{', '.join(languages)}]",
        "routine_id: R2", "routine_name: source_discovery_scout", "routine_version: 0.3.0",
        "prompt_path: routines/source_discovery_scout/routine_prompt.md",
        "url_verification:", "  enabled: false", "dedupe:", "  enabled: true",
    ]) + "\n", encoding="utf-8")


def build(country=None, iso=None, country_name=None, languages=None, workstream="A2", sector="both",
          data_root=None, configs_dir=None, run_id=None):
    resolved = resolve_country(country=country, iso=iso, name=country_name, languages=languages)
    if resolved is None:
        raise SystemExit("No country given. Pass --country (name/ISO) or --iso + --languages. Any country is allowed.")
    iso2, name, local_langs = resolved
    if not local_langs:
        raise SystemExit(f"No language known for {name!r}. Pass --languages (e.g. --languages fr).")
    ws = (workstream or "A2").upper()
    if ws not in WORKSTREAMS:
        raise SystemExit(f"Unknown workstream {ws!r}. One of: {', '.join(sorted(WORKSTREAMS))} (see research_plan.yaml).")
    sector = sector if sector in ("both", "banking", "payments") else "both"
    topics = list(WORKSTREAMS[ws][1])                                   # the workstream's canonical search topics
    languages = list(dict.fromkeys(local_langs + ["en"]))
    data_root = data_root or str(_ROOT / "data")

    record_country = "ZZ" if iso2 in REGION_SCOPES else iso2   # regions/global stamp records country=ZZ
    config = {"country": record_country, "country_name": name, "sector": sector,
              "workstreams": [ws], "topics": topics, "languages": languages}
    config_path = Path(configs_dir or (_ROOT / "configs" / "discovery_runs")) / f"{iso2.lower()}_{ws.lower()}.yaml"
    _write_config(config_path, record_country, name, sector, ws, topics, languages)
    (Path(data_root) / "registries").mkdir(parents=True, exist_ok=True)

    return {
        "country": iso2, "country_name": name, "sector": sector, "workstreams": [ws],
        "workstream": ws, "workstream_label": WORKSTREAMS[ws][0], "topics": topics, "languages": languages,
        "run_id": run_id or _next_run_id(data_root, iso2, ws),   # explicit run_id = RESUME (don't mint a new one)
        "config_path": str(config_path),
        "promotion_db": str(Path(data_root) / "registries" / f"{iso2}.db"),   # PER-COUNTRY registry
        "data_root": data_root,
        "deliverable_name": master_export.deliverable_name(config),           # PER-COUNTRY Excel
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Assemble a scout config for a (country, workstream) — any country.")
    ap.add_argument("--country", help="a country name or ISO2 (convenience lookup)")
    ap.add_argument("--iso", help="ISO2 code (use with --languages for ANY country)")
    ap.add_argument("--country-name", help="display name (optional)")
    ap.add_argument("--languages", help="comma-separated local language codes (e.g. fr or el,tr)")
    ap.add_argument("--workstream", default="A2", help="one of A1 A2 A3 A4 A5 A6 A8 (see research_plan.yaml)")
    ap.add_argument("--sector", default="both", help="both | banking | payments")
    ap.add_argument("--data-root", default=str(_ROOT / "data"))
    args = ap.parse_args(argv)
    out = build(country=args.country, iso=args.iso, country_name=args.country_name,
                languages=(args.languages.split(",") if args.languages else None),
                workstream=args.workstream, sector=args.sector.lower(), data_root=args.data_root)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
