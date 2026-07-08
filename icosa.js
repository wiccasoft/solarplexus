// =============================================================
// PARÇA 1: TEMEL KURULUM, EKSENLER, BUTONLAR VE ICOSAHEDRON (20 FACE)
// =============================================================

// 1. Sahne, Kamera ve WebGL Renderer Kurulumu
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050505, 0.015);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(4, 4, 6); // Çapraz perspektif başlangıç açısı

const renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

// 2. İnteraktif Kontroller (DÖNME KAPATILDI - Pan, Zoom ve Orbit Serbest)
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = true; 

// 3. Merkez Koordinat Sistemi (AxesHelper - İstenen Eksen Göstergesi)
// Kırmızı: X ekseni, Yeşil: Y ekseni, Mavi: Z ekseni
const axesHelper = new THREE.AxesHelper(3);
scene.add(axesHelper);

// Tüm Modelleri İçine Alacak Ana Geometri Grubu
const geometryGroup = new THREE.Group();
scene.add(geometryGroup);

// Altın Oran Sabiti
const phi = (1 + Math.sqrt(5)) / 2;

// -------------------------------------------------------------
// A) EN DIŞTAKİ ICOSAHEDRON (YEŞİL) - Tam 20 Üçgen Yüzey (Detail=0)
// -------------------------------------------------------------
const icoVerticesCorrected = [
    -1, phi, 0,   1, phi, 0,   -1, -phi, 0,   1, -phi, 0,
     0, -1, phi,  0, 1, phi,    0, -1, -phi,  0, 1, -phi,
     phi, 0, -1,  phi, 0, 1,   -phi, 0, -1,  -phi, 0, 1
];

const icoIndices = [
    0, 11, 5,    0, 5, 1,     0, 1, 7,     0, 7, 10,    0, 10, 11,
    1, 5, 9,     5, 11, 4,    11, 10, 2,   10, 7, 6,    7, 1, 8,
    3, 9, 4,     3, 4, 2,     3, 2, 6,     3, 6, 8,     3, 8, 9,
    4, 9, 5,     2, 4, 11,    6, 2, 10,    8, 6, 7,     9, 8, 1
];

const icoGeom = new THREE.BufferGeometry();
icoGeom.setAttribute('position', new THREE.Float32BufferAttribute(icoVerticesCorrected, 3));
icoGeom.setIndex(icoIndices);
icoGeom.computeVertexNormals();

const icoMat = new THREE.MeshBasicMaterial({ 
    color: 0x00ff00, 
    wireframe: true, 
    transparent: true, 
    opacity: 0.25 
});
const icoMesh = new THREE.Mesh(icoGeom, icoMat);
geometryGroup.add(icoMesh);

// 4. Kamera Açı Butonları İçin Akıcı Geçiş Motoru (changeView)
let isAnimating = false;
let targetPos = new THREE.Vector3();

function changeView(viewType) {
    isAnimating = true;
    if (viewType === 'top') {
        targetPos.set(0, 7.5, 0.001); // Mandala (Üst) Görünümü
    } else if (viewType === 'bottom') {
        targetPos.set(0, -7.5, 0.001); // Alt Görünüm
    } else if (viewType === 'reset') {
        targetPos.set(4, 4, 6); // Perspektif Görünüm
    }
}
window.changeView = changeView; // HTML butonlarının tetikleyebilmesi için global'e bağlama


// =============================================================
// PARÇA 2: ORTADAKİ KÜP VE VECTOR EQUILIBRIUM (CUB_OCTAHEDRON)
// =============================================================

// -------------------------------------------------------------
// B) ORTADAKİ KÜP (SARI)
// -------------------------------------------------------------
const cubeGeom = new THREE.BoxGeometry(2, 2, 2);
const cubeEdges = new THREE.EdgesGeometry(cubeGeom);
const cubeMat = new THREE.LineBasicMaterial({ 
    color: 0xffff00, 
    transparent: true, 
    opacity: 0.4 
});
const cubeLine = new THREE.LineSegments(cubeEdges, cubeMat);
geometryGroup.add(cubeLine);

// -------------------------------------------------------------
// C) VECTOR EQUILIBRIUM (MOR / CUB_OCTAHEDRON)
// -------------------------------------------------------------
// Küpün kenar orta noktaları ile oluşturulan 12 köşe
const veVertices = [
     1,  1,  0, 1, -1,  0, -1,  1,  0, -1, -1,  0,
     1,  0,  1, 1,  0, -1, -1,  0,  1, -1,  0, -1,
     0,  1,  1, 0,  1, -1, 0, -1,  1,  0, -1, -1
];

// Hexagon, Üçgen ve Kare yüzeyler için indeks haritası
const veIndices = [
    0, 4, 8, 0, 8, 9, 0, 9, 5, 0, 5, 1, 0, 1, 4,
    2, 8, 6, 2, 9, 8, 2, 7, 9, 2, 3, 7, 2, 6, 3,
    1, 5, 11, 1, 11, 10, 1, 10, 4, 3, 11, 7, 3, 10, 11,
    3, 6, 10, 4, 10, 8, 6, 8, 10, 5, 9, 11, 7, 11, 9
];

const veGeom = new THREE.BufferGeometry();
veGeom.setAttribute('position', new THREE.Float32BufferAttribute(veVertices, 3));
veGeom.setIndex(veIndices);
veGeom.computeVertexNormals();

const veMat = new THREE.MeshBasicMaterial({ 
    color: 0xaa00ff, 
    wireframe: true, 
    transparent: true, 
    opacity: 0.5 
});
const veMesh = new THREE.Mesh(veGeom, veMat);
geometryGroup.add(veMesh);


// =============================================================
// PARÇA 3: İÇTEKİ İÇ İÇE GEÇMİŞ TETRAHEDRONLAR (MAVİ & KIRMIZI)
// =============================================================
const tetraIndices = [0, 1, 2,   0, 2, 3,   0, 3, 1,   1, 3, 2];

// Fonksiyon: Tetrahedron ve Kaplamasını Oluştur
function createTetrahedron(verts, color, group) {
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
    geom.setIndex(tetraIndices);
    geom.computeVertexNormals();

    const matWire = new THREE.MeshBasicMaterial({ color, wireframe: true, transparent: true, opacity: 0.6 });
    const matSolid = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.05, side: THREE.DoubleSide });
    
    group.add(new THREE.Mesh(geom, matWire), new THREE.Mesh(geom, matSolid));
}

// 1. TETRAHEDRON (MAVİ)
createTetrahedron([1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1], 0x00aaff, geometryGroup);

// 2. TETRAHEDRON (KIRMIZI)
createTetrahedron([1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1], 0xff3333, geometryGroup);

// =============================================================
// PARÇA 4: MERKEZDEKİ OCTAHEDRON VE ARKA PLAN YILDIZ PARÇACIKLARI
// =============================================================

// E) EN MERKEZDEKİ OCTAHEDRON (CYAN / TURKUAZ)
const octaVertices = [1, 0, 0, -1, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 1, 0, 0, -1];
const octaIndices = [0, 2, 4, 0, 4, 3, 0, 3, 5, 0, 5, 2, 1, 2, 5, 1, 5, 3, 1, 3, 4, 1, 4, 2];
const octaGeom = new THREE.BufferGeometry();
// ... (Geometri oluşturma kodları)

const octaMat = new THREE.MeshBasicMaterial({ color: 0x00ffff, wireframe: true });
const octaMesh = new THREE.Mesh(octaGeom, octaMat);
const octaFaceMat = new THREE.MeshBasicMaterial({ color: 0x00ffff, transparent: true, opacity: 0.15, side: THREE.DoubleSide });
const octaSolid = new THREE.Mesh(octaGeom, octaFaceMat);
geometryGroup.add(octaMesh, octaSolid);

// F) ARKA PLAN YILDIZ PARÇACIKLARI
// ... (Yıldız parçacıkları oluşturma kodları)
const starParticles = new THREE.Points(starsGeom, new THREE.PointsMaterial({color: 0xffffff, size: 0.08, transparent: true, opacity: 0.5}));
scene.add(starParticles);
