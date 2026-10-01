"""Build 2024 Westminster records and simplified SVG paths from official CSV / ONS BUC GeoJSON.
Run from src/uk with python3 prepare.py; no third-party dependencies.
"""
import csv, json, math, collections
from pathlib import Path
P=Path(__file__).parent
rows=list(csv.DictReader((P/'candidacies.csv').open(encoding='utf-8-sig')))
groups=collections.defaultdict(list)
for r in rows: groups[r['Constituency geographic code']].append(r)
assert len(groups)==650
alias={'Lab':'Labour','Con':'Conservative','LD':'Lib Dem','RUK':'Reform UK','SNP':'SNP','PC':'Plaid Cymru','Green':'Green','DUP':'DUP','SF':'Sinn Féin','SDLP':'SDLP','APNI':'Alliance','UUP':'UUP','TUV':'TUV'}
print('abbreviations', collections.Counter((r['Main party abbreviation'],r['Main party name']) for r in rows).most_common(28))
units=[]
for code, rr in groups.items():
    rr.sort(key=lambda r:int(r['Candidate result position'] or 999))
    a=rr[0]; valid=int(a['Election valid vote count']); region=a['English region name'] or a['Country name']; country=a['Country name']
    votes=collections.Counter(); changes={}; candidates=[]
    for r in rr:
        k=alias.get(r['Main party abbreviation'], 'Independent' if r['Candidate is standing as independent']=='true' else (r['Main party name'] or 'Other'))
        v=int(r['Candidate vote count'] or 0); votes[k]+=v
        candidates.append([r['Candidate given name']+' '+r['Candidate family name'],k,v])
        if r['Candidate vote change'] and k not in changes: changes[k]=round(100*float(r['Candidate vote change']),1)
    winner=alias.get(a['Main party abbreviation'], 'Independent' if a['Candidate is standing as independent']=='true' else (a['Main party name'] or 'Other'))
    units.append({'c':code,'n':a['Constituency name'],'r':region,'country':country,'valid':valid,'elect':int(a['Electorate']),'winner':winner,'margin':round(100*(int(rr[0]['Candidate vote count'])-int(rr[1]['Candidate vote count']))/valid,1),'votes':dict(votes),'change':changes,'candidates':candidates})
units.sort(key=lambda d:d['n'])
print('seat counts',collections.Counter(d['winner'] for d in units))
print('nation counts',collections.Counter(d['country'] for d in units))
major=['Labour','Conservative','Reform UK','Lib Dem','Green','SNP','Plaid Cymru']
gb=[d for d in units if d['country']!='Northern Ireland']; denominator=sum(d['valid'] for d in gb)
nat={k:round(100*sum(d['votes'].get(k,0) for d in gb)/denominator,3) for k in major}
print('GB baseline',nat)
# Keep every candidacy for full detail, small compressed keys in output.
slim=[]
for d in units:
    slim.append({'c':d['c'],'n':d['n'],'r':d['r'],'t':d['country'],'v':d['valid'],'e':d['elect'],'w':d['winner'],'m':d['margin'],
                 'a':[[party,votes] for name,party,votes in d['candidates']],
                 'person':d['candidates'][0][0], 'h':d['change'].get('Labour')})
(P/'data.json').write_text(json.dumps({'nat':nat,'units':slim},ensure_ascii=False,separators=(',',':')))
geo=json.loads((P/'boundaries.geojson').read_text()); assert len(geo['features'])==650
# BNG EPSG:27700 coordinates already planar, north-up. Small western isles kept in geographic position.
allpts=[p for f in geo['features'] for poly in ([f['geometry']['coordinates']] if f['geometry']['type']=='Polygon' else f['geometry']['coordinates']) for ring in poly for p in ring]
xmin=min(p[0] for p in allpts); xmax=max(p[0] for p in allpts); ymin=min(p[1] for p in allpts); ymax=max(p[1] for p in allpts)
W=690; scale=W/(xmax-xmin); H=round((ymax-ymin)*scale+20)
def point(p): return ((p[0]-xmin)*scale+10,(ymax-p[1])*scale+10)
def dp(pts,eps):
    if len(pts)<3:return pts
    a,b=pts[0],pts[-1]; dx=b[0]-a[0];dy=b[1]-a[1]; length=math.hypot(dx,dy) or 1
    j,maximum=max(enumerate(pts[1:-1],1),key=lambda q:abs(dy*q[1][0]-dx*q[1][1]+b[0]*a[1]-b[1]*a[0])/length)
    dist=abs(dy*maximum[0]-dx*maximum[1]+b[0]*a[1]-b[1]*a[0])/length
    if dist<=eps:return [a,b]
    return dp(pts[:j+1],eps)[:-1]+dp(pts[j:],eps)
paths={}
for f in geo['features']:
    polys=[f['geometry']['coordinates']] if f['geometry']['type']=='Polygon' else f['geometry']['coordinates']
    chunks=[]
    for poly in polys:
        for ring in poly:
            xy=list(map(point,ring)); mid=len(xy)//2
            reduced=dp(xy[:mid+1],1.3)[:-1]+dp(xy[mid:],1.3)
            # Leave a tiny shape visible even when simplification collapses it.
            if len(reduced)<4:
                reduced=xy if len(xy)<7 else [xy[i] for i in (0,len(xy)//4,len(xy)//2,3*len(xy)//4,len(xy)-1)]
            chunks.append('M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in reduced[:-1])+'Z')
    paths[f['properties']['PCON24CD']]=''.join(chunks)
assert set(paths)==set(groups)
(P/'paths.json').write_text(json.dumps({'w':W+20,'h':H,'paths':paths},separators=(',',':')))
print('data / geometry bytes', (P/'data.json').stat().st_size,(P/'paths.json').stat().st_size,'canvas',W+20,H)
