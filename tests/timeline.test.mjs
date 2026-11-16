import {test} from 'node:test';
import assert from 'node:assert/strict';
import {moveCue,activeCue,shiftCues,cueBoundaries,snapTime,nextBoundary,snapCue} from '../web/timeline.mjs';
test('edge snapping uses nearest boundary inside threshold only',()=>{
 const cues=[{start:1,end:2},{start:2,end:3}];
 assert.deepEqual(cueBoundaries(cues),[1,2,3]);
 assert.equal(snapTime(1.92,cueBoundaries(cues),.15),2);
 assert.equal(snapTime(1.5,cueBoundaries(cues),.15),1.5);
});
test('keyboard boundary steps skip the current edge in either direction',()=>{
 const cues=[{start:1,end:2},{start:3,end:4}];
 assert.equal(nextBoundary(cues,2,1),3);assert.equal(nextBoundary(cues,2,-1),1);
 assert.equal(nextBoundary(cues,0,-1),null);assert.equal(nextBoundary(cues,5,1),null);
});
test('trim snaps to playhead without crossing other subtitles',()=>{
 const cue={start:1,end:3};
 assert.equal(snapCue(cue,.93,'start',0,4,[2],.1).cue.start,2);
 assert.equal(snapCue(cue,1.9,'end',0,4,[5],.2).cue.end,4);
 assert.equal(snapCue(cue,1.9,'end',0,4,[5],.2).target,null);
});
test('moving can snap either edge while preserving cue duration',()=>{
 const result=snapCue({start:1,end:2},.95,'move',0,5,[3],.1);
 assert.ok(Math.abs(result.cue.start-2)<1e-9);assert.equal(result.cue.end,3);assert.equal(result.target,3);
});
test('global shift preserves duration and spacing without negative times',()=>{
 const cues=[{start:1,end:2,text:'a'},{start:3,end:4,text:'b'}];
 assert.deepEqual(shiftCues(cues,.5).map(c=>[c.start,c.end]),[[1.5,2.5],[3.5,4.5]]);
 assert.deepEqual(shiftCues(cues,-5).map(c=>[c.start,c.end]),[[0,1],[2,3]]);
 assert.equal(cues[0].start,1);
});
test('overlay is absent during pauses and switches exactly at cue boundaries',()=>{
  const cues=[{start:0,end:1},{start:2,end:3}];
  assert.equal(activeCue(cues,.5),0);assert.equal(activeCue(cues,1),-1);assert.equal(activeCue(cues,2),1);assert.equal(activeCue(cues,3),-1);
});
test('moving a block preserves its length and avoids adjacent cues',()=>{
  const c={start:2,end:4,text:'سلام'};
  assert.deepEqual(moveCue(c,10,'move',1,6),{...c,start:4,end:6});
  assert.deepEqual(moveCue(c,-10,'move',1,6),{...c,start:1,end:3});
});
test('trimming cannot invert or overlap a cue',()=>{
  const c={start:2,end:4,text:'سلام'};
  assert.equal(moveCue(c,-20,'start',1,6).start,1);
  assert.equal(moveCue(c,20,'end',1,6).end,6);
  assert.ok(moveCue(c,20,'start',1,6).start<c.end);
  assert.ok(moveCue(c,-20,'end',1,6).end>c.start);
});
