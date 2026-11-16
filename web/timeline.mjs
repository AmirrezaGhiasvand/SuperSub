export function clamp(value,min,max){return Math.max(min,Math.min(max,value))}
export function activeCue(cues,time){return cues.findIndex(c=>c.start<=time&&time<c.end)}
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
