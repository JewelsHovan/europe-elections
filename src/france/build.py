import json
base = open("../shared/base.css").read()
extra = open("extra.css").read()
body = open("body.filled.html").read()
js = open("map.js").read()
data = open("data.json").read()
geo = open("paths.json").read()
import math
D = json.loads(data); G = json.loads(geo)
lg = lambda p: math.log(p / (1 - p)); ex = lambda x: 1 / (1 + math.exp(-x))
R = [(60, "#1c2868", "Safe RN (60+)"), (55, "#3d4fa1", "Likely RN (55–60)"), (52, "#8d9bd6", "Lean RN (52–55)"), (48, "#b8b1a2", "Toss-up (48–52)"), (45, "#efc77a", "Lean Philippe (45–48)"), (40, "#d98f2b", "Likely Philippe (40–45)"), (-1, "#9a5a0c", "Safe Philippe (under 40)")]
col = {}
for d in D["deps"]:
    v = 100 * ex(lg(0.56) + d["lean"])
    col[d["c"]] = next(r[1] for r in R if v >= r[0])
paths = "".join(f'<path d="{p}" fill="{col[c]}" stroke="#fff" stroke-width="0.5"/>' for c, p in G["paths"].items())
legend = "".join(f'<span><span class="sw" style="background:{r[1]}"></span>{r[2]}</span>' for r in R)
static = (f'<div class="static-only"><svg viewBox="0 0 {G["w"]} {G["h"]}" role="img" aria-label="Projected runoff, Le Pen vs Philippe at 56% nationally">{paths}</svg>'
          f'<div id="legend-static" style="display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;margin-top:8px">{legend}</div>'
          '<p class="static-note">Static view: projected runoff, Le Pen vs Philippe at 56% nationally. Open the page in a browser for the interactive map.</p></div>')
html = body.replace("%%STATIC%%", static).replace("%%STYLE%%", base + extra).replace("%%DATA%%", data).replace("%%GEO%%", geo).replace("%%JS%%", js)
open("../../france/index.html", "w").write(html)
print(len(html.encode()), "bytes")
