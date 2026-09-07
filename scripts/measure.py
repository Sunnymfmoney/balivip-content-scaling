"""Measures candidate copy against the real fonts, so line breaks are decided by pixels."""
import asyncio, json, os, sys
from playwright.async_api import async_playwright
CSS = open("css.txt").read().replace("{{","{").replace("}}","}").replace(
    "{FONTS}", "/Users/sunnymfmoney/.claude/skills/balivip-wedding-design/fonts")

async def widths(items):
    html = "<html><head><meta charset='utf-8'><style>%s</style></head><body>" % CSS
    html += "<div class='slide'><div class='pad'><div class='body-wrap'>"
    for i,(t,cls,size) in enumerate(items):
        st = f"font-size:{size}px;" if size else ""
        html += f"<div class='{cls}' style='{st}white-space:nowrap;display:inline-block' id='m{i}'>{t}</div><br>"
    html += "</div></div></div></body></html>"
    open("/tmp/_m.html","w").write(html)
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome")
        pg = await b.new_page(viewport={"width":3000,"height":1350})
        await pg.goto("file:///tmp/_m.html"); await pg.wait_for_timeout(250)
        out = await pg.evaluate("""(n) => Array.from({length:n},(_,i)=>
            Math.round(document.getElementById('m'+i).getBoundingClientRect().width))""", len(items))
        await b.close()
    return out

if __name__ == "__main__":
    items = json.load(open(sys.argv[1]))
    for (t,cls,size), w in zip(items, asyncio.run(widths(items))):
        flag = "OVER" if w > 840 else "ok  "
        print(f"{flag} {w:4}px  {cls}{'/'+str(size) if size else ''}  {t}")
