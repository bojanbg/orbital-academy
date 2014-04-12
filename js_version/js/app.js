// SETUP SCENE + CAMERA

var width = window.innerWidth,
    height = window.innerHeight;

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 45, width / height, 0.01, 1000 );
camera.position.z = 5;

var renderer = new THREE.WebGLRenderer();
renderer.setSize( width, height );
document.body.appendChild( renderer.domElement );

// EARTH

var geometry = new THREE.SphereGeometry(1, 32, 32);
var material = new THREE.MeshPhongMaterial();

material.map = THREE.ImageUtils.loadTexture('images/no_clouds_4k.jpg');
material.bumpMap = THREE.ImageUtils.loadTexture('images/elev_bump_4k.jpg');
material.bumpScale = 0.005;
material.specularMap = THREE.ImageUtils.loadTexture('images/water_4k.png');
material.specular = new THREE.Color('grey');

var earth = new THREE.Mesh(geometry, material);
scene.add(earth);

// LIGHT

scene.add(new THREE.AmbientLight(0x333333));

var directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5,3,5);
scene.add(directionalLight);

// CIRCLE

/* --------
Orbital parameters:
        a = semi-major axis
        e = eccentricity [0, +inf)
        w = argument of periapsis [0 deg, 360 deg) [ line.rotation.z ]
        i = inclination [0 deg, 180 deg) [ line.rotation.y ]
        o = longitude of ascending node [0 deg, 360 deg)
----------- */

// var circleMaterial = new THREE.MeshBasicMaterial({ color: 0x0000ff, wireframe: true });
// var radius = 5;
// var segments = 32;

// var circleGeometry = new THREE.CircleGeometry( radius, segments );
// var circle = new THREE.Mesh( circleGeometry, circleMaterial );
// scene.add(circle);

// var ringGeometry = new THREE.RingGeometry(1.5, 1.505, 128);
// var ringMaterial = new THREE.MeshBasicMaterial({ color: 0x0000fa, side: THREE.DoubleSide });
// var ring = new THREE.Mesh( ringGeometry, ringMaterial );
// scene.add(ring);

function createOrbit(semiMajorAxis, eccentricity, periapsisArg, inclination) {
  var semiMinorAxis = semiMajorAxis*Math.sqrt(1- Math.pow(eccentricity, 2));
  var translation = semiMajorAxis * eccentricity;

  var lineMaterial = new THREE.LineBasicMaterial({ color:0x0000ff, opacity:1 });
  var ellipse = new THREE.EllipseCurve(translation, 0, semiMajorAxis, semiMinorAxis, 0, 2.0 * Math.PI, false);
  var ellipsePath = new THREE.CurvePath();
  ellipsePath.add(ellipse);
  var ellipseGeometry = ellipsePath.createPointsGeometry(128);
  ellipseGeometry.computeTangents();
  var line = new THREE.Line(ellipseGeometry, lineMaterial);
  line.rotation.x = Math.PI/2;
  scene.add( line );
}

// var lineGeometry = new THREE.Geometry();
// lineGeometry.vertices.push(new THREE.Vector3(-5, 0, 0));
// lineGeometry.vertices.push(new THREE.Vector3(0, 5, 0));
// lineGeometry.vertices.push(new THREE.Vector3(5, 0, 0));
// lineGeometry.vertices.push(new THREE.Vector3(0, -5, 0));
// lineGeometry.vertices.push(new THREE.Vector3(-5, 0, 0));

// var newLine = new THREE.Line( lineGeometry, lineMaterial );
// scene.add( newLine );

// CONTROLS

var controls = new THREE.TrackballControls(camera);

// RENDER FUNCTION

function render() {
  controls.update();
  earth.rotation.y += 0.001;
  requestAnimationFrame(render);
  renderer.render(scene, camera);
}

render();
createOrbit(2.5, 0.5);
