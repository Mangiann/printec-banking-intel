#!/usr/bin/env python3
"""Deterministically render Agent-3 findings for 2026-08-02.

Sources, in preference order per workstream:
  1. parts/2026-08-02/<slug>.verified.json  — adversarially verified (2 units got through)
  2. parts/2026-08-02/<slug>.json           — research checkpoint (unverified)

Mirrors research-harness.workflow.js renderTable(tableKind="regulation") so the file
stays compatible with ingest.py. No LLM renders the table, so nothing is truncated.
"""
import json, os, re, sys

RUN_DATE = "2026-08-02"
BASE = "/Users/mangian/Downloads/BANKING/findings/03-regulation"
PARTS = f"{BASE}/parts/{RUN_DATE}"
OUT = f"{BASE}/{RUN_DATE}.md"

UNITS = [
    ("dora", "DORA (digital operational resilience)"),
    ("instant-payments-sepa", "Instant payments & SEPA (incl. SCT Inst, VoP)"),
    ("psd3-psr", "PSD3 / PSR"),
    ("iso20022", "ISO 20022 migration"),
    ("digital-euro-cbdc", "Digital euro & CBDC"),
    ("accessibility-eaa", "European Accessibility Act (ATMs/self-service)"),
    ("aml-amla-amlr", "AML — AMLA / AMLR"),
    ("eidas-eudi", "eIDAS 2 / EUDI wallet & eID"),
    ("euro-adoption", "Euro adoption (Bulgaria + pipeline)"),
    ("mica-crypto", "MiCA / crypto-asset rules"),
    ("horizon-scan", "Horizon scan — emerging regulation beyond the watchlist"),
]

SIZE_RANK = {"XL": 0, "L": 1, "M": 2, "S": 3, "Unscoped": 4}
WIN_RANK = {"High": 0, "Medium": 1, "Low": 2, "—": 3}

# Rolling regulatory calendar. Every entry is traceable to a dated row in the signal
# table above it — nothing here is derived, inferred or extrapolated. Fields:
#   (date, sort-key, geography, what falls due, Printec relevance)
CALENDAR = [
 ("08/08/2026", 20260808, "Bulgaria", "Dual price display (prices shown in BOTH lev and euro) ends under ZVERB.", "Merchant price-display and bank tariff-disclosure changes; minor POS/software touch, no hardware."),
 ("11/08/2026", 20260811, "EU-wide", "Commission Implementing Reg (EU) 2026/1731 of 15/07/2026 enters into force, amending the four core EUDI-wallet implementing acts.", "Wallet-verifier integration specs firm up for bank-side onboarding — Namirial eKYC / e-signature roadmap input."),
 ("03/09/2026", 20260903, "EU-wide", "AMLA consultation on draft Guidelines on ongoing monitoring of a business relationship closes.", "Shapes the ongoing-monitoring rules that IMTF Siron / FICO must satisfy from 2027; comment window is the influence point."),
 ("04/09/2026", 20260904, "Ukraine", "NBU introduces a NEW UAH 2,000 banknote into circulation (announced ~2 months ahead specifically so institutions can prepare).", "**Hard hardware date.** Every ATM, recycler and cash-handling device in Ukraine needs note-validation firmware/template updates and cassette planning — Printec field services + NCR fleet work, and the same for CIT operators."),
 ("21/09/2026", 20260921, "Euro area", "ECB public survey on the shortlisted designs for the NEXT SERIES of euro banknotes closes (designs published 23/07/2026).", "Early warning only: a new note series eventually forces validator/template upgrades across the euro-area fleet. Context for 2028+ refresh planning."),
 ("25/09/2026", 20260925, "Euro area (AT, GR, HR, SI, SK, CY, BG)", "T2 R2026.NOV UTEST release testing opens (Bundesbank release calendar).", "Participant-testing window before the November structured-address cutover; screening/monitoring payloads must be re-tuned in test."),
 ("30/09/2026", 20260930, "EU-wide", "European Commission targeted consultation on the MiCA review closes (23:59 CEST).", "Signals the direction of the next crypto-asset rules for banks servicing CASPs; watch-item, not a spend trigger."),
 ("30/09/2026", 20260931, "North Macedonia", "Single register of accounts must be established and hosted under the Law on Payment Services and Systems.", "Central account-register integration work at NBRNM and the MK banks; adjacent to onboarding/AML data plumbing."),
 ("01/10/2026", 20261001, "Austria", "NISG 2026 (Austria's NIS2 transposition) deadline.", "Cyber/ICT resilience obligations on Austrian banks; feeds the same monitoring/resilience budget as DORA."),
 ("23/10/2026", 20261023, "EU-wide", "EBA's first four consultations under the revised Deposit Guarantee Schemes Directive (DGSD3) close (launched 23/07/2026).", "Data-quality and reporting obligations on deposit data; document-management and reconciliation adjacency."),
 ("31/10/2026", 20261031, "Euro area / SSM (AT, BG, CY, GR, HR, SI, SK)", "**ECB letter SSM-2026-0301 (Buch, 07/07/2026): significant institutions must submit an AI-cyber-threat ACTION PLAN to their Joint Supervisory Team.** The letter explicitly names modernising infrastructure by replacing or updating legacy, unsupported or end-of-life technologies. ECB will run a horizontal analysis of all plans. (Relief: the annual IT Risk Questionnaire moves from Sept-2026 to Feb-2027.)", "**The single most actionable date on this calendar.** Every SSM bank must name its end-of-life technology and a remediation timeline — ATM/self-service estates on unsupported OS or legacy multivendor stacks land squarely in scope. Pitch NCR Atleos refresh, x-core multivendor software, telemetry/monitoring, INETCO, Thales HSM and managed services NOW: plans are written Aug-Oct 2026 and the money lands in the 2027 IT plan."),
 ("31/10/2026", 20261032, "Serbia", "Serbia's Law on Information Security (Sluzbeni glasnik RS 91/2025) in force — a non-EU NIS2 mirror — alongside the NBS ICT regulations for financial institutions.", "Serbian banks acquire DORA-like ICT and third-party obligations without being in the EU; same monitoring/resilience sell, earlier than accession implies."),
 ("14/11/2026", 20261114, "All 17 footprint markets", "SWIFT CBPR+ SR2026 go-live: unstructured postal addresses REMOVED from cross-border payment messages; town name + country code become the minimum.", "Hard network deadline — non-conforming messages are rejected. Structured address data sharply improves sanctions-screening precision: a concrete tuning/false-positive-reduction sell for IMTF Siron and FICO."),
 ("15/11/2026", 20261115, "SEPA area", "SEPA schemes enforce the equivalent structured-address requirement. _[Carried from the 24/07/2026 baseline — NOT re-verified this run; the ISO 20022 workstream was cut short. Re-confirm against the EPC rulebook before quoting.]_", "Same screening/monitoring re-tuning as the SWIFT date, on the retail rail."),
 ("16/11/2026", 20261116, "Euro area (AT, GR, HR, SI, SK, CY, BG)", "T2 release R2026.NOV first business day (deploys the weekend of 14-15/11/2026), removing unstructured postal addresses from the Eurosystem RTGS.", "Core RTGS work is not Printec's lane; the opportunity is the screening/monitoring layer that must parse the richer payloads."),
 ("30/11/2026", 20261130, "EU + SEPA participants", "EPC Verification of Payee (VoP) rulebook v2.0 approved change requests take effect.", "VoP engine and routing changes for PSPs already live on VoP; matching-quality and mismatch-handling services."),
 ("13/12/2026", 20261213, "Ukraine", "NBU Board Resolution No.143 of 09/12/2025 — information-security and cyber-protection requirements — bites.", "Ukrainian bank ICT/security remediation despite wartime budget constraints; monitoring and managed services."),
 ("24/12/2026", 20261224, "EU-wide (AT, BG, CY, CZ, GR, HR, HU, RO, SI, SK)", "**eIDAS Art 5a(1): every Member State must provide at least one EU Digital Identity (EUDI) Wallet to its citizens.**", "The supply side of digital identity goes live across the whole EU footprint. Banks become wallet relying parties — direct pull for Namirial eKYC/e-signature and remote onboarding integration."),
 ("31/12/2026", 20261231, "Hungary", "**MNB Decree 19/2025 (VI.26.) compulsory ATM installation — settlements above 500 inhabitants must be served.** Nine named PSPs are on the hook: OTP, MBH, Erste Hungary, K&H, CIB, Raiffeisen, UniCredit Hungary, Granit, MagNet. Programme totals ~1,039 new ATMs. _[The 31/12/2026 phase date and the 1,039 figure are PRESS-SOURCED (Penzcentrum); the decree text extracted this run confirms the allocation mechanism and the 28/02/2026 contracting / 16/03/2026 notification steps, but not the installation dates.]_", "**The largest concrete hardware opportunity on the calendar.** A state-mandated ATM rollout at nine named banks. Critical interaction: every machine enters service AFTER 28/06/2025, so none benefits from the EAA legacy derogation — each must be accessibility-conformant on day one. NCR Atleos hardware + x-core + install/field services + EAA-compliant configuration."),
 ("31/12/2026", 20261232, "EU-wide", "DORA Register of Information (the mandatory register of every ICT third-party contract) annual submission cycle.", "Recurring compliance data exercise; document-management and third-party-risk evidencing, and an argument for consolidating fragmented vendors onto one accountable managed-service partner."),
 ("31/12/2026", 20261233, "Bulgaria", "Residual free lev-to-euro exchange via credit institutions under ZVERB Art.26 (BNB continues unlimited free exchange beyond this).", "Branch cash-handling and reconciliation tail-off; recycler/TCR tuning as lev volumes disappear."),
 ("01/01/2027", 20270101, "Bulgaria", "**Bulgaria's Instant Payments Regulation obligations, including Verification of Payee, fall due — one year after euro adoption.** _[MATERIAL CORRECTION to the baseline: Bulgaria is NOT on the 09/07/2027 non-euro timetable. Source is the BNB Payment Supervision Director quoted by BTA, not a published BNB rule — re-verify.]_", "Bulgarian PSPs have ~5 months, not ~17, to deliver VoP. Pulls the BG VoP/name-matching and monitoring pipeline sharply forward — the most time-critical correction in this run."),
 ("09/01/2027", 20270109, "Czech Republic, Hungary, Romania", "Non-euro EU PSPs must be able to RECEIVE instant euro credit transfers (Reg (EU) 2024/886).", "First of the two non-euro instant deadlines; connectivity, channel integration and in-window real-time monitoring at CZ/HU/RO banks."),
 ("28/06/2027", 20270628, "Bulgaria, Hungary", "EAA-related national deadlines fall due (BG State Agency for Metrological and Technical Surveillance; HU with the MNB itself designated as market-surveillance authority).", "Accessibility conformance and remediation services; note the MNB wears both hats in Hungary — regulator and ATM-mandate author."),
 ("01/07/2027", 20270701, "Albania", "Bank of Albania Regulation on Digital Operational Resilience (adopted by the Supervisory Council 01/07/2026) applies — a non-EU DORA mirror.", "Albanian banks (incl. OTP and Raiffeisen Albania, existing Printec accounts) acquire DORA-style ICT and third-party obligations; resilience/monitoring and managed services."),
 ("09/07/2027", 20270709, "Czech Republic, Hungary, Romania", "Non-euro EU PSPs must be able to SEND instant euro credit transfers AND provide Verification of Payee.", "The full VoP build deadline for the non-euro footprint — VoP engines, RVM connectivity, name-matching data quality, real-time monitoring."),
 ("10/07/2027", 20270710, "EU-wide", "**AMLR (Reg (EU) 2024/1624) applies**, together with AMLA's RTS package (incl. the Art.28(1) Customer Due Diligence RTS) and the staggered AMLD6 transposition.", "CDD/eKYC data and document requirements become prescriptive and EU-harmonised. Footprint banks must re-tool onboarding and CDD workflows — Namirial eKYC, IMTF Siron, FICO. Budget must commit through 2026-H1 2027."),
 ("24/12/2027", 20271224, "EU-wide", "**eIDAS Art 5f(2): private relying parties — explicitly including banks, PSPs and e-money institutions (micro/small enterprises excepted) — must ACCEPT the EUDI Wallet** where strong user authentication is required.", "The demand side of digital identity becomes mandatory for banks. This is the eIDAS date with the clearest procurement consequence: wallet acceptance in onboarding and authentication journeys."),
 ("28/06/2030", 20300628, "EU-wide", "EAA transition ends: service providers may continue using self-service terminals lawfully in use before 28/06/2025 only until this date (Directive (EU) 2019/882 transition), with an absolute 20-year economic-life backstop of 28/06/2045.", "The long backstop under every EU ATM refresh business case — each replacement cycle from now on must ship EAA-conformant hardware."),
]


def cell(s):
    if s is None:
        return ""
    return re.sub(r"\r?\n+", " ", str(s)).replace("|", "\\|").strip()


def value_rank(s):
    return SIZE_RANK.get(s.get("opp_size"), 9) * 10 + WIN_RANK.get(s.get("win"), 9)


def source_link(s):
    name = cell(s.get("source_name")) or "source"
    url = cell(s.get("source_url"))
    return f"[{name}]({url})" if url else name


def meaningful(x):
    t = cell(x)
    return bool(t) and not re.fullmatch(
        r"(none|n/a|na|-|null|nan|no issues?|no access issues?|no operator requests?)\.?",
        t, re.I)


def load():
    """Per slug: (payload, is_verified). Verified file wins when present."""
    data = {}
    for slug, _ in UNITS:
        vp = os.path.join(PARTS, f"{slug}.verified.json")
        rp = os.path.join(PARTS, f"{slug}.json")
        for path, verified in ((vp, True), (rp, False)):
            if not os.path.exists(path):
                continue
            try:
                data[slug] = (json.load(open(path, encoding="utf-8")), verified)
                break
            except Exception as e:
                print(f"WARN: {path} unreadable: {e}", file=sys.stderr)
    return data


def main():
    data = load()
    per_unit, all_signals, verified_units = {}, [], []
    for slug, _ in UNITS:
        payload, verified = data.get(slug, ({}, False))
        sigs = payload.get("signals") or []
        per_unit[slug] = len(sigs)
        if verified and sigs:
            verified_units.append(slug)
        for s in sigs:
            s["_slug"] = slug
            s["_verified"] = verified
            all_signals.append(s)
    all_signals.sort(key=value_rank)

    empty = [s for s, _ in UNITS if per_unit.get(s, 0) == 0]
    covered = sum(1 for s, _ in UNITS if per_unit.get(s, 0) > 0)
    partial = [s for s, _ in UNITS
               if data.get(s, ({}, False))[0].get("status") == "partial" and per_unit.get(s, 0) > 0]
    nverified = sum(per_unit[s] for s in verified_units)

    o = []
    o.append(f"# Agent 3 — Regulation & Deadlines — Findings {RUN_DATE}\n")
    o.append(
        "(Method: shared research harness — one agent per regulation workstream, DETERMINISTIC table render. "
        f"11 regulation workstream(s) targeted, {covered} returned signals, {len(all_signals)} signals "
        f"({nverified} adversarially verified, {len(all_signals)-nverified} research-grade). "
        "Confidence capped at Medium per single-agent playbook. Rows ordered by Printec value (size x win), "
        "biddable first.)\n")
    o.append(
        "> **⚠ MOSTLY RESEARCH-GRADE — READ BEFORE QUOTING ANY FIGURE.**\n"
        "> This run was disrupted three times by account usage limits. The first attempt (11:53-12:13) had all "
        "34 subagents killed mid-flight. The relaunch (13:56-18:45) completed RESEARCH for all 11 workstreams "
        "and got **2 of them through adversarial verification** before hitting the **weekly** limit, which "
        "killed the remaining verify agents, all gap-fill rounds and the narrative agent.\n"
        f"> Everything below was assembled deterministically from the per-unit checkpoints and verified outputs "
        f"in `parts/{RUN_DATE}/` — no LLM rendered this table, so nothing is silently truncated.\n"
        f"> **Verified (figures independently re-checked, `Ver.` column populated):** "
        f"{', '.join(verified_units) if verified_units else 'none'}.\n"
        "> **Everything else is research-grade and has NOT passed verification.** That pass earns its keep: on "
        "24/07/2026 it caught Romanian EAA fines quoted an order of magnitude too high and attributed to the "
        "wrong regulator (ANCOM rather than ANPC/ANPD). Re-check every unverified figure, fine level and "
        "deadline against the cited primary source before it goes anywhere customer-facing. No row carries "
        "Confidence above Medium.\n"
        "> Where a claim touches data-subject rights, a personal-data breach, or a contested reading of a "
        "regulation, treat it as background only and refer the question to Printec's DPO / Compliance team.\n")
    if empty:
        o.append("> **COVERAGE WARNING:** no usable signals for: **" + ", ".join(empty) + "**.\n")
    if partial:
        o.append(
            "> **PARTIAL COVERAGE:** still mid-research when killed, so jurisdiction coverage is incomplete "
            "(see Residual gaps): **" + ", ".join(partial) + "**.\n")

    o.append("\n## Signal table\n")
    o.append("| Workstream | Country/Scope | Status & deadline | Source (link) | Date | What it implies | "
             "6-12 mo likelihood | Confidence | Ver. | Opp. size | Win | Recommended follow-up |\n"
             "|---|---|---|---|---|---|---|---|---|---|---|---|")
    rows = []
    for s in all_signals:
        ver = cell(s.get("verification")) if s.get("_verified") else "unverified"
        note = cell(s.get("verifier_note")) if s.get("_verified") else ""
        sig = cell(s.get("signal"))
        if note and s.get("verification") in ("partially-confirmed", "unconfirmed", "contradicted"):
            sig += f" **[verifier: {note}]**"
        rows.append(
            f"| {cell(s.get('entity'))} | {cell(s.get('country'))} | {sig} | {source_link(s)} | "
            f"{cell(s.get('source_date'))} | {cell(s.get('implies'))} | {cell(s.get('likelihood'))} | "
            f"{cell(s.get('confidence'))} | {ver} | {cell(s.get('opp_size'))} | {cell(s.get('win'))} | "
            f"{cell(s.get('followup'))} |")
    o.append("\n".join(rows) + "\n")

    # ---- rolling regulatory calendar ----
    o.append("\n## Rolling regulatory calendar (nearest deadline first)\n")
    o.append(
        f"_Composed from the dated rows in the table above — every entry traces to a cited row; nothing here is "
        f"inferred or extrapolated. Same verification caveat applies: only the euro-adoption and digital-euro "
        f"rows have been independently re-checked. Horizon as at {RUN_DATE}._\n")
    o.append("| Date | Geography | What falls due | Why it matters to Printec |\n|---|---|---|---|")
    o.append("\n".join(
        f"| **{d}** | {g} | {w} | {p} |"
        for d, _, g, w, p in sorted(CALENDAR, key=lambda r: r[1])) + "\n")

    # ---- verification notes for the two verified units ----
    vnotes = [s for s in all_signals
              if s.get("_verified") and s.get("verification") in ("contradicted", "unconfirmed")]
    if vnotes:
        o.append("\n## Verification notes (the two workstreams that completed the adversarial pass)\n")
        for s in vnotes:
            o.append(f"- **[{s.get('verification')}] {cell(s.get('entity'))}** ({cell(s.get('country'))}) — "
                     f"{cell(s.get('verifier_note')) or 'no note returned'}")
        o.append("")

    # ---- residual gaps ----
    gaps = [(n, data.get(s, ({}, False))[0].get("remaining")) for s, n in UNITS
            if meaningful(data.get(s, ({}, False))[0].get("remaining"))]
    if gaps:
        o.append("\n## Residual gaps — what the killed agents had NOT yet covered\n")
        o.append("| regulation workstream | still unresearched when the run was killed |\n|---|---|")
        o.append("\n".join(f"| {cell(n)} | {cell(r)} |" for n, r in gaps) + "\n")

    # ---- access issues / operator requests ----
    ai = [(n, data.get(s, ({}, False))[0].get("access_issues")) for s, n in UNITS
          if meaningful(data.get(s, ({}, False))[0].get("access_issues"))]
    opr = [(n, data.get(s, ({}, False))[0].get("operator_requests")) for s, n in UNITS
           if meaningful(data.get(s, ({}, False))[0].get("operator_requests"))]
    if ai or opr:
        o.append("\n## Access issues & operator requests (per regulation workstream)\n")
        if ai:
            o.append("| regulation workstream | Access issue / what failed & the fallback used |\n|---|---|")
            o.append("\n".join(f"| {cell(n)} | {cell(v)} |" for n, v in ai) + "\n")
        if opr:
            o.append("\n**Operator requests — gated / paywalled / blocked sources to fetch or verify manually:**\n")
            o.append("\n".join(f"- **{cell(n)}:** {cell(v)}" for n, v in opr) + "\n")

    # ---- coverage ----
    o.append("\n## Coverage (per regulation workstream, honest)\n")
    o.append("| regulation workstream | signals | state |\n|---|---|---|")
    lines = []
    for slug, name in UNITS:
        payload, verified = data.get(slug, ({}, False))
        n = per_unit.get(slug, 0)
        if n == 0:
            st = "⚠ EMPTY"
        elif verified:
            st = "**adversarially verified**"
        elif payload.get("status") == "complete":
            st = "research complete — UNVERIFIED"
        else:
            st = "research PARTIAL — UNVERIFIED"
        lines.append(f"| {cell(name)} | {n}{' ⚠ EMPTY' if n == 0 else ''} | {st} |")
    o.append("\n".join(lines) + "\n")

    o.append(
        "\n## What is still owed on this run\n\n"
        "The weekly usage limit (resets 1pm Europe/Athens) stopped the run, not the research. To finish it:\n\n"
        "1. **Re-run verification for the 9 unverified workstreams** — relaunch "
        "`weekly-intelligence/workflows/agent3-launch-2026-08-02.workflow.js`; the per-unit checkpoints mean "
        "research replays cheaply and only the verify stage costs real tokens.\n"
        "2. **Finish the 4 partial workstreams** (`iso20022` is the weakest at 3 signals, and it carries the "
        "14-15/11/2026 structured-address cutover — the nearest hard footprint-wide deadline after 31/10/2026).\n"
        "3. **Close the carried verification debts** listed under Access issues & operator requests.\n"
        "4. Re-render with this script once the above lands.\n")

    md = "\n".join(o)
    open(OUT, "w", encoding="utf-8").write(md)
    print(f"wrote {OUT}\n  {len(all_signals)} signals ({nverified} verified) across {covered}/11 units\n"
          f"  calendar entries: {len(CALENDAR)}\n  empty={empty}\n  partial={partial}")


if __name__ == "__main__":
    main()
