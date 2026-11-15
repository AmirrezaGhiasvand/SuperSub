export function clamp(value,min,max){return Math.max(min,Math.min(max,value))}
export function activeCue(cues,time){return cues.findIndex(c=>c.start<=time&&time<c.end)}
export function moveCue(cue,delta,mode,previousEnd,nextStart){
  const minimum=Math.min(.08,cue.end-cue.start);
  if(mode==='start')return {...cue,start:clamp(cue.start+delta,previousEnd,cue.end-minimum)};
  if(mode==='end')return {...cue,end:clamp(cue.end+delta,cue.start+minimum,nextStart)};
  const shift=clamp(delta,previousEnd-cue.start,nextStart-cue.end);
  return {...cue,start:cue.start+shift,end:cue.end+shift};
}
