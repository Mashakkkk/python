import * as THREE from 'three';
const geometries={box:new THREE.BoxGeometry(1,1,1),sphere:new THREE.SphereGeometry(1,10,7),cylinder:new THREE.CylinderGeometry(1,1,1,12),cone:new THREE.ConeGeometry(1,1,10)};
const mats=new Map();
export function material(color,extra={}){const key=color+JSON.stringify(extra);if(!mats.has(key))mats.set(key,new THREE.MeshStandardMaterial({color,roughness:.88,...extra}));return mats.get(key);}
function mesh(parent,kind,color,x,y,z,sx,sy,sz,extra){const m=new THREE.Mesh(geometries[kind]??kind,material(color,extra));m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
const box=(p,c,x,y,z,w,h,d,extra)=>mesh(p,'box',c,x,y,z,w,h,d,extra);
const cylinder=(p,c,x,y,z,r,h)=>mesh(p,'cylinder',c,x,y,z,r,h,r);
function textSign(parent,text,x,y,z,w,h,color='#f5ecd6',background='#405d50'){
  const c=document.createElement('canvas');c.width=1024;c.height=256;const cx=c.getContext('2d');cx.fillStyle=background;cx.fillRect(0,0,1024,256);cx.fillStyle=color;cx.textAlign='center';cx.textBaseline='middle';cx.font='500 95px Georgia';cx.fillText(text,512,133);const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshStandardMaterial({map:tex,roughness:.9}));m.position.set(x,y,z);parent.add(m);return m;
}
function noiseTexture(base,noise=12){const c=document.createElement('canvas');c.width=c.height=128;const ctx=c.getContext('2d'),im=ctx.createImageData(128,128),rgb=new THREE.Color(base);for(let i=0;i<im.data.length;i+=4){const n=(Math.random()-.5)*noise;im.data[i]=rgb.r*255+n;im.data[i+1]=rgb.g*255+n;im.data[i+2]=rgb.b*255+n;im.data[i+3]=255;}ctx.putImageData(im,0,0);const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(18,18);return t;}
function bake(root,minimum=3){
  root.updateMatrixWorld(true);const batches=new Map();root.traverse(o=>{if(o.isMesh&&!o.isInstancedMesh&&!o.material.transparent){const key=o.geometry.uuid+o.material.uuid;let b=batches.get(key);if(!b){b={geo:o.geometry,mat:o.material,items:[]};batches.set(key,b);}b.items.push(o);}});
  for(const b of batches.values()){if(b.items.length<minimum)continue;const im=new THREE.InstancedMesh(b.geo,b.mat,b.items.length);for(let i=0;i<b.items.length;i++)im.setMatrixAt(i,b.items[i].matrixWorld);im.castShadow=b.items.some(o=>o.castShadow);im.receiveShadow=true;for(const o of b.items)o.removeFromParent();root.add(im);}
}
export function createWorld(scene){
  const root=new THREE.Group();scene.add(root);const objects=[],obstacles=[],trees=[],lamps=[],windows=[];
  const ground=box(root,'#ccc8b7',0,-.34,0,49,.65,37);ground.material=new THREE.MeshStandardMaterial({color:'#e5e0cf',map:noiseTexture('#bcb7a6'),roughness:1});
  box(root,'#b4bba8',0,-.05,0,48,.12,36);
  const road=box(root,'#767e77',0,.03,14.3,48,.13,6.2);road.material=new THREE.MeshStandardMaterial({color:'#9eaaa2',map:noiseTexture('#7f857e',25),roughness:.98});
  box(root,'#dedace',0,.11,10.25,48,.22,1.8);box(root,'#d6d3c4',0,.12,-7.9,48,.25,3.0);box(root,'#d0cbb9',3,.13,1,3,.25,19);
  // Fine pavement seams, low curbs, a crossing and road markings.
  for(let x=-23;x<24;x+=1.5){box(root,'#c3c2b3',x,.24,10.25,.022,.008,1.7);box(root,'#c5c5b7',x,.25,-7.9,.025,.006,2.9);}
  for(let x=-22;x<23;x+=5)box(root,'#e2dfc9',x,.104,14.3,2.2,.012,.11);
  for(let z=12;z<17;z+=.72)box(root,'#e4e2d0',3,.11,z,3.1,.02,.37);
  box(root,'#bfc6b1',-8,.14,1,24,.28,16.4);box(root,'#7f9662',-8,.27,1,23.4,.1,15.8);
  box(root,'#ddd3b5',-8,.34,1,23.8,.13,2);box(root,'#dad1b2',-6,.35,1,2,.14,16);
  box(root,'#d3cbb0',-8,.34,-5.4,23.8,.12,1.4);box(root,'#d3cbb0',-8,.34,7.5,23.8,.12,1.4);box(root,'#d3cbb0',-18.9,.34,1,1.4,.12,14);box(root,'#d3cbb0',.4,.34,1,1.4,.12,14);
  // Circular planted beds and a small fountain at the crossing.
  cylinder(root,'#d8d0b7',-6,.43,1,2,.21);cylinder(root,'#aaa78e',-6,.57,1,1.55,.28);cylinder(root,'#abc3b5',-6,.74,1,1.36,.03);cylinder(root,'#cdc6af',-6,.86,1,.29,.45);cylinder(root,'#d6d0ba',-6,1.09,1,.75,.13);cylinder(root,'#abc3b5',-6,1.18,1,.67,.02);obstacles.push({x:-6,z:1,w:3.7,d:3.7});
  const water=new THREE.Mesh(new THREE.CylinderGeometry(.025,.08,.65,8),new THREE.MeshStandardMaterial({color:'#d4e5df',transparent:true,opacity:.65}));water.position.set(-6,1.53,1);root.add(water);
  function bench(x,z,angle=0){const g=new THREE.Group();g.position.set(x,.14,z);g.rotation.y=angle;root.add(g);for(let i=0;i<5;i++){box(g,'#a28860',0,.58,-.2+i*.105,1.9,.07,.085);box(g,'#a28860',0,.84+i*.095,-.27,1.9,.075,.06);}for(const dx of [-.73,.73]){box(g,'#4b5b4c',dx,.32,0,.055,.5,.5);box(g,'#4b5b4c',dx,.9,-.3,.055,.56,.05);box(g,'#4b5b4c',dx,.77,0,.06,.06,.6);}objects.push({id:'bench-'+objects.length,type:'bench',x,z,angle,label:'Лавочка в парке'});}
  bench(-11,-3.8,0);bench(-15,5.9,Math.PI);bench(-2,5.9,Math.PI);bench(-11,5.9,Math.PI);bench(-2,-3.8);bench(-17,-3.8);
  function tree(x,z,size=1){
    cylinder(root,'#7c7456',x,1.2*size,z,.14*size,2.4*size);const branch=cylinder(root,'#81765b',x+.18,2*size,z,.06*size,1.1*size);branch.rotation.z=-.45;
    const leaves=new THREE.Group();leaves.position.set(x,2.55*size,z);scene.add(leaves);const colors=['#728650','#879958','#617a4a','#97a56a'];
    for(let i=0;i<9;i++){const t=i*2.4,r=i===0?0:.75;const leaf=mesh(leaves,'sphere',colors[i%4],Math.sin(t)*r*size,(Math.sin(i*4)*.45+.3)*size,Math.cos(t)*r*size,.9*size,(.9+Math.random()*.3)*size,.8*size);}
    bake(leaves,1); // matrixWorld includes its position; reset afterward for correctly batched crowns.
    leaves.position.set(0,0,0);leaves.traverse(o=>{if(o.isMesh){o.material=o.material.clone();o.material.transparent=true;}});trees.push({group:leaves,phase:x+z,x,z,y:2.9*size,opacity:1});
    cylinder(root,'#8c9678',x,.34,z,.62,.06);obstacles.push({x,z,w:.75,d:.75});
  }
  [[-19,-5,1],[-20,6,1.1],[-14,-2,1.05],[-16,3,.95],[-9,-3,1],[-9,4,1.05],[-2,-2,1],[-3,4,.85],[1,8,.95],[7,8,1.1],[20,8,1],[21,-5,1.2],[-21,-9,1.05],[2,-9,.9]].forEach(p=>tree(...p));
  function planter(x,z,w,d){box(root,'#bab6a0',x,.4,z,w,.5,d);box(root,'#5e6647',x,.68,z,w-.15,.05,d-.15);for(let i=0;i<Math.round(w*d*14);i++){const px=x+(Math.random()-.5)*(w-.25),pz=z+(Math.random()-.5)*(d-.2);mesh(root,'sphere',['#aaa17b','#ddd0a4','#ac938b','#9b765f'][i%4],px,.85+Math.random()*.14,pz,.11,.16,.11);}obstacles.push({x,z,w,d});}
  planter(-11,3,2,.8);planter(-15,-1,2,.7);planter(-3,-.8,1.2,.7);planter(5,-4.8,.75,2);planter(19,-4.8,.75,2);
  // Cafe terrace, interior tables, striped awning and two adjoining facades.
  box(root,'#d3c4a6',12,-.005,1,15,.35,15);
  for(let x=5;x<20;x+=.65)box(root,'#b9af97',x,.18,1,.018,.01,14.7);
  function building(x,z,w,d,h,color,label,signColor){
    const g=new THREE.Group();root.add(g);
    // Ground floor is hollow and accessible from the south; upper floors have complete walls.
    box(g,color,x,(h+3)/2,z,w,h-3,d);box(g,color,x-w/2+.22,1.65,z,.44,3.3,d);box(g,color,x+w/2-.22,1.65,z,.44,3.3,d);box(g,color,x,1.65,z-d/2+.2,w,3.3,.4);
    box(g,'#bbb4a2',x,.12,z,w,.2,d);box(g,'#e4d9c1',x,3.3,z+d/2+.1,w+.2,.23,.24);
    box(g,'#ddd5bd',x,h+.1,z,w+.6,.3,d+.5);box(g,'#5e665e',x,h+.32,z,w,.18,d);
    box(g,'#dbd1b7',x-w/2, h+.52,z,.22,.65,d+.4);box(g,'#dbd1b7',x+w/2,h+.52,z,.22,.65,d+.4);box(g,'#dbd1b7',x,h+.52,z-d/2,w,.65,.22);box(g,'#dbd1b7',x,h+.52,z+d/2,w,.65,.22);
    box(g,'#958e7c',x+1,h+.7,z-1,.65,.9,.75);box(g,'#b0a993',x+1,h+1.19,z-1,.83,.13,.9);
    for(let y=4.4;y<h-.5;y+=2.4){
      box(g,'#c8c0aa',x,y-1.0,z+d/2+.08,w,.1,.14);
      for(let wx=x-w/2+1.1;wx<x+w/2-.5;wx+=1.85){box(g,'#e1d7c0',wx,y,z+d/2+.07,1.12,1.68,.15);const win=box(g,'#778d88',wx,y,z+d/2+.16,.9,1.43,.03,{metalness:.1,roughness:.28});windows.push(win);box(g,'#d9d3bd',wx,y,z+d/2+.2,.055,1.44,.05);box(g,'#d9d3bd',wx,y-.1,z+d/2+.2,.92,.05,.05);box(g,'#e4d7bd',wx,y-.91,z+d/2+.23,1.27,.15,.37);
        if(y<5){box(g,'#5e6b59',wx,y-.69,z+d/2+.45,1.12,.12,.3);for(let j=0;j<5;j++)mesh(g,'sphere',j%2?'#728354':'#9a8e66',wx-.4+j*.2,y-.55,z+d/2+.44,.16,.19,.16);}
      }
    }
    for(let wx=x-w/2+.7;wx<x+w/2;wx+=1.75){box(g,'#4f6259',wx,1.5,z+d/2,.1,2.8,.12);}
    textSign(g,label,x,2.95,z+d/2+.13,w-.45,.58,'#f3ead4',signColor);
    // Obstacles follow walls, leaving a broad front entrance and accessible interior.
    obstacles.push({x:x-w/2+.1,z,w:.3,d},{x:x+w/2-.1,z,w:.3,d},{x,z:z-d/2+.1,w,d:.3});
    return {x,z,w,d,h,g};
  }
  const home=building(-15,-13,9,6,10.6,'#cfbda2','ЛИПОВАЯ, 8','#8b8c70');
  const apt=building(-5,-13,10,6,12.9,'#c4b39b','АТЕЛЬЕ  •  ЦВЕТЫ','#6c7e71');
  const cafe=building(8,-13,9,6,8.2,'#ded1b1','КАФЕ  «ТЁПЛО»','#536b56');
  const bookshop=building(17,-13,8.6,6,10.6,'#adbaa9','КНИЖНАЯ ЛАВКА','#586c60');
  // Side windows make the neighborhood convincing from every orbit angle.
  for(const b of [home,apt,cafe,bookshop])for(let y=4.3;y<b.h-.5;y+=2.4)for(const side of [-1,1])for(let z=b.z-1.8;z<b.z+2;z+=1.9){box(root,'#788984',b.x+side*(b.w/2+.01),y,z,.04,1.35,.95);box(root,'#d9cfb5',b.x+side*(b.w/2+.06),y-.78,z,.25,.12,1.16);}
  // Interior furnishings visible through open shop fronts.
  box(root,'#947a59',8,.7,-14.3,5.8,1.25,.65);box(root,'#ded5bf',8,1.37,-14.3,6.0,.14,.83);box(root,'#65776c',9,1.68,-14.3,.9,.52,.48);
  for(let k=0;k<5;k++){const x=14+k*1.3;box(root,'#967e5d',x,1.2,-15.4,1.15,2.3,.35);for(let y=.3;y<2.4;y+=.45){box(root,'#c0a380',x,y,-15.15,1.1,.05,.4);for(let j=0;j<7;j++)box(root,['#8e6253','#657d6b','#c9b37f','#748393'][j%4],x-.44+j*.14,y+.18,-15.1,.1,.32,.18);}}
  // Awning over the cafe.
  for(let i=0;i<14;i++){const awn=box(root,i%2?'#e5dbc1':'#718773',4.0+i*.6,2.78,-8.6,.6,.06,2.9);awn.rotation.x=.15;box(root,i%2?'#e5dbc1':'#718773',4+i*.6,2.49,-7.18,.6,.3,.07);}
  for(const x of [3.8,12])cylinder(root,'#68775f',x,1.3,-7.25,.037,2.55);
  function table(x,z,inside=false){cylinder(root,'#515e4d',x,.45,z,.035,.65);cylinder(root,'#72816a',x,.15,z,.35,.06);cylinder(root,'#c1aa81',x,.83,z,.56,.09);cylinder(root,'#eee5ce',x-.1,.925,z,.085,.13);cylinder(root,'#7e8e64',x+.24,.95,z+.1,.06,.16);
    for(const dz of [-.95,.95]){const a=dz<0?0:Math.PI;const seatZ=z+dz;box(root,'#647a62',x,.52,seatZ,.51,.08,.5);box(root,'#71866c',x,.86,seatZ+(dz<0?-.22:.22),.5,.56,.06);for(const dx of [-.19,.19])for(const s of [-.18,.18])box(root,'#475b49',x+dx,.3,seatZ+s,.034,.48,.034);objects.push({id:'cafe-'+objects.length,type:'cafe',x,z:seatZ,angle:a,indoor:inside,label:inside?'Место у окна':'Столик на террасе'});}
    obstacles.push({x,z,w:.8,d:.65});
  }
  table(7,-4.2);table(11,-4.2);table(16,-4.2);table(8,1);table(14,1);table(6,-11,true);table(10,-11,true);
  for(const [x,z] of [[8,1],[14,1]]){cylinder(root,'#8a816a',x,1.6,z,.033,3);const u=mesh(root,new THREE.ConeGeometry(1.65,.5,8),'#d8caa8',x,3.1,z,1,1,1);}
  // Chalk menu, flower pots and a hanging shop sign.
  const board=box(root,'#304c43',13,1,-7.1,.8,1.3,.1);board.rotation.x=-.13;textSign(root,'кофе',13,1.2,-7.02,.67,.3,'#eee8cd','#304c43');textSign(root,'и тишина',13,.85,-6.98,.67,.22,'#eee8cd','#304c43');
  for(const x of [3.5,12.5,20.3]){cylinder(root,'#a48a6b',x,.42,-9,.33,.6);for(let i=0;i<5;i++)mesh(root,'sphere','#6e825b',x+Math.sin(i)*.2,.95,-9+Math.cos(i)*.2,.24,.42,.24);}
  function lamp(x,z){cylinder(root,'#536250',x,1.6,z,.045,3.1);cylinder(root,'#536250',x,.25,z,.13,.35);const cap=mesh(root,'sphere','#f2e6bc',x,3.18,z,.19,.24,.19,{emissive:'#ffcc78',emissiveIntensity:0});cylinder(root,'#536250',x,3.42,z,.24,.055);const l=new THREE.PointLight('#ffce83',0,8,2);l.position.set(x,3.1,z);scene.add(l);lamps.push({light:l,cap});}
  [[-19,9],[-7,9],[4,9],[18,9],[-19,-7],[0,-7],[19,-7]].forEach(p=>lamp(...p));
  // Bus stop shelter, bicycles, street bins and parked cars.
  for(const x of [13.5,17.5])for(const z of [10,11.25])cylinder(root,'#5b6c62',x,1.25,z,.035,2.4);
  box(root,'#728173',15.5,2.5,10.6,4.5,.12,1.7);box(root,'#b7c9bf',15.5,1.3,11.3,4,2.2,.045,{transparent:true,opacity:.4,roughness:.2});box(root,'#947d5c',15.5,.58,10.8,3.1,.1,.42);textSign(root,'ЛИПОВАЯ УЛИЦА',15.5,2.48,11.5,3.6,.35,'#f0e8d2','#617567');
  cylinder(root,'#738170',18.4,1.8,10.6,.045,3.5);box(root,'#466d75',18.4,3.3,10.6,.6,.72,.08);textSign(root,'А',18.4,3.3,10.65,.4,.5);
  function bicycle(x,z){const g=new THREE.Group();g.position.set(x,.15,z);g.rotation.y=.25;root.add(g);const wheelGeo=new THREE.TorusGeometry(.34,.032,6,20);for(const dx of [-.57,.57]){const m=mesh(g,wheelGeo,'#455248',dx,.36,0,1,1,1);for(let i=0;i<6;i++){const spoke=box(g,'#929a8b',dx,.36,0,.014,.65,.012);spoke.rotation.z=i*Math.PI/3;}}
    for(const [x,y,len,ang] of [[-.25,.57,.65,-.65],[.15,.58,.7,.65],[0,.4,.65,Math.PI/2],[.43,.68,.8,.3]]){const t=box(g,'#9d9c7a',x,y,0,.033,len,.04);t.rotation.z=ang;}box(g,'#434a40',-.25,.99,0,.27,.06,.13);box(g,'#424d43',.38,1.05,0,.06,.04,.35);}
  bicycle(1,-8.5);bicycle(19.5,-8.1);bicycle(20.4,-8.1);
  function car(x,z,color){const g=new THREE.Group();g.position.set(x,.15,z);root.add(g);box(g,color,0,.58,0,3.8,.6,1.65);box(g,color,-.1,1.03,0,2.15,.67,1.5);box(g,'#758d8b',-.1,1.13,.76,1.85,.41,.025,{roughness:.25,metalness:.15});box(g,'#758d8b',-.1,1.13,-.76,1.85,.41,.025);box(g,color,-.1,1.13,.785,.075,.46,.035);box(g,'#dfd8b6',1.91,.6,.48,.025,.19,.35);box(g,'#b47d64',-1.91,.6,.48,.025,.18,.32);for(const dx of [-1.2,1.2])for(const dz of [-.82,.82]){const t=cylinder(g,'#3f4941',dx,.34,dz,.34,.19);t.rotation.x=Math.PI/2;const hub=cylinder(g,'#91998a',dx,.34,dz*1.08,.18,.015);hub.rotation.x=Math.PI/2;}}
  car(-15,12.4,'#a8b2a1');car(-8,12.4,'#c4bba0');car(21,15.9,'#697e78');
  for(const [x,z] of [[-18,9],[2,-6],[19,-6]]){cylinder(root,'#66765b',x,.6,z,.23,.9);cylinder(root,'#53634b',x,1.08,z,.26,.09);}
  // Ground-cover tufts use instancing, not thousands of separate draw calls.
  const tuft=new THREE.ConeGeometry(.045,.19,3),grass=new THREE.InstancedMesh(tuft,material('#8f9e6b'),480);const dummy=new THREE.Object3D();for(let i=0;i<480;i++){const x=-19+Math.random()*19,z=-4.4+Math.random()*10.8;if(Math.abs(x+6)<1.4||Math.abs(z-1)<1.3){dummy.position.set(0,-10,0);}else dummy.position.set(x,.44,z);dummy.rotation.z=(Math.random()-.5)*.6;dummy.updateMatrix();grass.setMatrixAt(i,dummy.matrix);}root.add(grass);
  // Small visual anchors: park sign and street name.
  textSign(root,'ЛИПОВЫЙ СКВЕР',-18,1.35,8.4,2.2,.38,'#ede8cf','#6d7e5d');cylinder(root,'#6e795c',-18, .75,8.4,.036,1.5);
  bake(root);
  // Rain is a single draw call and fades with weather.
  const rainGeo=new THREE.BufferGeometry(),positions=new Float32Array(900*3);for(let i=0;i<900;i++){positions[i*3]=(Math.random()-.5)*48;positions[i*3+1]=Math.random()*16;positions[i*3+2]=(Math.random()-.5)*34;}rainGeo.setAttribute('position',new THREE.BufferAttribute(positions,3));const rain=new THREE.Points(rainGeo,new THREE.PointsMaterial({color:'#d4e0dc',size:.055,transparent:true,opacity:0,depthWrite:false}));scene.add(rain);
  let focus=null,eye=null;
  return {root,objects,obstacles,setFocus(person,camera){focus=person;eye=camera;},update(time,dt,night,rainAmount){for(const t of trees){t.group.rotation.z=Math.sin(time*.8+t.phase)*.002;let occludes=false;if(focus&&eye){const dx=focus.x-eye.x,dy=1-eye.y,dz=focus.z-eye.z;const f=THREE.MathUtils.clamp(((t.x-eye.x)*dx+(t.y-eye.y)*dy+(t.z-eye.z)*dz)/(dx*dx+dy*dy+dz*dz),0,1);occludes=Math.hypot(eye.x+f*dx-t.x,eye.y+f*dy-t.y,eye.z+f*dz-t.z)<2.0;}t.opacity=THREE.MathUtils.damp(t.opacity,occludes?.16:1,5,dt);t.group.traverse(o=>{if(o.isMesh){o.material.opacity=t.opacity;o.material.depthWrite=t.opacity>.9;o.castShadow=t.opacity>.9;}});}for(const l of lamps){l.light.intensity=night*3;l.cap.material.emissiveIntensity=night*1.5;}if(windows.length){windows[0].material.emissive.set('#e5ad65');windows[0].material.emissiveIntensity=night*.85;}rain.material.opacity=rainAmount*.5;rain.visible=rainAmount>.01;if(rain.visible){for(let i=0;i<900;i++){positions[i*3+1]-=dt*9;if(positions[i*3+1]<0)positions[i*3+1]=16;}rainGeo.attributes.position.needsUpdate=true;}}};
}
