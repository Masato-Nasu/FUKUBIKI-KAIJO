export const machineCenter={x:596,y:670};
// Angular movement stays continuous across the -180/180 seam.
export function angleDelta(previous,current){return ((current-previous+540)%360)-180}
// A peripheral side outlet reaches the tray before one full turn.
// The black sphere on the FRONT is a handle, not an outlet.
export function releaseTarget(angle,start=0){return angle<start?start-150:start+210}
export function atOutlet(angle,start=0){return angle>=start+210||angle<=start-150}
export function outletPosition(angle){const rad=angle*Math.PI/180;return{x:machineCenter.x+200*Math.cos(rad)+285*Math.sin(rad),y:machineCenter.y+200*Math.sin(rad)-285*Math.cos(rad)}}
