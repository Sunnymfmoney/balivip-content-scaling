#!/usr/bin/env python3
"""
Prove every authored line renders on exactly one line. No orphans, no guessing.

    python3 scripts/fit.py build/venue-myths

A wrapped line means the copy is too long for its type size. Shorten it, or move
the <br>. Run scripts/build.py first.
"""
import asyncio, glob, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = {"carousel": (1080, 1350), "story": (1080, 1920), "reel": (1080, 1920)}


def fmt_of(build_dir):
    name = os.path.basename(build_dir.rstrip("/"))
    for kind in ("carousels", "stories", "reels"):
        p = os.path.join(ROOT, "content", kind, name, "deck.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8")).get("format", "carousel")
    return "carousel"


async def main(dirs):
    from playwright.async_api import async_playwright
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        for d in dirs:
            files = sorted(glob.glob(os.path.join(d, "*.html")))
            if not files:
                print(f"  nothing built in {d}")
                continue
            w, h = SIZES[fmt_of(d)]
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            for f in files:
                await pg.goto("file://" + os.path.abspath(f))
                await pg.wait_for_timeout(200)
                rows = await pg.evaluate("""() => [...document.querySelectorAll('.seg')].map(e => {
                    const r = e.getClientRects();
                    const last = r[r.length-1];
                    return {t: e.textContent, n: r.length,
                            cls: e.parentElement.className.split(' ')[0],
                            tail: r.length > 1 ? Math.round(last.width) : 0};
                })""")
                for r in rows:
                    if r["n"] > 1:
                        bad.append((os.path.basename(d), os.path.basename(f).replace(".html", ""),
                                    r["cls"], r["n"], r["tail"], r["t"]))
            await pg.close()
        await b.close()

    for deck, slide, cls, n, tail, t in bad:
        print(f"WRAP  {deck}/{slide}  {cls:9} {n} lines, last {tail}px  |  {t}")
    print("=" * 70)
    print("PASS  every authored line fits one rendered line" if not bad
          else f"FAIL  {len(bad)} lines wrap")
    return 1 if bad else 0


if __name__ == "__main__":
    dirs = sys.argv[1:] or sorted(d for d in glob.glob(os.path.join(ROOT, "build", "*")) if os.path.isdir(d))
    if not dirs:
        sys.exit("nothing built yet. Run scripts/build.py first.")
    sys.exit(asyncio.run(main(dirs)))
