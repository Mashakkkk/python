export class Ambience {
  constructor(){this.context=null;this.on=false;this.timer=null;}
  async toggle(){
    if(!this.context){const C=window.AudioContext||window.webkitAudioContext;if(!C)throw new Error('Браузер не поддерживает звук');this.context=new C();const ctx=this.context;this.master=ctx.createGain();this.master.gain.value=0;this.master.connect(ctx.destination);
      const buffer=ctx.createBuffer(1,ctx.sampleRate*4,ctx.sampleRate),data=buffer.getChannelData(0);let prev=0;for(let i=0;i<data.length;i++){prev=(prev+(Math.random()*2-1)*.03)/1.02;data[i]=prev;}
      const source=ctx.createBufferSource();source.buffer=buffer;source.loop=true;const filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=600;source.connect(filter);filter.connect(this.master);source.start();
    }
    await this.context.resume();this.on=!this.on;this.master.gain.setTargetAtTime(this.on?.36:0,this.context.currentTime,.4);
    if(this.on){this.timer=setInterval(()=>this.bird(),4800);this.bird();}else clearInterval(this.timer);return this.on;
  }
  bird(){if(!this.on||document.hidden)return;const c=this.context;for(let i=0;i<3;i++){const o=c.createOscillator(),g=c.createGain(),t=c.currentTime+i*.16;o.type='sine';o.frequency.setValueAtTime(2400+i*120,t);o.frequency.exponentialRampToValueAtTime(3600,t+.06);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.022,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+.12);o.connect(g);g.connect(this.master);o.start(t);o.stop(t+.13);}}
}
