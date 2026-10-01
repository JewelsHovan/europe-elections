"""Build a single offline page, including a no-JavaScript 2023 map."""
import json, html
from pathlib import Path
h=Path(__file__).parent
rows=json.loads((h/'data.json').read_text());geo=json.loads((h/'paths.json').read_text())
colors={'PP':'#4b94ce','PSOE':'#d54d4a','Vox':'#569d64','SUMAR':'#b668a9','ERC':'#dda450','Junts':'#e9c66f','EH Bildu':'#87b09d','EAJ-PNV':'#96af93','BNG':'#8ab2be','CCa':'#e2bd68','UPN':'#74a0d5'}
by={d['c']:d for d in rows}
static='' 
for c,path in geo['paths'].items():
    d=by[c];static+=f'<path d="{path}" fill="{colors.get(d["w"],"#888b94")}" stroke="#1a1d23" stroke-width="0.9"><title>{html.escape(d["n"])}: {html.escape(d["w"])} leads; {d["m"]} seat(s)</title></path>'
for text,x,y in [('Canary Islands (inset)',42,455),('Ceuta',299,507),('Melilla',365,507)]:static+=f'<text x="{x}" y="{y}" fill="#c4c9d0" font-size="12">{text}</text>'

body=(h/'body.html').read_text().replace('%%STYLE%%',(h.parent/'shared/base.css').read_text()+(h/'extra.css').read_text())
# The fallback is already present when scripts do not run; the client replaces this SVG on load.
body=body.replace('%%STATIC_MAP%%',static).replace('%%DATA%%',(h/'data.json').read_text()).replace('%%GEO%%',(h/'paths.json').read_text()).replace('%%JS%%',(h/'map.js').read_text())
out=h.parent.parent/'spain/index.html';out.write_text(body);print(out,len(body.encode()),'bytes')
