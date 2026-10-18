import * as THREE from 'three';
import {OrbitControls} from '../vendor/OrbitControls.js';
const C={wood:0xE8C99A,thin:0xEDD3A8,jute:0xC9AE7C,acc:0xD9502B,sage:0xBFCDBF};
export function viewer(el,M){
 const r=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});r.setPixelRatio(Math.min(devicePixelRatio,2));
 const W=()=>el.clientWidth,H=()=>el.clientHeight;r.setSize(W(),H());el.appendChild(r.domElement);
 const sc=new THREE.Scene();sc.add(new THREE.HemisphereLight(0xffffff,0xA9B5AF,1.8));const dl=new THREE.DirectionalLight(0xffffff,1.5);dl.position.set(1,2,1.6).multiplyScalar(2000);sc.add(dl);
 const S=M.size,cx=S[0]/2,cy=S[1]/2,cz=S[2]/2,R=Math.max(...S);
 const cam=new THREE.PerspectiveCamera(32,W()/H(),10,20000);cam.position.set(cx+R*1.6,cy+R*1.0,cz+R*2.9);
 const ctl=new OrbitControls(cam,r.domElement);ctl.target.set(cx,cy*0.9,cz);ctl.enableDamping=true;ctl.update();
 const fl=new THREE.Mesh(new THREE.CircleGeometry(R*1.2,48),new THREE.MeshLambertMaterial({color:0xE9EDE8}));fl.rotation.x=-Math.PI/2;fl.position.set(cx,-1,cz);sc.add(fl);
 const em=new THREE.LineBasicMaterial({color:0x1F2A2E,transparent:true,opacity:.45});const meshes={};
 for(const p of M.parts){const [x,y,z,w,h,d]=p.b;const base=p.jute?C.jute:(p.t===5?C.thin:C.wood);const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color:base,roughness:.85}));m.userData.base=base;
  m.position.set(x+w/2,y+h/2,z+d/2);m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry),em));sc.add(m);(meshes[p.id]=meshes[p.id]||[]).push(m)}
 const firstStep={};M.steps.forEach((s,k)=>(s.n||[]).forEach(n=>{if(!(n in firstStep))firstStep[n]=k}));
 // pieza que solo se prepara (sin "n") antes de colocarse: aparece en el paso donde se coloca
 const placeStep={};const asm=M.steps.map((s,k)=>s.n.length&&k>0?k:-1);
 for(const id in meshes){let k=firstStep[id];M.steps.forEach((s,j)=>{if(s.n.includes(id)&&j>0)k=j});placeStep[id]=k===undefined?0:k}
 function step(i){for(const [id,ms] of Object.entries(meshes)){const k=placeStep[id];
   ms.forEach(m=>{const vis=i<0||k<=i||(M.steps[i]&&M.steps[i].f.includes(id));m.visible=vis;
    const now=i>=0&&(k===i||M.steps[i].f.includes(id));m.material.color.setHex(i<0?m.userData.base:now?C.acc:C.sage);m.material.opacity=1})}}
 step(-1);
 (function loop(){requestAnimationFrame(loop);ctl.update();r.render(sc,cam)})();
 new ResizeObserver(()=>{r.setSize(W(),H());cam.aspect=W()/H();cam.updateProjectionMatrix()}).observe(el);
 return {step};
}
