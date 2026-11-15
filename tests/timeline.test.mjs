import {test} from 'node:test';
import assert from 'node:assert/strict';
import {moveCue,activeCue} from '../web/timeline.mjs';
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
