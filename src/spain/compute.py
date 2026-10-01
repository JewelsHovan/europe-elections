"""Turn the archived provincial CSV into reproducible constituency records.
Source reproduces Interior Ministry/JEC reports; 2023 provisional, 2019 definitive.
Run from src/spain: python3 compute.py && python3 geo.py && python3 build.py.
"""
import csv, html, json, collections
from pathlib import Path

HERE=Path(__file__).parent
geo=json.loads((HERE/'provinces.geojson').read_text())
names={f['properties']['cod_prov']:f['properties']['name'] for f in geo['features']}
cc_names=['Andalusia','Aragon','Asturias','Balearic Islands','Canary Islands','Cantabria','Castile–La Mancha','Castile and León','Catalonia','Extremadura','Galicia','Madrid','Navarre','Basque Country','Murcia','La Rioja','Valencian Community','Ceuta','Melilla']
# The geometry's cod_ccaa is NOT the electoral CSV's region code; use CSV's province rows.
def read(year):
    out=collections.defaultdict(lambda:{'votes':{},'seats':{},'valid':0,'blank':0,'region':''})
    for row in csv.reader((HERE/f'results{year}.csv').open()):
        region,code,_,name,votes,*rest=row
        if not code or (year==2019 and (len(rest)<3 or rest[-1]!='B')): continue
        d=out[code];d['region']=cc_names[int(region)-1]
        name=html.unescape(name)
        n=int(votes)
        if name=='Válidos': d['valid']=n
        elif name=='Blancos': d['blank']=n
        elif name not in ('Censo','Votantes','Nulos'):
            # Codes in final parentheses identify list consistently across provinces.
            code_name=name.rsplit('(',1)[-1].rstrip(')') if '(' in name else name
            if code_name=='VOX': code_name='Vox'
            if code_name in ('PSC-PSOE','PSE-EE/PSOE','PSdeG-PSOE'):code_name='PSOE'
            if code_name.startswith('SUMAR'):code_name='SUMAR'
            if code_name.startswith('PODEMOS') or code_name in ('ECP','UP'):code_name='UP'
            if code_name.startswith('ERC-'):code_name='ERC'
            if code_name=='JUNTS' or code_name=='JxCAT-JUNTS':code_name='Junts'
            if code_name=='CCa-PNC':code_name='CCa'
            d['votes'][code_name]=n
            d['seats'][code_name]=int(rest[1]) if len(rest)>1 and rest[1] else 0
    return out

a=read(2023); b=read(2019)
assert len(a)==len(b)==52
assert sum(sum(d['seats'].values()) for d in a.values())==350

def alloc(v,valid,seats,code):
    # The 3% threshold is of ALL valid votes, including blank ballots.
    if seats==1: return {max(v,key=v.get):1} # Ceuta & Melilla plurality
    qs=sorted(((n / k, p) for p,n in v.items() if n>=.03*valid for k in range(1,seats+1)),reverse=True)
    c=collections.Counter(p for q,p in qs[:seats]);return dict(c)

rows=[]
for code,d in sorted(a.items()):
    s=sum(d['seats'].values()); got=alloc(d['votes'],d['valid'],s,code)
    if got!={p:v for p,v in d['seats'].items() if v}:print('mismatch',code,got,d['seats'])
    assert got=={p:v for p,v in d['seats'].items() if v}
    v=d['votes']; prev=b[code]['votes']; v19=b[code]['valid']
    rows.append(dict(c=code,n=names[code],r=d['region'],m=s,valid=d['valid'],blank=d['blank'],v=v,s=got,
                     p19={p:round(prev.get(p,0)/v19*100,2) for p in ['PP','PSOE','Vox','UP']},
                     w=max(v,key=v.get)))
(HERE/'data.json').write_text(json.dumps(rows,ensure_ascii=False,separators=(',',':')))
print('2023 seats:',dict(collections.Counter({p:sum(d['s'].get(p,0) for d in rows) for p in set(p for d in rows for p in d['s'])})))
print('2023 provinces:',len(rows))
