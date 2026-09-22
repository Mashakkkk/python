import { Navigation } from './navigation.js';
import { chooseIntent, actionLabels } from './planner.js';
import { parseDescription } from './appearance.js';
export const SAVE_KEY='living-quarter-v1';
const clamp=x=>Math.max(0,Math.min(1,x));
export class Simulation {
  constructor(obstacles,objects,saved=null) {
    this.nav=new Navigation(obstacles);this.objects=objects.map(o=>({...o,owner:null}));this.people=[];this.minute=saved?.minute??870;this.day=saved?.day??1;this.weather=saved?.weather??'clear';this.speed=1;this.elapsed=0;this.event=()=>{};this.nextId=1;
    if(saved?.people?.length){for(const p of saved.people)this.restore(p);this.nextId=Math.max(...this.people.map(p=>p.id))+1;}
    else this.populate();
  }
  add(spec,x=-3,z=10){
    const point=this.nav.nearest({x,z});const pos=point?this.nav.point(point.x,point.z):{x:0,z:0};
    // Find an unoccupied spawn cell so created people never stack.
    let spawn=pos;
    for(let r=0;r<6;r++){let found=false;for(let i=0;i<12;i++){const q={x:pos.x+Math.sin(i*Math.PI/6)*r*.8,z:pos.z+Math.cos(i*Math.PI/6)*r*.8};if(this.nav.canStand(q)&&this.people.every(p=>Math.hypot(p.x-q.x,p.z-q.z)>.65)){spawn=q;found=true;break;}}if(found)break;}
    const p={...structuredClone(spec),id:this.nextId++,x:spawn.x,z:spawn.z,angle:0,action:'idle',phase:'acting',path:[],queue:[],seatId:null,partnerId:null,timer:1,manual:false,run:false,moving:false,reason:'Осматривается',memory:[],needs:{energy:.7+Math.random()*.25,mood:.75,hunger:.1+Math.random()*.4,social:.25+Math.random()*.4,interest:.4,fatigue:.1}};
    this.people.push(p);if(spec.source!=='default')this.command(p.id,[{...spec.initialIntent,duration:spec.initialIntent.duration==='until_changed'?Infinity:undefined}],true);return p;
  }
  populate(){
    const names=['Анна','Михаил','Лев','София','Илья','Вера','Артём','Елена','Денис','Нина','Роман','Ольга'];
    const colors=['#ac5146','#7d8b6b','#9d805f','#bbaa84','#53758a','#c48b71','#697c8a','#899674','#8e7469','#b89363','#516951','#b18c8c'];
    const spawn=[[-14,2],[-3,7],[-17,-6],[5,-6],[13,0],[-9,8],[-1,-5],[8,8],[18,7],[-14,8],[4,1],[-6,-7]];
    for(let i=0;i<12;i++){const s=parseDescription(i%2?'Мужчина общительный':'Девушка спокойная любит читать');s.name=names[i];s.source='default';s.appearance.clothing.outerwear=colors[i];s.appearance.hair.color=['#392e27','#695140','#b6a07d','#9e8e79'][i%4];s.appearance.hair.length=i%3===0?'medium':'short';s.appearance.ageGroup=i===9?'senior':i%3?'adult':'young_adult';s.interests=[['reading'],['coffee'],['parks'],['running']][i%4];const p=this.add(s,...spawn[i]);p.timer=i*.7;}
    ['read','drink','walk','shop','phone','rest'].forEach((a,i)=>this.begin(this.people[i],{action:a}));
  }
  release(p){if(p.seatId){const seat=this.objects.find(o=>o.id===p.seatId);if(seat?.owner===p.id)seat.owner=null;p.seatId=null;}if(p.partnerId){const q=this.people.find(q=>q.id===p.partnerId);if(q?.partnerId===p.id){q.partnerId=null;q.timer=1;}p.partnerId=null;}}
  command(id,steps,internal=false){const p=this.people.find(p=>p.id===id);if(!p||(!internal&&p.source==='default'))return false;this.release(p);p.retryStep=null;p.queue=structuredClone(steps);p.path=[];p.manual=true;p.timer=0;this.advance(p);return true;}
  advance(p){this.release(p);if(p.queue.length){const step=p.queue.shift();if(step.action==='auto'){p.manual=false;p.timer=0;p.action='idle';return;}if(step.action==='stop'){p.path=[];p.action='idle';p.phase='acting';p.timer=Infinity;p.moving=false;return;}this.begin(p,step);}else{p.manual=false;p.action='idle';p.phase='acting';p.timer=1;}}
  begin(p,step){
    this.release(p);p.currentStep={...step};p.action=step.action;p.reason=step.reason||'Следует вашему намерению';p.path=[];p.phase='acting';p.timer=step.duration??(18+Math.random()*20);p.targetId=step.targetId??null;p.blocked=0;
    let dest=step.point;
    if(['read','rest','drink','eat'].includes(step.action)){
      const type=['drink','eat'].includes(step.action)?'cafe':'bench';const indoor=type==='cafe'&&(step.location==='window'||this.weather==='rain');const seats=this.objects.filter(o=>o.type===type&&!o.owner&&(!indoor||o.indoor));seats.sort((a,b)=>Math.hypot(a.x-p.x,a.z-p.z)-Math.hypot(b.x-p.x,b.z-p.z));if(step.seatId){const exact=seats.findIndex(o=>o.id===step.seatId);if(exact>=0)seats.unshift(...seats.splice(exact,1));}
      const seat=seats[0];if(seat){seat.owner=p.id;p.seatId=seat.id;dest={x:seat.x,z:seat.z};p.seatAngle=seat.angle??0;}else{p.action=step.action==='read'?'read':'idle';p.reason='Все места заняты — подожду рядом';p.retryStep={...step};p.timer=8;this.event(p.reason,p);}
    }
    if(step.action==='talk'){
      const q=this.people.find(q=>q.id===step.targetId&&!q.partnerId);if(q&&!q.manual&&q.phase!=='travel'&&!q.seatId){this.release(q);q.path=[];q.action='talk';q.timer=30;q.phase='acting';q.partnerId=p.id;p.partnerId=q.id;dest={x:q.x+1,z:q.z};}else{p.action='wave';p.timer=4;p.reason='Знакомый занят — поздороваюсь и пойду дальше';}
    }
    if(['shop','home','work','wait'].includes(step.action))dest=({shop:{x:16,z:-10},home:{x:-15,z:-10},work:{x:-6,z:-10},wait:{x:15,z:10}})[step.action];
    if(['walk','run'].includes(step.action)&&!dest){const places=[{x:-15,z:-5},{x:-14,z:8},{x:0,z:7},{x:0,z:-5},{x:6,z:1},{x:18,z:5}];dest=places[Math.floor(Math.random()*places.length)];p.timer=2;}
    if(dest){p.destination=dest;p.path=this.nav.find(p,dest);if(p.path.length)p.phase='travel';else if(Math.hypot(p.x-dest.x,p.z-dest.z)>1.7){this.release(p);p.action='idle';p.timer=3;p.reason='Не получается пройти — выберу другое место';this.event(p.reason,p);}}
  }
  update(dt){
    dt=Math.min(dt,.1)*this.speed;if(!dt)return;this.elapsed+=dt;this.minute+=dt*.6;if(this.minute>=1440){this.minute-=1440;this.day++;}
    for(const p of this.people){
      const n=p.needs;const traveling=p.phase==='travel';n.hunger=clamp(n.hunger+dt*.0008);n.social=clamp(n.social+dt*.0006);n.energy=clamp(n.energy-dt*(traveling?(p.action==='run'?.0025:.00065):.0001));n.fatigue=1-n.energy;n.interest=clamp(n.interest+dt*.0005);
      p.moving=false;
      if(traveling&&p.path.length){
        const dest=p.path[0],dx=dest.x-p.x,dz=dest.z-p.z,dist=Math.hypot(dx,dz),speed=p.action==='run'||p.run?2.9:1.15;const move=Math.min(dist,dt*speed);let nx=p.x+(dx/dist||0)*move,nz=p.z+(dz/dist||0)*move;
        const blocker=this.people.find(q=>q.id!==p.id&&q.action!=='home'&&Math.hypot(nx-q.x,nz-q.z)<.49);
        if(blocker){p.blocked+=dt;const sign=p.id<blocker.id?1:-1;const side={x:p.x+(-dz/dist||0)*move*sign,z:p.z+(dx/dist||0)*move*sign};if(this.nav.canStand(side)&&this.people.every(q=>q.id===p.id||Math.hypot(side.x-q.x,side.z-q.z)>.5)){nx=side.x;nz=side.z;}else{nx=p.x;nz=p.z;}if(p.blocked>5){const temp=new Navigation([...this.nav.obstacles,{x:blocker.x,z:blocker.z,w:.8,d:.8}]);const route=temp.find(p,p.destination);if(route.length)p.path=route;else{this.release(p);p.phase='acting';p.action='idle';p.timer=3;p.reason='Проход занят — немного подожду';}p.blocked=0;}}
        else p.blocked=0;
        p.moving=Math.hypot(nx-p.x,nz-p.z)>.001;p.x=nx;p.z=nz;if(p.moving)p.angle=Math.atan2(dx,dz);
        if(Math.hypot(p.x-dest.x,p.z-dest.z)<.12)p.path.shift();
        if(!p.path.length){p.phase='acting';p.moving=false;if(p.seatId){const seat=this.objects.find(o=>o.id===p.seatId);p.angle=p.seatAngle;if(seat){p.x=seat.x;p.z=seat.z;}}this.remember(p,p.action);if(p.partnerId){const q=this.people.find(q=>q.id===p.partnerId);if(q){p.angle=Math.atan2(q.x-p.x,q.z-p.z);q.angle=p.angle+Math.PI;}}}
      }else{
        if(['rest','read','home'].includes(p.action))n.energy=clamp(n.energy+dt*.004);
        if(['eat','drink'].includes(p.action)){n.hunger=clamp(n.hunger-dt*.016);n.mood=clamp(n.mood+dt*.003);}
        if(p.action==='talk'){n.social=clamp(n.social-dt*.02);n.mood=clamp(n.mood+dt*.003);}
        if(['read','shop','walk'].includes(p.action))n.interest=clamp(n.interest-dt*.004);
        p.timer-=dt;if(p.timer<=0){if(p.retryStep){const retry=p.retryStep;p.retryStep=null;this.begin(p,retry);}else if(p.queue.length||p.manual)this.advance(p);else this.begin(p,chooseIntent(p,this));}
      }
      if(this.weather==='rain'&&!p.manual&&p.phase==='acting'&&!['drink','eat','shop','home'].includes(p.action)&&this.elapsed%5<dt)this.begin(p,chooseIntent(p,this));
    }
  }
  remember(p,action){p.memory.push({action,text:actionLabels[action]??action,minute:Math.floor(this.minute)});p.memory=p.memory.slice(-6);}
  snapshot(){return {version:1,minute:this.minute,day:this.day,weather:this.weather,people:this.people.map(p=>{const a=structuredClone(p);a.timer=Number.isFinite(a.timer)?a.timer:-1;if(a.currentStep?.duration===Infinity)a.currentStep.duration=-1;if(a.retryStep?.duration===Infinity)a.retryStep.duration=-1;a.queue=a.queue.map(s=>({...s,duration:s.duration===Infinity?-1:s.duration}));return a;})};}
  restore(data){
    const p=structuredClone(data);p.path=Array.isArray(p.path)?p.path:[];p.queue=(p.queue??[]).map(s=>({...s,duration:s.duration===-1?Infinity:s.duration}));p.timer=p.timer===-1?Infinity:p.timer;if(p.currentStep?.duration===-1)p.currentStep.duration=Infinity;if(p.retryStep?.duration===-1)p.retryStep.duration=Infinity;
    if(p.seatId){const o=this.objects.find(o=>o.id===p.seatId);if(o&&!o.owner)o.owner=p.id;else{p.seatId=null;p.action='idle';p.timer=1;}}
    this.people.push(p);
  }
}
export function validateSave(raw){
  if(!raw||raw.version!==1||!Array.isArray(raw.people)||!raw.people.length||raw.people.length>24||!Number.isFinite(raw.minute)||raw.minute<0||raw.minute>=1440||!['clear','cloudy','rain'].includes(raw.weather))return null;
  const ids=new Set();for(const p of raw.people){if(!Number.isInteger(p.id)||ids.has(p.id)||typeof p.name!=='string'||!p.appearance?.hair||!p.appearance?.clothing||!p.personality||!p.needs||!Array.isArray(p.interests)||!Number.isFinite(p.x)||!Number.isFinite(p.z)||Math.abs(p.x)>26||Math.abs(p.z)>20||!['default','text','image'].includes(p.source))return null;ids.add(p.id);}return raw;
}
