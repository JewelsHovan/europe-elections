# Europe Election Maps

Static pages with interactive maps, polling and news for upcoming national elections. Published at https://jewelshovan.github.io/europe-elections/.

Each country page is one self-contained HTML file built from `src/<country>/`. For France: `cd src/france && python3 fill.py && python3 build.py`. To rebuild the landing page: `python3 src/build_index.py`. Page conventions are in `src/SPEC.md`.
