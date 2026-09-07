#!/usr/bin/env python3
"""
Turn a deck JSON into slide HTML.

    python3 scripts/build.py content/carousels/how-not-to-plan

Reads   <deck>/deck.json
Writes  build/<deck-name>/NN.html

You do not normally call this directly. Use `make <deck>` or scripts/ship.py,
which builds, renders, and runs the quality gate in one go.
"""
import os, sys, json, glob
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIZES = {"carousel": (1080, 1350), "story": (1080, 1920), "reel": (1080, 1920)}


def load_manifest():
    """key -> photo path. Missing manifest is fine until a deck names a photo."""
    p = os.path.join(ROOT, "photos", "manifest.tsv")
    if not os.path.exists(p):
        return {}
    out = {}
    for line in open(p, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or "\t" not in line:
            continue
        k, v = line.split("\t", 1)
        out[k.strip()] = v.strip()
    return out


M = load_manifest()
PLACEMENT = json.load(open(os.path.join(ROOT, "brand", "placement.json"), encoding="utf-8"))


def photo(key):
    if key not in M:
        sys.exit(
            f"\n  PHOTO NOT FOUND: '{key}'\n"
            f"  Add a line to photos/manifest.tsv:\n"
            f"      {key}\t<path under photos/>\n"
        )
    p = os.path.join(ROOT, "photos", M[key])
    if not os.path.exists(p):
        sys.exit(f"\n  manifest.tsv points '{key}' at a file that is not there:\n      {p}\n")
    return "file://" + quote(os.path.abspath(p))


def css(fmt):
    tmpl = open(os.path.join(ROOT, "brand", "css", "carousel.css.tmpl"), encoding="utf-8").read()
    tmpl = tmpl.replace("{{", "{").replace("}}", "}")
    tmpl = tmpl.replace("{FONTS}", os.path.join(ROOT, "brand", "fonts"))
    extra = open(os.path.join(ROOT, "brand", "css", "components.css"), encoding="utf-8").read()
    w, h = SIZES[fmt]
    # one place decides the canvas, so story and reel reuse the whole carousel system
    size = f"html,body{{width:{w}px;height:{h}px}}.slide{{width:{w}px;height:{h}px}}"
    if fmt in ("story", "reel"):
        # Instagram overlays its own UI on a 9:16 frame: the profile row across the top
        # and the reply bar across the bottom. Copy has to clear both.
        size += (
            ".pad{padding:260px 110px 300px}"
            ".num{top:180px;right:110px}.num.low{top:auto;bottom:220px}"
            ".foot{position:absolute;left:110px;right:110px;bottom:190px;margin-top:0}"
            ".scrim{background:linear-gradient(180deg,rgba(12,15,20,.92) 0%,rgba(12,15,20,.55) 22%,"
            "rgba(12,15,20,.10) 42%,rgba(12,15,20,.10) 58%,rgba(12,15,20,.70) 82%,rgba(12,15,20,.95) 100%)}"
            ".scrim.top{background:linear-gradient(180deg,rgba(12,15,20,.95) 0%,rgba(12,15,20,.72) 26%,"
            "rgba(12,15,20,.12) 50%,rgba(12,15,20,.30) 78%,rgba(12,15,20,.88) 100%)}"
            # the CTA runs its footer inline, otherwise it lands on top of the button
            ".cta .photo-top{height:1180px}.cta .fade{top:980px;height:200px}"
            ".cta .pad{padding:260px 110px 240px}"
            ".cta .foot{position:static;margin-top:44px}"
            ".card .photo-top{height:1100px!important}"
        )
    return tmpl + extra + size


# ---------- type sizing. Long copy steps down, it never overflows. ----------

def lead_size(t, cover=False):
    L = len(t.replace("<br>", " "))
    if cover:
        return 84 if L <= 70 else (76 if L <= 96 else 68)
    return 104 if L <= 22 else (86 if L <= 40 else (72 if L <= 62 else (60 if L <= 88 else 54)))


def quote_size(t):
    L = len(t)
    return 46 if L <= 110 else (42 if L <= 180 else (38 if L <= 260 else 34))


def quote_photo_h(t):
    L = len(t)
    return 880 if L <= 110 else (800 if L <= 180 else (720 if L <= 260 else 645))


def segs(t):
    """Wrap every authored line so fit.py can prove it renders on one line."""
    return "<br>".join(f'<span class="seg">{p}</span>' for p in t.split("<br>"))


# ---------- slide kinds ----------

def slide(s, n, tot, fmt):
    k = s.get("kind", "content")

    if k == "review":
        h = quote_photo_h(s["quote"])
        who = s["who"]
        return (
            f'<div class="slide card">'
            f'<img class="photo-top" style="height:{h}px" src="{photo(s["photo"])}">'
            f'<div class="topscrim"></div><div class="fade" style="top:{h-190}px"></div>'
            f'<div class="num">{n:02d} / {tot:02d}</div><div class="pad"><div class="pbot">'
            f'<div class="rcard"><div class="rhead">'
            f'<div class="ravatar">{who[0]}</div>'
            f'<div><div class="rname">{who}</div>'
            f'<div class="rstars">&#9733;&#9733;&#9733;&#9733;&#9733;</div></div>'
            f'<div class="rgoogle">Google</div></div>'
            f'<div class="rtext" style="font-size:{quote_size(s["quote"])}px">{s["quote"]}</div></div>'
            f'<div class="rbelow"><span>4.9</span><span class="dot">&middot;</span>'
            f'<span class="sub">90 reviews on Google</span><span class="dot">&middot;</span>'
            f'<span class="sub">Since 2003</span></div>'
            f'<div class="foot"><div class="brand">balivipwedding.com</div></div></div></div></div>'
        )

    if k == "cta":
        return (
            f'<div class="slide cta">'
            f'<img class="photo-top" style="object-position:{s.get("crop","50% 50%")}" src="{photo(s["photo"])}">'
            f'<div class="fade"></div>'
            f'<div class="pad"><div class="body-wrap"><div class="eyebrow">Balivip Wedding</div>'
            f'<div class="lead" style="font-size:{72 if len(s["lead"].replace("<br>"," "))<52 else 62}px;'
            f'margin-top:28px">{segs(s["lead"])}</div>'
            f'<div class="rule"></div><div class="body">{segs(s["body"])}</div>'
            f'<div class="action">{s.get("action","WhatsApp &nbsp;&middot;&nbsp; Link in bio")}</div>'
            f'<div class="foot"><div class="brand">balivipwedding.com</div>'
            f'<div class="brand">{n} / {tot}</div></div>'
            f'</div></div></div>'
        )

    if k == "checklist":
        items = "".join(f'<li><span class="seg">{i}</span></li>' for i in s["items"])
        return (
            f'<div class="slide"><img class="ph" src="{photo(s["photo"])}">'
            f'<div class="scrim check"></div>'
            f'<div class="num low">{n:02d} / {tot:02d}</div>'
            f'<div class="pad top"><div class="body-wrap">'
            f'<div class="lead" style="font-size:{lead_size(s["lead"])}px">{segs(s["lead"])}</div>'
            f'<div class="rule"></div><ul class="checklist">{items}</ul>'
            f'<div class="foot"><div class="brand">balivipwedding.com</div></div>'
            f'</div></div></div>'
        )

    # cover and content share one shape
    trio = s.get("trio")
    if trio:
        imgs = ("".join(f'<img class="third {c}" src="{photo(i)}">' for c, i in zip("abc", trio))
                + '<div class="vline one"></div><div class="vline two"></div>'
                + '<div class="band"></div><div class="splitfade"></div>')
        scrim, cls = "", " trio"
    else:
        pos = s.get("pos") or PLACEMENT.get(s["photo"], {}).get("pos", "bottom")
        imgs = f'<img class="ph" src="{photo(s["photo"])}">'
        scrim = f'<div class="scrim{" top" if pos == "top" else ""}"></div>'
        cls = ""

    top = " top" if (not trio and (s.get("pos") or PLACEMENT.get(s.get("photo",""), {}).get("pos")) == "top") else ""

    if k == "cover":
        inner = (f'<div class="bigtitle">{s["title"]}</div>'
                 f'<div class="rule"></div>'
                 f'<div class="hook">{segs(s["hook"])}</div>')
    else:
        inner = (f'<div class="lead" style="font-size:{lead_size(s["lead"])}px">{segs(s["lead"])}</div>'
                 f'<div class="rule"></div>'
                 f'<div class="body">{segs(s["body"])}</div>')

    foot = (f'<div class="foot"><div class="brand">balivipwedding.com</div>'
            f'<div class="brand">{"Swipe" if k == "cover" else ""}</div></div>')

    return (f'<div class="slide{cls}">{imgs}{scrim}'
            f'<div class="num{" low" if top else ""}">{n:02d} / {tot:02d}</div>'
            f'<div class="pad{top}"><div class="body-wrap">{inner}{foot}</div></div></div>')


def page(inner, fmt):
    return (f"<html><head><meta charset='utf-8'><style>{css(fmt)}</style></head>"
            f"<body>{inner}</body></html>")


def build(deck_dir):
    deck_dir = deck_dir.rstrip("/")
    cfg = json.load(open(os.path.join(deck_dir, "deck.json"), encoding="utf-8"))
    fmt = cfg.get("format", "carousel")
    if fmt not in SIZES:
        sys.exit(f"unknown format '{fmt}'. Use one of: {', '.join(SIZES)}")
    slides = cfg["slides"]
    name = os.path.basename(deck_dir)
    out = os.path.join(ROOT, "build", name)
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "*.html")):
        os.remove(f)
    tot = len(slides)
    for i, s in enumerate(slides):
        html = page(slide(s, i + 1, tot, fmt), fmt)
        open(os.path.join(out, f"{i+1:02d}.html"), "w", encoding="utf-8").write(html)
    print(f"built  {name}  {tot} slides  ({fmt}, {SIZES[fmt][0]}x{SIZES[fmt][1]})")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for d in sys.argv[1:]:
        build(d)
