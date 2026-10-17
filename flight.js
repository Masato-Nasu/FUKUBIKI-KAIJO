// Side ejection: horizontal velocity stays constant; gravity accelerates the fall.
export function ballPath(source,landing){
 const points=[],impactX=Math.max(48,Math.min(landing.x-55,source.x-70));
 for(let i=0;i<=48;i++){const t=i/48;points.push({x:source.x+(impactX-source.x)*t,y:source.y+(landing.y-source.y)*t*t,offset:.72*t})}
 // A small damped bounce and a short roll, entirely inside the tray.
 for(let i=1;i<=16;i++){const t=i/16;points.push({x:impactX+(landing.x-22-impactX)*t,y:landing.y-18*4*t*(1-t),offset:.72+.18*t})}
 for(let i=1;i<=10;i++){const t=i/10,ease=1-(1-t)**2;points.push({x:landing.x-22+22*ease,y:landing.y,offset:.90+.10*t})}
 return points;
}
