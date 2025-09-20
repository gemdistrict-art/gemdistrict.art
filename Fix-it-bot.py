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
