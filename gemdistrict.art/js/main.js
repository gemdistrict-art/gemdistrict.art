class GemDistrictApp {
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
});