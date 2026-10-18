import * as THREE from 'three';
import {OrbitControls} from '../vendor/OrbitControls.js';
function woodTex(seed,base,dark){const c=document.createElement('canvas');c.width=1024;c.height=1024;const g=c.getContext('2d');
 g.fillStyle=base;g.fillRect(0,0,1024,1024);let s=seed;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
 for(let i=0;i<170;i++){const y0=rnd()*1024,a=4+rnd()*22,f=0.004+rnd()*0.01,ph=rnd()*6;g.strokeStyle=dark;g.globalAlpha=0.05+rnd()*0.16;g.lineWidth=0.6+rnd()*2.6;g.beginPath();
  for(let x=0;x<=1024;x+=8){const y=y0+Math.sin(x*f+ph)*a+Math.sin(x*f*3.1+ph)*a*0.25;x?g.lineTo(x,y):g.moveTo(x,y)}g.stroke()}
 for(let i=0;i<5;i++){const x=rnd()*1024,y=rnd()*1024;const gr=g.createRadialGradient(x,y,1,x,y,10+rnd()*14);gr.addColorStop(0,'rgba(120,70,30,.35)');gr.addColorStop(1,'rgba(120,70,30,0)');g.globalAlpha=1;g.fillStyle=gr;g.beginPath();g.ellipse(x,y,26,9,0,0,7);g.fill()}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;return t}
function juteTex(){const c=document.createElement('canvas');c.width=256;c.height=256;const g=c.getContext('2d');g.fillStyle='#B8955E';g.fillRect(0,0,256,256);
 for(let i=0;i<256;i+=6){g.fillStyle=i%12?'#C9A86F':'#A9864F';g.fillRect(i,0,3,256);g.globalAlpha=.55;g.fillStyle='#D4B57D';g.fillRect(0,i,256,3);g.globalAlpha=1}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;return t}
export function viewer(el,M,opt={}){
 const r=new THREE.WebGLRenderer({antialias:true,alpha:!opt.render,preserveDrawingBuffer:true});r.setPixelRatio(opt.render?1:Math.min(devicePixelRatio,2));
 r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.05;r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;
 const W=()=>el.clientWidth,H=()=>el.clientHeight;r.setSize(W(),H());el.appendChild(r.domElement);
 const sc=new THREE.Scene();if(opt.render)sc.background=new THREE.Color(0xEFE6D8);
 sc.add(new THREE.HemisphereLight(0xFFF1DC,0x6E5640,0.75));
 const dl=new THREE.DirectionalLight(0xFFDDAA,3.4);dl.position.set(2600,3400,3200);dl.castShadow=true;dl.shadow.mapSize.set(2048,2048);
 Object.assign(dl.shadow.camera,{left:-1800,right:1800,top:2400,bottom:-600,near:100,far:9000});dl.shadow.bias=-0.0004;dl.target.position.set(800,900,275);sc.add(dl,dl.target);
 const fill=new THREE.DirectionalLight(0xFFD9A8,0.6);fill.position.set(-2000,1200,1500);sc.add(fill);
 const cam=new THREE.PerspectiveCamera(30,W()/H(),10,30000);
 const ctl=new OrbitControls(cam,r.domElement);ctl.enableDamping=true;
 function view(v){if(v==='open'){cam.position.set(2900,1500,4300);ctl.target.set(800,980,275)}else{cam.position.set(3300,1250,4300);ctl.target.set(800,1000,275)};ctl.update()}view(opt.view);
 const floorM=new THREE.MeshStandardMaterial({color:0xD9CBB5,roughness:.95});const fl=new THREE.Mesh(new THREE.PlaneGeometry(9000,9000),floorM);fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;sc.add(fl);
 if(opt.render){const wall=new THREE.Mesh(new THREE.PlaneGeometry(9000,5000),new THREE.MeshStandardMaterial({color:0xF2EBDF,roughness:1}));wall.position.set(800,2500,-60);wall.receiveShadow=true;sc.add(wall)}
 const T18=woodTex(7,'#D49A55','#7A4418'),T5=woodTex(31,'#DCA866','#84501F'),TW=woodTex(99,'#B97638','#5E3414'),TJ=juteTex();
 [T18,T5].forEach(t=>t.repeat.set(1/900,1/900));TW.repeat.set(1/120,1/120);TJ.repeat.set(1/40,1/40);TJ.anisotropy=8;
 const mats={};const mat=(k)=>mats[k]||(mats[k]=new THREE.MeshStandardMaterial(k==='j'?{map:TJ,roughness:1}:k==='w'?{map:TW,roughness:.55}:{map:k==='5'?T5:T18,roughness:.5,metalness:0}));
 const edgeM=new THREE.LineBasicMaterial({color:0x5A3415,transparent:true,opacity:.35});const groups={};const all=[];
 for(const p of M.m3d){const shapes=p.shape.map(poly=>{const s=new THREE.Shape(poly[0].map(([x,y])=>new THREE.Vector2(x,y)));poly.slice(1).forEach(h=>s.holes.push(new THREE.Path(h.map(([x,y])=>new THREE.Vector2(x,y)))));return s});
  const geo=new THREE.ExtrudeGeometry(shapes,{depth:p.t,bevelEnabled:false,curveSegments:16});
  const k=p.jute?'j':p.g==='CU'||p.g==='MA'?'w':String(p.t===5?5:18);const m=new THREE.Mesh(geo,mat(k).clone());m.userData.k=k;
  const P=p.pose,U=new THREE.Vector3(...P.U),V=new THREE.Vector3(...P.V),N=new THREE.Vector3(...P.N);
  m.matrixAutoUpdate=false;m.matrix.makeBasis(U,V,N).setPosition(...P.O);m.castShadow=m.receiveShadow=true;
  m.material.side=THREE.DoubleSide;m.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo,30),edgeM));m.userData.step=p.step;sc.add(m);all.push(m)}
 const rg=new THREE.CylinderGeometry(16,16,M.rodL,32);rg.rotateZ(Math.PI/2);
 for(const d of M.rods){const m=new THREE.Mesh(rg,mat('w').clone());m.position.set(d.x-9+M.rodL/2,d.y,d.z);m.castShadow=true;m.userData.step=2;sc.add(m);all.push(m)}
 const acc=new THREE.Color(0xD9502B),sage=new THREE.Color(0xC9D3C6);
 function step(i){for(const m of all){const k=m.userData.step;m.visible=i<1||k<=i;const now=i>=1&&k===i;
  m.material.color.set(i<1?0xffffff:now?0xffffff:0xF0F0F0);m.material.emissive=new THREE.Color(now?0x5A1A05:0x000000);m.material.emissiveIntensity=now?0.55:0}}
 step(opt.step??-1);
 (function loop(){requestAnimationFrame(loop);ctl.update();r.render(sc,cam)})();
 new ResizeObserver(()=>{r.setSize(W(),H());cam.aspect=W()/H();cam.updateProjectionMatrix()}).observe(el);
 return {step,view};
}
