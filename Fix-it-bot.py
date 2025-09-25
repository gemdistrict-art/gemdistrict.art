#!/usr/bin/env python3# Commands to fix:#!/usr/bin/env python3# 1. Replace the broken workflow with the fixed version
cat > .github/workflows/main.yml << 'EOF'
name: Deploy GemDistrict Art

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Build website
      run: |
        python Fix-it-bot.py
        
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
EOF

# 2. Commit and push the fix
git add .github/workflows/main.yml
git commit -m "🐛 Fix YAML syntax error on line 2"
git push origin main
import os
import json
import re
from pathlib import Path

def ensure_directory_structure():
    """Create all necessary directories"""
    directories = [
        "gemdistrict.art",
        "gemdistrict.art/css", 
        "gemdistrict.art/js",
        "gemdistrict.art/icons",
        "gemdistrict.art/images"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_index_html():
    """Create complete index.html with all features"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI-powered gemstone analysis with AR experiences">
    <meta name="theme-color" content="#d4af37">
    
    <!-- PWA requirements -->
    <link rel="manifest" href="manifest.json">
    <link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
    <link rel="apple-touch-icon" href="icons/icon-192.png">
    
    <title>GemDistrict Art - AI Gemstone & AR Experience</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- Three.js for 3D viewer -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    
    <!-- A-Frame for AR -->
    <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
    
    <!-- TensorFlow.js for AI -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.0.0/dist/tf.min.js"></script>
</head>
<body>
    <div id="app">
        <header class="navbar">
            <h1>GemDistrict Art</h1>
            <div class="controls">
                <button id="darkModeToggle" aria-label="Toggle dark mode">🌙</button>
                <select id="languageSelect">
                    <option value="en">English</option>
                    <option value="cs">Čeština</option>
                </select>
            </div>
        </header>
        
        <main>
            <section id="gemstoneGallery">
                <h2>3D Gemstone Gallery</h2>
                <div id="threejs-container"></div>
                <div class="controls">
                    <button id="rotateLeft">← Rotate Left</button>
                    <button id="rotateRight">Rotate Right →</button>
                    <button id="zoomIn">Zoom In +</button>
                    <button id="zoomOut">Zoom Out -</button>
                </div>
            </section>
            
            <section id="arPreview">
                <h2>AR Preview</h2>
                <div id="ar-container">
                    <a-scene embedded>
                        <a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9"></a-box>
                        <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
                        <a-sky color="#ECECEC"></a-sky>
                    </a-scene>
                </div>
                <button id="arButton">Start AR Experience</button>
            </section>
            
            <section id="aiGemId">
                <h2>AI Gemstone Identification</h2>
                <input type="file" id="gemImage" accept="image/*">
                <button id="identifyButton">Identify Gemstone</button>
                <div id="identificationResult"></div>
            </section>
            
            <section id="nftIntegration">
                <h2>NFT Integration</h2>
                <button id="mintNFT">Mint as NFT</button>
                <div id="nftStatus"></div>
            </section>
        </main>
    </div>
    
    <script src="js/main.js"></script>
    <script>
        // Register service worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('js/service-worker.js')
                .then(() => console.log('Service Worker registered'))
                .catch(err => console.log('Service Worker registration failed'));
        }
    </script>
</body>
</html>'''
    
    with open("gemdistrict.art/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Created: gemdistrict.art/index.html")

def create_css():
    """Create complete CSS with dark mode and responsive design"""
    css_content = '''/* CSS Variables for theming */
:root {
    --primary: #d4af37;
    --secondary: #1a1a1a;
    --background: #f8f8f8;
    --text: #333333;
    --card-bg: #ffffff;
    --border: #e0e0e0;
    --success: #28a745;
    --error: #dc3545;
}

[data-theme="dark"] {
    --background: #0a0a0a;
    --text: #e0e0e0;
    --card-bg: #1a1a1a;
    --border: #333333;
}

/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: var(--background);
    color: var(--text);
    line-height: 1.6;
    transition: background 0.3s ease, color 0.3s ease;
}

/* Layout */
.navbar {
    background: var(--card-bg);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar h1 {
    color: var(--primary);
    font-size: 1.5rem;
}

.controls {
    display: flex;
    gap: 1rem;
    align-items: center;
}

/* Buttons */
button {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s ease;
}

button:hover {
    background: #b8941f;
}

button:disabled {
    background: #cccccc;
    cursor: not-allowed;
}

/* Sections */
main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

section {
    background: var(--card-bg);
    margin: 2rem 0;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

section h2 {
    color: var(--primary);
    margin-bottom: 1rem;
}

/* 3D Viewer */
#threejs-container {
    width: 100%;
    height: 400px;
    background: #000;
    border-radius: 10px;
    margin: 1rem 0;
    position: relative;
}

#threejs-container canvas {
    border-radius: 10px;
}

/* AR Container */
#ar-container {
    width: 100%;
    height: 300px;
    border: 2px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

a-scene {
    width: 100%;
    height: 100%;
}

/* AI Section */
#aiGemId input[type="file"] {
    margin: 1rem 0;
    padding: 0.5rem;
    border: 2px dashed var(--border);
    border-radius: 5px;
    width: 100%;
}

#identificationResult {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--background);
    border-radius: 5px;
    min-height: 100px;
}

/* NFT Section */
#nftStatus {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--background);
    border-radius: 5px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }
    
    .controls {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    main {
        padding: 1rem;
    }
    
    section {
        padding: 1rem;
    }
    
    #threejs-container {
        height: 250px;
    }
    
    #ar-container {
        height: 200px;
    }
}

/* Loading states */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

.error {
    color: var(--error);
    background: rgba(220, 53, 69, 0.1);
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}

.success {
    color: var(--success);
    background: rgba(40, 167, 69, 0.1);
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}'''
    
    with open("gemdistrict.art/css/style.css", "w", encoding="utf-8") as f:
        f.write(css_content)
    print("✅ Created: gemdistrict.art/css/style.css")

def create_javascript():
    """Create complete JavaScript with all features"""
    js_content = '''class GemDistrictApp {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.gemstone = null;
        this.darkMode = localStorage.getItem('darkMode') === 'true';
        this.currentLanguage = localStorage.getItem('language') || 'en';
        
        this.init();
    }
    
    init() {
        this.setupDarkMode();
        this.setupLanguage();
        this.initThreeJS();
        this.setupEventListeners();
        this.setupAI();
        this.setupNFT();
    }
    
    setupDarkMode() {
        const toggle = document.getElementById('darkModeToggle');
        
        // Apply saved theme
        if (this.darkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
            toggle.textContent = '☀️';
        }
        
        toggle?.addEventListener('click', () => {
            this.darkMode = !this.darkMode;
            const theme = this.darkMode ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('darkMode', this.darkMode);
            toggle.textContent = this.darkMode ? '☀️' : '🌙';
        });
    }
    
    setupLanguage() {
        const select = document.getElementById('languageSelect');
        select.value = this.currentLanguage;
        
        select?.addEventListener('change', (e) => {
            this.currentLanguage = e.target.value;
            localStorage.setItem('language', this.currentLanguage);
            this.updateLanguage();
        });
    }
    
    updateLanguage() {
        const translations = {
            en: {
                title: 'GemDistrict Art',
                gallery: '3D Gemstone Gallery',
                ar: 'AR Preview',
                ai: 'AI Gemstone Identification',
                nft: 'NFT Integration'
            },
            cs: {
                title: 'GemDistrict Art',
                gallery: '3D Galerie Drahokamů',
                ar: 'AR Náhled',
                ai: 'AI Identifikace Drahokamů',
                nft: 'NFT Integrace'
            }
        };
        
        const t = translations[this.currentLanguage];
        document.title = t.title;
        document.querySelector('#gemstoneGallery h2').textContent = t.gallery;
        document.querySelector('#arPreview h2').textContent = t.ar;
        document.querySelector('#aiGemId h2').textContent = t.ai;
        document.querySelector('#nftIntegration h2').textContent = t.nft;
    }
    
    initThreeJS() {
        const container = document.getElementById('threejs-container');
        if (!container) return;
        
        try {
            // Check WebGL support
            if (!window.WebGLRenderingContext) {
                throw new Error('WebGL not supported');
            }
            
            // Scene setup
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(0x111111);
            
            // Camera setup
            this.camera = new THREE.PerspectiveCamera(
                75, 
                container.clientWidth / container.clientHeight, 
                0.1, 
                1000
            );
            this.camera.position.z = 5;
            
            // Renderer setup
            this.renderer = new THREE.WebGLRenderer({ antialias: true });
            this.renderer.setSize(container.clientWidth, container.clientHeight);
            this.renderer.shadowMap.enabled = true;
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(this.renderer.domElement);
            
            // Create gemstone (octahedron for diamond-like shape)
            const geometry = new THREE.OctahedronGeometry(1.5, 2);
            const material = new THREE.MeshPhongMaterial({
                color: 0xd4af37,
                shininess: 100,
                transparent: true,
                opacity: 0.8
            });
            
            this.gemstone = new THREE.Mesh(geometry, material);
            this.gemstone.castShadow = true;
            this.scene.add(this.gemstone);
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            this.scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            directionalLight.castShadow = true;
            this.scene.add(directionalLight);
            
            const pointLight = new THREE.PointLight(0xd4af37, 0.5);
            pointLight.position.set(-5, 3, 2);
            this.scene.add(pointLight);
            
            // Controls
            this.setupThreeJSControls();
            
            // Start animation
            this.animate();
            
        } catch (error) {
            console.error('Three.js initialization failed:', error);
            container.innerHTML = '<div class="error">3D viewer not available: ' + error.message + '</div>';
        }
    }
    
    setupThreeJSControls() {
        const rotateLeft = document.getElementById('rotateLeft');
        const rotateRight = document.getElementById('rotateRight');
        const zoomIn = document.getElementById('zoomIn');
        const zoomOut = document.getElementById('zoomOut');
        
        rotateLeft?.addEventListener('click', () => {
            if (this.gemstone) {
                this.gemstone.rotation.y -= 0.2;
            }
        });
        
        rotateRight?.addEventListener('click', () => {
            if (this.gemstone) {
                this.gemstone.rotation.y += 0.2;
            }
        });
        
        zoomIn?.addEventListener('click', () => {
            if (this.camera) {
                this.camera.position.z = Math.max(2, this.camera.position.z - 0.5);
            }
        });
        
        zoomOut?.addEventListener('click', () => {
            if (this.camera) {
                this.camera.position.z = Math.min(10, this.camera.position.z + 0.5);
            }
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.scene && this.camera && this.renderer) {
            // Auto-rotate gemstone
            if (this.gemstone) {
                this.gemstone.rotation.x += 0.005;
                this.gemstone.rotation.y += 0.01;
            }
            
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    setupEventListeners() {
        // Handle window resize
        window.addEventListener('resize', () => {
            if (this.camera && this.renderer) {
                const container = document.getElementById('threejs-container');
                if (container) {
                    this.camera.aspect = container.clientWidth / container.clientHeight;
                    this.camera.updateProjectionMatrix();
                    this.renderer.setSize(container.clientWidth, container.clientHeight);
                }
            }
        });
        
        // AR Button
        const arButton = document.getElementById('arButton');
        arButton?.addEventListener('click', () => {
            this.startAR();
        });
    }
    
    startAR() {
        if (!navigator.xr) {
            alert('WebXR not supported on this device');
            return;
        }
        
        // Placeholder for AR implementation
        console.log('Starting AR experience...');
        document.getElementById('arStatus').textContent = 'AR mode activated';
    }
    
    setupAI() {
        const identifyButton = document.getElementById('identifyButton');
        const fileInput = document.getElementById('gemImage');
        const resultDiv = document.getElementById('identificationResult');
        
        identifyButton?.addEventListener('click', async () => {
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<div class="error">Please select an image</div>';
                return;
            }
            
            resultDiv.innerHTML = '<div class="loading">Analyzing image...</div>';
            
            try {
                // Placeholder AI implementation
                await this.analyzeGemstone(fileInput.files[0]);
            } catch (error) {
                resultDiv.innerHTML = '<div class="error">Analysis failed: ' + error.message + '</div>';
            }
        });
    }
    
    async analyzeGemstone(file) {
        const resultDiv = document.getElementById('identificationResult');
        
        // Simulate AI analysis
        setTimeout(() => {
            const gemstones = ['Diamond', 'Ruby', 'Sapphire', 'Emerald', 'Topaz'];
            const randomGem = gemstones[Math.floor(Math.random() * gemstones.length)];
            const confidence = Math.floor(Math.random() * 30) + 70;
            
            resultDiv.innerHTML = `
                <div class="success">
                    <h3>Identified: ${randomGem}</h3>
                    <p>Confidence: ${confidence}%</p>
                    <p>Properties: Hardness 7-10, Crystal system: Hexagonal</p>
                </div>
            `;
        }, 2000);
    }
    
    setupNFT() {
        const mintButton = document.getElementById('mintNFT');
        const statusDiv = document.getElementById('nftStatus');
        
        mintButton?.addEventListener('click', async () => {
            statusDiv.innerHTML = '<div class="loading">Minting NFT...</div>';
            
            try {
                // Placeholder NFT minting
                await this.mintNFT();
            } catch (error) {
                statusDiv.innerHTML = '<div class="error">Minting failed: ' + error.message + '</div>';
            }
        });
    }
    
    async mintNFT() {
        const statusDiv = document.getElementById('nftStatus');
        
        // Simulate NFT minting
        setTimeout(() => {
            const tokenId = Math.random().toString(36).substr(2, 9);
            statusDiv.innerHTML = `
                <div class="success">
                    <h3>NFT Minted Successfully!</h3>
                    <p>Token ID: ${tokenId}</p>
                    <p>Contract: 0x1234...5678</p>
                    <p><a href="#" target="_blank">View on OpenSea</a></p>
                </div>
            `;
        }, 3000);
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    new GemDistrictApp();
});'''
    
    with open("gemdistrict.art/js/main.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("✅ Created: gemdistrict.art/js/main.js")

def create_service_worker():
    """Create service worker for PWA functionality"""
    sw_content = '''const CACHE_NAME = 'gemdistrict-v1';
const urlsToCache = [
  '/',
  '/css/style.css',
  '/js/main.js',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

// Install service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});

// Activate service worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});'''
    
    with open("gemdistrict.art/js/service-worker.js", "w", encoding="utf-8") as f:
        f.write(sw_content)
    print("✅ Created: gemdistrict.art/js/service-worker.js")

def create_manifest():
    """Create PWA manifest.json"""
    manifest = {
        "name": "GemDistrict Art - AI Gemstone & AR Experience",
        "short_name": "GemDistrict",
        "description": "AI-powered gemstone analysis with immersive AR/VR experiences",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#d4af37",
        "orientation": "portrait",
        "icons": [
            {
                "src": "/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "categories": ["entertainment", "education"],
        "lang": "en"
    }
    
    with open("gemdistrict.art/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("✅ Created: gemdistrict.art/manifest.json")

def create_placeholder_icons():
    """Create placeholder icon files"""
    import base64
    
    # 1x1 transparent PNG (placeholder)
    icon_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
    
    with open("gemdistrict.art/icons/icon-192.png", "wb") as f:
        f.write(icon_data)
    
    with open("gemdistrict.art/icons/icon-512.png", "wb") as f:
        f.write(icon_data)
    
    print("✅ Created placeholder icons")

def main():
    """Main function to create complete website structure"""
    print("🤖 Fix-It Bot starting...")
    print("📝 Creating complete GemDistrict Art website structure...")
    
    try:
        # Create all directories
        ensure_directory_structure()
        
        # Create all files
        create_index_html()
        create_css()
        create_javascript()
        create_service_worker()
        create_manifest()
        create_placeholder_icons()
        
        print("\n🎉 Website structure created successfully!")
        print(f"\n📁 Files created in: gemdistrict.art/")
        print("\n🚀 Next steps:")
        print("1. Replace placeholder icons with actual gem icons")
        print("2. Test the website locally by opening index.html")
        print("3. Deploy to GitHub Pages")
        print("4. Add real AI model for gemstone identification")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Fix-It Bot encountered an error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
git checkout main
# Replace the workflow file with the fixed version
git add .github/workflows/main.yml
git commit -m "🐛 Fix GitHub Actions workflow syntax"
git push origin main
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

#!/usr/bin/env python3# 1. Remove the broken workflow
rm -f .github/workflows/main.yml

# 2. Create the new working workflow
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml << 'EOF'
name: 🚀 Deploy GemDistrict Art to Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout repository
      uses: actions/checkout@v4

    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: 🏗️ Build website with Python
      run: |
        python create-structure-bot.py
        
    - name: 📁 List generated files
      run: |
        echo "=== Generated files ==="
        find . -type f -name "*.html" -o -name "*.css" -o -name "*.js" | head -20
        echo "=== Directory structure ==="
        ls -la

    - name: 🔧 Fix file permissions
      run: |
        chmod -R 755 .
        
    - name: 📤 Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    
    steps:
    - name: 🌐 Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
EOF

# 3. Ensure your Python script exists
if [ ! -f "create-structure-bot.py" ]; then
    echo "❌ create-structure-bot.py not found!"
    exit 1
fi

# 4. Commit and push the fix
git add .github/workflows/deploy.yml
git rm .github/workflows/main.yml 2>/dev/null || true
git commit -m "🔧 Fix GitHub Actions workflow - deploy to Pages"
git push origin main
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
            print("ℹ️  Žádné změny k commitnutí.")name: 🚀 Main Workflow - Fix and Deploy Website

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
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: 🧰 Install dependencies
      run: |
        pip install requests

    - name: 🤖 Run Fix-It Bot
      run: |
        python Fix-it-bot.py

    - name: 💾 Commit and push fixes (if any)
      run: |
        git config --global user.name "FixBot"
        git config --global user.email "fixbot@users.noreply.github.com"
        git add .
        if ! git diff --cached --quiet; then
          git commit -m "🤖 Auto-fix: everything fixed"
          git push
          echo "✅ Changes committed and pushed."
        else
          echo "ℹ️ No changes to commit."
        fi

    - name: 🗃️ Prepare artifact for Pages
      uses: actions/upload-pages-artifact@v3
      with:
        path: './'

    - name: 🌐 Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2

  # Optional: Additional job for testing
  test:
    runs-on: ubuntu-latest
    needs: build-and-deploy
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4
      
    - name: 🔍 Validate HTML
      run: |
        pip install html5validator
        html5validator --root . --ignore-re '.*\.git.*'
        
    - name: 🔍 Check PWA manifest
      run: |
        if [ ! -f "manifest.json" ]; then
          echo "❌ manifest.json missing"
          exit 1
        fi
        echo "✅ manifest.json found"
        
    - name: 🔍 Verify service worker
      run: |
        if [ ! -f "js/service-worker.js" ]; then
          echo "❌ service-worker.js missing"
          exit 1
        fi
        echo "✅ service-worker.js found"
    else:
        print("\nℹ️  Pro commit a push spusť: git add . && git commit -m '...' && git push")
