#!/usr/bin/env python3
import os
from pathlib import Path
import base64

# Vytvoř kořenovou složku
ROOT = Path("gemdistrict.art")
ROOT.mkdir(exist_ok=True)

# 1. Vytvoř index.html
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gem District</title>
  <link rel="icon" href="images/favicon.png">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <h1>Welcome to Gem District</h1>
  <p>Discover the future of luxury with exclusive NFT art.</p>
  <script src="js/main.js"></script>
</body>
</html>'''

(ROOT / "index.html").write_text(index_html, encoding="utf-8")
print("✅ Vytvořen: index.html")

# 2. Vytvoř css/style.css
css_dir = ROOT / "css"
css_dir.mkdir(exist_ok=True)

style_css = '''body {
  font-family: Arial, sans-serif;
  background: #f4f4f4;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #007bff;
}'''

(css_dir / "style.css").write_text(style_css, encoding="utf-8")
print("✅ Vytvořen: css/style.css")

# 3. Vytvoř js/main.js
js_dir = ROOT / "js"
js_dir.mkdir(exist_ok=True)

main_js = '''console.log("Gem District is live!");'''

(js_dir / "main.js").write_text(main_js, encoding="utf-8")
print("✅ Vytvořen: js/main.js")

# 4. Vytvoř images/favicon.png (1x1 pixel placeholder)
images_dir = ROOT / "images"
images_dir.mkdir(exist_ok=True)

# Base64 data pro 1x1 černý pixel (PNG)
favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
favicon_data = base64.b64decode(favicon_b64)

(images_dir / "favicon.png").write_bytes(favicon_data)
print("✅ Vytvořen: images/favicon.png")

print("\n🎉 Struktura gemdistrict.art byla úspěšně vytvořena!")
print(f"\n📁 Složka: {ROOT.absolute()}")
