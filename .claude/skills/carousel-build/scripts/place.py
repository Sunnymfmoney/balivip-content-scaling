#!/usr/bin/env python3
"""
Decide where type sits on a photograph, deterministically.

The rule is aesthetic before it is legible: type belongs in the EMPTY part of the
frame — sky, water, a wall, out-of-focus ground — and must never sit over the subject.
Legibility is handled downstream by a scrim that darkens whichever end the copy lands
on, so brightness is only a light tiebreaker. DETAIL is the signal that matters.

This replaces the obvious-but-wrong heuristic of "put type on the darkest band",
which loses every time the empty part of the frame is a bright sky.

    python3 place.py manifest.tsv placement.json [--w 1080] [--h 1350]

manifest.tsv is two tab-separated columns: key<TAB>path/to/photo.jpg
placement.json maps each key to {"pos": "top"|"bottom", ...diagnostics}.

Deterministic: same inputs always produce the same output, so re-running it never
disturbs a placement you have already reviewed.
"""
import json, sys
from PIL import Image, ImageFilter, ImageStat

DETAIL_WEIGHT = 0.72   # how busy the band is. This is the decision.
LUMA_WEIGHT   = 0.28   # the scrim can rescue brightness, so it only breaks ties.
EDGE_CEILING  = 40.0   # edge energy above this is "full of subject"
MARGIN_FLOOR  = 0.02   # below this the two bands are a coin toss; flagged for a human

def cover_crop(path, W, H):
    im = Image.open(path); im.draft("RGB", (W*2, H*2)); im = im.convert("L")
    s = max(W/im.width, H/im.height)
    im = im.resize((max(W, int(im.width*s)), max(H, int(im.height*s))))
    l = (im.width-W)//2; t = (im.height-H)//2
    return im.crop((l, t, l+W, t+H))

def band_score(band):
    """Lower is better: an empty band scores near zero."""
    edges  = ImageStat.Stat(band.filter(ImageFilter.FIND_EDGES)).mean[0]
    detail = min(edges/EDGE_CEILING, 1.0)
    luma   = ImageStat.Stat(band).mean[0]/255.0
    return DETAIL_WEIGHT*detail + LUMA_WEIGHT*luma

def place(manifest, out_path, W=1080, H=1350):
    M = dict(l.rstrip("\n").split("\t") for l in open(manifest) if l.strip())
    out = {}
    for k, p in M.items():
        g = cover_crop(p, W, H)
        # the two zones type can occupy, inset from the edges by the layout padding
        top = band_score(g.crop((int(W*0.09), int(H*0.04), int(W*0.91), int(H*0.48))))
        bot = band_score(g.crop((int(W*0.09), int(H*0.52), int(W*0.91), int(H*0.96))))
        margin = abs(top-bot)
        out[k] = {
            "pos": "top" if top < bot else "bottom",
            "top": round(top, 3), "bottom": round(bot, 3),
            "margin": round(margin, 3),
            "review": margin < MARGIN_FLOOR,   # too close to call, put a human on it
        }
    json.dump(out, open(out_path, "w"), indent=1)
    tops = sum(1 for v in out.values() if v["pos"] == "top")
    close = [k for k, v in out.items() if v["review"]]
    print(f"{tops} top / {len(out)} total")
    if close:
        print(f"too close to call, review by eye: {', '.join(sorted(close))}")
    return out

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__); sys.exit(1)
    W = int(a[a.index("--w")+1]) if "--w" in a else 1080
    H = int(a[a.index("--h")+1]) if "--h" in a else 1350
    place(a[0], a[1], W, H)
