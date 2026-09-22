export const actionLabels={walk:'Гуляет',run:'Бежит',read:'Читает книгу',rest:'Отдыхает',phone:'Смотрит телефон',drink:'Пьёт кофе',eat:'Обедает',talk:'Разговаривает',shop:'Выбирает книгу',home:'Дома',work:'На работе',wait:'Ждёт автобус',idle:'Наблюдает',wave:'Приветствует знакомого'};
export function planCommand(text,people=[],selfId=null) {
  const s=text.toLowerCase().trim();if(!s)return {steps:[],error:'Напишите, чем хочется заняться.'};
  const steps=[];let note='';
  if(/самостоятель|своим дел|свобод/.test(s))steps.push({action:'auto',label:'Вернуться к своим делам'});
  else if(/стой|стоп|останов/.test(s))steps.push({action:'stop',label:'Остановиться здесь'});
  else {
    if(/бег|беж|пробе/.test(s)){const loops=/два|2/.test(s)?2:/три|3/.test(s)?3:1;for(let i=0;i<loops;i++)for(const p of [{x:-15,z:-5},{x:0,z:-5},{x:0,z:8},{x:-15,z:8}])steps.push({action:'run',point:p,label:`Пробежать ${i+1}-й круг · ${p.x===-15?(p.z===-5?'север':'запад'):(p.z===-5?'восток':'юг')} парка`});}
    if(/поговор|подойди к|поболта|к человеку|знаком/.test(s)){
      let target=people.find(p=>p.id!==selfId&&s.includes(p.name.toLowerCase()));
      if(!target&&/красн/.test(s))target=people.find(p=>p.id!==selfId&&red(p.appearance.clothing.outerwear));
      if(!target)target=people.find(p=>p.id!==selfId);
      if(target)steps.push({action:'talk',targetId:target.id,label:`Подойти к ${target.name} и поговорить`});else note='Рядом пока нет собеседников — можно прогуляться.';
    }
    if(/кафе|кофе|чай|напит/.test(s)){steps.push({action:/поес|еда|обед|перекус/.test(s)?'eat':'drink',location:/окн/.test(s)?'window':'cafe',label:/окн/.test(s)?'Дойти до кафе, найти свободное место у окна и сесть':'Дойти до кафе, сесть и заказать напиток'});}
    else if(/поес|перекус|обед|еду/.test(s))steps.push({action:'eat',label:'Зайти в кафе и перекусить'});
    if(/книжн|магазин|посмотр.{0,12}книг/.test(s))steps.push({action:'shop',label:'Зайти в книжный и посмотреть книги'});
    if(/чита|почит|чтени/.test(s))steps.push({action:'read',duration:Infinity,label:'Найти свободную лавочку, сесть и почитать'});
    if(/телефон/.test(s))steps.push({action:'phone',label:'Остановиться и посмотреть телефон'});
    if(/отдох|отдых|лавоч|сядь|сесть|посид/.test(s)&&!steps.some(x=>['read','drink','eat'].includes(x.action)))steps.push({action:'rest',label:'Найти свободную лавочку и отдохнуть'});
    if(/гуля|прогул|пройд/.test(s)&&!steps.length)for(const p of [{x:-14,z:3},{x:-6,z:8},{x:0,z:0}])steps.push({action:'walk',point:p,label:'Прогуляться по дорожкам парка'});
    if(/домой/.test(s))steps.push({action:'home',label:'Вернуться домой'});
    if(/автобус|остановк/.test(s))steps.push({action:'wait',label:'Подойти к остановке и подождать транспорт'});
  }
  if(!steps.length)return {steps:[],error:note||'Пока понимаю прогулки, бег, кафе, чтение, книжный, телефон, отдых и разговоры. Например: «Пробеги два круга, потом отдохни».'};
  return {steps,note};
}
function red(hex){const n=parseInt(hex.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;return r>g*1.35&&r>b*1.2;}
export function chooseIntent(p,world) {
  const n=p.needs,h=world.minute/60;
  if(world.weather==='rain')return {action:p.interests.includes('reading')?'shop':'drink',reason:'Переждать дождь в помещении'};
  if(h<6||h>22)return {action:'home',reason:'Пора домой'};
  if(n.energy<.25)return {action:'rest',reason:'Немного устал'};
  if(n.hunger>.65)return {action:'eat',reason:'Хочется перекусить'};
  if(n.social>.65&&p.personality.sociability>.45){const near=world.people.filter(q=>q.id!==p.id&&!q.partnerId&&!q.manual&&Math.hypot(p.x-q.x,p.z-q.z)<12);if(near.length)return {action:'talk',targetId:near[0].id,reason:'Хочется общения'};}
  if(h>8&&h<10&&p.appearance.ageGroup==='adult')return {action:'work',reason:'Утренний распорядок'};
  const scored=[['walk',.4+n.interest*.35],['read',p.interests.includes('reading')?.85:.18],['drink',p.interests.includes('coffee')?.65:.27],['run',p.personality.energy*.55],['shop',p.personality.curiosity*.4],['phone',.3],['wait',.17]];
  const recent=p.memory.slice(-2).map(m=>m.action);
  scored.forEach(s=>s[1]+=Math.random()*.3-(recent.includes(s[0])?.5:0));scored.sort((a,b)=>b[1]-a[1]);return {action:scored[0][0],reason:'По настроению'};
}
