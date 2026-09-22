export const COLORS = {dark:'#342b29',brown:'#6d4931',blond:'#c5a366',gray:'#aaa6a0',red:'#a45a35'};
export const ageLabels={young_adult:'Молодой человек',adult:'Взрослый',senior:'Пожилой'};
const first=(s,patterns,fallback)=>patterns.find(([re])=>re.test(s))?.[1]??fallback;
export function parseDescription(text='',source='text') {
  const s=text.toLowerCase();
  const female=/девуш|женщин|бабуш|она\b|застенчивая|спокойная/u.test(s);
  const age=Number(s.match(/\b(\d{2})\s*(?:лет|год)/)?.[1]);
  const top=first(s,[[/зел[её]н/,'#647c51'],[/красн/,'#ac5146'],[/син[ийяе]/,'#54758a'],[/голуб/,'#7b9fae'],[/ж[её]лт/,'#bfa061'],[/беж/,'#c6b38e'],[/бел/,'#d9d8ca'],[/ч[её]рн/,'#383d39'],[/розов/,'#b87981']],female?'#80937b':'#7e8997');
  const hairColor=first(s,[[/светл.{0,15}волос|блон/,'blond'],[/рыж/,'red'],[/сед/,'gray'],[/каштан|коричнев.{0,12}волос/,'brown']],'dark');
  const action=first(s,[[/чит|книг.{0,10}лавоч/,'read'],[/книжн|магазин/,'shop'],[/кофе|кафе|напит|чай/,'drink'],[/бег|беж|пробеж/,'run'],[/телефон/,'phone'],[/есть|поес|перекус|еда/,'eat'],[/отдых|отдох|посид|сидеть/,'rest']],'walk');
  const nameMatch=text.match(/(?:имя|зовут|по имени)\s*[:—-]?\s*([А-ЯЁа-яёA-Za-z]{2,25})/iu);
  return {
    name:nameMatch ? nameMatch[1][0].toUpperCase()+nameMatch[1].slice(1) : female?'Алиса':'Саша',source,
    appearance:{gender:female?'female':'male',ageGroup:age>=60||/пожил|бабуш|дедуш/.test(s)?'senior':age>=30||/взросл|мужчин|женщин/.test(s)?'adult':'young_adult',height:first(s,[[/невысок|низкого/,'short'],[/высок/,'tall']],'medium'),bodyType:first(s,[[/стройн|худ/,'slim'],[/крупн|полн/,'broad']],'average'),skin:first(s,[[/т[её]мн.{0,10}кож|смугл/,'#a67654'],[/светл.{0,10}кож/,'#edd0b7']],'#d6ac8c'),hair:{length:first(s,[[/длинн.{0,12}волос/,'long'],[/до плеч/,'medium']],'short'),color:COLORS[hairColor],style:first(s,[[/кудр|вьющ/,'curly'],[/пучок/,'bun']],'straight')},clothing:{outerwear:top,bottom:/светл.{0,10}брюк/.test(s)?'#b5ad99':'#465365',shoes:'#e1ded2'},accessories:/(?:^|[\s,])очк/.test(s)?['glasses']:[]},
    personality:{sociability:/застен|необщит|интроверт/.test(s)?.25:/общит|дружел/.test(s)?.85:.55,energy:/спокой|медлен/.test(s)?.4:/энергич|актив|спорт/.test(s)?.85:.6,curiosity:/любозн|книг|чит/.test(s)?.8:.55,patience:/спокой|терпел/.test(s)?.85:.55,confidence:/застен|робк/.test(s)?.35:.65},
    interests:[...(/чит|книг/.test(s)?['reading']:[]),...(/парк|природ/.test(s)?['parks']:[]),...(/кофе|кафе/.test(s)?['coffee']:[]),...(/бег|спорт/.test(s)?['running']:[])],
    initialIntent:{action,location:['read','rest'].includes(action)?'park_bench':['eat','drink'].includes(action)?'cafe':'park',duration:action==='read'?'until_changed':'automatic'}
  };
}
// Deliberately a local colour estimator, not an identity or face-recognition model.
export async function analyzePhoto(file) {
  if(!file||!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('Поддерживаются только JPG, PNG и WebP. Выберите другой файл.');
  if(file.size>10*1024*1024)throw new Error('Изображение слишком большое. Максимум — 10 МБ.');
  let bmp;try{bmp=await createImageBitmap(file);}catch{throw new Error('Не удалось прочитать изображение. Возможно, файл повреждён.');}
  if(bmp.width<32||bmp.height<32){bmp.close();throw new Error('Нужен портрет размером хотя бы 32 × 32 пикселя.');}
  const c=document.createElement('canvas');c.width=96;c.height=128;const ctx=c.getContext('2d',{willReadFrequently:true});
  const ratio=Math.max(96/bmp.width,128/bmp.height),w=bmp.width*ratio,h=bmp.height*ratio;ctx.drawImage(bmp,(96-w)/2,(128-h)/2,w,h);bmp.close();
  function sample(x,y,w,h){const a=ctx.getImageData(x,y,w,h).data,channels=[[],[],[]];for(let i=0;i<a.length;i+=4){if(a[i+3]<128)continue;for(let k=0;k<3;k++)channels[k].push(a[i+k]);}return '#'+channels.map(a=>{a.sort((x,y)=>x-y);return (a[Math.floor(a.length/2)]??150).toString(16).padStart(2,'0');}).join('');}
  return {hair:sample(32,15,32,13),skin:sample(39,35,18,22),top:sample(27,84,42,30)};
}
