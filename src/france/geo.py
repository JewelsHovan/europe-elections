import json, math
g=json.load(open('dep.geojson'))
k=math.cos(math.radians(46.5))
def proj(p): return ((p[0]+5.3)*k, (51.2-p[1]))
pts=[proj(p) for f in g['features'] for poly in ([f['geometry']['coordinates']] if f['geometry']['type']=='Polygon' else f['geometry']['coordinates']) for ring in poly for p in ring]
minx=min(p[0] for p in pts); maxx=max(p[0] for p in pts); miny=min(p[1] for p in pts); maxy=max(p[1] for p in pts)
W=560; s=W/(maxx-minx); H=(maxy-miny)*s
print('W,H',W,H)
def dp(pl,eps):
    if len(pl)<3: return pl
    a,b=pl[0],pl[-1]; dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy) or 1e-9
    i,dm=0,0
    for j in range(1,len(pl)-1):
        d=abs(dy*pl[j][0]-dx*pl[j][1]+b[0]*a[1]-b[1]*a[0])/L
        if d>dm: i,dm=j,d
    if dm>eps: return dp(pl[:i+1],eps)[:-1]+dp(pl[i:],eps)
    return [a,b]
paths={}; n=0
for f in g['features']:
    polys=[f['geometry']['coordinates']] if f['geometry']['type']=='Polygon' else f['geometry']['coordinates']
    d=''
    for poly in polys:
        for ring in poly:
            xy=[((proj(p)[0]-minx)*s+10,(proj(p)[1]-miny)*s+10) for p in ring]
            h=len(xy)//2
            r=dp(xy[:h+1],0.6)[:-1]+dp(xy[h:],0.6)
            if len(r)<4: continue
            n+=len(r)
            d+='M'+'L'.join('%.1f %.1f'%p for p in r[:-1])+'Z'
    paths[f['properties']['code']]=d
# centroid labels approx (bbox center of largest ring)
json.dump({'w':W+20,'h':round(H+20),'paths':paths},open('paths.json','w'),separators=(',',':'))
print('points',n, 'bytes',len(json.dumps(paths)))

rg=json.load(open('reg.geojson'))
rp={}
for f in rg['features']:
    polys=[f['geometry']['coordinates']] if f['geometry']['type']=='Polygon' else f['geometry']['coordinates']
    d=''
    for poly in polys:
        for ring in poly:
            xy=[((proj(p)[0]-minx)*s+10,(proj(p)[1]-miny)*s+10) for p in ring]
            h=len(xy)//2
            r=dp(xy[:h+1],0.8)[:-1]+dp(xy[h:],0.8)
            if len(r)<4: continue
            d+='M'+'L'.join('%.1f %.1f'%p for p in r[:-1])+'Z'
    rp[f['properties']['nom']]=d
C={'Paris':(2.35,48.86),'Lyon':(4.84,45.76),'Marseille':(5.37,43.30),'Toulouse':(1.44,43.60),'Bordeaux':(-0.58,44.84),'Nantes':(-1.55,47.22),'Lille':(3.06,50.63),'Strasbourg':(7.75,48.58),'Nice':(7.26,43.70),'Rennes':(-1.68,48.11),'Montpellier':(3.88,43.61),'Perpignan':(2.90,42.70),'Toulon':(5.93,43.12),'Le Havre':(0.11,49.49)}
cities={k:[round((proj(v)[0]-minx)*s+10,1),round((proj(v)[1]-miny)*s+10,1)] for k,v in C.items()}
json.dump({'w':W+20,'h':round(H+20),'paths':paths,'regions':rp,'cities':cities},open('paths.json','w'),separators=(',',':'))
print('total bytes',len(open('paths.json').read()), list(rp)[:3])
