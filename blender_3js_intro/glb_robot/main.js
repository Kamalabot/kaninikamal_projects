import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

// --- Scene ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

// --- Camera ---
const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(0, 2, 5);

// --- Renderer ---
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
document.body.appendChild(renderer.domElement);

// --- Controls ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// --- Lights ---
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
scene.add(directionalLight);

// --- GLTF Loader ---
const loader = new GLTFLoader();

loader.load(
  // Path to your model (make sure it’s in the same folder or adjust path)
  "./robot_on_wheel.glb",

  // onLoad callback
  (gltf) => {
    const model = gltf.scene;
    model.scale.set(1.5, 1.5, 1.5);
    scene.add(model);
    console.log("✅ Model loaded:", model);
  },

  // onProgress callback
  (xhr) => {
    console.log(`Loading: ${(xhr.loaded / xhr.total) * 100}% loaded`);
  },

  // onError callback
  (error) => {
    console.error("❌ Error loading model:", error);
  }
);

// --- Animation Loop ---
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

// --- Resize Handler ---
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- Zoom Controls ---
const increaseBtn = document.getElementById("increase");
const decreaseBtn = document.getElementById("decrease");

increaseBtn.addEventListener("click", () => (camera.position.z -= 0.5));
decreaseBtn.addEventListener("click", () => (camera.position.z += 0.5));