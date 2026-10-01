import json, math
D=json.load(open('raw.json'))
for z,c in {'ZA':'971','ZB':'972','ZC':'973','ZD':'974','ZM':'976'}.items():
    D[c].update({k:v for k,v in D[z].items() if k.startswith('p')})
REG={'Auvergne-Rhône-Alpes':'01 03 07 15 26 38 42 43 63 69 73 74','Bourgogne-Franche-Comté':'21 25 39 58 70 71 89 90',
'Bretagne':'22 29 35 56','Centre-Val de Loire':'18 28 36 37 41 45','Corse':'2A 2B','Grand Est':'08 10 51 52 54 55 57 67 68 88',
'Hauts-de-France':'02 59 60 62 80','Île-de-France':'75 77 78 91 92 93 94 95','Normandie':'14 27 50 61 76',
'Nouvelle-Aquitaine':'16 17 19 23 24 33 40 47 64 79 86 87','Occitanie':'09 11 12 30 31 32 34 46 48 65 66 81 82',
'Pays de la Loire':'44 49 53 72 85',"Provence-Alpes-Côte d'Azur":'04 05 06 13 83 84','Outre-mer':'971 972 973 974 976'}
regof={c:r for r,cs in REG.items() for c in cs.split()}
codes=sorted(regof)
assert len(codes)==101, len(codes)
FR=['RN','UXD','REC','EXD']; LEFT=['UG','DVG','ECO','EXG','SOC','RDG','FI','COM','VEC']; CEN=['ENS','DVC','HOR','UDI']; RIGHT=['LR','DVD']
EU={'bardella':'La FRANCE REVIENT','glucksmann':'REVEIL EUR','hayer':"BESOIN D'EUROPE",'aubry':'LFI - UP','bellamy':'LA DROITE POUR FAIRE ENTENDRE LA VOIX DE LA FRANCE EN EUROPE','toussaint':'EUROPE ÉCOLOGIE','marechal':'LA FRANCE FIERE, MENEE PAR MARION MARECHAL ET SOUTENUE PAR ÉRIC ZEMMOUR'}
lg=lambda p: math.log(p/(1-p)); ex=lambda x: 1/(1+math.exp(-x))
# national totals over all units in D (France entière incl. abroad)
def tot(f):
    return sum(f(d) for c,d in D.items() if not c.startswith('Z') or c in ('ZX','ZZ','ZN','ZP','ZS','ZW') )
# presidential national: sum over everything with p keys excluding duplicates (971.. got copies) -> use Z codes only for pres
pres=[d for c,d in D.items() if 'p2_exp' in d and c not in ('971','972','973','974','976')]
LP22n=sum(d['p2_LE PEN'] for d in pres)/sum(d['p2_exp'] for d in pres)
leg=[d for d in D.values() if 'l_nu' in d]
FRn=sum(sum(d['l_nu'].get(k,0) for k in FR) for d in leg)/sum(d['l_exp'] for d in leg)
Ln=sum(sum(d['l_nu'].get(k,0) for k in LEFT) for d in leg)/sum(d['l_exp'] for d in leg)
print('nat LP22 R2 %.4f  FR24 %.4f  LEFT24 %.4f'%(LP22n,FRn,Ln))
out=[]
for c in codes:
    d=D[c]; r={'c':c,'n':d['name'],'r':regof[c]}
    r['ins']=int(d['l_ins'])
    e1=d['p1_exp']; r['p1']={k:round(100*d['p1_'+n]/e1,1) for k,n in [('lepen','LE PEN'),('macron','MACRON'),('melenchon','MÉLENCHON'),('zemmour','ZEMMOUR'),('pecresse','PÉCRESSE'),('jadot','JADOT')]}
    r['lp22']=round(100*d['p2_LE PEN']/d['p2_exp'],1)
    nu=d['l_nu']; le=d['l_exp']
    b={'fr':sum(nu.get(k,0) for k in FR)/le,'left':sum(nu.get(k,0) for k in LEFT)/le,'cen':sum(nu.get(k,0) for k in CEN)/le,'right':sum(nu.get(k,0) for k in RIGHT)/le}
    r['l24']={k:round(100*v,1) for k,v in b.items()}
    r['lead24']=max(b,key=b.get)
    r['turn24']=round(100*d['l_vot']/d['l_ins'],1)
    li=d['e_li']; ee=d['e_exp']; r['eu24']={k:round(100*li.get(v,0)/ee,1) for k,v in EU.items()}
    lp=d['p2_LE PEN']/d['p2_exp']
    if c.startswith('97'):
        lean=lg(lp)-lg(LP22n)   # RN rarely stood in 2024 overseas legislative races; use 2022 runoff only
    else:
        lean=0.5*(lg(lp)-lg(LP22n))+0.5*(lg(b['fr'])-lg(FRn))
    r['lean']=round(lean,4)
    r['leanL']=round(lg(max(b['left'],0.02))-lg(Ln),4)
    r['flip']=round(100*ex(-lean),1)
    r['shift']=round(100*(b['fr']-(d['p1_LE PEN']+d['p1_ZEMMOUR']+d['p1_DUPONT-AIGNAN'])/e1),1)
    out.append(r)
json.dump({'nat':{'lp22':round(100*LP22n,2),'fr24':round(100*FRn,2),'left24':round(100*Ln,2)},'deps':out},open('data.json','w'),ensure_ascii=False,separators=(',',':'))
# check scenario
for nat in (0.50,0.53,0.56):
    blue=[(r['n'],round(100*ex(lg(nat)+r['lean']),1)) for r in out if ex(lg(nat)+r['lean'])<0.5]
    print(nat,len(blue),blue)
s=sorted(out,key=lambda r:r['flip'])
print('lowest flip (most RN):',[(r['n'],r['flip']) for r in s[:8]])
print('highest flip:',[(r['n'],r['flip']) for r in s[-15:]])
print('lead24:',__import__('collections').Counter(r['lead24'] for r in out))
print('shift range',min(r['shift'] for r in out),max(r['shift'] for r in out))
