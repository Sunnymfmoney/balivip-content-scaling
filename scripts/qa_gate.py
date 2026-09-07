#!/usr/bin/env python3
"""
Block anything that must not be published.

    python3 scripts/qa_gate.py content/carousels/how-not-to-plan-a-destination-wedding

Exit code 1 means do not post. Every rule here exists because the claim it blocks
already went out once and had to be pulled.
"""
import os, sys, json, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = {"carousel": (1080, 1350), "story": (1080, 1920), "reel": (1080, 1920)}

BANNED = json.load(open(os.path.join(ROOT, "reference", "banned-claims.json"), encoding="utf-8"))


def text_of(deck):
    """Every word that will be visible on a slide."""
    out = []
    for s in deck["slides"]:
        for f in ("title", "hook", "lead", "body", "quote", "who", "action"):
            if f in s:
                out.append(str(s[f]))
        for i in s.get("items", []):
            out.append(str(i))
    return "\n".join(out).replace("<br>", " ")


def check(deck_dir):
    deck_dir = deck_dir.rstrip("/")
    name = os.path.basename(deck_dir)
    deck = json.load(open(os.path.join(deck_dir, "deck.json"), encoding="utf-8"))
    fails, warns = [], []
    copy = text_of(deck)

    # 1. Claims that must never ship.
    for pat, why in BANNED.items():
        m = re.search(pat, copy, re.I)
        if m:
            fails.append(f"BANNED CLAIM  \"{m.group(0)}\"  {why}")

    # 2. No em dashes. Brand rule, no exceptions.
    if "—" in copy:
        fails.append("EM DASH  found an em dash. Use a comma, a full stop, or rewrite.")

    # 3. A review must be reproduced word for word, so it can be checked against Google.
    for i, s in enumerate(deck["slides"], 1):
        if s.get("kind") == "review":
            if "..." in s.get("quote", "") and not s.get("elision_is_in_source"):
                fails.append(
                    f"REVIEW TRIMMED  slide {i}, {s.get('who','?')}. A review is quoted "
                    f"verbatim or not at all. If the source review really does contain an "
                    f"ellipsis, set \"elision_is_in_source\": true on that slide."
                )
            if not s.get("who"):
                fails.append(f"REVIEW  slide {i} has no attributed name.")

    # 4. Every deck ends on one ask.
    if deck["slides"] and deck["slides"][-1].get("kind") != "cta":
        warns.append("the last slide is not a CTA, so the deck does not ask for anything")

    # 5. Rendered files, if they exist, must be the right shape.
    build = os.path.join(ROOT, "build", name)
    pngs = sorted(glob.glob(os.path.join(build, "*.png")))
    if pngs:
        want = SIZES[deck.get("format", "carousel")]
        if len(pngs) != len(deck["slides"]):
            fails.append(f"RENDER  {len(deck['slides'])} slides in deck.json, {len(pngs)} PNGs on disk")
        try:
            from PIL import Image
            for p in pngs:
                if Image.open(p).size != want:
                    fails.append(f"RENDER  {os.path.basename(p)} is not {want[0]}x{want[1]}")
        except ImportError:
            warns.append("Pillow not installed, skipped the image size check")
    else:
        warns.append("no PNGs yet, copy checked but nothing rendered")

    print("=" * 62)
    print(f"  {name}  ({deck.get('format','carousel')}, {len(deck['slides'])} slides)")
    for w in warns:
        print(f"  warn  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    print("  PASS  nothing blocking" if not fails else "  DO NOT POST")
    print("=" * 62)
    return 1 if fails else 0


if __name__ == "__main__":
    targets = sys.argv[1:]
    if not targets:
        targets = sorted(glob.glob(os.path.join(ROOT, "content", "*", "*")))
    sys.exit(max(check(t) for t in targets) if targets else 0)
