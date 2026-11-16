import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

test('real entry module links with the actual versioned timeline module',async()=>{
 const app=new vm.SourceTextModule(fs.readFileSync('web/app.js','utf8'));
 const geometry=new vm.SourceTextModule(fs.readFileSync('web/timeline.mjs','utf8'));
 await app.link(specifier=>{
   assert.match(specifier,/timeline\.mjs\?v=/);
   return geometry;
 });
 assert.equal(app.status,'linked');
});
test('page uses startup loader with visible failure handling',()=>{
 const html=fs.readFileSync('web/index.html','utf8');
 assert.match(html,/src="\/bootstrap\.js\?v=/);
 assert.match(fs.readFileSync('web/bootstrap.js','utf8'),/await import/);
 assert.match(fs.readFileSync('web/bootstrap.js','utf8'),/could not start/);
});
