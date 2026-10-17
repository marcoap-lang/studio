import * as THREE from 'three';
import {OrbitControls} from '../vendor/OrbitControls.js';
import {CSS2DRenderer,CSS2DObject} from '../vendor/CSS2DRenderer.js';
const P=window.D.P;
// Posición 3D (mm): x desde la izquierda, y desde el suelo, z desde atrás (0) hacia el frente (550)
const DOORL='JKLNY';
function box(no,rect){const p=P[no-1],[x,y,w,h]=rect||p.th;let z0=3,d=547;
 const L=p.l;
 if(L==='E'||L==='F'||L==='Q')d=p.W;
 if(no===8){z0=550-50-18;d=18} if(no===9){z0=3;d=18}
 if(L==='H'){z0=21;d=461}
 if(L==='I'){z0=-3;d=6}
 if(no===15){z0=3;d=19}
 const A=x+w/2<800, base=A?528:503;
 if(L==='J'||L==='K'){z0=base;d=19} if(L==='L'){z0=base+19;d=3} if(L==='Y'){z0=base+22;d=2} if(L==='N'){z0=base+24;d=15}
 return {x,y,w,h,z0,d,tube:L==='M',A};}
const COL={wood:0xE8C99A,ply:0xEDD3A8,grey:0xC5CEC8,hl:0xD9502B,steel:0x6B7B78,jute:0xC9AE7C,alu:0xAEB8B5,doorA:0xF0D6AA,doorB:0xD4AF7C,juteA:0xD0B688,juteB:0xB89C6A};
export function createViewer(el,{labels=true,final=false}={}){
 const W=()=>el.clientWidth,Hh=()=>el.clientHeight;
 const r=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
 r.setPixelRatio(Math.min(devicePixelRatio,2));r.setSize(W(),Hh());el.appendChild(r.domElement);
 const lr=new CSS2DRenderer();lr.setSize(W(),Hh());Object.assign(lr.domElement.style,{position:'absolute',inset:0,pointerEvents:'none'});el.appendChild(lr.domElement);
 const sc=new THREE.Scene();
 const cam=new THREE.PerspectiveCamera(32,W()/Hh(),10,20000);cam.position.set(2600,1900,3600);
 const ctl=new OrbitControls(cam,r.domElement);ctl.target.set(800,950,275);ctl.enableDamping=true;ctl.minDistance=1200;ctl.maxDistance=7000;ctl.maxPolarAngle=Math.PI*0.52;ctl.update();
 sc.add(new THREE.HemisphereLight(0xffffff,0xA9B5AF,1.7));const dl=new THREE.DirectionalLight(0xffffff,1.6);dl.position.set(1500,3000,2500);sc.add(dl);
 const fl=new THREE.Mesh(new THREE.CircleGeometry(1900,64),new THREE.MeshLambertMaterial({color:0xE9EDE8}));fl.rotation.x=-Math.PI/2;fl.position.set(800,-1,275);sc.add(fl);
 const meshes={};const edgeM=new THREE.LineBasicMaterial({color:0x1F2A2E,transparent:true,opacity:.45});
 function mk(key,bs,col){if(!Array.isArray(bs))bs=[bs];
  const mat=new THREE.MeshStandardMaterial({color:col,roughness:.85,metalness:bs[0].tube?.6:0,transparent:true});
  const grp=new THREE.Group();const c0=new THREE.Vector3();
  bs.forEach((b,i)=>{let g;
   if(b.tube){g=new THREE.CylinderGeometry(12.5,12.5,b.w-8,20);g.rotateZ(Math.PI/2)} else g=new THREE.BoxGeometry(b.w,b.h,b.d);
   const m=new THREE.Mesh(g,mat);
   if(b.tube)m.position.set(b.x+b.w/2,b.y,275); else m.position.set(b.x+b.w/2,b.y+b.h/2,b.z0+b.d/2);
   if(!b.tube)m.add(new THREE.LineSegments(new THREE.EdgesGeometry(g),edgeM));
   if(i===0)c0.copy(m.position);grp.add(m)});
  grp.material=mat;grp.userData.home=grp.position.clone();grp.userData.base=col;sc.add(grp);
  if(labels){const div=document.createElement('div');div.className='lbl';div.textContent=key;const o=new CSS2DObject(div);
   const b=bs[0];o.position.set(c0.x,c0.y+(b.tube?40:0),b.tube?c0.z:b.z0+b.d+2);if(['L','I','Y'].includes(P[(+key||1)-1]?.l))o.position.y=b.y+b.h*.7;grp.add(o);grp.userData.lbl=o;o.visible=false}
  meshes[key]=grp;return grp}
 for(const p of P){const rects=(p.pp||[p.th]).map(r=>box(p.no,r));const A=rects[0].A;
  let base=p.l==='M'?COL.steel:p.mat.includes('18')||p.l==='I'?COL.ply:COL.wood;
  if('JKLN'.includes(p.l))base=A?COL.doorA:COL.doorB; if(p.l==='Y')base=COL.jute;
  mk(p.no,rects,base)}
 mk('riel',{x:18,y:1950,w:1564,h:32,z0:500,d:50},COL.alu);
 // Puertas: zona de traslape, flechas y etiquetas
 const extras=new THREE.Group();sc.add(extras);
 const ov=new THREE.Mesh(new THREE.BoxGeometry(40,1880,62),new THREE.MeshBasicMaterial({color:COL.hl,transparent:true,opacity:.28,depthWrite:false}));ov.position.set(800,68+940,531);extras.add(ov);
 const arrM=new THREE.MeshBasicMaterial({color:0x1F2A2E});
 function arrow(x,z,dir){const g=new THREE.Group();const sh=new THREE.Mesh(new THREE.CylinderGeometry(7,7,260,12),arrM);sh.rotation.z=Math.PI/2;g.add(sh);const hd=new THREE.Mesh(new THREE.ConeGeometry(22,60,16),arrM);hd.rotation.z=-dir*Math.PI/2;hd.position.x=dir*150;g.add(hd);g.position.set(x,1180,z);extras.add(g)}
 arrow(420,600,1);arrow(1200,575,-1);
 const tags=[];function setX(v){extras.visible=v;tags.forEach(t=>t.visible=v)}
 function tag(t,x,y,z,cls){const d=document.createElement('div');d.className=cls;d.textContent=t;const o=new CSS2DObject(d);o.position.set(x,y,z);extras.add(o);tags.push(o);return o}
 tag('Puerta A (frente) →',420,1290,600,'dtag');tag('← Puerta B (atrás)',1200,1290,575,'dtag dtagb');tag('traslape 40 mm',800,1960,560,'dtag dtago');
 setX(false);
 let anim=[];
 function show(step,STEPS){const seen=new Set();for(let i=0;i<step;i++){STEPS[i].n.forEach(n=>seen.add(n));(STEPS[i].x||[]).forEach(n=>seen.add(n))}
  const cur=STEPS[step],nw=new Set([...cur.n,...(cur.x||[])]),fc=new Set(cur.f||[]);anim=[];
  for(const [k,m] of Object.entries(meshes)){const key=isNaN(k)?k:+k;const isNew=nw.has(key),was=seen.has(key);
   m.visible=isNew||was;m.position.copy(m.userData.home);
   const hl=isNew||(fc.has(key)&&was);m.material.color.setHex(hl?COL.hl:(was?COL.grey:m.userData.base));m.material.opacity=1;
   if(m.userData.lbl)m.userData.lbl.visible=hl&&labels;
   if(isNew){const off=new THREE.Vector3(0,0,0);const L=P[key-1]?.l;
    if(['I','P'].includes(L)||key===15)off.z=-700;else if(['J','K','L','N','Y','riel'].includes(L)||key==='riel')off.z=700;else if(L==='M')off.z=500;else if(['A'].includes(L))off.x=(key===1?-700:700);else off.y=600;
    m.position.add(off);m.userData.from=m.position.clone();anim.push(m)}}
  setX(step>=12);t0=performance.now()}
 function showFinal(){setX(true);for(const m of Object.values(meshes)){m.visible=true;m.position.copy(m.userData.home);m.material.color.setHex(m.userData.base);if(m.userData.lbl)m.userData.lbl.visible=false}anim=[]}
 let t0=0;
 const ease=t=>1-Math.pow(1-t,3);
 function loop(now){requestAnimationFrame(loop);if(anim.length){const t=Math.min(1,(now-t0-150)/900);if(t>0)for(const m of anim){m.position.lerpVectors(m.userData.from,m.userData.home,ease(t))}if(t>=1)anim=[]}
  ctl.update();r.render(sc,cam);lr.render(sc,cam)}
 requestAnimationFrame(loop);
 const dir=new THREE.Vector3(1800,950,3325).normalize();
 function fit(){const a=W()/Hh(),hf=Math.atan(Math.tan(THREE.MathUtils.degToRad(16))*a),f=Math.min(THREE.MathUtils.degToRad(16),hf);const dist=1250/Math.sin(f);cam.position.copy(ctl.target).addScaledVector(dir,dist);ctl.maxDistance=dist*2;ctl.update()}
 fit();
 new ResizeObserver(()=>{cam.aspect=W()/Hh();cam.updateProjectionMatrix();fit();r.setSize(W(),Hh());lr.setSize(W(),Hh())}).observe(el);
 if(final){showFinal();ctl.autoRotate=true;ctl.autoRotateSpeed=.6;r.domElement.addEventListener('pointerdown',()=>ctl.autoRotate=false)}
 return {show,showFinal,ctl};
}
