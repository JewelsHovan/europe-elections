# United Kingdom page rebuild

From `src/uk/`:

```sh
python3 prepare.py
python3 build.py
```

Source files retained here (all below 20 MB):

- `candidacies.csv` — official House of Commons Library candidate-level results for 4 July 2024, https://electionresults.parliament.uk/general-elections/6/candidacies.csv (downloaded 1 Oct 2026). Includes the candidate vote-change field against the 2019 notional result where available. Open Parliament Licence.
- `boundaries.geojson` — ONS Westminster Parliamentary Constituencies (July 2024) Boundaries UK BUC, ultra-generalised (500m), https://open-geography-portalx-ons.hub.arcgis.com/api/download/v1/items/ef63f363ac824b79ae9670744fcc4307/geojson?layers=0 (downloaded 1 Oct 2026). EPSG:27700 British National Grid; contains OS data © Crown copyright and database right 2024.

`prepare.py` joins all 650 seats by `PCON24CD` / Commons Library geographic code, generates `data.json` (candidate party/vote records and Labour vote change) and `paths.json` (Douglas–Peucker simplification of ONS boundaries, 1.3 SVG pixels). `build.py` inlines the shared CSS, UK CSS/JS, data and a precoloured default SVG in `../../uk/index.html`. There is no network request at view time. The JS reads paths from the fallback SVG rather than repeating the geometry as JSON.

Four-poll baseline at 1 Oct 2026: YouGov 27–28 Sep, Opinium 23–25 Sep, Survation 22–23 Sep, More in Common 25–29 Sep (latest worksheet in the [polling tables archive](https://www.moreincommon.org.uk/polling-tables/)). Simple unweighted mean, Labour 26.5, Reform 23.5, Conservatives 19.75, Lib Dem 11, Green 9.25; indicative SNP 2 and Plaid 1. The slider shifts Reform against Labour equally. Each local GB party share is its 2024 share plus the difference between that party's national poll and its 2024 GB national valid-vote share, floored at zero; minor parties and independents retain their own 2024 shares, and NI is held at its 2024 result. There is no renormalisation because only ranks determine FPTP winners. This is intentionally simpler than an MRP and can substantially overstate or understate individual parties' seats. It does not model Restore Britain, candidate withdrawals, tactical voting, by-elections or party defections. The change layer uses Labour candidate vote-share change from the CSV; missing entries remain missing.

Checks: 650 geometry codes match 650 result codes. Generated page ~460 KB. At the baseline the toy model returns Labour 330, Conservative 116, Reform 80; at Reform 27 / Labour 23 it returns Reform 219, Labour 214. These are illustrations, not the independently published 2026 MRP estimates. The fixed battleground range Reform 21–27 (opposite Labour swing) changes the projected winner in 215 seats.
