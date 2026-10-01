"""Make compact regional data from 2018/2022 Chamber results; Aosta Valley uses a separate ballot."""
import json
from pathlib import Path
root=Path(__file__).parent
raw=json.loads((root/'results.json').read_text())
out=[]
for row in raw:
    v=row['2022']; old=row['2018']
    def starts(d,p): return next(value for key,value in d.items() if key.startswith(p))
    cd=starts(v,'Lega, Forza Italia'); cs=starts(v,'Impegno Civico'); m=v['Movimento 5 Stelle'];
    oldcd=starts(old,'Forza Italia, Lega')
    # Winner is against the REAL, separately running lists, not a retrospective alliance.
    tickets={'Centre-right':cd,'Centre-left':cs,'M5S':m,'Action–IV':v['Azione - Italia Viva']}
    winner=max(tickets,key=tickets.get)
    margin=round(tickets[winner]-sorted(tickets.values())[-2],1)
    name={'Abruzzi':'Abruzzo','Emilia Romagna':'Emilia-Romagna','Friuli Venezia Giulia':'Friuli-Venezia Giulia','Trentino Alto Adige':'Trentino-Alto Adige/Südtirol'}.get(row['name'],row['name'])
    out.append(dict(c=row['code'],n=name,cd=cd,cs=cs,m5=m,iv=v['Azione - Italia Viva'],
        parties={k:v.get(src) for k,src in [('FdI',"Fratelli d'Italia"),('Lega','Lega'),('FI','Forza Italia'),('PD','Partito Democratico'),('AVS','Alleanza Verdi e Sinistra'),('M5S','Movimento 5 Stelle'),('Action–IV','Azione - Italia Viva')]},
        cd18=oldcd, m518=old.get('Movimento 5 Stelle'),actual=winner,am=margin))
# Aosta: standalone FPTP contest. The autonomist winner included PD/Action/IV;
# the M5S-supported list was separate. No nationally comparable list vote.
out.insert(1,dict(c='02',n='Valle d’Aosta',cd=29.8,actual='Autonomists',am=8.83,special=True,
    note='Franco Manes (Autonomists/PD/Action/IV) 38.63%; centre-right 29.80%; Valdostan Renaissance 11.90%; Open Aosta Valley (with M5S) 10.87%; Sovereign and Popular Italy 4.28%; People’s Union 2.56%; Italian Communist Party 1.96%. No proportional ballot.'))
assert len(out)==20
(root/'data.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
for d in out:
 if not d.get('special'):print(d['n'],round(d['cd']-d['cs']-d['m5'],1))
