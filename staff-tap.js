// Use the button's native click event on touch screens, mice and keyboards.
export function bindStaffTap(button,done,{root=button.ownerDocument,view=root.defaultView,interval=1600,now=()=>performance.now(),setTimer=setTimeout,clearTimer=clearTimeout,onArmed=()=>{}}={}){
 let first=null,timer;
 const cancel=()=>{first=null;clearTimer(timer);button.classList.remove('armed');onArmed(false)};
 button.addEventListener('click',e=>{e.preventDefault();if(button.disabled)return;const current=now();if(first!==null&&current-first<=interval){cancel();done();return}first=current;button.classList.add('armed');onArmed(true);clearTimer(timer);timer=setTimer(cancel,interval)});
 button.addEventListener('contextmenu',e=>e.preventDefault());button.addEventListener('keydown',e=>{if(e.repeat&&['Enter',' '].includes(e.key))e.preventDefault()});
 root.addEventListener('visibilitychange',()=>{if(root.hidden)cancel()});view?.addEventListener('blur',cancel);return{cancel};
}
