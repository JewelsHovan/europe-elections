"""Insert link-preview tags (Open Graph, Twitter) into a built page. Run after each build.

Usage: python3 src/add_og.py <slug> "<title>" "<description>"
Use "." as the slug for the landing page. The page must have a preview.png next to it (or, for the landing page, at the repo root).
"""
import html
import os
import re
import sys

BASE = "https://julienhovan.com/europe-elections/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

slug, title, desc = sys.argv[1:4]
folder = "" if slug == "." else slug + "/"
path = os.path.join(ROOT, folder, "index.html")
page = open(path, encoding="utf-8").read()
page = re.sub(r"\n?<!-- og -->.*?<!-- /og -->", "", page, flags=re.S)
t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
tags = f"""
<!-- og -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Europe Election Maps">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{BASE}{folder}">
<meta property="og:image" content="{BASE}{folder}preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<!-- /og -->"""
page = page.replace("</title>", "</title>" + tags, 1)
open(path, "w", encoding="utf-8").write(page)
print(f"og tags added to {folder or './'}index.html")
