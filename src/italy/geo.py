"""Equirectangular regional SVG paths simplified in screen coordinates (RDP)."""
import json, math
from pathlib import Path
root=Path(__file__).parent
features=json.loads((root/'regions.geojson').read_text())['features']
k=math.cos(math.radians(42.5))
project=lambda p:(p[0]*k,-p[1])
def polygons(f):
    c=f['geometry']['coordinates']
    return [c] if f['geometry']['type']=='Polygon' else c
points=[project(p) for f in features for poly in polygons(f) for ring in poly for p in ring]
minx=min(p[0] for p in points); maxx=max(p[0] for p in points)
miny=min(p[1] for p in points); maxy=max(p[1] for p in points)
scale=590/(maxx-minx)
w=610; h=round((maxy-miny)*scale+20)
def xy(p):
 x,y=project(p);return ((x-minx)*scale+10,(y-miny)*scale+10)
def rdp(pts,eps):
 if len(pts)<3:return pts
 a,b=pts[0],pts[-1]; dx,dy=b[0]-a[0],b[1]-a[1]; ll=math.hypot(dx,dy) or 1e-8
 distances=[abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/ll for p in pts[1:-1]]
 if not distances or max(distances)<=eps:return [a,b]
 i=1+distances.index(max(distances))
 return rdp(pts[:i+1],eps)[:-1]+rdp(pts[i:],eps)
paths={}
for f in features:
 d=''
 for poly in polygons(f):
  for ring in poly:
   pts=list(map(xy,ring));
   # Ignore very small uninhabited islets at this scale.
   if (max(p[0] for p in pts)-min(p[0] for p in pts))*(max(p[1] for p in pts)-min(p[1] for p in pts))<2:continue
   mid=len(pts)//2
   r=rdp(pts[:mid+1],0.7)[:-1]+rdp(pts[mid:],0.7)
   if len(r)<4:continue
   d+='M'+'L'.join(f'{p[0]:.1f} {p[1]:.1f}' for p in r[:-1])+'Z'
 paths[f['properties']['reg_istat_code']]=d
assert len(paths)==20 and all(paths.values())
(root/'paths.json').write_text(json.dumps({'w':w,'h':h,'paths':paths},separators=(',',':')))
print('geometry bytes', (root/'paths.json').stat().st_size,'height',h)
