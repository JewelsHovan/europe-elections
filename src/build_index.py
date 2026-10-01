"""Build the site's landing page from the country pages that exist."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COUNTRIES = [
    ("france", "France", "Presidential election, April 2027"),
    ("germany", "Germany", "Bundestag; state elections in 2026–27"),
    ("uk", "United Kingdom", "Westminster, due by August 2029"),
    ("spain", "Spain", "Cortes Generales, due by summer 2027"),
    ("italy", "Italy", "Parliament, due by late 2027"),
]

ONLY = set(sys.argv[1:])  # optional: publish only these slugs
rows = []
for slug, name, election in COUNTRIES:
    if ONLY and slug not in ONLY:
        continue
    path = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = m.group(1) if m else ""
    rows.append(f'<tr><td><a href="{slug}/">{name}</a></td><td>{election}</td><td class="small">{desc}</td></tr>')

base = open(os.path.join(ROOT, "src", "shared", "base.css"), encoding="utf-8").read()
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Europe Election Maps</title>
<meta name="description" content="Interactive maps, polling and news for upcoming national elections in France, Germany, the UK, Spain and Italy.">
<style>{base}
.small {{ font-size: 13px; color: var(--ink-2); }}
td a {{ font-weight: 600; }}
</style>
</head>
<body>
<main class="solo">
  <h1>Europe Election Maps</h1>
  <dl class="meta">
    <div><dt>Updated</dt><dd>1 Oct 2026</dd></div>
    <div><dt>Countries</dt><dd>{len(rows)}</dd></div>
  </dl>
  <p class="lead">One page per country, each with an interactive map built from official results, the latest polls, public mood and the week's news. The maps work on phones: tap a region for its record.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Country</th><th>Next election</th><th>Page</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
  <p class="muted small">Projections on these pages are simple swing models applied to past results. They show relative positions, not forecasts. Sources are listed on each page.</p>
</main>
</body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
print(f"index.html: {len(rows)} countries")
