#!/usr/bin/env python3
"""plain_lint.py — does the user-facing text follow WRITING_POLICY.md?

Checks the measurable rules over everything the dashboard shows (intel-cache/dashboard-data.json):
  * banned dramatic / headline phrases
  * ALL-CAPS emphasis inside sentences (a word of 4+ capital letters that is not a known acronym)
  * sentences over 30 words
  * paragraphs over ~6 sentences
  * several dated deadlines crammed into one sentence (3+ dates in a sentence)
Prints a summary, writes intel-cache/writing_report.json with every finding, and exits 0 — it reports;
it does not block a build. Run after build_dashboard.py and inside the plain-English editor step.

  python plain_lint.py --data <intel-cache> [--max-sentence 30] [--fail-on N]
"""
import argparse, json, re, io, os

BANNED = [r"\bthe endgame\b", r"\bplumbing ha(?:s|ve) (?:already )?moved\b", r"\bthe sharper change\b", r"\bthe story is\b",
          r"\bthe real prize\b", r"\bthe clock is ticking\b", r"\bis exploding\b", r"\bopportunity is hiding\b",
          r"\bthe winner will be\b", r"\bnobody is watching\b", r"\bkeeps? (?:it|the story) honest\b", r"\bloudest voice\b",
          r"\bthe endgame\b", r"\bgrowth spine\b", r"\bdefensible .{0,30}annuity\b", r"\binverting\b", r"\bthe calendar explains why\b"]
# ALL-CAPS emphasis means an ORDINARY ENGLISH WORD shouted mid-sentence ("make ALL points accept
# cards"). Company names, acronyms and codes are legitimately upper-case — BORICA, SWIFT, EDRPOU,
# IBAN — and keeping a list of them is a losing game, so the test is the other way round: flag a
# capitalised token only when the same word in lower case is ordinary English.
COMMON = set("""all also and any are been both but can did does each else even ever every few for from
had has have here how however into its just least less like made make many may more most much must never
next non not now off once one only onto other our out over own per rather same she should since some such
than that the their them then there these they this those thus too under until upon use used very was way
well were what when where whether which while who whom why will with within without would year years yes yet
you your after against all almost along already although always among around because before being below
best better beyond big both call called change changed clear come coming could day days different due early
end enough entire fact far first following full further get give given going good great half high higher
hold holding important increase increased key large larger last late later left level little long longer look
low lower main major mean means might much need needed new news old open opened order others part parts past
place point points possible present previous put quite read ready real really recent right rise rising
run running same second seen sent set several short show shown side significant similar simple single
small so soon still stop strong such take taken tell term terms think three through time times today
together total toward true turn two under up use using want week weeks whole wide will work working world
worth accordance report reports""".split())

def sentences(t):
    """Sentences, with a bullet or a numbered item counting as one unit.

    The policy asks for lists where several facts or deadlines pile up, so a list must not be measured
    as one enormous sentence — that would penalise exactly the structure the policy prescribes."""
    t=re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t or "")
    t=re.sub(r"\*\*", "", t)
    units=[]
    for line in re.split(r"\n+", t):
        line=re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", line)      # strip the bullet marker
        units += [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(\[])", line) if x.strip()]
    return units

def check(text, table_cell=False):
    out=[]
    if not text or not isinstance(text,str): return out
    for pat in BANNED:
        for m in re.finditer(pat, text, re.I):
            out.append({"rule":"banned phrase","excerpt":text[max(0,m.start()-40):m.end()+40]})
    for m in re.finditer(r"\b[A-Z]{3,}\b", text):
        w=m.group(0)
        near = text[max(0, m.start()-2):m.end()+12]
        if re.search(r"\d", near):        # "ALL 58.3bn" is the Albanian lek code, not shouting
            continue
        if w.lower() in COMMON and not re.match(r"^[A-Z]+\d", w):
            out.append({"rule":"ALL-CAPS emphasis","excerpt":text[max(0,m.start()-40):m.end()+40]})
    for s in sentences(text):
        n=len(s.split())
        if n>30: out.append({"rule":"long sentence (%d words)"%n,"excerpt":s[:160]})
        if len(re.findall(r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d{4}\b|\b\d{2}/\d{2}/\d{4}\b", s))>=3:
            out.append({"rule":"several deadlines in one sentence","excerpt":s[:160]})
    # Paragraph length is only meaningful where the text CAN hold paragraph breaks. A markdown table
    # cell cannot contain a line break, so a signal cell is always a single block by construction —
    # measuring it here would report a rule the format makes impossible to satisfy.
    if not table_cell:
        for para in re.split(r"\n\s*\n", text):
            n=len(sentences(para))
            if n>6: out.append({"rule":"dense paragraph (%d sentences)"%n,"excerpt":para[:120]})
    return out

FIELDS = {"signals":["bank_theme","signal","implies","follow_up"], "outlook":["scope","summary","projected","rationale","drivers"],
          "product_outlooks":["scope","summary","projected","rationale","drivers"], "futures":["scope","projected","rationale","drivers"],
          "patterns":["Pattern","Evidence (see Metrics/Milestones)","What it means for Printec"], "competitors":["latest"],
          "derived":["title","claim","why_not_visible_in_one_signal","falsifier","trigger"]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data",required=True); ap.add_argument("--fail-on",type=int,default=None)
    a=ap.parse_args()
    D=json.load(io.open(os.path.join(a.data,"dashboard-data.json"),encoding="utf-8"))
    findings=[]
    for coll,fields in FIELDS.items():
        for i,item in enumerate(D.get(coll) or []):
            for f in fields:
                v=item.get(f)
                if isinstance(v,list): v="\n\n".join(str(x) for x in v)
                for x in check(v, table_cell=(coll=="signals")):
                    x.update({"where":coll,"index":i,"field":f,"title":str(item.get("bank_theme") or item.get("scope") or item.get("name") or item.get("Pattern") or item.get("title") or "")[:70]})
                    findings.append(x)
    b=(D.get("futures_board") or {})
    bl=b.get("bottom_line") or {}
    for k in ("headline","thesis"):
        for x in check(bl.get(k)): x.update({"where":"bottom_line","index":0,"field":k,"title":""}); findings.append(x)
    for j,pp in enumerate(bl.get("picture") or []):
        for x in check(pp): x.update({"where":"bottom_line","index":j,"field":"picture","title":""}); findings.append(x)
    for sec in ("drivers","gems"):
        for j,g in enumerate(bl.get(sec) or []):
            for f in ("title","detail"):
                for x in check(g.get(f)): x.update({"where":"bottom_line."+sec,"index":j,"field":f,"title":g.get("title","")[:70]}); findings.append(x)
    for j,r in enumerate(bl.get("endstate_2030") or []):
        for f in ("now","then","note"):
            for x in check(r.get(f)): x.update({"where":"bottom_line.endstate","index":j,"field":f,"title":r.get("metric","")}); findings.append(x)
    for k,tk in (("money","note"),("competition","note"),("threats","note"),("timeline","event")):
        for j,r in enumerate(b.get(k) or []):
            for x in check(r.get(tk)): x.update({"where":"board."+k,"index":j,"field":tk,"title":""}); findings.append(x)
    for x in check(D.get("competition_brief")): x.update({"where":"competition_brief","index":0,"field":"brief","title":""}); findings.append(x)
    from collections import Counter
    byrule=Counter(re.sub(r" \(.*\)","",x["rule"]) for x in findings)
    print("writing check: %d finding(s)" % len(findings), "|", ", ".join(f"{k}: {v}" for k,v in byrule.most_common()) or "clean")
    json.dump({"n":len(findings),"by_rule":dict(byrule),"findings":findings}, io.open(os.path.join(a.data,"writing_report.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.fail_on is not None and len(findings)>a.fail_on:
        raise SystemExit("writing check: %d findings exceed the limit of %d" % (len(findings), a.fail_on))

if __name__ == "__main__":
    main()
