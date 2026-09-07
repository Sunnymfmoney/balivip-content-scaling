#!/usr/bin/env python3
"""
Turn built HTML into PNGs.

    python3 scripts/render.py build/how-not-to-plan

Writes NN.png beside each NN.html. Run scripts/build.py first.
"""
import asyncio, glob, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = {"carousel": (1080, 1350), "story": (1080, 1920), "reel": (1080, 1920)}


def fmt_of(build_dir):
    """Read the format back from the deck that produced this build."""
    name = os.path.basename(build_dir.rstrip("/"))
    for kind in ("carousels", "stories", "reels"):
        p = os.path.join(ROOT, "content", kind, name, "deck.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8")).get("format", "carousel")
    return "carousel"


async def main(dirs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        total = 0
        for d in dirs:
            files = sorted(glob.glob(os.path.join(d, "*.html")))
            if not files:
                print(f"  nothing to render in {d}")
                continue
            w, h = SIZES[fmt_of(d)]
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            for f in files:
                await pg.goto("file://" + os.path.abspath(f))
                # let the webfonts settle, otherwise the first slide renders in fallback type
                await pg.wait_for_timeout(320)
                await pg.screenshot(path=f.replace(".html", ".png"))
            await pg.close()
            print(f"rendered  {os.path.basename(d)}  {len(files)} slides at {w}x{h}")
            total += len(files)
        await b.close()
        return total


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1:]))
