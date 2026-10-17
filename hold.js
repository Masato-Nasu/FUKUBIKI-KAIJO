export function holdGate(done,{delay=1000,now=()=>performance.now(),setTimer=setTimeout,clearTimer=clearTimeout}={}){
 let active=false,timer,started;
 const cancel=()=>{active=false;clearTimer(timer)};
 const complete=()=>{if(!active)return false;active=false;clearTimer(timer);done();return true};
 const tick=()=>{if(!active)return;const left=delay-(now()-started);if(left>0){timer=setTimer(tick,left);return}complete()};
 return{start(){if(active)return;active=true;started=now();timer=setTimer(tick,delay)},finish(){if(active&&now()-started>=delay)return complete();cancel();return false},cancel};
}
// Listen on the document so release remains reliable even when capture is unavailable.
export function bindHold(button,done,{root=button.ownerDocument,view=root.defaultView,delay=1000,now,setTimer,clearTimer}={}){
 let pointer=null,key=null;
 const clearVisual=()=>button.classList.remove('holding');
 const gate=holdGate(()=>{clearVisual();pointer=null;key=null;done()},{delay,now,setTimer,clearTimer});
 const cancel=()=>{gate.cancel();pointer=null;key=null;clearVisual()};
 const begin=()=>{if(button.disabled)return false;button.classList.add('holding');gate.start();return true};
 const outside=(x,y)=>{const r=button.getBoundingClientRect();return x<r.left-16||x>r.right+16||y<r.top-16||y>r.bottom+16};
 button.addEventListener('pointerdown',e=>{if(pointer!==null||key!==null||button.disabled||(e.button!==undefined&&e.button!==0))return;e.preventDefault();pointer=e.pointerId;if(!begin()){pointer=null;return}try{button.setPointerCapture?.(e.pointerId)}catch{}});
 root.addEventListener('pointermove',e=>{if(pointer===e.pointerId&&outside(e.clientX,e.clientY))cancel()},{capture:true});
 root.addEventListener('pointerup',e=>{if(pointer!==e.pointerId)return;gate.finish();cancel()},{capture:true});
 root.addEventListener('pointercancel',e=>{if(pointer===e.pointerId)cancel()},{capture:true});
 // Older embedded browsers may provide only touch events.
 if(!view?.PointerEvent){button.addEventListener('touchstart',e=>{if(pointer!==null||button.disabled||e.touches.length!==1)return;e.preventDefault();pointer='touch';begin()},{passive:false});root.addEventListener('touchmove',e=>{if(pointer==='touch'&&(e.touches.length!==1||outside(e.touches[0].clientX,e.touches[0].clientY)))cancel()},{capture:true,passive:true});root.addEventListener('touchend',()=>{if(pointer==='touch'){gate.finish();cancel()}},{capture:true});root.addEventListener('touchcancel',cancel,{capture:true})}
 button.addEventListener('keydown',e=>{if(![' ','Enter'].includes(e.key)||e.repeat||pointer!==null||key!==null)return;e.preventDefault();key=e.key;begin()});root.addEventListener('keyup',e=>{if(key===e.key){gate.finish();cancel()}},{capture:true});
 button.addEventListener('contextmenu',e=>e.preventDefault());button.addEventListener('click',e=>e.preventDefault());
 root.addEventListener('visibilitychange',()=>{if(root.hidden)cancel()});view?.addEventListener('blur',cancel);
 return{cancel};
}
