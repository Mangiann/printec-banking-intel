# -*- coding: utf-8 -*-
import os, sys, win32com.client
here = os.path.dirname(os.path.abspath(__file__))
pptx = os.path.join(here, 'Printec-Banking-Intelligence-Exec-Briefing.pptx')
outdir = os.path.join(here, 'render')
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    try: os.remove(os.path.join(outdir, f))
    except: pass
app = win32com.client.Dispatch('PowerPoint.Application')
pres = app.Presentations.Open(pptx, WithWindow=False)
# export at 1600px wide
for i, slide in enumerate(pres.Slides, 1):
    p = os.path.join(outdir, 'slide%02d.png' % i)
    slide.Export(p, 'PNG', 1600, 900)
pres.Close()
app.Quit()
print('exported', len(os.listdir(outdir)), 'pngs to', outdir)
