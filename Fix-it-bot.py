#!/usr/bin/env python3
import os
from pathlib import Path
import re

ROOT = Path(".")
IMAGE_DIR = ROOT / "images"

def fix_image_case():
    """Opraví img src tagy na správnou velikost písmen podle skutečných souborů."""
    if not IMAGE_DIR.exists():
        print("🖼️  Složka 'images' neexistuje.")
        return

    # Vytvoř mapování: lowercase název → správný název
    real_files = {f.name.lower(): f.name for f in IMAGE_DIR.iterdir() if f.is_file()}

    fixed = 0
    for html_file in ROOT.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        new_content = content

        # Najdi všechny img src
        pattern = r'<img\s+[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for src in matches:
            if src.startswith("images/") and not src.startswith("http"):
                filename = src.split("/")[-1]
                lower_filename = filename.lower()
                if lower_filename in real_files and filename != real_files[lower_filename]:
                    correct_path = src.replace(filename, real_files[lower_filename])
                    new_content = new_content.replace(src, correct_path)
                    print(f"🖼️  Opraven obrázek: {src} → {correct_path}")
                    fixed += 1

        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")

    print(f"✅ Opraveno {fixed} obrázků.")

def add_favicon_and_meta():
    """Přidá favicon a základní meta tagy, pokud chybí."""
    html_file = ROOT / "index.html"
    if not html_file.exists():
        print("📄 index.html neexistuje.")
        return

    content = html_file.read_text(encoding="utf-8")

    # Favicon
    if '<link rel="icon"' not in content:
        insert_after = '<head>'
        favicon_tag = '    <link rel="icon" type="image/png" href="images/favicon.png">\n'
        if (IMAGE_DIR / "favicon.png").exists():
            content = content.replace(insert_after, insert_after + "\n" + favicon_tag)
            print("✅ Přidán favicon tag.")

    # Meta description
    if '<meta name="description"' not in content:
        meta_desc = '    <meta name="description" content="Gem District - Exclusive NFT Art Gallery">\n'
        content = content.replace("<head>", "<head>\n" + meta_desc)
        print("✅ Přidán meta description tag.")

    # Open Graph
    if '<meta property="og:title"' not in content:
        og_tags = '''    <meta property="og:title" content="Gem District">
    <meta property="og:description" content="Exclusive NFT Art Gallery">
    <meta property="og:image" content="images/og-image.jpg">
    <meta property="og:url" content="https://gemdistrict.art">
'''
        content = content.replace("<head>", "<head>\n" + og_tags)
        print("✅ Přidány Open Graph tagy.")

    html_file.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    print("🤖 Spouštím Fix-It Bota pro gemdistrict.art...\n")
    fix_image_case()
    add_favicon_and_meta()
    print("\n🎉 Bot dokončil opravy. Nezapomeň commitnout změny!")

#!/usr/bin/env python3
import os
from pathlib import Path
import re

ROOT = Path(".")
IMAGE_DIR = ROOT / "images"

# Jazyky, které podporuješ
LANGUAGES = ["en", "de", "fr", "es", "ru", "zh"]

def fix_image_case():
    """Opraví img src tagy na správnou velikost písmen podle skutečných souborů."""
    if not IMAGE_DIR.exists():
        print("🖼️  Složka 'images' neexistuje.")
        return

    real_files = {f.name.lower(): f.name for f in IMAGE_DIR.iterdir() if f.is_file()}
    fixed = 0

    for html_file in ROOT.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        new_content = content

        pattern = r'<img\s+[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for src in matches:
            if src.startswith("images/") and not src.startswith("http"):
                filename = src.split("/")[-1]
                lower_filename = filename.lower()
                if lower_filename in real_files and filename != real_files[lower_filename]:
                    correct_path = src.replace(filename, real_files[lower_filename])
                    new_content = new_content.replace(src, correct_path)
                    print(f"🖼️  Opraven obrázek: {src} → {correct_path}")
                    fixed += 1

        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")

    print(f"✅ Opraveno {fixed} obrázků.")

def add_favicon_and_meta():
    """Přidá favicon a základní meta tagy, pokud chybí."""
    html_file = ROOT / "index.html"
    if not html_file.exists():
        print("📄 index.html neexistuje.")
        return

    content = html_file.read_text(encoding="utf-8")

    if '<link rel="icon"' not in content and (IMAGE_DIR / "favicon.png").exists():
        favicon_tag = '    <link rel="icon" type="image/png" href="images/favicon.png">\n'
        content = content.replace('<head>', '<head>\n' + favicon_tag)
        print("✅ Přidán favicon tag.")

    if '<meta name="description"' not in content:
        meta_desc = '    <meta name="description" content="Gem District - Exclusive NFT Art Gallery">\n'
        content = content.replace("<head>", "<head>\n" + meta_desc)
        print("✅ Přidán meta description tag.")

    if '<meta property="og:title"' not in content:
        og_tags = '''    <meta property="og:title" content="Gem District">
    <meta property="og:description" content="Exclusive NFT Art Gallery">
    <meta property="og:image" content="images/og-image.jpg">
    <meta property="og:url" content="https://gemdistrict.art">
'''
        content = content.replace("<head>", "<head>\n" + og_tags)
        print("✅ Přidány Open Graph tagy.")

    html_file.write_text(content, encoding="utf-8")

def check_translations_integrity():
    """Zkontroluje, zda všechny data-i18n klíče existují ve všech jazycích."""
    html_files = list(ROOT.rglob("*.html"))
    if not html_files:
        return

    # Najdi všechny klíče z HTML
    all_keys = set()
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        matches = re.findall(r'data-i18n\s*=\s*["\']([^"\']+)["\']', content)
        all_keys.update(matches)

    if not all_keys:
        print("ℹ️  Žádné data-i18n klíče nenalezeny.")
        return

    # Načti aktuální translations z prvního HTML souboru, kde je definován
    translations_script = None
    target_file = None

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        if "const translations = {" in content:
            translations_script = content
            target_file = html_file
            break

    if not translations_script:
        print("⚠️  Skript 'translations' nebyl nalezen. Nelze kontrolovat překlady.")
        return

    # Extrahuj aktuální klíče pro každý jazyk
    current_translations = {}
    for lang in LANGUAGES:
        lang_pattern = rf'"{lang}"\s*:\s*{{(.*?)}}'
        match = re.search(lang_pattern, translations_script, re.DOTALL)
        if match:
            lang_block = match.group(1)
            keys_in_lang = re.findall(r'"([^"]+)"\s*:', lang_block)
            current_translations[lang] = set(keys_in_lang)
        else:
            current_translations[lang] = set()

    # Zkontroluj chybějící klíče
    missing = {}
    for lang in LANGUAGES:
        missing_keys = all_keys - current_translations[lang]
        if missing_keys:
            missing[lang] = missing_keys

    if not missing:
        print("✅ Všechny jazyky mají všechny klíče přeložené.")
        return

    # Přidej chybějící klíče
    for lang in missing:
        for key in missing[lang]:
            placeholder = f"[{key} - {lang.upper()}]"
            # Vytvoř řádek pro vložení
            new_line = f'      "{key}": "{placeholder}",\n'
            # Najdi blok jazyka
            lang_start = re.search(rf'("{lang}"\s*:\s*{{)', translations_script)
            if lang_start:
                insert_pos = lang_start.end()
                # Najdi konec bloku (první uzavírací závorka po začátku bloku)
                block_start = lang_start.end() - 1
                brace_count = 1
                pos = block_start + 1
                while pos < len(translations_script) and brace_count > 0:
                    if translations_script[pos] == '{':
                        brace_count += 1
                    elif translations_script[pos] == '}':
                        brace_count -= 1
                    pos += 1

                if brace_count == 0:
                    # Vlož před poslední }
                    insert_at = pos - 1
                    translations_script = translations_script[:insert_at] + new_line + translations_script[insert_at:]
                    print(f"🔤 Přidán chybějící klíč '{key}' do jazyka '{lang}'")

    # Ulož aktualizovaný soubor
    if target_file:
        target_file.write_text(translations_script, encoding="utf-8")
        print("✅ Překlady byly aktualizovány.")

if __name__ == "__main__":
    print("🤖 Spouštím vylepšeného Fix-It Bota pro gemdistrict.art...\n")
    fix_image_case()
    add_favicon_and_meta()
    check_translations_integrity()
    print("\n🎉 Bot dokončil všechny opravy. Nezapomeň commitnout změny!")
#!/usr/bin/env python3
import os
from pathlib import Path
import re

ROOT = Path(".")
IMAGE_DIR = ROOT / "images"
LANGUAGES = ["en", "de", "fr", "es", "ru", "zh"]

# =============================
# 1. Vytvoření chybějících složek a souborů
# =============================

def ensure_structure():
    """Vytvoří všechny chybějící složky a soubory."""
    print("🔧 Vytvářím chybějící strukturu...")

    # Složky
    for folder in ["css", "js", "images", ".github/workflows"]:
        Path(folder).mkdir(parents=True, exist_ok=True)

    # Soubory
    files_to_create = {
        "index.html": generate_index_html(),
        "css/style.css": generate_css(),
        "js/main.js": generate_js(),
        ".github/workflows/main.yml": generate_workflow(),
        "CNAME": "gemdistrict.art\n",
        "README.md": generate_readme(),
        ".gitignore": generate_gitignore(),
        "Fix-it-bot.py": Path(__file__).read_text(encoding="utf-8")  # Zkopíruje sebe sama
    }

    for filepath, content in files_to_create.items():
        fp = Path(filepath)
        if not fp.exists():
            fp.write_text(content, encoding="utf-8")
            print(f"✅ Vytvořen: {filepath}")

    # Favicon (placeholder)
    favicon_path = IMAGE_DIR / "favicon.png"
    if not favicon_path.exists():
        # Vytvoříme jednoduchý černobílý favicon pomocí base64 (1x1 pixel)
        import base64
        favicon_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
        favicon_path.write_bytes(favicon_data)
        print("✅ Vytvořen: images/favicon.png")

def generate_index_html():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gem District</title>
  <link rel="icon" href="images/favicon.png">
  <link rel="stylesheet" href="css/style.css">
  <meta name="description" content="Gem District - Exclusive NFT Art Gallery">
  <meta property="og:title" content="Gem District">
  <meta property="og:description" content="Exclusive NFT Art Gallery">
  <meta property="og:image" content="images/og-image.jpg">
  <meta property="og:url" content="https://gemdistrict.art">
</head>
<body>

  <!-- Jazykový přepínač -->
  <div class="language-switcher">
    <button onclick="setLanguage('en')">🇬🇧 EN</button>
    <button onclick="setLanguage('de')">🇩🇪 DE</button>
    <button onclick="setLanguage('fr')">🇫🇷 FR</button>
    <button onclick="setLanguage('es')">🇪🇸 ES</button>
    <button onclick="setLanguage('ru')">🇷🇺 RU</button>
    <button onclick="setLanguage('zh')">🇨🇳 中文</button>
  </div>

  <!-- Obsah s podporou překladů -->
  <h1 data-i18n="welcome">Welcome to GemDistrict Art</h1>
  <p data-i18n="subtitle">Discover rare gemstones with AR, 3D, and AI-powered features</p>
  <button data-i18n="explore">Explore the Collection</button>
  <p data-i18n="ai">AI Identifier</p>
  <p data-i18n="gemstones">Gemstones Collection</p>
  <p data-i18n="3d-viewer">3D Gemstone Viewer</p>

  <!-- Skript s překlady -->
  <script>
    const translations = {
      en: {
        welcome: "Welcome to GemDistrict Art",
        subtitle: "Discover rare gemstones with AR, 3D, and AI-powered features",
        explore: "Explore the Collection",
        ai: "AI Identifier",
        gemstones: "Gemstones Collection",
        "3d-viewer": "3D Gemstone Viewer",
        features: "GemDistrict Features",
        "ai-id": "AI Gemstone Identifier",
        "nft-title": "Gemstone NFT",
        "sources-title": "Gemstone Sources",
        contact: "Contact",
        "footer-about": "Discover rare gemstones with AR, 3D, and AI-powered features.",
        origin: "Origin",
        price: "Price",
        identify: "Identify Gemstone",
        result: "AI Result",
        "connect-wallet": "Connect Wallet",
        "mint-nft": "Mint NFT",
        "visit-prague": "Visit us in the heart of Prague"
      },
      de: {
        welcome: "Willkommen bei GemDistrict Art",
        subtitle: "Entdecken Sie seltene Edelsteine mit AR, 3D und KI-Technologie",
        explore: "Kollektion erkunden",
        ai: "KI-Identifikator",
        gemstones: "Edelsteinkollektion",
        "3d-viewer": "3D-Edelsteinbetrachter",
        features: "GemDistrict Funktionen",
        "ai-id": "KI-Edelstein-Identifikator",
        "nft-title": "Edelstein-NFT",
        "sources-title": "Herkunft der Edelsteine",
        contact: "Kontakt",
        "footer-about": "Entdecken Sie seltene Edelsteine mit AR, 3D und KI-Technologie.",
        origin: "Herkunft",
        price: "Preis",
        identify: "Edelstein identifizieren",
        result: "KI-Ergebnis",
        "connect-wallet": "Wallet verbinden",
        "mint-nft": "NFT erstellen",
        "visit-prague": "Besuchen Sie uns im Herzen von Prag"
      },
      fr: {
        welcome: "Bienvenue chez GemDistrict Art",
        subtitle: "Découvrez des pierres précieuses rares avec AR, 3D et IA",
        explore: "Explorer la collection",
        ai: "Identificateur IA",
        gemstones: "Collection de pierres précieuses",
        "3d-viewer": "Visualiseur 3D",
        features: "Fonctionnalités GemDistrict",
        "ai-id": "Identification par IA",
        "nft-title": "NFT de pierre précieuse",
        "sources-title": "Origines des pierres",
        contact: "Contact",
        "footer-about": "Découvrez des pierres précieuses rares avec AR, 3D et IA.",
        origin: "Origine",
        price: "Prix",
        identify: "Identifier la pierre",
        result: "Résultat IA",
        "connect-wallet": "Connecter le portefeuille",
        "mint-nft": "Créer le NFT",
        "visit-prague": "Visitez-nous au cœur de Prague"
      },
      es: {
        welcome: "Bienvenido a GemDistrict Art",
        subtitle: "Descubre gemas raras con AR, 3D y funciones de inteligencia artificial",
        explore: "Explorar la colección",
        ai: "Identificador IA",
        gemstones: "Colección de gemas",
        "3d-viewer": "Visor 3D",
        features: "Funciones de GemDistrict",
        "ai-id": "Identificador de gemas con IA",
        "nft-title": "NFT de gema",
        "sources-title": "Orígenes de las gemas",
        contact: "Contacto",
        "footer-about": "Descubre gemas raras con AR, 3D e IA.",
        origin: "Origen",
        price: "Precio",
        identify: "Identificar gema",
        result: "Resultado IA",
        "connect-wallet": "Conectar billetera",
        "mint-nft": "Acuñar NFT",
        "visit-prague": "Visítenos en el corazón de Praga"
      },
      ru: {
        welcome: "Добро пожаловать в GemDistrict Art",
        subtitle: "Откройте для себя редкие драгоценные камни с AR, 3D и функциями на основе ИИ",
        explore: "Исследовать коллекцию",
        ai: "Идентификатор ИИ",
        gemstones: "Коллекция драгоценных камней",
        "3d-viewer": "3D-просмотрщик камней",
        features: "Функции GemDistrict",
        "ai-id": "Идентификация камней с помощью ИИ",
        "nft-title": "NFT-драгоценный камень",
        "sources-title": "Источники камней",
        contact: "Контакт",
        "footer-about": "Откройте для себя редкие драгоценные камни с AR, 3D и ИИ.",
        origin: "Происхождение",
        price: "Цена",
        identify: "Определить камень",
        result: "Результат ИИ",
        "connect-wallet": "Подключить кошелек",
        "mint-nft": "Создать NFT",
        "visit-prague": "Посетите нас в центре Праги"
      },
      zh: {
        welcome: "欢迎来到GemDistrict艺术",
        subtitle: "通过AR、3D和人工智能功能探索稀有宝石",
        explore: "探索收藏",
        ai: "AI识别",
        gemstones: "宝石收藏",
        "3d-viewer": "3D宝石查看器",
        features: "GemDistrict功能",
        "ai-id": "AI宝石识别",
        "nft-title": "宝石NFT",
        "sources-title": "宝石来源",
        contact: "联系",
        "footer-about": "通过AR、3D和AI功能探索稀有宝石。",
        origin: "产地",
        price: "价格",
        identify: "识别宝石",
        result: "AI结果",
        "connect-wallet": "连接钱包",
        "mint-nft": "铸造NFT",
        "visit-prague": "来布拉格市中心参观我们"
      }
    };

    function setLanguage(lang) {
      const elements = document.querySelectorAll('[data-i18n]');
      elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
          el.textContent = translations[lang][key];
        }
      });
      localStorage.setItem('preferredLanguage', lang);
    }

    window.addEventListener('DOMContentLoaded', () => {
      const savedLang = localStorage.getItem('preferredLanguage');
      const browserLang = navigator.language.split('-')[0];
      const lang = translations[browserLang] ? browserLang : (savedLang || 'en');
      setLanguage(lang);
    });
  </script>

</body>
</html>'''

def generate_css():
    return '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
  background: #f4f4f4;
  padding: 2rem;
}

.language-switcher {
  margin-bottom: 2rem;
  text-align: center;
}

.language-switcher button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
}

.language-switcher button:hover {
  background: #333;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

p {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
}

button {
  display: block;
  margin: 2rem auto;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}'''

def generate_js():
    return '''console.log("Gem District is live with multilingual support!");'''

def generate_workflow():
    return '''name: 🚀 Hlavní workflow — Oprava a nasazení webu

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 📥 Checkout kódu
        uses: actions/checkout@v4

      - name: 🐍 Nastavení Pythonu
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: 🧰 Instalace závislostí
        run: |
          pip install requests

      - name: 🤖 Spuštění Fix-It Bota
        run: |
          python Fix-it-bot.py

      - name: 💾 Commit a push oprav (pokud nějaké jsou)
        run: |
          git config --global user.name "FixBot"
          git config --global user.email "fixbot@users.noreply.github.com"
          git add .
          if ! git diff --cached --quiet; then
            git commit -m "🤖 Auto-fix: všechno opraveno"
            git push
            echo "✅ Změny byly commitnuty a pushnuty."
          else
            echo "ℹ️  Žádné změny k commitnutí."
          fi

      - name: ⚙️ Konfigurace GitHub Pages
        uses: actions/configure-pages@v3

      - name: 🗃️ Příprava artifactu pro Pages
        uses: actions/upload-pages-artifact@v2
        with:
          path: './'

      - name: 🌐 Nasazení na GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3'''

def generate_readme():
    return '''# GemDistrict

Official multilingual website for GemDistrict NFT project.

- Built with HTML, CSS, JS
- Supports 6 languages: EN, DE, FR, ES, RU, ZH
- Auto-fixed by enhanced Fix-It Bot
- Deployed via GitHub Pages'''

def generate_gitignore():
    return '''.DS_Store
*.log
.env
__pycache__/
*.pyc'''

# =============================
# 2. Oprava obrázků
# =============================

def fix_image_case():
    if not IMAGE_DIR.exists():
        print("🖼️  Složka 'images' neexistuje.")
        return

    real_files = {f.name.lower(): f.name for f in IMAGE_DIR.iterdir() if f.is_file()}
    fixed = 0

    for html_file in ROOT.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        new_content = content
        pattern = r'<img\s+[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for src in matches:
            if src.startswith("images/") and not src.startswith("http"):
                filename = src.split("/")[-1]
                lower_filename = filename.lower()
                if lower_filename in real_files and filename != real_files[lower_filename]:
                    correct_path = src.replace(filename, real_files[lower_filename])
                    new_content = new_content.replace(src, correct_path)
                    print(f"🖼️  Opraven obrázek: {src} → {correct_path}")
                    fixed += 1

        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")

    print(f"✅ Opraveno {fixed} obrázků.")

# =============================
# 3. Kontrola překladů
# =============================

def check_translations_integrity():
    html_files = list(ROOT.rglob("*.html"))
    if not html_files:
        return

    all_keys = set()
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        matches = re.findall(r'data-i18n\s*=\s*["\']([^"\']+)["\']', content)
        all_keys.update(matches)

    if not all_keys:
        print("ℹ️  Žádné data-i18n klíče nenalezeny.")
        return

    translations_script = None
    target_file = None

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        if "const translations = {" in content:
            translations_script = content
            target_file = html_file
            break

    if not translations_script:
        print("⚠️  Skript 'translations' nebyl nalezen. Nelze kontrolovat překlady.")
        return

    current_translations = {}
    for lang in LANGUAGES:
        lang_pattern = rf'"{lang}"\s*:\s*{{(.*?)}}'
        match = re.search(lang_pattern, translations_script, re.DOTALL)
        if match:
            lang_block = match.group(1)
            keys_in_lang = re.findall(r'"([^"]+)"\s*:', lang_block)
            current_translations[lang] = set(keys_in_lang)
        else:
            current_translations[lang] = set()

    missing = {}
    for lang in LANGUAGES:
        missing_keys = all_keys - current_translations[lang]
        if missing_keys:
            missing[lang] = missing_keys

    if not missing:
        print("✅ Všechny jazyky mají všechny klíče přeložené.")
        return

    for lang in missing:
        for key in missing[lang]:
            placeholder = f"[{key} - {lang.upper()}]"
            new_line = f'      "{key}": "{placeholder}",\n'
            lang_start = re.search(rf'("{lang}"\s*:\s*{{)', translations_script)
            if lang_start:
                insert_pos = lang_start.end()
                block_start = lang_start.end() - 1
                brace_count = 1
                pos = block_start + 1
                while pos < len(translations_script) and brace_count > 0:
                    if translations_script[pos] == '{':
                        brace_count += 1
                    elif translations_script[pos] == '}':
                        brace_count -= 1
                    pos += 1

                if brace_count == 0:
                    insert_at = pos - 1
                    translations_script = translations_script[:insert_at] + new_line + translations_script[insert_at:]
                    print(f"🔤 Přidán chybějící klíč '{key}' do jazyka '{lang}'")

    if target_file:
        target_file.write_text(translations_script, encoding="utf-8")
        print("✅ Překlady byly aktualizovány.")

# =============================
# 4. Hlavní funkce
# =============================

if __name__ == "__main__":
    print("🤖 Spouštím SUPER Fix-It Bota — opravím všechno v GitHubu!\n")

    # 1. Vytvoří všechno, co chybí
    ensure_structure()

    # 2. Opraví cesty k obrázkům
    fix_image_case()

    # 3. Zkontroluje a doplní překlady
    check_translations_integrity()

    print("\n🎉 Bot dokončil VŠECHNY opravy.")

    # 4. Commitne a pushne změny (pokud běží v GitHub Actions)
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("\n💾 Commituji a pushuji změny zpět do main...")
        os.system('git config --global user.name "FixBot"')
        os.system('git config --global user.email "fixbot@users.noreply.github.com"')
        os.system('git add .')
        if os.system('git diff --cached --quiet') != 0:
            os.system('git commit -m "🤖 SUPER BOT: Všechno opraveno automaticky"')
            os.system('git push')
            print("✅ Změny byly úspěšně pushnuty do main!")
        else:
            print("ℹ️  Žádné změny k commitnutí.")
    else:
        print("\nℹ️  Pro commit a push spusť: git add . && git commit -m '...' && git push")
