"""Build constituency records and compact paths from official 2025 results and geometry.
Run in src/germany/: python3 process.py (requires pyshp)."""
import csv
import io
import json
import math
import zipfile
from collections import defaultdict, Counter
import shapefile

PARTIES = ['Union', 'AfD', 'SPD', 'Greens', 'Left', 'FDP', 'BSW', 'SSW', 'Other']
KEY = {'CDU':'Union', 'CSU':'Union', 'AfD':'AfD', 'SPD':'SPD', 'GRÜNE':'Greens',
       'Die Linke':'Left', 'FDP':'FDP', 'BSW':'BSW', 'SSW':'SSW'}
# Average: last published survey of each of ARD/Infratest, INSA, Forsa, FGW, Verian and YouGov.
# BSW is not separately reported by ARD or FGW; 3.4 is the mean of the other four.
POLL = {'Union':19.5, 'AfD':27.9, 'SPD':13.6, 'Greens':15.3,
        'Left':11.2, 'FDP':4, 'BSW':3.4, 'SSW':0.2}
R = defaultdict(lambda: {'first':{},'second':{},'previous':{}})
with open('kerg2.csv', encoding='utf-8-sig') as f:
    lines = list(csv.reader(f, delimiter=';'))
for row in lines[10:]:
    if len(row) < 19 or row[2] not in ('Wahlkreis', 'Bund'): continue
    id = row[3].zfill(3) if row[2]=='Wahlkreis' else 'national'
    d = R[id]; d['name'] = row[4]; d['state'] = row[6]
    party = KEY.get(row[8], 'Other')
    if row[7]=='System-Gruppe':
        if row[8]=='Gültige' and row[10] in ('1','2'): d['valid'+row[10]]=int(row[11])
        if row[8]=='Wahlberechtigte': d['eligible']=int(row[11])
        if row[8]=='Wählende': d['voters']=int(row[11])
    elif row[7] in ('Partei','Einzelbewerber/Wählergruppe'):
        k = 'first' if row[10]=='1' else 'second'
        if row[11]: d[k][party] = d[k].get(party,0)+int(row[11])
        if k=='second' and row[13]: d['previous'][party]=d['previous'].get(party,0)+int(row[13])
nat = R['national']
base={p:round(100*nat['second'].get(p,0)/nat['valid2'],2) for p in PARTIES}
POLL['Other']=round(100-sum(POLL.values()),1)
assert len(R)==300
states={}
with zipfile.ZipFile('geometry.zip') as z:
    stem='btw25_geometrie_wahlkreise_shp_geo'
    shp=shapefile.Reader(shp=io.BytesIO(z.read(stem+'.shp')), shx=io.BytesIO(z.read(stem+'.shx')), dbf=io.BytesIO(z.read(stem+'.dbf')))
    geoms={str(sr.record.WKR_NR).zfill(3):sr for sr in shp.iterShapeRecords()}
    states={str(sr.record.LAND_NR).zfill(2):sr.record.LAND_NAME for sr in shp.iterShapeRecords()}
assert len(geoms)==299
# Equirectangular with longitude corrected for German mid-latitude, y down.
lonmin,latmin,lonmax,latmax=shp.bbox
fac=math.cos(math.radians(51)); width=630; scale=width/((lonmax-lonmin)*fac)
height=round((latmax-latmin)*scale+20)
def project(pt): return ((pt[0]-lonmin)*fac*scale+10, (latmax-pt[1])*scale+10)
def dist(p,a,b):
    dx=b[0]-a[0];dy=b[1]-a[1]
    if dx==dy==0: return math.dist(p,a)
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def simplify(points, epsilon=0.8):
    # Iterative Douglas–Peucker (input ring is opened at a stable vertex).
    keep={0,len(points)-1}; stack=[(0,len(points)-1)]
    while stack:
        i,j=stack.pop()
        if j-i<=1:continue
        k=max(range(i+1,j), key=lambda k:dist(points[k],points[i],points[j]))
        if dist(points[k],points[i],points[j])>epsilon:
            keep.add(k); stack.extend([(i,k),(k,j)])
    return [points[k] for k in sorted(keep)]
paths={}
for code,sr in geoms.items():
    sh=sr.shape; parts=list(sh.parts)+[len(sh.points)]; segments=[]
    for a,b in zip(parts,parts[1:]):
        ring=[project(p) for p in sh.points[a:b]]
        if len(ring)<4:continue
        # discard tiny islands but keep enclave rings of perceptible size
        if (max(x for x,y in ring)-min(x for x,y in ring))*(max(y for x,y in ring)-min(y for x,y in ring))<0.7:continue
        # polygon DP with two arcs avoids the degeneracy of same start/end point
        half=len(ring)//2
        pts=simplify(ring[:half+1])+simplify(ring[half:])[1:-1]
        if len(pts)<3:continue
        segments.append('M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'Z')
    paths[code]=''.join(segments)
assert all(paths.values())
rows=[]
for code in sorted(geoms):
    d=R[code]; assert 'valid1' in d and 'valid2' in d,code
    def shares(k,denom): return [round(100*d[k].get(p,0)/denom,1) for p in PARTIES]
    previous_total=sum(d['previous'].values())
    first=shares('first',d['valid1']);second=shares('second',d['valid2'])
    previous=shares('previous',previous_total)
    winner=PARTIES[max(range(len(first)),key=lambda i:first[i])]
    # Only flags direct candidacies for major parties. 'Other' collects smaller candidates.
    rows.append({'c':code,'n':d['name'],'r':d['state'],'e':d['eligible'],'v':d['valid2'],
                 't':round(100*d['voters']/d['eligible'],1),
                 'f':first,'s':second,'p':previous,'w':winner})
out={'parties':PARTIES,'states':states,'base':base,'poll':POLL,'rows':rows}
with open('data.json','w') as f:json.dump(out,f,ensure_ascii=False,separators=(',',':'))
with open('paths.json','w') as f:json.dump({'w':width+20,'h':height,'paths':paths},f,separators=(',',':'))
print('bytes data/geo:',len(open('data.json').read().encode()),len(open('paths.json').read().encode()))
print('2025 first winners',Counter(d['w'] for d in rows))
print('national base',base,'poll',POLL)
print('missing 2021 sums',[(x['c'],sum(x['p'])) for x in rows if sum(x['p'])<98][:8])
