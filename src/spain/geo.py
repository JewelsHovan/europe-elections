"""Simplify WGS84 province polygons into small SVG paths; Canary Islands use an inset."""
import json,math
from pathlib import Path
h=Path(__file__).parent
features=json.loads((h/'provinces.geojson').read_text())['features']
def xy(p,island):
    lon,lat=p
    return (45+(lon+18.3)*43, 466+(29.5-lat)*35) if island else (26+(lon+9.6)*49, 18+(44-lat)*51)
def dist(p,a,b):
    dx=b[0]-a[0];dy=b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))) if dx*dx+dy*dy else 0
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def simplify(p,eps=.85):
    if len(p)<4:return p
    a,b=p[0],p[-1];i=max(range(1,len(p)-1),key=lambda i:dist(p[i],a,b));d=dist(p[i],a,b)
    if d<=eps:return [a,b]
    return simplify(p[:i+1],eps)[:-1]+simplify(p[i:],eps)
paths={}
for f in features:
    c=f['properties']['cod_prov'];island=c in ('35','38')
    if c in ('51','52'):continue # magnified labelled constituency tiles below map
    geom=f['geometry'];polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
    chunks=[]
    for poly in polys:
        for ring in poly:
            pts=[xy(p,island) for p in ring]
            # Very small remote islets are retained if they occupy at least ~1px.
            if max(p[0] for p in pts)-min(p[0] for p in pts)<.8 and max(p[1] for p in pts)-min(p[1] for p in pts)<.8:continue
            # rotate closed ring to avoid equal start/end RDP degeneracy
            pts=pts[:-1]; k=min(range(len(pts)),key=lambda i:pts[i][0]);pts=pts[k:]+pts[:k];pts.append(pts[0]);
            # split closed outline into two halves so its endpoints differ
            mid=len(pts)//2
            q=simplify(pts[:mid+1])+simplify(pts[mid:])[1:]
            chunks.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y in q)+'Z')
    paths[c]=''.join(chunks)
paths['51']='M302,513h24v23h-24Z'
paths['52']='M370,513h24v23h-24Z'
(h/'paths.json').write_text(json.dumps({'w':770,'h':550,'paths':paths},separators=(',',':')))
print('SVG paths',len(paths),(h/'paths.json').stat().st_size)
