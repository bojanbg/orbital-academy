// SETUP SCENE + CAMERA

var width = window.innerWidth,
    height = window.innerHeight;

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 45, width / height, 0.01, 1000 );
camera.position.z = 1.5;

var renderer = new THREE.WebGLRenderer();
renderer.setSize( width, height );
document.body.appendChild( renderer.domElement );

// EARTH

var geometry = new THREE.SphereGeometry(0.5, 32, 32);
var material = new THREE.MeshPhongMaterial();
// var material = new THREE.MeshBasicMaterial();
// material.map = THREE.ImageUtils.loadTexture('images/earth/earth_no_clouds_8k.jpg');
material.map = THREE.ImageUtils.loadTexture('images/earthmap1k.jpg');
// material.map = THREE.ImageUtils.loadTexture('images/earth/nasa-earth-small.png');
material.bumpMap = THREE.ImageUtils.loadTexture('images/earthbump1k.jpg');
material.bumpScale = 0.01;
material.specularMap = THREE.ImageUtils.loadTexture('images/earthspec1k.jpg');
material.specular  = new THREE.Color('grey');
var earthMesh = new THREE.Mesh(geometry, material);
scene.add(earthMesh);

// LIGHT

scene.add(new THREE.AmbientLight(0x333333));

var directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5,3,5);
scene.add(directionalLight);

// CONTROLS

var controls = new THREE.TrackballControls(camera);

// RENDER FUNCTION

function render() {
  controls.update();
  requestAnimationFrame(render);
  renderer.render(scene, camera);
  // earthMesh.rotation.x += 0.01;
  // earthMesh.rotation.y += 0.01;
}

render();
