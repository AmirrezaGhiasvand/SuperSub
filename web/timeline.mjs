export function clamp(value,min,max){return Math.max(min,Math.min(max,value))}
export function activeCue(cues,time){return cues.findIndex(c=>c.start<=time&&time<c.end)}
export function cueBoundaries(cues){return [...new Set(cues.flatMap(c=>[c.start,c.end]).filter(Number.isFinite))].sort((a,b)=>a-b)}
export function snapTime(time,targets,threshold){
  let nearest=time,distance=threshold+1e-9;
  for(const target of targets){const gap=Math.abs(target-time);if(gap<distance){nearest=target;distance=gap}}
  return nearest;
}
export function nextBoundary(cues,time,direction){
  const edges=cueBoundaries(cues);
  return direction<0?edges.filter(t=>t<time-.001).at(-1)??null:edges.find(t=>t>time+.001)??null;
}
export function snapCue(cue,delta,mode,previousEnd,nextStart,targets,threshold){
  let moved=moveCue(cue,delta,mode,previousEnd,nextStart),correction=0,best=threshold+1e-9,target=null;
  const edges=mode==='start'?[moved.start]:mode==='end'?[moved.end]:[moved.start,moved.end];
  for(const edge of edges)for(const t of targets){const gap=Math.abs(t-edge);if(gap<best){const adjusted=moveCue(moved,t-edge,mode,previousEnd,nextStart);const aligned=mode==='start'?adjusted.start:mode==='end'?adjusted.end:edge+(adjusted.start-moved.start);if(Math.abs(aligned-t)<.000001){best=gap;correction=t-edge;target=t}}}
  return {cue:moveCue(moved,correction,mode,previousEnd,nextStart),target};
}
export function shiftCues(cues,delta){
  if(!Number.isFinite(delta))throw Error('Enter a valid shift amount.');
  if(!cues.length)return [];
  const applied=Math.max(delta,-cues[0].start);
  return cues.map(c=>({...c,start:Math.round((c.start+applied)*1000)/1000,end:Math.round((c.end+applied)*1000)/1000}));
}
export function moveCue(cue,delta,mode,previousEnd,nextStart){
  const minimum=Math.min(.08,cue.end-cue.start);
  if(mode==='start')return {...cue,start:clamp(cue.start+delta,previousEnd,cue.end-minimum)};
  if(mode==='end')return {...cue,end:clamp(cue.end+delta,cue.start+minimum,nextStart)};
  const shift=clamp(delta,previousEnd-cue.start,nextStart-cue.end);
  return {...cue,start:cue.start+shift,end:cue.end+shift};
}
