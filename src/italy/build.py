"""Build standalone Italy page. Run from any directory with python3 src/italy/build.py."""
from pathlib import Path
import json, html
root=Path(__file__).parent
repo=root.parent.parent
data=json.loads((root/'data.json').read_text());geo=json.loads((root/'paths.json').read_text())
by={d['c']:d for d in data}
def color(d):
 if d.get('special'):return '#817d86'
 gap=(d['cd']+41-43.8)-(d['cs']+d['m5']+43.6-41.6)
 return '#1f3f7a' if gap>8 else '#3f68b0' if gap>4 else '#9db6e0' if gap>0 else '#efa79e' if gap>-4 else '#d05a4e' if gap>-8 else '#932a22'
svg=''.join(f'<path data-c="{c}" d="{path}" fill="{color(by[c])}"><title>{html.escape(by[c]["n"])}: {"separate ballot" if by[c].get("special") else "right " + str(by[c]["cd"]) + "%, centre-left " + str(by[c]["cs"]) + "%, M5S " + str(by[c]["m5"]) + "%"}</title></path>' for c,path in geo['paths'].items())
rows=''.join(f'<tr><td>{html.escape(d["n"])}</td><td>{d["actual"]} +{d["am"]:.1f}</td><td class="num">{d["cd"]:.1f}%</td><td class="num">{"n/a" if d.get("special") else f"{d["cs"]+d["m5"]:.1f}%"}</td><td class="num">{"n/a" if d.get("special") else f"+{d["cd"]-d["cd18"]:.1f} pts"}</td><td class="num">see interactive map</td></tr>' for d in data)
body=(root/'body.html').read_text()
for key,value in {'%%STYLE%%':(repo/'src/shared/base.css').read_text()+(root/'extra.css').read_text(),'%%DATA%%':(root/'data.json').read_text(),'%%GEO%%':(root/'paths.json').read_text(),'%%JS%%':(root/'map.js').read_text(),'%%SVG%%':svg,'%%ROWS%%':rows,'%%W%%':str(geo['w']),'%%H%%':str(geo['h'])}.items():body=body.replace(key,value)
assert '%%' not in body and '<path ' in body and '<script>' in body
out=repo/'italy/index.html';out.write_text(body);print(out, out.stat().st_size,'bytes')
