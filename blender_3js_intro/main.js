import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";
import { OrbitControls } from "https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js";

// --- Scene setup ---
const scene = new THREE.Scene();

// --- Camera setup ---
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.z = 3;

// --- Renderer setup ---
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// --- OrbitControls setup ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// --- Cube geometry and material ---
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({
  color: 0x0077ff,
  roughness: 0.4,
  metalness: 0.6,
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// --- Lighting ---
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 1);
pointLight.position.set(2, 2, 2);
scene.add(pointLight);

// --- Animation loop ---
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
animate();

// --- Responsive resize ---
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- Cube resizing controls ---
const increaseBtn = document.getElementById("increase");
const decreaseBtn = document.getElementById("decrease");

let currentScale = 1;

increaseBtn.addEventListener("click", () => {
  currentScale += 0.1;
  cube.scale.set(currentScale, currentScale, currentScale);
});

decreaseBtn.addEventListener("click", () => {
  currentScale = Math.max(0.1, currentScale - 0.1);
  cube.scale.set(currentScale, currentScale, currentScale);
});
