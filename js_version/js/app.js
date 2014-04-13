// SETUP SCENE + CAMERA

var width = window.innerWidth,
    height = window.innerHeight;

var tangent = new THREE.Vector3();
var axis = new THREE.Vector3();
var up = new THREE.Vector3(0, 1, 0);

var orbit, orbitPath, points, line;

var counter = 0;

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 45, width / height, 0.01, 1000 );
camera.position.z = 60;

var renderer = new THREE.WebGLRenderer();
renderer.setSize( width, height );
document.body.appendChild( renderer.domElement );

// EARTH

var geometry = new THREE.SphereGeometry(15, 32, 32);
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

// ORBITS

/* --------
Orbital parameters:
        a = semi-major axis
        e = eccentricity [0, +inf)
        w = argument of periapsis [0 deg, 360 deg) [ line.rotation.y ]
        i = inclination [0 deg, 180 deg) [ line.rotation.z ]
        o = longitude of ascending node [0 deg, 360 deg)
----------- */

function createOrbit(semiMajorAxis, eccentricity, periapsisArg, inclination) {
  var semiMinorAxis = semiMajorAxis*Math.sqrt(1- Math.pow(eccentricity, 2));
  var translation = semiMajorAxis * eccentricity;

  var lineMaterial = new THREE.LineBasicMaterial({ color:696969, opacity:1 });
  orbit = new THREE.EllipseCurve(translation, 0, semiMajorAxis, semiMinorAxis, 0, 2.0 * Math.PI, false);
  orbitPath = new THREE.CurvePath();
  orbitPath.add(orbit);
  var ellipseGeometry = orbitPath.createPointsGeometry(128);
  ellipseGeometry.computeTangents();
  points = orbit.getPoints(100);
  line = new THREE.Line(ellipseGeometry, lineMaterial);
  line.rotation.x = Math.PI/2;
  line.rotation.z = Math.radians( inclination );
  line.rotation.y = Math.radians( periapsisArg );

  scene.add( line );

}

var boxMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
var boxGeometry = new THREE.CubeGeometry(1, 1, 1);
var box = new THREE.Mesh(boxGeometry, boxMaterial);

scene.add(box);

// CONTROLS

var controls = new THREE.TrackballControls(camera);

// HELPER FUNCTIONS

Math.radians = function(degrees) {
  return degrees * Math.PI / 180;
};

function moveBox() {
    var currentPoint = points[counter];
    var vector = new THREE.Vector3( currentPoint.x, currentPoint.y, 0 );
    var axis = new THREE.Vector3( 1, 0, 0 );
    var angle = Math.PI / 2;
    var matrix = new THREE.Matrix4().makeRotationAxis( axis, angle );
    vector.applyMatrix4( matrix );

    box.position = vector;
    counter += 1;
    if(counter > 99) { counter = 0; }
}

var sky = new THREE.Mesh(
  new THREE.SphereGeometry(90, 64, 64),
  new THREE.MeshBasicMaterial({
    map: THREE.ImageUtils.loadTexture('images/galaxy_starfield.png'),
    side: THREE.BackSide
  })
);

scene.add( sky );

// RENDER FUNCTION

function render() {
  controls.update();
  earth.rotation.y += 0.001;
  requestAnimationFrame(render);
  renderer.render(scene, camera);
}

createOrbit(32, 0.5, 0, 0);
setInterval(moveBox, 100);
render();
