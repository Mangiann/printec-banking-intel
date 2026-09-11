#!/usr/bin/env python3
"""
run_weekly.py - One-command weekly refresh: ingest -> build dashboard -> publish.

Chains ingest.py, build_dashboard.py and (optionally) publish.py. Writes the publishable data
into <root>/intel-cache/dashboard-data.json, refreshes the web app's bundled snapshot at
<root>/dashboard-web/data.json, and pushes it to the live Vercel dashboard (the only dashboard).
Run this AFTER the master-signal-table.md has been updated with this week's triangulation.

Usage:
  python run_weekly.py --root <BANKING_folder> [--week YYYY-MM-DD]
Optional: --skill <engine_dir> (defaults to this script's parent's parent),
          --data <cache_dir> (defaults to <root>/intel-cache so week-over-week state lives
          with the research folder, not inside a read-only installed skill),
          --assets <dashboard-web dir> (defaults to <root>/dashboard-web),
          --no-publish to skip the live-dashboard push even when env vars are set.

Publishing to the live site is automatic when PRINTEC_DASHBOARD_URL and PRINTEC_UPLOAD_SECRET
are set in the environment; otherwise it is skipped with a note (the run still succeeds).
"""
import argparse, os, sys, subprocess, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--skill")
    ap.add_argument("--data")
    ap.add_argument("--assets")
    ap.add_argument("--week", default=datetime.date.today().isoformat())
    ap.add_argument("--no-publish", action="store_true")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    skill = args.skill or os.path.dirname(here)
    refs = os.path.join(skill, "references")
    data = args.data or os.path.join(args.root, "intel-cache")
    assets = args.assets or os.path.join(args.root, "dashboard-web")
    os.makedirs(data, exist_ok=True)

    py = sys.executable
    # refresh external series (best-effort: if a source is unreachable, the cached file is reused)
    subprocess.run([py, os.path.join(here, "fetch_ecb.py"), "--data", data])
    subprocess.run([py, os.path.join(here, "fetch_competitors.py"), "--data", data])
    subprocess.run([py, os.path.join(here, "fetch_competitor_segments.py"), "--data", data])
    # Tier-0 tender sweeps (Agent 2's TED + Ukraine blind spots): POST-only public APIs a
    # script can reach but WebFetch cannot. Best-effort; the cached JSON is reused on failure.
    subprocess.run([py, os.path.join(here, "fetch_ted.py"), "--data", data, "--week", args.week])
    subprocess.run([py, os.path.join(here, "fetch_prozorro.py"), "--data", data, "--week", args.week])
    # Greek sub-threshold ΚΗΜΔΗΣ/Diavgeia tender floor (below TED threshold): subject= free-text sweep.
    subprocess.run([py, os.path.join(here, "fetch_diavgeia.py"), "--data", data, "--week", args.week])
    # Tier-0 job-board/ATS listing cache (Agent 5 Jobs + Agent 1 disclosures blind spot):
    # reachable-by-plain-request endpoints (robota.ua, Workable, hrscapi, SuccessFactors/Erste
    # HTML, infostud, FledgeHR). Plumbing only - agents still explore freely. Best-effort.
    subprocess.run([py, os.path.join(here, "fetch_jobs.py"), "--data", data, "--week", args.week])
    # Tier-0 competitor-newsroom cache (Agent 6): vendor sites whose GLOBAL page is JS-only but whose
    # COUNTRY sites are WordPress (mellon.rs/.bg/.hr/.ro). Belt-and-suspenders FLOOR - the agent still
    # free-searches every newsroom + local press on top. Best-effort; cached JSON reused on failure.
    subprocess.run([py, os.path.join(here, "fetch_competitor_news.py"), "--data", data, "--week", args.week])
    subprocess.run([py, os.path.join(here, "ingest.py"), "--root", args.root,
                    "--refs", refs, "--data", data, "--week", args.week], check=True)
    # product-line critic (agent-briefs/10-product-critic.md): says how many signals still carry
    # keyword-only product tags. The critic itself is an agent step; this only builds its batches.
    subprocess.run([py, os.path.join(here, "product_critic.py"), "batches",
                    "--root", args.root, "--work", os.path.join(data, "_product_critic")])
    subprocess.run([py, os.path.join(here, "forecast.py"),
                    "--data", data, "--week", args.week], check=True)
    # the 2nd and 3rd baseline projection lines — must follow forecast.py, which sets the horizon
    # each line is drawn to, and precede build_dashboard.py, which folds them into the payload
    subprocess.run([py, os.path.join(here, "project_lines.py"),
                    "--data", data, "--week", args.week], check=True)
    # provenance/trust pass (best-effort: a network hiccup must not fail the whole run)
    subprocess.run([py, os.path.join(here, "verify.py"),
                    "--root", args.root, "--data", data, "--week", args.week,
                    "--registry", os.path.join(refs, "source_access_registry.json")])
    subprocess.run([py, os.path.join(here, "build_dashboard.py"),
                    "--refs", refs, "--data", data, "--assets", assets,
                    "--week", args.week], check=True)
    # writing standard (WRITING_POLICY.md): report what still reads badly — banned phrases, ALL-CAPS
    # emphasis, over-long sentences, dense paragraphs. Reports only; the editor step fixes them.
    subprocess.run([py, os.path.join(here, "plain_lint.py"), "--data", data])
    print(f"\nDashboard data built: {os.path.join(data, 'dashboard-data.json')}"
          f"\nWeb snapshot refreshed: {os.path.join(assets, 'data.json')}")

    # ---- publish to the live Vercel dashboard (optional) ----
    if not args.no_publish:
        data_json = os.path.join(data, "dashboard-data.json")
        rc = subprocess.run([py, os.path.join(here, "publish.py"),
                             "--root", args.root, "--data-json", data_json]).returncode
        if rc != 0:
            print("warn: publish step returned non-zero — the live dashboard may not be updated "
                  "(the rest of the run succeeded).")
    else:
        print("publish: skipped (--no-publish).")

if __name__ == "__main__":
    main()
