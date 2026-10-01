# Europe Election Maps

Static pages with interactive maps, polling and news for upcoming national elections. Published at https://julienhovan.com/europe-elections/ (GitHub Pages on JewelsHovan, served through the custom domain).

Each country page is one self-contained HTML file built from `src/<country>/`. For France: `cd src/france && python3 fill.py && python3 build.py`. To rebuild the landing page: `python3 src/build_index.py`. Page conventions are in `src/SPEC.md`.

After building a page, add its link-preview image and tags (needs a local server on port 8770 for the screenshot):
`node src/preview.mjs http://localhost:8770/<slug>/ "#mapwrap" "<title>" "<subtitle>" <slug>/preview.png` then `python3 src/add_og.py <slug> "<title>" "<description>"`.
