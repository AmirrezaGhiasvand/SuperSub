from pathlib import Path
import json, uuid, threading, shutil
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
app = FastAPI(title='SuperSub')
lock = threading.Lock()
jobs = {}
MODELS = {'turbo': 'whisper-large-v3-turbo', 'persian': 'givia-persian', 'nava': 'nava-ct2'}

def project(pid):
    if not pid.isalnum(): raise HTTPException(400, 'Invalid project')
    p = DATA / pid
    if not p.exists(): raise HTTPException(404)
    return p

def save(p, value):
    tmp = p / 'project.tmp'
    tmp.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    tmp.replace(p / 'project.json')

def reflow(words, limit):
    cues, group = [], []
    for w in words:
        if group and (len(group) >= limit or w['start'] - group[-1]['end'] > .7):
            cues.append(dict(start=group[0]['start'], end=group[-1]['end'], text=' '.join(x['word'] for x in group)))
            group = []
        group.append(w)
        if w['word'].endswith(('.', '؟', '!', '?')):
            cues.append(dict(start=group[0]['start'], end=group[-1]['end'], text=' '.join(x['word'] for x in group)))
            group = []
    if group: cues.append(dict(start=group[0]['start'], end=group[-1]['end'], text=' '.join(x['word'] for x in group)))
    return cues

@app.get('/api/models')
def models():
    return [dict(id=k, name=v, ready=(ROOT/'models'/v/'model.bin').exists(), experimental=k!='turbo') for k,v in MODELS.items()]

@app.get('/api/projects')
def projects():
    return [json.loads(p.read_text(encoding='utf-8')) for p in DATA.glob('*/project.json')]

@app.post('/api/projects')
def upload(file: UploadFile):
    pid = uuid.uuid4().hex
    p = DATA / pid
    p.mkdir()
    suffix = Path(file.filename or '').suffix.lower()
    with (p / ('source'+suffix)).open('wb') as out: shutil.copyfileobj(file.file, out)
    value = dict(id=pid, name=file.filename, source='source'+suffix, words=[], cues=[])
    save(p,value)
    return value

@app.get('/api/projects/{pid}/media')
def media(pid: str):
    p=project(pid); value=json.loads((p/'project.json').read_text(encoding='utf-8'))
    return FileResponse(p/value['source'])

@app.delete('/api/projects/{pid}')
def delete(pid: str):
    if jobs.get(pid,{}).get('status')=='running': raise HTTPException(409,'Cancel processing first')
    shutil.rmtree(project(pid)); return {'ok':True}

@app.post('/api/projects/{pid}/run')
def run(pid: str, settings: dict):
    p=project(pid)
    model=settings.get('model','turbo'); limit=int(settings.get('limit',8))
    if model not in MODELS or not 1<=limit<=30: raise HTTPException(400,'Invalid settings')
    if model=='nava': raise HTTPException(400,'Nava requires validated forced alignment; experimental transcription is disabled.')
    if model!='turbo' and settings.get('language')!='fa': raise HTTPException(400,'Select Persian for this model')
    if not (ROOT/'models'/MODELS[model]/'model.bin').exists(): raise HTTPException(400,'Model is not installed')
    if not lock.acquire(False): raise HTTPException(409,'Another transcription is running')
    jobs[pid]={'status':'running','progress':0,'cancel':False}
    def work():
        try:
            from faster_whisper import WhisperModel
            value=json.loads((p/'project.json').read_text(encoding='utf-8'))
            engine=WhisperModel(str(ROOT/'models'/MODELS[model]),device='cpu',compute_type='int8',local_files_only=True)
            segments,info=engine.transcribe(str(p/value['source']),language=settings.get('language') or None,word_timestamps=True,vad_filter=True,initial_prompt=settings.get('glossary') or None)
            words=[]
            for seg in segments:
                if jobs[pid]['cancel']: jobs[pid]['status']='cancelled'; return
                for w in seg.words or []:
                    words.append(dict(start=w.start,end=w.end,word=w.word.strip().replace('ي','ی').replace('ك','ک')))
                jobs[pid]['progress']=round(100*seg.end/max(info.duration,.001))
            value.update(words=words,cues=reflow(words,limit),settings=settings,edited=False)
            save(p,value); jobs[pid]['status']='complete'
        except Exception as e: jobs[pid].update(status='failed',error=str(e))
        finally: lock.release()
    threading.Thread(target=work,daemon=True).start()
    return jobs[pid]

@app.get('/api/projects/{pid}/status')
def status(pid: str): return jobs.get(pid,{'status':'idle'})

@app.post('/api/projects/{pid}/cancel')
def cancel(pid: str):
    if pid in jobs: jobs[pid]['cancel']=True
    return {'ok':True}

@app.put('/api/projects/{pid}/cues')
def edit(pid: str, cues: list[dict]):
    previous=0
    for c in cues:
        if not isinstance(c.get('text'),str) or not 0<=previous<=float(c['start'])<float(c['end']): raise HTTPException(400,'Invalid or overlapping timing')
        previous=float(c['end'])
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8')); v.update(cues=cues,edited=True); save(p,v)
    return v

@app.post('/api/projects/{pid}/reflow')
def flow(pid: str, settings: dict):
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8'))
    if v.get('edited'): raise HTTPException(409,'Manual edits exist. Automatic reflow requires realignment, which is not yet available.')
    limit=int(settings.get('limit',8))
    if not 1<=limit<=30: raise HTTPException(400)
    v['cues']=reflow(v['words'],limit); save(p,v); return v

def stamp(seconds):
    ms=round(float(seconds)*1000); s,ms=divmod(ms,1000); m,s=divmod(s,60); h,m=divmod(m,60)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

@app.get('/api/projects/{pid}/srt')
def export(pid: str):
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8'))
    out=p/'subtitles.srt'
    out.write_text('\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(v['cues'],1))+'\n',encoding='utf-8')
    return FileResponse(out,filename=Path(v['name']).stem+'.srt')

app.mount('/assets',StaticFiles(directory=ROOT/'assets', check_dir=False),name='assets')
app.mount('/',StaticFiles(directory=ROOT/'web',html=True),name='web')
