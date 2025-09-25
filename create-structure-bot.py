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
print(f"\n📁 Složka: {ROOT.absolute()}")#!/usr/bin/env python3
import os
from pathlib import Path
import base64
import json

# Create root directory
ROOT = Path("gemdistrict.art")
ROOT.mkdir(exist_ok=True)

# 1. Create complete index.html with all features
index_html = '''<!DOCTYPE html>
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

(ROOT / "index.html").write_text(index_html, encoding="utf-8")
print("✅ Created: index.html")

# 2. Create complete CSS with dark mode and responsive design
css_dir = ROOT / "css"
css_dir.mkdir(exist_ok=True)

style_css = '''/* CSS Variables for theming */
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

(css_dir / "style.css").write_text(style_css, encoding="utf-8")
print("✅ Created: css/style.css")

# 3. Create complete JavaScript with all features
js_dir = ROOT / "js"
js_dir.mkdir(exist_ok=True)

main_js = '''class GemDistrictApp {
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

(js_dir / "main.js").write_text(main_js, encoding="utf-8")
print("✅ Created: js/main.js")

# 4. Create service worker for PWA
service_worker_js = '''const CACHE_NAME = 'gemdistrict-v1';
const urlsToCache = [
  '/',
  '/css/style.css',
  '/js/main.js',
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

// Update service worker
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

(js_dir / "service-worker.js").write_text(service_worker_js, encoding="utf-8")
print("✅ Created: js/service-worker.js")

# 5. Create manifest.json for PWA
manifest_json = {
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

with open(ROOT / "manifest.json", "w", encoding="utf-8") as f:
  json.dump(manifest_json, f, indent=2)
print("✅ Created: manifest.json")

# 6. Create icons directory and placeholder icons
icons_dir = ROOT / "icons"
icons_dir.mkdir(exist_ok=True)

# Create 192x192 icon (placeholder - in real app, use actual gem icon)
icon_192_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
icon_192_data = base64.b64decode(icon_192_b64)
(icons_dir / "icon-192.png").write_bytes(icon_192_data)
print("✅ Created: icons/icon-192.png")

# Create 512x512 icon
(icons_dir / "icon-512.png").write_bytes(icon_192_data)
print("✅ Created: icons/icon-512.png")

print("\n🎉 Enhanced GemDistrict Art structure created successfully!")
print(f"\n📁 Directory: {ROOT.absolute()}")
print("\n🚀 Next steps:")
print("1. Replace placeholder icons with actual gem icons")
print("2. Add real AI model for gemstone identification")
print("3. Implement real NFT minting")
print("4. Test PWA functionality")
print("5. Deploy to web server")
'''

# Run the improved script
exec(enhanced_script)
