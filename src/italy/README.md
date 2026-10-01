# Italy page rebuild

From the repository root:

```sh
python3 src/italy/parse.py    # fetches and caches 2018/2022 regional Camera HTML if absent
python3 src/italy/compute.py  # results.json -> data.json
python3 src/italy/geo.py      # regions.geojson -> paths.json
python3 src/italy/build.py    # body.html + shared/base.css + extra.css + map.js + data -> italy/index.html
```

`parse.py` retrieves 19 comparable regions (ISTAT codes 01, 03–20) from `http://electionresources.org/it/{2018,2022}/chamber.php?region=XX`, which reproduces regional Interior Ministry results rounded to one decimal. The authoritative 2022 database: https://elezionistorico.interno.gov.it/index.php?tpel=C&dtel=25/09/2022&es0=S&tpa=I&lev0=0&levsut0=0&ms=S&tpe=A . CISE independently reports regional coalition shares: https://cise.luiss.it/2022/09/26/risultati-camera-lanalisi-dettagliata-di-liste-e-coalizioni-per-regioni-e-zone-geopolitiche/ . `cise-table.png` is its published regional list-vote chart, kept for checking. Aosta's separate 2022 FPTP returns are hand-entered from the Aosta regional authority at https://www.regione.vda.it/amministrazione/Elezioni/Dati_e_risultati/elezioni/VotiLista_i.aspx?idele=168 ; it is deliberately excluded from swing comparisons. The English Wikipedia summary has a transcription error for the centre-right share (28.80%; the correct 16,016/53,746 is **29.80%**).

Boundary raw file `regions.geojson` (2.6 MB) is from https://raw.githubusercontent.com/guglielmo/geojson-italy/master/geojson/limits_IT_regions.geojson (openpolis/guglielmo, ISTAT-derived WGS84). Geometry uses screen-space Ramer–Douglas–Peucker simplification at 0.7 px, producing a ~32 KB SVG path JSON. No file exceeds 20 MB.

The projected coalition comparison is an additive regional swing in percentage points around **2022 national centre-right 43.8%** and **a retrospective centre-left + M5S total 41.6%**; the latter was not an alliance. Preset national vote-share pairs are the 29 Sep 2026 BiDiMedia polling average or a reported 28 Sep Ipsos coalition test. The slider adds `s` to the right and subtracts `s` from the broad side. Party-share and 2018→2022 change layers show actual historical results. These regional results do not allocate constituency seats, correct turnout or forecast the electoral-law outcome. The 2022 Action–Italia Viva vote is kept apart from both modelled alliances. Futuro Nazionale did not exist in 2022 and has no measured regional baseline.
