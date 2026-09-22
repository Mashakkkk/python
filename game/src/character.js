import * as THREE from 'three';
const sphere=new THREE.SphereGeometry(1,12,8),capsule=new THREE.CapsuleGeometry(1,1,4,8),box=new THREE.BoxGeometry(1,1,1);
const torsoShape=new THREE.LatheGeometry([[0,-.29],[.18,-.29],[.2,-.23],[.18,-.03],[.235,.15],[.23,.23],[.12,.28],[.065,.28]].map(([x,y])=>new THREE.Vector2(x,y)),16);
const thighShape=new THREE.CylinderGeometry(.095,.074,.43,12),calfShape=new THREE.CylinderGeometry(.075,.055,.38,12),sleeveShape=new THREE.CylinderGeometry(.087,.064,.31,12),forearmShape=new THREE.CylinderGeometry(.066,.045,.28,12);
const materials=new Map();
function mat(color){if(!materials.has(color))materials.set(color,new THREE.MeshStandardMaterial({color,roughness:.92}));return materials.get(color);}
function part(parent,geo,color,x,y,z,sx,sy,sz,shadow=true){const m=new THREE.Mesh(geo,mat(color));m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=shadow;m.receiveShadow=true;parent.add(m);return m;}
function joint(parent,x,y,z){const g=new THREE.Group();g.position.set(x,y,z);parent.add(g);return g;}
export function createCharacter(spec){
  const a=spec.appearance,skin=a.skin,shirt=a.clothing.outerwear,trousers=a.clothing.bottom,hair=a.hair.color;
  const root=new THREE.Group(),body=new THREE.Group();root.add(body);
  const scale=a.height==='tall'?1.1:a.height==='short'?.92:1;root.scale.setScalar(scale);
  const broad=a.bodyType==='broad'?1.2:a.bodyType==='slim'?.85:1;
  const torso=part(body,torsoShape,shirt,0,1.19,0,broad,1,.62);
  const pelvis=part(body,sphere,trousers,0,.88,0,.205*broad,.18,.14);
  // Collar, shirt placket and a soft hem make the silhouette read as clothing.
  part(body,box,'#d8d4c5',0,1.44,.107,.13,.10,.045,false);
  part(body,box,shirt,0,1.17,.137,.025,.43,.012,false);
  part(body,capsule,skin,0,1.5,0,.066,.055,.067);
  const head=joint(body,0,1.65,0);
  part(head,sphere,skin,0,0,0,.126,.173,.13);
  part(head,sphere,skin,0,-.065,.047,.093,.093,.102);
  part(head,sphere,skin,.125,-.005,0,.026,.042,.032,false);part(head,sphere,skin,-.125,-.005,0,.026,.042,.032,false);
  const details=new THREE.Group();head.add(details);
  part(details,sphere,skin,0,-.013,.128,.023,.034,.04,false);
  for(const x of [-.045,.045]){part(details,sphere,'#e9e7df',x,.025,.113,.025,.014,.012,false);part(details,sphere,'#343b31',x,.025,.125,.009,.01,.006,false);part(details,box,hair,x,.059,.111,.048,.009,.011,false);}
  part(details,box,'#a47764',0,-.072,.131,.052,.008,.007,false);
  const hairCap=part(head,sphere,hair,0,.062,-.018,.136,.136,.129);
  part(head,sphere,hair,-.045,.11,.063,.094,.062,.085);
  if(a.hair.length!=='short')part(head,sphere,hair,0,-.09,-.074,.145,a.hair.length==='long'?.24:.15,.09);
  if(a.hair.style==='bun')part(head,sphere,hair,0,.15,-.1,.077,.074,.07);
  if(a.hair.style==='curly')for(let i=0;i<7;i++)part(head,sphere,hair,Math.sin(i)*.095,.12+Math.cos(i*3)*.025,Math.cos(i)*.073,.055,.055,.055);
  if(a.accessories?.includes('glasses'))for(const x of [-.046,.046]){const lens=part(details,box,'#44433b',x,.023,.127,.072,.047,.009,false);part(details,box,'#b5c2b9',x,.023,.133,.054,.033,.006,false);}
  const legs=[],arms=[];
  for(const s of [-1,1]){
    const hip=joint(body,s*.102,.9,0);part(hip,thighShape,trousers,0,-.2,0,1,1,1);const knee=joint(hip,0,-.4,0);part(knee,calfShape,trousers,0,-.18,0,1,1,1);part(knee,sphere,a.clothing.shoes,0,-.365,.046,.072,.053,.125);part(knee,box,'#c9c6b9',0,-.4,.04,.136,.018,.22);legs.push({hip,knee});
    const shoulder=joint(body,s*.22*broad,1.4,0);part(shoulder,sphere,shirt,0,-.025,0,.085,.088,.084);part(shoulder,sleeveShape,shirt,0,-.15,0,1,1,1);const elbow=joint(shoulder,0,-.3,0);part(elbow,forearmShape,shirt,0,-.12,0,1,1,1);part(elbow,sphere,skin,0,-.277,.005,.044,.068,.033);arms.push({shoulder,elbow});
  }
  const props=new THREE.Group();body.add(props);
  const book=new THREE.Group();book.position.set(0,1.02,.32);book.rotation.x=.3;props.add(book);part(book,box,'#657968',-.078,0,0,.155,.025,.21,false).rotation.z=.12;part(book,box,'#637968',.078,0,0,.155,.025,.21,false).rotation.z=-.12;part(book,box,'#e7ddbf',0,.018,0,.28,.01,.18,false);book.visible=false;
  const phone=part(props,box,'#303b39',.18,1.17,.3,.075,.135,.013,false);phone.rotation.x=-.45;phone.visible=false;
  const cup=part(props,new THREE.CylinderGeometry(.043,.034,.1,12),'#f1e8d5',.17,1.1,.3,1,1,1,false);cup.visible=false;
  const food=part(props,sphere,'#c89754',.13,1.12,.3,.065,.029,.045,false);food.visible=false;
  const umbrella=new THREE.Group();umbrella.position.set(.25,1.65,0);root.add(umbrella);part(umbrella,new THREE.CylinderGeometry(.012,.012,1.1,6),'#72736a',0,.2,0,1,1,1,false);part(umbrella,new THREE.ConeGeometry(.65,.26,12),'#748478',0,.8,0,1,1,1);umbrella.visible=false;
  const ring=new THREE.Mesh(new THREE.RingGeometry(.37,.42,40),new THREE.MeshBasicMaterial({color:'#e2f5bf',transparent:true,opacity:.9,depthWrite:false}));ring.rotation.x=-Math.PI/2;ring.position.y=.14;root.add(ring);ring.visible=false;
  let phase=Math.random()*6,blendSit=0,smoothedAngle=0;
  return {root,ring,update(p,dt,time,distance=0,weather='clear'){
    const park=p.x>-20&&p.x<4&&p.z>-7&&p.z<9;const groundHeight=p.seatId&&p.phase==='acting'?(p.seatId.startsWith('bench-')?.3:.12):park?.32:.12;root.position.set(p.x,groundHeight,p.z);let diff=p.angle-smoothedAngle;diff=Math.atan2(Math.sin(diff),Math.cos(diff));smoothedAngle+=diff*Math.min(1,dt*9);root.rotation.y=smoothedAngle;
    const sitting=!!p.seatId&&p.phase==='acting';blendSit=THREE.MathUtils.damp(blendSit,sitting?1:0,5,dt);const locomotion=p.moving;const running=locomotion&&(p.action==='run'||p.run);phase+=dt*(running?12:7);
    body.position.y=-.35*blendSit+(locomotion?Math.abs(Math.sin(phase))*(running?.05:.018):Math.sin(time*2+p.id)*.008)*(1-blendSit);pelvis.scale.y=.18-.08*blendSit;
    torso.rotation.z=Math.sin(time*1.5+p.id)*.007;head.rotation.y=THREE.MathUtils.damp(head.rotation.y,locomotion?0:Math.sin(time*.45+p.id)*.17,4,dt);
    const reading=p.action==='read'&&!locomotion,looking=p.action==='phone'&&!locomotion,drinking=p.action==='drink'&&!locomotion,eating=p.action==='eat'&&!locomotion,talking=['talk','wave'].includes(p.action)&&!locomotion;
    book.visible=reading;phone.visible=looking;cup.visible=drinking;food.visible=eating;umbrella.visible=weather==='rain'&&!sitting&&!['shop','home','work'].includes(p.action);
    for(let i=0;i<2;i++){
      const wave=Math.sin(phase+i*Math.PI),leg=legs[i],arm=arms[i];
      leg.hip.rotation.x=THREE.MathUtils.damp(leg.hip.rotation.x,blendSit*-1.45+(locomotion?wave*(running?.8:.45):0)*(1-blendSit),12,dt);leg.knee.rotation.x=THREE.MathUtils.damp(leg.knee.rotation.x,blendSit*1.5+(running?Math.max(0,-wave)*1.1:locomotion?Math.max(0,-wave)*.35:0),12,dt);
      let shoulder=locomotion?-wave*(running?.7:.35):0,elbow=running?-.8:-.12;
      if(sitting){shoulder=-.35;elbow=-.7;}if(reading){shoulder=-.65;elbow=-.8;}if(looking&&i===1){shoulder=-.8;elbow=-1.05;}
      if((drinking||eating)&&i===1){const sip=Math.max(0,Math.sin(time*1.1));shoulder=-.7-sip*.5;elbow=-.8-sip*.45;cup.position.y=1.1+sip*.33;cup.position.z=.3-sip*.16;food.position.copy(cup.position);}
      if(talking&&i===1){shoulder=-.7-Math.sin(time*3)*.22;elbow=-.8;}
      if(umbrella.visible&&i===1){shoulder=-.4;elbow=-1.3;}
      arm.shoulder.rotation.x=THREE.MathUtils.damp(arm.shoulder.rotation.x,shoulder,8,dt);arm.elbow.rotation.x=THREE.MathUtils.damp(arm.elbow.rotation.x,elbow,8,dt);arm.shoulder.rotation.z=THREE.MathUtils.damp(arm.shoulder.rotation.z,talking&&i===1?-.25:(i===0?.06:-.06),8,dt);
    }
    details.visible=distance<45;root.visible=!(p.phase==='acting'&&['home','work'].includes(p.action));
  }};
}
