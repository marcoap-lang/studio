import * as THREE from 'three';
import {OrbitControls} from '../vendor/OrbitControls.js';
const C={wood:0xE8C99A,edge:0xD9502B,jute:0xC9AE7C,thin:0xEDD3A8};
export function viewer(el,M,{onStep}={}){
 const r=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});r.setPixelRatio(Math.min(devicePixelRatio,2));
 const W=()=>el.clientWidth,H=()=>el.clientHeight;r.setSize(W(),H());el.appendChild(r.domElement);
 const sc=new THREE.Scene();sc.add(new THREE.HemisphereLight(0xffffff,0xA9B5AF,1.8));const dl=new THREE.DirectionalLight(0xffffff,1.5);dl.position.set(1,2,1.6).multiplyScalar(2000);sc.add(dl);
 const S=M.size,cx=S[0]/2,cy=S[1]/2,cz=S[2]/2,R=Math.max(...S);
 const cam=new THREE.PerspectiveCamera(32,W()/H(),10,20000);cam.position.set(cx+R*1.6,cy+R*1.0,cz+R*2.9);
 const ctl=new OrbitControls(cam,r.domElement);ctl.target.set(cx,cy*0.9,cz);ctl.enableDamping=true;ctl.update();
 const fl=new THREE.Mesh(new THREE.CircleGeometry(R*1.2,48),new THREE.MeshLambertMaterial({color:0xE9EDE8}));fl.rotation.x=-Math.PI/2;fl.position.set(cx,-1,cz);sc.add(fl);
 const em=new THREE.LineBasicMaterial({color:0x1F2A2E,transparent:true,opacity:.45});const meshes={};
 for(const p of M.parts){const [x,y,z,w,h,d]=p.b;const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color:p.jute?C.jute:(p.t===5?C.thin:C.wood),roughness:.85}));
  m.position.set(x+w/2,y+h/2,z+d/2);m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry),em));sc.add(m);(meshes[p.id]=meshes[p.id]||[]).push(m)}
 function step(i){ // i<0 => terminado
  const seen=new Set();M.steps.forEach((s,k)=>{if(i<0||k<=i)(s.n||[]).forEach(n=>seen.add(n))});
  const cur=new Set(i>=0?(M.steps[i].n||[]):[]);
  for(const [id,ms] of Object.entries(meshes))ms.forEach(m=>{const always=!M.steps.some(s=>(s.n||[]).includes(id));m.visible=i<0||always||seen.has(id);m.material.emissive=new THREE.Color(cur.has(id)?0x5a1a08:0x000000)})}
 step(-1);
 (function loop(){requestAnimationFrame(loop);ctl.update();r.render(sc,cam)})();
 new ResizeObserver(()=>{r.setSize(W(),H());cam.aspect=W()/H();cam.updateProjectionMatrix()}).observe(el);
 return {step};
}
