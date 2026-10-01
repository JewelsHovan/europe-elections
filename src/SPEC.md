# Country page spec

Each country gets one self-contained page at `<country>/index.html` (for example `germany/index.html`). It is built from sources in `src/<country>/`. The site is published on GitHub Pages at `https://jewelshovan.github.io/europe-elections/`, and people will mostly open it on phones from a WhatsApp link.

The reference implementation is France: `france/index.html`, built by `src/france/` (`parse.py` → `compute.py` → `geo.py` → `fill.py` → `build.py`; `map.js`, `extra.css`, `body.html`). Read it before starting. Match its structure, tone, styling and interaction model.

## Rules

- **Only write inside `src/<your-country>/` and `<your-country>/`.** Do not touch `france/`, `src/france/`, `src/shared/`, `index.html` at the repo root, or any other country. Do not run git.
- **One file, no network at view time.** Inline all CSS, JS and data. No CDNs, fonts, fetch or iframes. Use `src/shared/base.css` (copy it in at build time, as France does). Target under 500 KB; simplify geometry to get there.
- **Page head:** `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, the viewport meta, a `<title>` like "Germany Election Map", and a one-sentence `<meta name="description">`.
- **Writing style:** plain and factual. The first paragraph gives the state of the race. No marketing words, emoji, exclamation marks, hero banners or stat tiles. Headings say what the section holds. Every news, poll and sentiment claim gets an inline source link and a date. Mark anything you could not verify. Today is 2026-10-01; your knowledge may be stale, so research current facts on the web (DuckDuckGo HTML, Wikipedia, national statistics offices and the press work; Google returns 403).
- **Mobile first:** it must work at 375 px wide. Controls wrap, the map is full width, the detail panel stacks below the map, tap selects (no hover dependence), and tap targets are at least 36 px tall. Test by rendering at 390×844 and at 1300 px wide with headless Chrome:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=390,2400 --virtual-time-budget=4000 --screenshot=/tmp/<country>-mobile.png file:///…/index.html`
  If the screenshot comes out blank, serve the folder with `python3 -m http.server <port>` and use the http URL. Use a unique port per country: Germany 8771, UK 8772, Spain 8773, Italy 8774. Do not pass `--user-data-dir`. Look at the screenshots and fix what is broken.
- **No-JS fallback:** the build also writes a static SVG of the default map layer inside a `<noscript>`-independent container, which the script replaces on load. The goal is that a preview that does not run JavaScript still shows a coloured map with a legend.

## Required content

1. **State of the race:** next national election date (or the legal deadline if none is set), the government in power, current national polling average and trend, and the main parties and leaders.
2. **Interactive map** at the most useful sub-national level for which official results and boundaries exist:
   - Germany: the 299 Bundestag Wahlkreise (2025 boundaries) or the 16 Länder if constituency geometry is impractical. Prefer Wahlkreise, showing Erststimme winners and Zweitstimme shares.
   - UK: the 650 Westminster constituencies (2024 boundaries). Use a simplified geographic map; a hex cartogram is acceptable if geography exceeds the size budget.
   - Spain: the 52 Congress constituencies (provinces plus Ceuta and Melilla). Seats are allocated by D'Hondt per province, so show seats as well as vote shares.
   - Italy: the regions, or the 2022 Camera collegi uninominali if practical, showing the 2022 coalition results.
   - Layers: the last national election (winner and margin), party vote shares, and change since the previous election. Add a **projection layer**: apply current national polling to the last result with a transparent swing model (uniform or proportional; document which). Add a **battleground** view: which units change hands within a plausible polling range. For Spain, show which provincial seats flip.
   - A slider or preset buttons for the polling scenario, as in France.
   - Tap or click opens a detail panel with the unit's full record. Include a searchable or select list of units.
   - A regional roll-up table (Länder, UK nations and regions, autonomous communities, Italian regions) that follows the scenario.
3. **Battlegrounds:** which areas decide the election and why, with real names and numbers from your data.
4. **Polling:** a table of the latest polls from at least 4 pollsters, with field dates and source links, plus leader approval or preferred-PM figures if available.
5. **Sentiment:** government approval, top voter concerns, and trust or direction-of-country measures, each with source and date.
6. **News this week** (roughly 24 Sep – 1 Oct 2026), with sources.
7. **Calendar:** upcoming elections and events, including any regional or state elections in the next 12 months.
8. **Method and sources:** data files used (official electoral bodies preferred), the geometry source, the model formula, and its limits.

Keep the build scripts and downloaded raw data in `src/<country>/` so the page can be rebuilt. If a raw file is over about 20 MB, do not keep it; note its URL in a `src/<country>/README.md`.

## Report back

Return under 300 words:
- the files written and the page size
- what the map shows and its level of detail
- 3–5 key findings with numbers
- anything you could not verify or had to approximate
- the paths of the mobile and desktop screenshots you checked
