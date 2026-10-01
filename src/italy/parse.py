"""Download regional Camera results mirrored from Interior Ministry by Election Resources.
Usage: python3 parse.py (from src/italy). Raw HTML and extracted JSON retained.
"""
from html import unescape
from pathlib import Path
import json, re, urllib.request

ROOT = Path(__file__).parent
out = []
for code in [c for c in range(1, 21) if c != 2]:
    item = {'code': f'{code:02d}'}
    for year in (2018, 2022):
        url = f'http://electionresources.org/it/{year}/chamber.php?region={code:02d}'
        path = ROOT / f'camera-{year}-{code:02d}.html'
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(url, timeout=20).read())
        text = path.read_text()
        rows = []
        for tr in re.findall(r'<TR[^>]*>(.*?)</TR>', text, re.S | re.I):
            cells = [unescape(re.sub(r'<[^>]*>', '', s)).strip() for s in re.findall(r'<TD[^>]*>(.*?)</TD>', tr, re.S | re.I)]
            if cells:
                rows.append([' '.join(c.split()) for c in cells])
        heading = next((r[0] for r in rows if 'Election Results - ' in r[0]), '')
        name = heading.split('Election Results - ')[-1]
        if not name: raise ValueError((url, rows[:5]))
        item['name'] = name
        data = {}
        for r in rows:
            if len(r) >= 3 and re.fullmatch(r'[\d,]+', r[1]) and re.fullmatch(r'[\d.]+', r[2]):
                data[r[0]] = float(r[2])
        item[str(year)] = data
    out.append(item)
(ROOT/'results.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
for d in out:
    print(d['code'], d['name'], '2022', list(d['2022'].items())[:6], '2018', list(d['2018'].items())[:4])
