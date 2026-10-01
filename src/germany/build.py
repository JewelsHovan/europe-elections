"""Run from src/germany: python3 process.py && python3 build.py."""
import html
import json
from pathlib import Path
here=Path(__file__).resolve().parent
base=(here/'../shared/base.css').read_text()
extra=(here/'extra.css').read_text()
body=(here/'body.html').read_text()
js=(here/'map.js').read_text()
data=(here/'data.json').read_text()
geo=(here/'paths.json').read_text()
D=json.loads(data);G=json.loads(geo)
colors={'Union':'#373f54','AfD':'#4654a5','SPD':'#c65856','Greens':'#429273','Left':'#9a6aba','FDP':'#d5a64b','BSW':'#b35d77','SSW':'#55a9ae','Other':'#818793'}
parties=D['parties']
def winner(d):
    v=[]
    for p,old in zip(parties,d['f']):
        v.append(max(0,old+D['poll'][p]-D['base'][p]) if old and p!='Other' else old)
    return parties[max(range(len(v)),key=lambda i:v[i])]
paths=''.join(f'<path d="{G["paths"][d["c"]]}" fill="{colors[winner(d)]}" stroke="var(--surface)" stroke-width=".7" fill-rule="evenodd"><title>{html.escape(d["c"]+" "+d["n"])}</title></path>' for d in D['rows'])
legend=''.join(f'<span><i class="sw" style="background:{colors[p]}"></i>{p}</span>' for p in parties[:-1])
static=f'<div class="static-only"><svg viewBox="0 0 {G["w"]} {G["h"]}" role="img" aria-label="Modelled 2026 first-vote leader in Germany’s 299 Bundestag constituencies, at AfD {D["poll"]["AfD"]} percent nationally">{paths}</svg><div class="static-legend">{legend}</div><p class="static-note">Static view: projected first-vote leads at the six-poll average, AfD {D["poll"]["AfD"]}%. Local leads are not seats. Open in a browser for interactive layers.</p></div>'
page=(body.replace('%%STYLE%%',base+'\n'+extra).replace('%%STATIC%%',static).replace('%%DATA%%',data).replace('%%GEO%%',geo).replace('%%JS%%',js))
assert '%%' not in page
out=here/'../../germany/index.html';out.write_text(page)
print(out.resolve(),len(page.encode()),'bytes')
