"""Build a fully inlined country page, including a non-JS default SVG map."""
from pathlib import Path
import json,html
P=Path(__file__).parent
D=json.loads((P/'data.json').read_text()); G=json.loads((P/'paths.json').read_text())
colors={'Labour':'#dc4949','Conservative':'#4c84d8','Reform UK':'#48a7bd','Lib Dem':'#e9ac50','Green':'#55ad67','SNP':'#f4d469','Plaid Cymru':'#71b08a','DUP':'#ca793d','Sinn Féin':'#378c65','SDLP':'#ba6776','Alliance':'#dfbb62','UUP':'#519ac2','TUV':'#724ea4','Independent':'#888b98','Other':'#888b98'}
base={'Labour':26.5,'Conservative':19.75,'Reform UK':23.5,'Lib Dem':11,'Green':9.25,'SNP':2,'Plaid Cymru':1}
def winner(d):
    v={}
    for k,n in d['a']:v[k]=max(v.get(k,0),100*n/d['v']) if k=='Independent' else v.get(k,0)+100*n/d['v']
    if d['t']!='Northern Ireland':
        for k,s in base.items():v[k]=max(0,v.get(k,0)+s-D['nat'][k])
    return max(v,key=v.get)
paths=''.join(f'<path data-code="{d["c"]}" d="{G["paths"][d["c"]]}" fill="{colors.get(winner(d),colors["Other"])}"><title>{html.escape(d["n"])}: {html.escape(winner(d))}</title></path>' for d in D['units'])
fallback=f'<svg id="map" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {G["w"]} {G["h"]}" role="img" aria-label="Static map of projected constituency winners">{paths}</svg>'
body=(P/'body.html').read_text();basecss=(P/'../shared/base.css').read_text();extra=(P/'extra.css').read_text()
body=body.replace('%%STYLE%%',basecss+extra).replace('%%FALLBACK%%',fallback).replace('%%DATA%%',(P/'data.json').read_text().replace('</','<\\/')).replace('%%JS%%',(P/'map.js').read_text())
out=P/'../../uk/index.html';out.write_text(body)
print(out.resolve(),out.stat().st_size,'bytes')
