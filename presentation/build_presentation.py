# -*- coding: utf-8 -*-
"""
Build the C-level PowerPoint deck for Printec Banking Market Intelligence.
On-brand "Ivory" aesthetic (matches the live dashboard). 16:9.
Native shapes only (no external assets) so it renders identically anywhere.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- palette
def H(s): return RGBColor(int(s[0:2],16),int(s[2:4],16),int(s[4:6],16))

BG      = H('F4EEE0')   # warm ivory page
BG2     = H('EFE7D6')
INK     = H('16130D')   # near-black
INK2    = H('5F594C')   # muted brown-grey
INK3    = H('928B7B')   # faint labels
CARD    = H('FFFDF8')   # near-white card
CARD2   = H('FBF6EC')   # inner surface
LINE    = H('E7DDC9')   # warm hairline
LINE2   = H('EFE7D6')
SIDE    = H('141310')   # dark sidebar
SIDE2   = H('1E1C17')
SIDEINK = H('F5F1E8')
SIDEMUT = H('B9B2A4')

CYAN    = H('23C0E2'); CYAN_S = H('D3EFF8'); CYAN_I = H('0B6F87')
YELLOW  = H('F0CF49'); YEL_S  = H('F8E9A0'); YEL_I  = H('7A5C00')
GREEN   = H('A6C47C'); GRN_S  = H('D2E2B4'); GRN_I  = H('3D5A1C')
BLUE    = H('A4C6E7'); BLU_S  = H('CFE1F3'); BLU_I  = H('27506F')
LILAC   = H('BFA7E6'); LIL_S  = H('E0D4F4'); LIL_I  = H('553897')
PEACH_S = H('F4D9CE'); PEACH_I= H('9C4A36')
HI      = H('7FB069')
DANGER  = H('E2715E')
DANG_S  = H('F6D9D0')

# six agent colours (soft fill, ink) — reused everywhere agents appear
AGENTC = [
    (CYAN_S, CYAN_I, CYAN),    # A1
    (BLU_S,  BLU_I,  BLUE),    # A2
    (LIL_S,  LIL_I,  LILAC),   # A3
    (GRN_S,  GRN_I,  GREEN),   # A4
    (YEL_S,  YEL_I,  YELLOW),  # A5
    (PEACH_S,PEACH_I,DANGER),  # A6
    (H('CFE7E0'), H('1C5A4A'), H('3DAA8C')),  # A8 — Futurist (monthly, 3-5yr); A7 is the Orchestrator
]

# fonts — Plus Jakarta Sans, the website's brand font (weights via the bold flag).
# One family for all text so it renders consistently wherever the font is installed.
F   = "Plus Jakarta Sans"
FSB = "Plus Jakarta Sans"
FL  = "Plus Jakarta Sans"
FSL = "Plus Jakarta Sans"

# ---------------------------------------------------------------- setup
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = 13.333, 7.5
BLANK = prs.slide_layouts[6]
HERE = os.path.dirname(os.path.abspath(__file__))

def I(v): return Inches(v)

def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.shadow.inherit = False
    bg.fill.solid(); bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    return s

def _dash(shp, val='dash'):
    ln = shp.line._get_or_add_ln()
    for e in ln.findall(qn('a:prstDash')): ln.remove(e)
    d = ln.makeelement(qn('a:prstDash'), {'val': val}); ln.append(d)

def _shadow(shp, alpha='14000', blur='120000', dist='45000'):
    spPr = shp._element.spPr
    for e in spPr.findall(qn('a:effectLst')): spPr.remove(e)
    eff = spPr.makeelement(qn('a:effectLst'), {})
    sh  = eff.makeelement(qn('a:outerShdw'),
            {'blurRad':blur,'dist':dist,'dir':'5400000','rotWithShape':'0'})
    clr = sh.makeelement(qn('a:srgbClr'), {'val':'2A2114'})
    a   = clr.makeelement(qn('a:alpha'), {'val':alpha})
    clr.append(a); sh.append(clr); eff.append(sh); spPr.append(eff)

def rrect(s, x, y, w, h, fill=None, line=None, lw=1.0, rad=0.14, dash=None, shadow=False):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, I(x), I(y), I(w), I(h))
    shp.shadow.inherit = False
    try: shp.adjustments[0] = max(0.0, min(0.5, rad/min(w, h)))
    except Exception: pass
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(lw)
    if dash: _dash(shp, dash)
    if shadow: _shadow(shp)
    return shp

def oval(s, x, y, w, h, fill=None, line=None, lw=1.0):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, I(x), I(y), I(w), I(h))
    shp.shadow.inherit = False
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(lw)
    return shp

def cline(s, x1, y1, x2, y2, color=INK3, w=1.0, dash=None):
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, I(x1), I(y1), I(x2), I(y2))
    cn.line.color.rgb = color; cn.line.width = Pt(w)
    cn.shadow.inherit = False
    if dash: _dash(cn, dash)
    return cn

def text(s, x, y, w, h, paras, anchor='t'):
    tb = s.shapes.add_textbox(I(x), I(y), I(w), I(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = {'t':MSO_ANCHOR.TOP,'m':MSO_ANCHOR.MIDDLE,'b':MSO_ANCHOR.BOTTOM}[anchor]
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get('align', PP_ALIGN.LEFT)
        if 'before' in p: para.space_before = Pt(p['before'])
        para.space_after = Pt(p.get('after', 0))
        if 'line' in p: para.line_spacing = p['line']
        for run in p['runs']:
            r = para.add_run(); r.text = run[0]
            f = r.font
            f.size = Pt(run[1]); f.name = run[2]; f.bold = run[3]; f.color.rgb = run[4]
            if len(run) > 5 and run[5]: f.italic = True
            if 'spc' in p:
                r._r.get_or_add_rPr().set('spc', str(int(p['spc']*100)))
    return tb

def R(t, sz, col, font=F, bold=False, italic=False):
    return (t, sz, font, bold, col, italic)

def header(s, kicker, title, kcol=CYAN_I, tsize=29, tw=11.6):
    text(s, 0.62, 0.46, tw, 0.3, [{'runs':[R(kicker, 11.5, kcol, FSB, True)], 'spc':1.8}])
    text(s, 0.6, 0.74, tw, 1.0, [{'runs':[R(title, tsize, INK, FSB, True)], 'line':1.02}])

def footer(s, n):
    text(s, 0.62, 7.06, 8, 0.3, [{'runs':[R('Printec Group', 8.5, INK3, FSB, True),
                                          R('   ·   Banking Market Intelligence', 8.5, INK3, F)]}])
    text(s, 11.5, 7.06, 1.2, 0.3, [{'runs':[R('%02d' % n, 8.5, INK3, FSB, True)], 'align':PP_ALIGN.RIGHT}])

def brandchip(s, x, y, dark=True, scale=1.0):
    w, h = 1.7*scale, 0.5*scale
    bx = rrect(s, x, y, w, h, fill=(SIDE if dark else CARD),
               line=(None if dark else LINE), lw=1.0, rad=0.12*scale)
    oval(s, x+0.18*scale, y+h/2-0.05*scale, 0.1*scale, 0.1*scale, fill=CYAN)
    text(s, x+0.34*scale, y, w-0.34*scale, h,
         [{'runs':[R('Printec', 14.5*scale, (SIDEINK if dark else INK), FSB, True)],
           'align':PP_ALIGN.LEFT}], anchor='m')
    return bx

# ---------------------------------------------------------------- node icons
def bot_icon(s, x, y, sz, col, face=None):
    """Minimal robot-head 'AI agent' mark inside an sz×sz box at (x,y)."""
    cline(s, x+sz/2, y+sz*0.04, x+sz/2, y+sz*0.22, color=col, w=1.3)
    oval(s, x+sz/2-sz*0.08, y-sz*0.02, sz*0.16, sz*0.16, fill=col)
    hh = sz*0.66
    rrect(s, x, y+sz*0.26, sz, hh, fill=(face or CARD), line=col, lw=1.3, rad=sz*0.22)
    er = sz*0.15
    ey = y+sz*0.26 + hh*0.40
    oval(s, x+sz*0.30-er/2, ey, er, er, fill=col)
    oval(s, x+sz*0.70-er/2, ey, er, er, fill=col)

def script_icon(s, x, y, sz, col, face=None):
    """Minimal 'Python script / file' mark inside an sz×sz box at (x,y)."""
    w = sz*0.8; px = x+(sz-w)/2
    rrect(s, px, y, w, sz, fill=(face or CARD), line=col, lw=1.3, rad=sz*0.12)
    for i in range(3):
        ly = y+sz*0.3 + i*sz*0.2
        cline(s, px+w*0.22, ly, px+w*0.78, ly, color=col, w=1.2)

# ================================================================ SLIDE 1 — Title
def s1():
    s = slide()
    # right-side faint agent constellation
    cx, cy = 10.4, 3.9
    nodes = [(cx,cy,0.62,CYAN)]
    import math
    ring = [(CYAN_S,CYAN),(BLU_S,BLUE),(LIL_S,LILAC),(GRN_S,GREEN),(YEL_S,YELLOW),(PEACH_S,DANGER)]
    pts=[]
    for k,(sf,sd) in enumerate(ring):
        ang = math.radians(-90 + k*60)
        px = cx + 1.9*math.cos(ang); py = cy + 1.9*math.sin(ang)
        pts.append((px,py,sf,sd))
    for (px,py,sf,sd) in pts:
        cline(s, cx+0.31, cy+0.21, px+0.21, py+0.18, color=LINE, w=1.25)
    for (px,py,sf,sd) in pts:
        oval(s, px, py, 0.42, 0.42, fill=sf, line=sd, lw=1.25)
    oval(s, cx, cy, 0.62, 0.62, fill=CYAN, line=None)
    text(s, cx-0.4, cy+0.66, 1.4, 0.3,
         [{'runs':[R('6 agents · 1 system', 9, INK3, FSB, True)],'align':PP_ALIGN.CENTER}])

    brandchip(s, 0.62, 0.62, dark=True, scale=1.06)
    text(s, 0.62, 2.15, 8.3, 0.4, [{'runs':[R('EXECUTIVE BRIEFING', 12, CYAN_I, FSB, True)], 'spc':2.4}])
    text(s, 0.58, 2.55, 8.6, 2.0,
         [{'runs':[R('Banking Market', 47, INK, FL)], 'line':1.0},
          {'runs':[R('Intelligence', 47, INK, FSB, True)], 'line':1.0}])
    text(s, 0.62, 4.45, 8.4, 0.7,
         [{'runs':[R('An autonomous, multi-agent research system that infers what banks in '
                     'Printec’s footprint will need — before they ask.', 16.5, INK2, F)], 'line':1.2}])
    # meta strip
    rrect(s, 0.62, 5.5, 8.2, 0.62, fill=CARD, line=LINE, lw=1.0, rad=0.12, shadow=True)
    metas = [('17', 'countries'), ('Weekly', 'cadence'), ('100%', 'claims cited')]
    mx = 0.95
    for i,(a,b) in enumerate(metas):
        text(s, mx, 5.58, 2.4, 0.5,
             [{'runs':[R(a+'  ', 15, INK, FSB, True), R(b, 12.5, INK2, F)]}], anchor='m')
        if i < 2: cline(s, mx+2.45, 5.62, mx+2.45, 6.0, color=LINE, w=1.0)
        mx += 2.62
    text(s, 0.62, 6.55, 9, 0.4,
         [{'runs':[R('Prepared for the Printec Group leadership team', 11.5, INK3, F),
                   R('   ·   June 2026', 11.5, INK3, F)]}])
    return s

# ================================================================ SLIDE 2 — Challenge
def s2():
    s = slide()
    header(s, 'THE CHALLENGE', 'Banks don’t publish their buying plans.')
    text(s, 0.62, 1.66, 11.4, 0.8,
         [{'runs':[R('Our job is to know what every bank across 17 countries will need ', 15.5, INK2, F),
                   R('6–12 months before they issue an RFP', 15.5, INK, FSB, True),
                   R(' — without a single bank interview.', 15.5, INK2, F)], 'line':1.25}])
    cards = [
        (AGENTC[1], 'The problem',
         'Buying signals are scattered — investor decks, public tenders, regulators, job boards, vendor results — across 17 countries and a dozen languages. No single source tells you what is coming.'),
        (AGENTC[3], 'The opening',
         'Banks hire, disclose, and get regulated before they buy. Read those tells early and you reach the decision-maker while there is still a deal to shape — not after the tender is public.'),
        (AGENTC[0], 'The discipline',
         'One rule above all: never invent a number. Every figure traces to a dated, named, re-checkable source — the system only classifies and counts values that already exist.'),
    ]
    x = 0.62; w = 3.66; gap = 0.21; y = 2.75; h = 3.35
    for (col, t, body) in cards:
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        rrect(s, x, y, 0.12, h, fill=col[2], rad=0.05)
        text(s, x+0.34, y+0.34, w-0.6, 0.5, [{'runs':[R(t, 17, INK, FSB, True)]}])
        text(s, x+0.34, y+0.96, w-0.62, h-1.2, [{'runs':[R(body, 13, INK2, F)], 'line':1.32}])
        x += w + gap
    footer(s, 2)
    return s

# ================================================================ SLIDE 3 — At a glance
def s3():
    s = slide()
    header(s, 'THE SYSTEM', 'One autonomous system. Every week. Fully cited.')
    text(s, 0.62, 1.66, 11.5, 0.8,
         [{'runs':[R('Six specialist research agents, a triangulating orchestrator, and an independent '
                     'validator turn the open web into a board-grade brief and a live dashboard.', 15.5, INK2, F)],
           'line':1.25}])
    tiles = [
        ('6',    'specialist agents',     AGENTC[0]),
        ('17',   'countries covered',     AGENTC[1]),
        ('7',    'dashboard views',       AGENTC[2]),
        ('24',   'live signals this week', AGENTC[3]),
        ('17',   'rated high-confidence', AGENTC[4]),
        ('298', 'sources re-checked / wk',AGENTC[5]),
    ]
    x = 0.62; w = 1.86; gap = 0.165; y = 2.75; h = 1.9
    for (num, lab, col) in tiles:
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        rrect(s, x+0.28, y+0.32, 0.42, 0.1, fill=col[2], rad=0.04)
        text(s, x+0.0, y+0.5, w, 0.8, [{'runs':[R(num, 37, INK, FL)], 'align':PP_ALIGN.CENTER}])
        text(s, x+0.12, y+1.3, w-0.24, 0.5,
             [{'runs':[R(lab, 11, INK2, FSB, True)], 'align':PP_ALIGN.CENTER, 'line':1.05}])
        x += w + gap
    # bottom statement
    rrect(s, 0.62, 5.06, 12.1, 1.16, fill=SIDE, line=None, rad=0.16, shadow=True)
    oval(s, 0.95, 5.5, 0.28, 0.28, fill=CYAN)
    text(s, 1.4, 5.18, 11.0, 1.0,
         [{'runs':[R('Live now at ', 14, SIDEINK, F), R('printec-market-research.vercel.app', 14, CYAN, FSB, True),
                   R('  —  it refreshes automatically every week with no redeploy, and every figure, '
                     'deadline and forecast is one click from its source.', 14, SIDEMUT, F)], 'line':1.3}], anchor='m')
    footer(s, 3)
    return s

# ================================================================ SLIDE 4 — Organogram
def s4():
    s = slide()
    header(s, 'ARCHITECTURE', 'How the system is organized')
    text(s, 0.62, 1.42, 12.1, 0.32,
         [{'runs':[R('Each collector ', 10.5, INK2, F),
                   R('fans out a subagent per bank, portal, market or competitor', 10.5, INK, FSB, True),
                   R('; the Orchestrator ', 10.5, INK2, F), R('runs', 10.5, INK, FSB, True),
                   R(' the engine and ', 10.5, INK2, F), R('spawns', 10.5, INK, FSB, True),
                   R(' the validator (now auditing the 2–5yr futures too). A8 · Future Outlook runs monthly.', 10.5, INK2, F)]}])
    conn = H('C9BFA8')
    def cxf(x, w): return x + w/2
    def badge(num, cyc):
        oval(s, 0.3, cyc-0.16, 0.32, 0.32, fill=CARD2, line=LINE, lw=1.0)
        text(s, 0.3, cyc-0.16, 0.32, 0.32, [{'runs':[R(num, 11, INK2, FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')

    # legend (top-right)
    lx = 9.35; ly = 0.52
    bot_icon(s, lx, ly, 0.24, INK)
    text(s, lx+0.36, ly-0.04, 3.4, 0.28, [{'runs':[R('AI agent ', 10, INK, FSB, True), R('· LLM', 9, INK3, F)]}])
    script_icon(s, lx, ly+0.38, 0.24, INK)
    text(s, lx+0.36, ly+0.34, 3.4, 0.28, [{'runs':[R('Python script ', 10, INK, FSB, True), R('· deterministic', 9, INK3, F)]}])

    # Mission
    mw, mh = 6.6, 0.4; mx = (SW-mw)/2; my = 1.76
    rrect(s, mx, my, mw, mh, fill=SIDE, rad=0.2, shadow=True)
    oval(s, mx+0.24, my+mh/2-0.05, 0.1, 0.1, fill=CYAN)
    text(s, mx+0.1, my, mw-0.1, mh,
         [{'runs':[R('MISSION', 9, CYAN, FSB, True), R('   infer what banks will need in the next 6–12 months',
                     10.5, SIDEINK, F)], 'align':PP_ALIGN.CENTER}], anchor='m')
    mcx = cxf(mx, mw); mby = my+mh

    # (1) Collectors
    DX0 = 0.72; DXW = 11.9
    ay = 2.4; ah = 0.8; agap = 0.16; aw = (DXW - 6*agap)/7
    names = ['Bank\nDisclosures','Tenders &\nProcurement','Regulation &\nDeadlines',
             'Market\nStatistics','Early Intent\nJobs+Leaders','Vendors &\nCompetitors',
             'Future\nOutlook']
    labels = ['A1','A2','A3','A4','A5','A6','A8']   # A7 is the Orchestrator; A8 (Futurist) runs monthly for the 3-5yr arc
    centers = []; ax = DX0
    for k in range(7):
        col = AGENTC[k]
        # offset card behind each = "fans out into N subagents"
        rrect(s, ax+0.05, ay-0.05, aw, ah, fill=col[0], line=col[1], lw=1.0, rad=0.12)
        rrect(s, ax, ay, aw, ah, fill=col[0], line=col[1], lw=1.0, rad=0.12)
        bot_icon(s, ax+0.12, ay+0.11, 0.22, col[1], face=col[0])
        text(s, ax+0.42, ay+0.1, aw-0.5, 0.24, [{'runs':[R(labels[k], 11, col[1], FSB, True)]}])
        nm = names[k].split('\n')
        text(s, ax+0.05, ay+0.37, aw-0.1, 0.42,
             [{'runs':[R(nm[0], 9, col[1], FSB, True)], 'align':PP_ALIGN.CENTER, 'line':1.0},
              {'runs':[R(nm[1], 9, col[1], FSB, True)], 'align':PP_ALIGN.CENTER, 'line':1.0}])
        centers.append(cxf(ax, aw)); ax += aw + agap
    badge('①', ay+ah/2)

    # (2) Orchestrator
    ow, oh = 7.9, 0.62; ox = (SW-ow)/2; oy = 3.54
    rrect(s, ox, oy, ow, oh, fill=CYAN, rad=0.16, shadow=True)
    bot_icon(s, ox+0.32, oy+oh/2-0.15, 0.3, H('06424F'), face=H('BDEAF5'))
    text(s, ox+0.8, oy+0.1, ow-1.0, 0.28, [{'runs':[R('ORCHESTRATOR · 1 agent', 12, H('06424F'), FSB, True)]}])
    text(s, ox+0.8, oy+0.37, ow-1.0, 0.22,
         [{'runs':[R('reads findings · triangulates · writes outlooks · runs the engine · spawns the validator', 9.5, H('094E60'), F)]}])
    ocx = cxf(ox, ow); badge('②', oy+oh/2)

    # branches
    ety = 4.62; bh = 1.66
    # (3) Engine (left) — Python scripts
    elx = 0.72; elw = 5.62
    rrect(s, elx, ety, elw, bh, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    script_icon(s, elx+0.3, ety+0.24, 0.32, SIDE)
    text(s, elx+0.8, ety+0.2, elw-1.0, 0.28, [{'runs':[R('③ COMPUTE — Deterministic engine', 11.5, INK, FSB, True)]}])
    text(s, elx+0.8, ety+0.47, elw-1.0, 0.22, [{'runs':[R('Python · scripts own the numbers (sum-verified) · no LLM', 8.5, INK3, F)]}])
    scripts = [('fetch_ecb · fetch_competitors','pull ECB + SEC-EDGAR figures, sum-verified'),
               ('ingest.py','parse master table + workbook → score'),
               ('forecast.py','project the trend lines'),
               ('verify.py','re-fetch & snapshot every source'),
               ('build_dashboard.py','assemble payload · merge verdicts'),
               ('publish.py','push to the live site')]
    sy = ety+0.74
    for nm, desc in scripts:
        text(s, elx+0.34, sy, elw-0.6, 0.2, [{'runs':[R(nm, 8.5, CYAN_I, FSB, True), R('  '+desc, 8.5, INK2, F)]}])
        sy += 0.135
    ecx = cxf(elx, elw)

    # (4) Validator (right) — fan-out of agents
    vrx = 6.54; vrw = 6.08
    rrect(s, vrx, ety, vrw, bh, fill=CARD, line=CYAN, lw=1.5, rad=0.16, dash='dash')
    bot_icon(s, vrx+0.3, ety+0.22, 0.32, CYAN_I, face=CYAN_S)
    text(s, vrx+0.8, ety+0.2, vrw-1.0, 0.28, [{'runs':[R('④ AUDIT — Validator workflow', 11.5, INK, FSB, True)]}])
    text(s, vrx+0.8, ety+0.47, vrw-1.0, 0.22, [{'runs':[R('spawned by the Orchestrator · independent LLM fact-check · outlooks + futures', 8.5, INK3, F)]}])
    vcx = cxf(vrx, vrw)
    fy = ety+0.78
    text(s, vrx+0.28, fy+0.05, 0.66, 0.4, [{'runs':[R('spawns', 8.5, INK3, FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    # stack of N checkers (3 offset cards -> "many")
    sX = vrx+1.0; shw = 1.66; shc = 0.44
    for i in (2,1,0):
        rrect(s, sX+i*0.09, fy+i*0.045, shw, shc, fill=CYAN_S, line=CYAN_I, lw=1.0, rad=0.1)
    bot_icon(s, sX+0.14, fy+0.1, 0.22, CYAN_I, face=CARD)
    text(s, sX+0.44, fy+0.04, shw-0.5, 0.2, [{'runs':[R('claim checkers', 8.5, CYAN_I, FSB, True)]}])
    text(s, sX+0.44, fy+0.21, shw-0.5, 0.22, [{'runs':[R('× N', 12, CYAN_I, FSB, True)]}])
    text(s, sX+shw+0.18, fy, 0.3, shc, [{'runs':[R('+', 14, INK3, FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    wX = sX+shw+0.5; ww = 1.46
    rrect(s, wX, fy, ww, shc, fill=CARD2, line=INK3, lw=1.0, rad=0.1)
    bot_icon(s, wX+0.13, fy+0.1, 0.22, INK2, face=CARD)
    text(s, wX+0.42, fy, ww-0.46, shc, [{'runs':[R('Writer', 9.5, INK, FSB, True)]}], anchor='m')
    text(s, vrx+0.3, ety+bh-0.36, vrw-0.6, 0.32,
         [{'runs':[R('N = one per 6–12mth outlook + one per 2–5yr future; paywalled cites count if snapshotted / in the KB. ', 8, INK2, F),
                   R('Writer → outlook_validation.json + futures_validation.json; the engine merges (✓ / ⚠).', 8, INK3, F)], 'line':1.1}])

    # (5) Outputs
    oW = 7.0; ogp = 0.3; oww = (oW-ogp)/2; o1x = (SW-oW)/2; o2x = o1x+oww+ogp
    oyt = 6.42; ohh = 0.46
    rrect(s, o1x, oyt, oww, ohh, fill=CARD, line=LINE, lw=1.0, rad=0.13, shadow=True)
    text(s, o1x+0.1, oyt, oww-0.2, ohh,
         [{'runs':[R('\U0001F5A5  Live dashboard', 11.5, INK, FSB, True), R(' · 8 views', 10, INK2, F)],'align':PP_ALIGN.CENTER}], anchor='m')
    rrect(s, o2x, oyt, oww, ohh, fill=CARD, line=LINE, lw=1.0, rad=0.13, shadow=True)
    text(s, o2x+0.1, oyt, oww-0.2, ohh,
         [{'runs':[R('\U0001F4C4  Board brief', 11.5, INK, FSB, True), R(' · BLUF + Top-3', 10, INK2, F)],'align':PP_ALIGN.CENTER}], anchor='m')
    o1cx = cxf(o1x, oww); o2cx = cxf(o2x, oww); badge('⑤', oyt+ohh/2)

    # ---- connectors
    busy = (mby + ay)/2
    cline(s, mcx, mby, mcx, busy, conn, 1.25)
    cline(s, centers[0], busy, centers[-1], busy, conn, 1.25)
    for c in centers: cline(s, c, busy, c, ay, conn, 1.25)
    cbusy = (ay+ah + oy)/2
    for c in centers: cline(s, c, ay+ah, c, cbusy, conn, 1.25)
    cline(s, centers[0], cbusy, centers[-1], cbusy, conn, 1.25)
    cline(s, ocx, cbusy, ocx, oy, conn, 1.5)
    text(s, ocx+0.12, cbusy-0.12, 1.4, 0.2, [{'runs':[R('findings', 8, INK3, F)]}])
    # orchestrator -> two branches
    sply = (oy+oh + ety)/2
    cline(s, ocx, oy+oh, ocx, sply, conn, 1.5)
    cline(s, ecx, sply, vcx, sply, conn, 1.5)
    cline(s, ecx, sply, ecx, ety, conn, 1.5)
    cline(s, vcx, sply, vcx, ety, CYAN, 1.5)
    text(s, (ecx+ocx)/2-0.6, sply-0.22, 1.2, 0.2, [{'runs':[R('runs', 8.5, INK2, FSB, True)],'align':PP_ALIGN.CENTER}])
    text(s, (vcx+ocx)/2-0.6, sply-0.22, 1.2, 0.2, [{'runs':[R('spawns', 8.5, CYAN_I, FSB, True)],'align':PP_ALIGN.CENTER}])
    # engine -> outputs
    oby = (ety+bh + oyt)/2
    cline(s, ecx, ety+bh, ecx, oby, conn, 1.5)
    cline(s, ecx, oby, o2cx, oby, conn, 1.25)
    cline(s, o1cx, oby, o1cx, oyt, conn, 1.25)
    cline(s, o2cx, oby, o2cx, oyt, conn, 1.25)

    footer(s, 4)
    return s

# ================================================================ SLIDE 5 — Six specialists
def s5():
    s = slide()
    header(s, '① THE COLLECTORS', 'Six specialists, six angles on the same question')
    text(s, 0.62, 1.32, 12.1, 0.3,
         [{'runs':[R('Each fans out one subagent per unit', 11.5, INK, FSB, True),
                   R('  —  bank · portal · regulation · country · competitor — so depth scales with the week.', 11.5, INK2, F)]}])
    data = [
        ('A1','Bank Disclosures','Reads what banks tell investors.',
         'IR & strategy-day decks, verbatim earnings-call transcripts','Monthly'),
        ('A2','Tenders & Procurement','Catches banks buying in the open.',
         'TED (EU-wide API) + 15 national portals + bank-owned pages','Weekly'),
        ('A3','Regulation & Deadlines','Tracks the rules that force spend.',
         'ECB / EBA / central banks: DORA, instant payments, accessibility','2× / month'),
        ('A4','Market Statistics','Measures the structural backdrop.',
         'ECB Data Portal + central banks + leading indicators (Trends, apps)','Monthly'),
        ('A5','Early Intent — Jobs + Leadership','Spots intent before the budget.',
         'Bank career pages, LinkedIn, senior-executive appointments','Weekly'),
        ('A6','Vendors & Competitors','Watches where money already flows.',
         '150+ rivals — giants to local peers; filings, tenders, footprint press','Weekly'),
    ]
    x0 = 0.62; w = 3.93; gap = 0.18; h = 2.34; y0 = 1.72
    for i,(tag,name,hunt,where,cad) in enumerate(data):
        col = AGENTC[i]
        r = i//3; c = i%3
        x = x0 + c*(w+gap); y = y0 + r*(h+0.2)
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        oval(s, x+0.32, y+0.34, 0.5, 0.5, fill=col[0], line=col[1], lw=1.25)
        text(s, x+0.32, y+0.34, 0.5, 0.5, [{'runs':[R(tag, 12, col[1], FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, x+0.98, y+0.3, w-1.2, 0.7, [{'runs':[R(name, 13.5, INK, FSB, True)], 'line':1.0}])
        text(s, x+0.34, y+1.02, w-0.66, 0.4, [{'runs':[R(hunt, 12, col[1], FSB, True)], 'line':1.1}])
        text(s, x+0.34, y+1.42, w-0.66, 0.7,
             [{'runs':[R('Where: ', 10.5, INK3, FSB, True), R(where, 10.5, INK2, F)], 'line':1.18}])
        rrect(s, x+0.34, y+h-0.45, 1.55, 0.3, fill=col[0], rad=0.1)
        text(s, x+0.34, y+h-0.45, 1.55, 0.3, [{'runs':[R(cad, 9.5, col[1], FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    footer(s, 5)
    return s

# ================================================================ SLIDE 6 — Inside an agent
def s6():
    s = slide()
    header(s, 'HOW AN AGENT WORKS', 'Fan out, search deep — never quit at the first wall')
    text(s, 0.62, 1.62, 11.6, 0.4,
         [{'runs':[R('Worked example — the Tenders agent (A2)', 12.5, BLU_I, FSB, True)]}])
    steps = [
        ('1','TRIAGE & FAN OUT', AGENTC[1],
         'Enumerate the live set, then spawn one subagent per portal / country — each with a fresh context to own its niche.'),
        ('2','SEARCH DEEP', AGENTC[3],
         'TED API + national portals + bank-owned pages, in the local language — buyer, value, deadline, winner, dated & linked.'),
        ('3','HIT A WALL? ESCALATE', AGENTC[4],
         'API → a Google cache → a real browser that renders JavaScript. Still gated (login/PDF)? Flag it for a human — never skip.'),
        ('4','REDUCE & OUTPUT', AGENTC[0],
         'The parent dedups across niches, triangulates, and writes one cited findings file. “A gap is a prompt to try harder.”'),
    ]
    x0 = 0.62; w = 2.86; gap = 0.21; y = 2.26; h = 2.64
    for i,(n,t,col,body) in enumerate(steps):
        x = x0 + i*(w+gap)
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        oval(s, x+0.3, y+0.3, 0.46, 0.46, fill=col[2])
        text(s, x+0.3, y+0.3, 0.46, 0.46, [{'runs':[R(n, 15, H('FFFFFF'), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, x+0.3, y+0.9, w-0.55, 0.6, [{'runs':[R(t, 12.5, INK, FSB, True)], 'line':1.02}])
        text(s, x+0.3, y+1.48, w-0.52, h-1.6, [{'runs':[R(body, 11, INK2, F)], 'line':1.24}])
        if i < 3:
            text(s, x+w-0.04, y+0.28, gap+0.08, 0.5,
                 [{'runs':[R('→', 22, H('A89F8C'), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    # callouts
    rrect(s, 0.62, 5.06, 7.55, 1.18, fill=CARD2, line=LINE, lw=1.0, rad=0.14)
    text(s, 0.92, 5.2, 7.0, 0.9,
         [{'runs':[R('The exhaustiveness standard   ', 12.5, GRN_I, FSB, True)]},
          {'runs':[R('3+ search angles (keywords, languages, sources) · go one level deeper · use proxies. '
                     'Only then declare a genuine gap — with the next-best alternative named.', 11.5, INK2, F)],
           'line':1.25, 'before':3}])
    rrect(s, 8.32, 5.06, 4.4, 1.18, fill=SIDE, line=None, rad=0.14, shadow=True)
    text(s, 8.6, 5.2, 3.9, 0.95,
         [{'runs':[R('In practice', 11, CYAN, FSB, True)]},
          {'runs':[R('PrivatBank’s tenders sit behind a JavaScript-rendered portal — read via a browser, it '
                     'surfaced a live recycling-ATM prequalification in a 7,401-ATM fleet.', 11, SIDEINK, F)], 'line':1.24, 'before':3}])
    footer(s, 6)
    return s

# ================================================================ SLIDE 7 — Triangulation
def s7():
    s = slide()
    header(s, '② SYNTHESIS — THE ORCHESTRATOR', 'Confidence is earned by agreement')
    # left: converge diagram
    lx, ly = 0.62, 1.9
    rrect(s, lx, ly, 5.7, 4.2, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    text(s, lx+0.36, ly+0.3, 5.0, 0.4, [{'runs':[R('From six streams to one ranked view', 13.5, INK, FSB, True)]}])
    # three agent chips converging to a node
    chip = [('A2', AGENTC[1], 2.5), ('A1', AGENTC[0], 3.35), ('A5', AGENTC[4], 4.2)]
    nodecx, nodecy = lx+3.95, ly+1.95
    for (tg,col,cy) in chip:
        rrect(s, lx+0.4, cy, 1.0, 0.5, fill=col[0], line=col[1], lw=1.0, rad=0.1)
        text(s, lx+0.4, cy, 1.0, 0.5, [{'runs':[R(tg, 12, col[1], FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        cline(s, lx+1.45, cy+0.25, nodecx-0.02, nodecy+0.25, color=H('C9BFA8'), w=1.25)
    rrect(s, nodecx, nodecy, 1.6, 0.5, fill=CYAN, rad=0.1, shadow=True)
    text(s, nodecx, nodecy, 1.6, 0.5, [{'runs':[R('HIGH', 13, H('07485A'), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    text(s, lx+0.4, ly+2.95, 5.0, 1.1,
         [{'runs':[R('One agent alone caps a signal at ', 12, INK2, F), R('Medium', 12, YEL_I, FSB, True),
                   R('. Two or more independent agents — different evidence types — on the same need makes it '
                     'eligible for ', 12, INK2, F), R('High', 12, GRN_I, FSB, True),
                   R('. Only the orchestrator promotes it, after re-checking the key figure on the live source.', 12, INK2, F)],
           'line':1.3}])
    # right: two lenses
    rx = 6.55; rw = 6.18
    lenses = [
        ('By evidence', AGENTC[3], 'How well-proven a signal is — confidence weight plus a bonus for each independent agent that confirms it.'),
        ('By value', AGENTC[2], 'The risk-adjusted prize — deal-size × win-probability × confidence. Threats & macro trends score zero, so noise can never outrank a concrete biddable deal.'),
    ]
    yy = 1.9
    for (t,col,body) in lenses:
        rrect(s, rx, yy, rw, 1.62, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        rrect(s, rx, yy, 0.12, 1.62, fill=col[2], rad=0.05)
        text(s, rx+0.34, yy+0.22, rw-0.6, 0.4, [{'runs':[R(t, 15, INK, FSB, True)]}])
        text(s, rx+0.34, yy+0.72, rw-0.62, 0.85, [{'runs':[R(body, 12, INK2, F)], 'line':1.26}])
        yy += 1.82
    rrect(s, rx, yy, rw, 0.76, fill=SIDE, rad=0.14, shadow=True)
    text(s, rx+0.34, yy, rw-0.6, 0.76,
         [{'runs':[R('The brief leads with value; the dashboard lets you toggle between both lenses.', 12, SIDEINK, F)],
           'line':1.2}], anchor='m')
    footer(s, 7)
    return s

# ================================================================ SLIDE 8 — Validation stack
def s8():
    s = slide()
    header(s, 'TRUST', 'Four layers between a claim and your decision')
    layers = [
        ('1','CITE EVERYTHING', AGENTC[0],
         'Every claim carries a named, dated, clickable source. The cardinal rule: never invent a number.'),
        ('2','RE-FETCH & SNAPSHOT', AGENTC[1],
         'A deterministic trust pass re-opens every cited URL each week and saves a timestamped copy — 274 of 298 reachable, defending against link-rot.'),
        ('3','FIGURE RE-CHECK', AGENTC[3],
         'Before any signal is “decision-grade”, the orchestrator re-opens a primary source and confirms the key number with a quoted snippet — or downgrades it.'),
        ('4','INDEPENDENT VALIDATOR', AGENTC[2],
         'A separate, adversarial pass traces every forward-looking call back to its sources and flags anything that does not trace — visibly, never hidden.'),
    ]
    x = 0.62; w = 7.4; h = 0.96; y = 1.78
    for i,(n,t,col,body) in enumerate(layers):
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.14, shadow=True)
        rrect(s, x, y, 0.85, h, fill=col[2], rad=0.06)
        text(s, x, y, 0.85, h, [{'runs':[R(n, 24, H('FFFFFF'), FL)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, x+1.06, y+0.14, w-1.3, 0.34, [{'runs':[R(t, 13, INK, FSB, True)]}])
        text(s, x+1.06, y+0.46, w-1.3, h-0.5, [{'runs':[R(body, 11, INK2, F)], 'line':1.18}])
        if i < 3:
            text(s, x+0.36, y+h-0.03, 0.5, 0.28, [{'runs':[R('↓', 13, INK3, FSB, True)]}])
        y += h + 0.16
    # right rail
    rrect(s, 8.34, 1.78, 4.38, 4.5, fill=SIDE, rad=0.18, shadow=True)
    oval(s, 8.66, 2.12, 0.34, 0.34, fill=CYAN)
    text(s, 8.66, 2.55, 3.8, 1.2,
         [{'runs':[R('The engine fabricates nothing.', 17, SIDEINK, FSB, True)], 'line':1.1}])
    text(s, 8.66, 3.7, 3.8, 1.4,
         [{'runs':[R('It only classifies and does arithmetic on values that already exist in a source. '
                     'Every number on the dashboard can be opened, re-checked, and audited.', 12.5, SIDEMUT, F)], 'line':1.34}])
    rrect(s, 8.66, 5.45, 3.78, 0.62, fill=SIDE2, rad=0.12)
    text(s, 8.66, 5.45, 3.78, 0.62, [{'runs':[R('Reachability is automatic. ', 11, CYAN, FSB, True),
                                               R('Figure accuracy is signed off.', 11, SIDEINK, F)],
                                       'align':PP_ALIGN.CENTER}], anchor='m')
    footer(s, 8)
    return s

# ================================================================ SLIDE 9 — Validator
def s9():
    s = slide()
    header(s, '④ THE VALIDATOR', 'An independent fact-checker, by design')
    text(s, 0.62, 1.66, 7.4, 1.0,
         [{'runs':[R('The weak point of any analysis is that the author proofreads their own work. So a separate '
                     'set of agents re-checks the forward-looking calls — with one job: confirm every claim traces '
                     'to its source, and flag the ones that don’t.', 14.5, INK2, F)],
           'line':1.3}])
    pts = [
        ('What it is', 'Fresh agents, spawned with a blank slate and an adversarial mandate — one fact-checker per market.'),
        ('How it stays independent', 'They re-read each call against the primary documents it cites — a fresh, separate pass that checks the claims, not the author. Like a code reviewer who didn’t write the code: independence is fresh context, not a different schedule.'),
        ('What it produces', 'Each outlook is marked “✓ independently validated”; any claim it can’t trace shows as a visible “⚠ not yet linked to a source” caveat — shown to the reader, never hidden. Its verdict overrides the analyst’s self-assessment.'),
    ]
    y = 2.74
    for (t,b) in pts:
        text(s, 0.62, y, 7.4, 0.4, [{'runs':[R(t, 13.5, LIL_I, FSB, True)]}])
        text(s, 0.62, y+0.36, 7.45, 0.86, [{'runs':[R(b, 12, INK2, F)], 'line':1.26}])
        y += 1.24
    # right: validated outlook card mock + result
    cx0 = 8.34; cw = 4.38
    rrect(s, cx0, 1.78, cw, 2.55, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    rrect(s, cx0+0.3, 2.06, 1.7, 0.34, fill=GRN_S, rad=0.1)
    text(s, cx0+0.3, 2.06, 1.7, 0.34, [{'runs':[R('GROWTH', 9.5, GRN_I, FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
    text(s, cx0+0.3, 2.5, cw-0.6, 0.4, [{'runs':[R('Ukraine · ATM modernization', 13, INK, FSB, True)]}])
    text(s, cx0+0.3, 2.9, cw-0.6, 0.7,
         [{'runs':[R('Reasoned outlook with cited drivers, projected range, and an evidence trail.', 11, INK2, F)], 'line':1.22}])
    rrect(s, cx0+0.3, 3.62, cw-0.6, 0.32, fill=GRN_S, rad=0.08)
    text(s, cx0+0.42, 3.62, cw-0.7, 0.32, [{'runs':[R('✓ Independently validated', 10.5, GRN_I, FSB, True)]}], anchor='m')
    rrect(s, cx0+0.3, 3.98, cw-0.6, 0.32, fill=DANG_S, rad=0.08)
    text(s, cx0+0.42, 3.98, cw-0.7, 0.32, [{'runs':[R('⚠ 1 claim not yet linked to a source', 10.5, PEACH_I, FSB, True)]}], anchor='m')
    # result strip
    rrect(s, cx0, 4.5, cw, 1.78, fill=SIDE, rad=0.16, shadow=True)
    text(s, cx0+0.3, 4.72, cw-0.6, 0.4, [{'runs':[R('This week’s audit', 11, CYAN, FSB, True)]}])
    res = [('21','outlooks audited'),('15','fully grounded'),('6','honest caveat')]
    bx = cx0+0.3
    for (n,l) in res:
        text(s, bx, 5.12, 1.25, 0.6, [{'runs':[R(n, 26, SIDEINK, FL)],'align':PP_ALIGN.LEFT}])
        text(s, bx, 5.75, 1.3, 0.4, [{'runs':[R(l, 9.5, SIDEMUT, FSB, True)], 'line':1.0}])
        bx += 1.32
    footer(s, 9)
    return s

# ================================================================ SLIDE 10 — Dashboard
def s10():
    s = slide()
    header(s, '⑤ REPORT', 'One live dashboard, seven questions answered')
    # ---- left: framed REAL screenshot of the live dashboard
    fx, fy, fw = 0.62, 1.82, 6.86
    bar_h = 0.36
    img_w = fw - 0.16
    img_h = img_w * (2080.0/3040.0)
    card_h = bar_h + img_h + 0.14
    rrect(s, fx, fy, fw, card_h, fill=CARD, line=H('CCC1A9'), lw=1.25, rad=0.12, shadow=True)
    rrect(s, fx, fy, fw, bar_h, fill=H('23211C'), rad=0.12)
    for i,c in enumerate([H('E2715E'), H('F0CF49'), H('7FB069')]):
        oval(s, fx+0.2+i*0.17, fy+bar_h/2-0.05, 0.1, 0.1, fill=c)
    rrect(s, fx+0.82, fy+0.08, fw-1.6, bar_h-0.16, fill=H('38332B'), rad=0.06)
    text(s, fx+0.82, fy, fw-1.6, bar_h,
         [{'runs':[R('printec-market-research.vercel.app', 9.5, H('CFC8BC'), F)], 'align':PP_ALIGN.CENTER}], anchor='m')
    shot = os.path.join(HERE, 'assets', 'dash_thisweek.png')
    if os.path.exists(shot):
        s.shapes.add_picture(shot, I(fx+0.08), I(fy+bar_h+0.02), width=I(img_w))
    else:
        rrect(s, fx+0.08, fy+bar_h+0.02, img_w, img_h, fill=CARD2, line=LINE)
    text(s, fx+0.02, fy+card_h+0.02, fw, 0.26,
         [{'runs':[R('Actual live view — “This week”, ', 9.5, INK3, FSB, True),
                   R('week of 2026-06-13', 9.5, INK3, F)]}])
    # ---- right: the seven views + live note
    rx = 7.74; rw = 4.98
    text(s, rx, 1.9, rw, 0.3, [{'runs':[R('THE SEVEN VIEWS', 11, CYAN_I, FSB, True)], 'spc':1.6}])
    views = [
        ('1','This week','what changed — and what is hot now', AGENTC[0]),
        ('2','Countries','where to focus', AGENTC[3]),
        ('3','Products','demand by Printec solution', AGENTC[1]),
        ('4','Competition','where rivals are strong vs. thin', AGENTC[5]),
        ('5','Accounts & deadlines','who to approach, and by when', AGENTC[4]),
        ('6','Outlook','where each market is heading, and why', AGENTC[2]),
        ('7','Patterns & history','how it fits the long-run story', AGENTC[3]),
    ]
    yy = 2.36
    for (num,t,q,col) in views:
        oval(s, rx, yy+0.02, 0.32, 0.32, fill=col[0], line=col[1], lw=1.0)
        text(s, rx, yy+0.02, 0.32, 0.32, [{'runs':[R(num, 10.5, col[1], FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, rx+0.46, yy-0.02, rw-0.5, 0.26, [{'runs':[R(t, 11.5, INK, FSB, True)]}])
        text(s, rx+0.46, yy+0.225, rw-0.5, 0.24, [{'runs':[R(q, 9.5, INK2, F)]}])
        yy += 0.485
    rrect(s, rx, 5.86, rw, 0.92, fill=SIDE, rad=0.14, shadow=True)
    oval(s, rx+0.26, 6.1, 0.22, 0.22, fill=CYAN)
    text(s, rx+0.58, 5.99, rw-0.74, 0.7,
         [{'runs':[R('Live & self-updating  ', 11.5, SIDEINK, FSB, True),
                   R('— new week every Friday, no redeploy; time-travel to any past week; every figure one click from its source.', 9.5, SIDEMUT, F)], 'line':1.16}], anchor='m')
    footer(s, 10)
    return s

# ================================================================ SLIDE 11 — Weekly rhythm
def s11():
    s = slide()
    header(s, 'CADENCE', 'A standing weekly cycle')
    text(s, 0.62, 1.62, 11.8, 0.4,
         [{'runs':[R('Agents run through the week on their own schedules; Friday synthesises, validates, and '
                     'publishes — automatically.', 12.5, INK2, F)]}])
    # timeline (weekly agents only)
    ty = 3.55
    cline(s, 0.95, ty, 12.4, ty, color=LINE, w=2.5)
    days = [
        ('MON','Tenders &\nProcurement', AGENTC[1], 1.75, False),
        ('TUE','Jobs &\nLeadership', AGENTC[4], 3.55, False),
        ('WED','Vendors &\nCompetitors', AGENTC[5], 5.35, False),
        ('FRI','Orchestrate →\nValidate → Publish', AGENTC[0], 9.6, True),
    ]
    for (d,lab,col,cxp,hi) in days:
        oval(s, cxp-0.13, ty-0.13, 0.26, 0.26, fill=(CYAN if hi else col[2]))
        rrect(s, cxp-0.7, ty-1.45, 1.4, 0.4, fill=(SIDE if hi else col[0]), rad=0.1, shadow=hi)
        text(s, cxp-0.7, ty-1.45, 1.4, 0.4, [{'runs':[R(d, 12, (CYAN if hi else col[1]), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        cline(s, cxp, ty-1.05, cxp, ty-0.13, color=(CYAN if hi else col[1]), w=1.5)
        nm = lab.split('\n')
        text(s, cxp-1.15, ty+0.24, 2.3, 0.8,
             [{'runs':[R(nm[0], 10.5, INK, FSB, True)],'align':PP_ALIGN.CENTER, 'line':1.05}] +
             ([{'runs':[R(nm[1], 10.5, INK, FSB, True)],'align':PP_ALIGN.CENTER, 'line':1.05}] if len(nm)>1 else []))
    # periodic-agents caption
    text(s, 1.0, 4.32, 11.4, 0.34,
         [{'runs':[R('Plus periodic inputs:  ', 10.5, INK3, FSB, True),
                   R('Bank Disclosures (monthly) · Regulation (twice-monthly) · Market Statistics (monthly).', 10.5, INK2, F)],
           'align':PP_ALIGN.CENTER}])
    # friday big block
    rrect(s, 8.55, 4.92, 4.17, 1.5, fill=SIDE, rad=0.16, shadow=True)
    text(s, 8.85, 5.08, 3.6, 0.4, [{'runs':[R('FRIDAY — synthesis & publish', 11.5, CYAN, FSB, True)]}])
    fl = ['Triangulate the six streams → master table',
          'Write the reasoned outlook + run the validator',
          'Engine builds & publishes → dashboard + brief live']
    yy = 5.44
    for it in fl:
        text(s, 8.85, yy, 3.65, 0.4, [{'runs':[R('→ ', 11, CYAN, FSB, True), R(it, 10.5, SIDEINK, F)], 'line':1.1}])
        yy += 0.32
    # left note
    rrect(s, 0.62, 4.92, 7.6, 1.5, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    text(s, 0.92, 5.12, 7.0, 0.4, [{'runs':[R('Why a cadence matters', 12.5, GRN_I, FSB, True)]}])
    text(s, 0.92, 5.5, 7.0, 0.9,
         [{'runs':[R('Weekly tenders, jobs and vendor moves catch fast-moving windows; the monthly inputs add the '
                     'structural backdrop. The result is a living picture, not a one-off report.', 12, INK2, F)], 'line':1.3}])
    footer(s, 11)
    return s

# ================================================================ SLIDE 12 — Payoff
def s12():
    s = slide()
    header(s, 'THE PAYOFF', 'From signal to decision')
    cards = [
        (AGENTC[0],'Early warning','Reach the bank before the RFP is written — while you can still shape the spec, not just respond to it.'),
        (AGENTC[4],'Named contacts','A new CDO or Head of Channels handed to sales, with the 6–12-month decision window already flagged.'),
        (AGENTC[3],'A board-grade brief','Bottom-line-up-front: the three highest-value moves with owner, by-when, and a deal-size band.'),
        (AGENTC[2],'Prioritised by value','Opportunities ranked by risk-adjusted prize — size × win × confidence — not by noise or recency.'),
        (AGENTC[1],'A defensible trail','Every claim re-checkable to a dated source. Nothing in front of the board is taken on faith.'),
    ]
    # 5 cards: row of 3 + row of 2 (centered)
    w=3.93; gap=0.21; h=2.06; y0=1.85
    pos = [(0.62,y0),(0.62+w+gap,y0),(0.62+2*(w+gap),y0),
           (0.62+0.5*(w+gap)+0.0, y0+h+0.22),(0.62+1.5*(w+gap)+0.0, y0+h+0.22)]
    # center the bottom two
    bx0 = (SW - (2*w+gap))/2
    pos[3]=(bx0, y0+h+0.22); pos[4]=(bx0+w+gap, y0+h+0.22)
    for i,(col,t,b) in enumerate(cards):
        x,y = pos[i]
        rrect(s, x, y, w, h, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
        oval(s, x+0.34, y+0.34, 0.42, 0.42, fill=col[2])
        text(s, x+0.34, y+0.34, 0.42, 0.42, [{'runs':[R('✓', 13, H('FFFFFF'), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, x+0.92, y+0.36, w-1.1, 0.5, [{'runs':[R(t, 14.5, INK, FSB, True)], 'line':1.0}])
        text(s, x+0.34, y+1.04, w-0.66, 0.9, [{'runs':[R(b, 11.5, INK2, F)], 'line':1.28}])
    footer(s, 12)
    return s

# ================================================================ SLIDE 13 — Roadmap
def s13():
    s = slide()
    header(s, 'STATUS & ROADMAP', 'Live today — and designed to grow')
    # live now
    rrect(s, 0.62, 1.8, 6.0, 4.45, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    rrect(s, 0.62, 1.8, 6.0, 0.62, fill=GRN_S, rad=0.16)
    text(s, 0.95, 1.8, 5.4, 0.62, [{'runs':[R('LIVE NOW', 13, GRN_I, FSB, True)], 'spc':1.5}], anchor='m')
    live = ['Expected-value ranking (value, not just visibility)',
            'Foresight layer — reasoned Outlook per market',
            'Trust pass: every source re-fetched & snapshotted',
            'Source links everywhere — figure → source in one click',
            'Independent traceability validator',
            'Full-size-range competitor map — local peers to giants',
            'Live dashboard auto-publishing every week']
    yy = 2.6
    for it in live:
        oval(s, 0.95, yy+0.04, 0.2, 0.2, fill=GREEN)
        text(s, 0.96, yy-0.0, 0.2, 0.28, [{'runs':[R('✓', 9.5, H('FFFFFF'), FSB, True)],'align':PP_ALIGN.CENTER}], anchor='m')
        text(s, 1.3, yy, 5.1, 0.5, [{'runs':[R(it, 12, INK, F)], 'line':1.12}])
        yy += 0.5
    # on the horizon
    rrect(s, 6.82, 1.8, 5.9, 4.45, fill=CARD, line=LINE, lw=1.0, rad=0.16, shadow=True)
    rrect(s, 6.82, 1.8, 5.9, 0.62, fill=CYAN_S, rad=0.16)
    text(s, 7.15, 1.8, 5.3, 0.62, [{'runs':[R('ON THE HORIZON', 13, CYAN_I, FSB, True)], 'spc':1.5}], anchor='m')
    nxt = [('Beyond banking','Extend to other Printec verticals — retail, fuel, postal, telco — once the method is proven.'),
           ('Deeper leading indicators','Broaden the early-signal sweep (search trends, app adoption, web traffic) feeding the Outlook.'),
           ('Competitor depth','Segment revenue for the listed regionals + RFP-win tracking per competitor — who actually won which deal.')]
    yy = 2.72
    for (t,b) in nxt:
        oval(s, 7.15, yy+0.05, 0.2, 0.2, fill=CYAN)
        text(s, 7.5, yy, 5.0, 0.4, [{'runs':[R(t, 13, INK, FSB, True)]}])
        text(s, 7.5, yy+0.36, 4.95, 0.7, [{'runs':[R(b, 11.5, INK2, F)], 'line':1.24}])
        yy += 1.18
    rrect(s, 7.15, yy-0.05, 5.25, 0.66, fill=CARD2, line=LINE, lw=1.0, rad=0.12)
    text(s, 7.4, yy-0.05, 4.9, 0.66,
         [{'runs':[R('Banking-first by design: ', 10.5, INK, FSB, True),
                   R('new verticals add collectors, not a rebuild.', 10.5, INK2, F)], 'line':1.18}], anchor='m')
    footer(s, 13)
    return s

# ================================================================ SLIDE 14 — Close
def s14():
    s = slide()
    rrect(s, 0, 0, SW, SH, fill=SIDE, rad=0.0)
    # subtle constellation top-right
    import math
    cx, cy = 11.0, 1.6
    for k,(sf,sd) in enumerate([(CYAN_S,CYAN),(BLU_S,BLUE),(GRN_S,GREEN),(YEL_S,YELLOW),(LIL_S,LILAC),(PEACH_S,DANGER)]):
        ang=math.radians(k*60); px=cx+1.0*math.cos(ang); py=cy+1.0*math.sin(ang)
        oval(s, px, py, 0.2, 0.2, fill=None, line=H('3A352B'), lw=1.0)
    brandchip(s, 0.7, 0.7, dark=False, scale=1.06)
    text(s, 0.7, 2.85, 11.6, 1.6,
         [{'runs':[R('Every number on the screen', 38, SIDEINK, FL)], 'line':1.04},
          {'runs':[R('traces to a source you can open.', 38, SIDEINK, FSB, True)], 'line':1.04}])
    text(s, 0.72, 4.75, 11.0, 0.6,
         [{'runs':[R('The system that knows what banks will need — before they ask.', 16, SIDEMUT, F)]}])
    rrect(s, 0.72, 5.6, 5.4, 0.66, fill=SIDE2, rad=0.14)
    oval(s, 1.0, 5.83, 0.2, 0.2, fill=CYAN)
    text(s, 1.32, 5.6, 4.8, 0.66, [{'runs':[R('printec-market-research.vercel.app', 13.5, CYAN, FSB, True)]}], anchor='m')
    text(s, 0.72, 6.7, 11, 0.4, [{'runs':[R('Printec Group  ·  Banking Market Intelligence  ·  June 2026', 10.5, SIDEMUT, F)]}])
    return s

# ---------------------------------------------------------------- build
for fn in [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]:
    fn()

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'Printec-Banking-Intelligence-Exec-Briefing.pptx')
prs.save(out)
print('SAVED:', out)
print('slides:', len(prs.slides._sldIdLst))
