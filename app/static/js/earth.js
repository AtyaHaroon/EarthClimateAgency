// earth.js
let scene, camera, renderer, earth, clouds;

function initEarth() {
  // Create scene
  scene = new THREE.Scene();
  scene.background = null; // Transparent background
  
  // Create camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 2.1;
  
  // Create renderer
  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(document.getElementById('earth-container').clientWidth, document.getElementById('earth-container').clientHeight);
  document.getElementById('earth-container').appendChild(renderer.domElement);
  
  // Add ambient light
  const ambientLight = new THREE.AmbientLight(0x333333);
  scene.add(ambientLight);
  
  // Add directional light
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 3, 5);
  scene.add(directionalLight);
  
  // Create Earth
  const earthGeometry = new THREE.SphereGeometry(1, 64, 64);
  const earthMaterial = new THREE.MeshPhongMaterial({
    map: new THREE.TextureLoader().load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_atmos_2048.jpg'),
    bumpMap: new THREE.TextureLoader().load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_normal_2048.jpg'),
    bumpScale: 0.05,
    specularMap: new THREE.TextureLoader().load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_specular_2048.jpg'),
    specular: new THREE.Color('darkgrey'),
    shininess: 5
  });
  
  earth = new THREE.Mesh(earthGeometry, earthMaterial);
  scene.add(earth);
  
  // Create clouds
  const cloudGeometry = new THREE.SphereGeometry(1.01, 64, 64);
  const cloudMaterial = new THREE.MeshPhongMaterial({
    map: new THREE.TextureLoader().load('https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_clouds_1024.png'),
    transparent: true,
    opacity: 0.4
  });
  
  clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
  scene.add(clouds);
  
  // Add stars
  const starsGeometry = new THREE.BufferGeometry();
  const starsMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.05,
    transparent: true
  });
  
  const starsVertices = [];
  for (let i = 0; i < 1000; i++) {
    const x = (Math.random() - 0.5) * 2000;
    const y = (Math.random() - 0.5) * 2000;
    const z = (Math.random() - 0.5) * 2000;
    starsVertices.push(x, y, z);
  }
  
  starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
  const stars = new THREE.Points(starsGeometry, starsMaterial);
  scene.add(stars);
  
  // Handle window resize
  window.addEventListener('resize', onWindowResize);
  
  // Start animation
  animate();
}

function onWindowResize() {
  camera.aspect = document.getElementById('earth-container').clientWidth / document.getElementById('earth-container').clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(document.getElementById('earth-container').clientWidth, document.getElementById('earth-container').clientHeight);
}

function animate() {
  requestAnimationFrame(animate);
  
  // Rotate Earth and clouds
  earth.rotation.y += 0.001;
  clouds.rotation.y += 0.0015;
  
  renderer.render(scene, camera);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('earth-container')) {
    initEarth();
  }
});