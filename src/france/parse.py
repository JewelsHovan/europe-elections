import csv, json, math, collections
def norm(c):
    c=c.strip().strip('"')
    if c.isdigit() and len(c)<2: c=c.zfill(2)
    return c
def num(s):
    s=s.strip().strip('"').replace('%','').replace(',','.').replace('\u202f','').replace(' ','')
    return float(s) if s else 0.0
D=collections.defaultdict(dict)
# presidential
for fn,key in [('p22t1.txt','p1'),('p22t2.txt','p2')]:
    for line in open(fn,encoding='latin1'):
        f=line.rstrip('\r\n').split(';')
        if f[0].startswith('Code'): continue
        c=norm(f[0]); d=D[c]; d['name']=f[1]
        d[key+'_ins']=num(f[3]); d[key+'_vot']=num(f[6]); d[key+'_exp']=num(f[14])
        i=17
        while i+6<=len(f):
            nom=f[i+1]; d[key+'_'+nom]=num(f[i+3]); i+=6
# legislative 2024
rows=list(csv.reader(open('leg24.csv',encoding='utf-8'),delimiter=';'))
hdr=rows[0]
for r in rows[1:]:
    if not r or not r[0]: continue
    c=norm(r[0]); d=D[c]; d.setdefault('name',r[1])
    d['l_ins']=num(r[2]); d['l_vot']=num(r[3]); d['l_exp']=num(r[7])
    i=16; nu=collections.Counter()
    while i+3<len(r) and r[i]:
        nu[r[i]]+=num(r[i+1]); i+=4
    d['l_nu']=dict(nu)
# european 2024
rows=list(csv.reader(open('eu24.csv',encoding='utf-8'),delimiter=';'))
hdr=rows[0]
for r in rows[1:]:
    if not r or not r[0]: continue
    c=norm(r[0]); d=D[c]; d.setdefault('name',r[1])
    d['e_ins']=num(r[2]); d['e_vot']=num(r[3]); d['e_exp']=num(r[7])
    i=16; li={}
    while i+7<len(r) and r[i]:
        li[r[i+2]]=num(r[i+4]); i+=8
    d['e_li']=li
json.dump(D,open('raw.json','w'),ensure_ascii=False)
print(len(D)); print(sorted(D)[:5], sorted(D)[-12:])
x=D['75']; print(x['name'], {k:v for k,v in x.items() if k.startswith('p2')}); print(x['l_nu']); print(sorted(x['e_li'].items(),key=lambda t:-t[1])[:8])
allnu=collections.Counter()
for d in D.values(): allnu.update(d.get('l_nu',{}))
print(allnu.most_common())
