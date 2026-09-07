#!/usr/bin/env python3
"""Fail the build if a banned claim, a label headline, or a visible rule survives.

    python3 qa_gate.py [source.py] [renders_dir] [banned.json] [expected_count]

banned.json is {"regex": "why it is banned"} — one entry per claim that has ever had
to be pulled. It is the memory of the project. Add to it every time something is
retracted, so the same mistake cannot ship twice.
"""
import re, sys, glob, os
import numpy as np
from PIL import Image

SRC   = sys.argv[1] if len(sys.argv)>1 else "v4.py"
RENDER= sys.argv[2] if len(sys.argv)>2 else "v4"
BANNED_F = sys.argv[3] if len(sys.argv)>3 else "banned.json"
EXPECT= int(sys.argv[4]) if len(sys.argv)>4 else 0
src = open(SRC).read()
fails, warns = [], []

# 1. Claims that must never ship. Each one shipped once and had to be pulled.
import json
BANNED = json.load(open(BANNED_F)) if os.path.exists(BANNED_F) else {}
for pat, why in BANNED.items():
    if re.search(pat, src, re.I):
        fails.append(f"BANNED CLAIM  {why}")

# 2. Every headline must stand alone if screenshotted and sent to one person.
for tag in ("A", "B", "C"):
    blk = re.search(rf"^{tag} = \[(.*?)^\]\]", src, re.S | re.M).group(1)
    # a CTA is an imperative by design, so it is exempt from the standalone-claim rule
    entries = re.findall(r'dict\((.*?)\),\n', blk, re.S)
    for e in entries:
        if 'k="cta"' in e: continue
        m = re.search(r'lead="([^"]*)"', e)
        if not m: continue
        lead = m.group(1)
        w = lead.replace("<br>", " ").rstrip(".").split()
        if len(w) <= 3 and not any(x.lower() in ("we","you","your","us") for x in w):
            fails.append(f"LABEL HEADLINE  {tag}: \"{lead}\" is a label, not a claim")

# 3. Divider rules must be invisible.
if os.path.exists("css.txt") and ".rule" in open("css.txt").read():
    if "background:transparent" not in open("css.txt").read().split(".rule")[1][:120]:
        fails.append("RULE  the divider line is not transparent")

# 4. Renders present and correctly sized.
pngs = sorted(glob.glob(f"{RENDER}/*.png"))
if EXPECT and len(pngs) != EXPECT:
    fails.append(f"RENDER  expected {EXPECT} slides, found {len(pngs)}")
for f in pngs:
    if Image.open(f).size != (1080, 1350):
        fails.append(f"RENDER  {os.path.basename(f)} is not 1080x1350")

# 5. Slide numbers must be readable against whatever sits behind them.
for f in pngs:
    a = np.array(Image.open(f).convert("L")).astype(float)
    best = 0
    for box in ((820,108,985,162), (820,1192,985,1246)):
        r = a[box[1]:box[3], box[0]:box[2]]
        best = max(best, np.percentile(r,97) - np.percentile(r,25))
    if best < 18:
        warns.append(f"contrast  {os.path.basename(f)} slide number is faint ({best:.0f})")

print("=" * 62)
for x in fails: print("FAIL   ", x)
for x in warns: print("warn   ", x)
if not fails: print(f"PASS    no banned claims, no label headlines, {len(pngs)} slides clean")
print("=" * 62)
sys.exit(1 if fails else 0)
