#!/usr/bin/env python3
"""
Scaffold a new deck.

    python3 scripts/new_deck.py venue-myths carousel
"""
import os, sys, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = {"carousel": "carousels", "story": "stories", "reel": "reels"}

TEMPLATE = {
    "carousel": [
        {"kind": "cover", "photo": "INT07",
         "title": "Your hook<br>goes here.", "hook": "One sentence that earns the swipe."},
        {"kind": "review", "photo": "PRF1", "who": "Mega Septiandara",
         "quote": "We were able to just be fully present and enjoy every moment knowing we were in great hands."},
        {"kind": "content", "photo": "INT04",
         "lead": "One idea per slide.", "body": "The detail underneath.<br>Two or three lines, no more."},
        {"kind": "cta", "photo": "INI12", "crop": "50% 18%",
         "lead": "One ask.", "action": "WhatsApp us now",
         "body": "Name what they get<br>and when they get it."},
    ],
    "story": [
        {"kind": "cover", "photo": "INT04",
         "title": "Stop the<br>scroll.", "hook": "One line."},
        {"kind": "content", "photo": "INI10",
         "lead": "Teach one thing.", "body": "Keep it to two lines on a story.<br>People are moving fast."},
        {"kind": "cta", "photo": "INI12", "crop": "50% 18%",
         "lead": "One ask.", "action": "Reply to this story",
         "body": "What they get, and when."},
    ],
}
TEMPLATE["reel"] = TEMPLATE["story"]


def main(name, kind):
    if kind not in FOLDER:
        sys.exit(f"KIND must be one of: {', '.join(FOLDER)}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        sys.exit("NAME must be lower case letters, numbers and hyphens, e.g. venue-myths")

    d = os.path.join(ROOT, "content", FOLDER[kind], name)
    if os.path.exists(os.path.join(d, "deck.json")):
        sys.exit(f"{name} already exists at content/{FOLDER[kind]}/{name}")
    os.makedirs(d, exist_ok=True)

    deck = {
        "title": name.replace("-", " ").title(),
        "format": kind,
        "note": "Cover, proof, the argument, one ask. Read CLAUDE.md before writing.",
        "slides": TEMPLATE[kind],
    }
    json.dump(deck, open(os.path.join(d, "deck.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print(f"\n  created  content/{FOLDER[kind]}/{name}/deck.json")
    print(f"  edit it, then run:  make {name}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "carousel")
