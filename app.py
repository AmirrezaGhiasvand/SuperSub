from pathlib import Path
import json, uuid, threading, shutil, subprocess, sys
import local_models
import media_tools
import math
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
app = FastAPI(title='SuperSub')
lock = threading.Lock()
jobs = {}
previews = {}

@app.get('/api/health')
def health():
    return {'app':'SuperSub','version':'timeline-1'}

def ensure_idle(pid):
    if jobs.get(pid,{}).get('status')=='running':
        raise HTTPException(409,'Wait for generation to finish or cancel it first.')

def prepare_preview(pid, p, source):
    previews[pid]={'status':'preparing'}
    def work():
        temporary=p/'preview.partial.mp4'
        try:
            media_tools.convert(source,temporary,preview=True)
            temporary.replace(p/'preview.mp4')
            previews[pid]={'status':'ready'}
        except Exception as e:
            previews[pid]={'status':'failed','error':str(e)}
        finally: temporary.unlink(missing_ok=True)
    threading.Thread(target=work,daemon=True).start()

def project(pid):
    if not pid.isalnum(): raise HTTPException(400, 'Invalid project')
    p = DATA / pid
    if not p.is_dir() or not (p/'project.json').is_file(): raise HTTPException(404)
    return p

def save(p, value):
    tmp = p / 'project.tmp'
    tmp.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    tmp.replace(p / 'project.json')

def reflow(words, limit, pause=.45):
    cues, group = [], []
    for w in words:
        if group and (len(group) >= limit or w['start'] - group[-1]['end'] >= pause or w['end']-group[0]['start']>6):
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
    return [dict(id=k, name=v['name'], path=v['path'], profile=v['profile'], ready=local_models.valid_folder(Path(v['path'])), experimental=v['profile']!='multilingual') for k,v in local_models.catalog().items()]

@app.post('/api/models/register')
def register_model(body: dict):
    try:
        key, entry = local_models.register(str(body.get('path','')), body.get('profile','multilingual'))
    except ValueError as e:
        raise HTTPException(400,str(e))
    return dict(id=key, **entry)

@app.post('/api/models/browse')
def browse_model():
    try:
        result = subprocess.run([sys.executable,str(ROOT/'model_picker.py')],capture_output=True,text=True,encoding='utf-8',timeout=120,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if result.returncode: raise RuntimeError('Folder picker is unavailable. Paste the model folder path instead.')
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, RuntimeError, json.JSONDecodeError) as e:
        raise HTTPException(400,'Folder picker closed or unavailable. Paste the model folder path instead.') from e

@app.get('/api/projects')
def projects():
    result=[]
    for p in DATA.glob('*/project.json'):
        try:
            v=json.loads(p.read_text(encoding='utf-8'))
            if v.get('generated', bool(v.get('words'))): result.append(v)
        except (OSError,ValueError): continue
    return result

@app.get('/api/projects/{pid}')
def get_project(pid: str):
    return json.loads((project(pid)/'project.json').read_text(encoding='utf-8'))

@app.get('/api/projects/{pid}/preview')
def preview_status(pid: str):
    p=project(pid)
    if (p/'preview.mp4').exists(): return {'status':'ready'}
    if pid not in previews:
        v=get_project(pid); prepare_preview(pid,p,p/v['source'])
    return previews[pid]

@app.post('/api/projects')
def upload(file: UploadFile):
    pid = uuid.uuid4().hex
    p = DATA / pid
    p.mkdir()
    suffix = Path(file.filename or '').suffix.lower()
    with (p / ('source'+suffix)).open('wb') as out: shutil.copyfileobj(file.file, out)
    value = dict(id=pid, name=file.filename, source='source'+suffix, words=[], cues=[])
    save(p,value)
    prepare_preview(pid,p,p/value['source'])
    return value

@app.get('/api/projects/{pid}/media')
def media(pid: str):
    p=project(pid); value=json.loads((p/'project.json').read_text(encoding='utf-8'))
    return FileResponse(p/'preview.mp4' if (p/'preview.mp4').exists() else p/value['source'])

@app.delete('/api/projects/{pid}')
def delete(pid: str):
    if jobs.get(pid,{}).get('status')=='running': raise HTTPException(409,'Cancel processing first')
    if previews.get(pid,{}).get('status')=='preparing': raise HTTPException(409,'Wait for video preparation to finish.')
    shutil.rmtree(project(pid)); return {'ok':True}

@app.post('/api/projects/{pid}/run')
def run(pid: str, settings: dict):
    p=project(pid)
    model=settings.get('model','turbo')
    try: limit=int(settings.get('limit',8))
    except (ValueError,TypeError): raise HTTPException(400,'Word limit must be an integer from 1 to 30.')
    try: pause=float(settings.get('pause',.45))
    except (ValueError,TypeError): raise HTTPException(400,'Pause threshold must be between 0.1 and 2 seconds.')
    if not math.isfinite(pause) or not .1<=pause<=2: raise HTTPException(400,'Pause threshold must be between 0.1 and 2 seconds.')
    entry = local_models.catalog().get(model)
    if not entry or not 1<=limit<=30: raise HTTPException(400,'Invalid settings')
    if entry['profile']=='nava': raise HTTPException(400,'Nava requires validated forced alignment; experimental transcription is disabled.')
    if entry['profile']=='persian' and settings.get('language')!='fa': raise HTTPException(400,'Select Persian for this model')
    if not local_models.valid_folder(Path(entry['path'])): raise HTTPException(400,'Local model unavailable. Locate its folder again.')
    if not lock.acquire(False): raise HTTPException(409,'Another transcription is running')
    jobs[pid]={'status':'running','phase':'Preparing audio','progress':None,'cancel':False}
    def work():
        try:
            from faster_whisper import WhisperModel
            value=json.loads((p/'project.json').read_text(encoding='utf-8'))
            audio=p/'audio.wav'
            media_tools.convert(p/value['source'],audio)
            if jobs[pid]['cancel']: jobs[pid]['status']='cancelled'; return
            jobs[pid]['phase']='Loading model'
            engine=WhisperModel(entry['path'],device='cpu',compute_type='int8',local_files_only=True)
            if jobs[pid]['cancel']: jobs[pid]['status']='cancelled'; return
            jobs[pid]['phase']='Recognizing speech'
            samples=media_tools.load_audio(audio)
            segments,info=engine.transcribe(samples,language=settings.get('language') or None,word_timestamps=True,vad_filter=True,initial_prompt=settings.get('glossary') or None)
            words=[]
            for seg in segments:
                if jobs[pid]['cancel']: jobs[pid]['status']='cancelled'; return
                for w in seg.words or []:
                    if not w.word.strip(): continue
                    words.append(dict(start=w.start,end=w.end,word=w.word.strip().replace('ي','ی').replace('ك','ک')))
                jobs[pid]['progress']=min(99,round(100*seg.end/max(info.duration,.001)))
            if jobs[pid]['cancel']: jobs[pid]['status']='cancelled'; return
            jobs[pid]['phase']='Building subtitles'
            if not words:
                jobs[pid].update(status='empty',phase='No speech detected',progress=100)
                return
            value.update(words=words,cues=reflow(words,limit,pause),settings=settings,edited=False,generated=True,duration=float(info.duration))
            save(p,value); jobs[pid].update(status='complete',phase='Complete',progress=100)
        except Exception as e: jobs[pid].update(status='failed',error=str(e))
        finally:
            try: (p/'audio.wav').unlink(missing_ok=True)
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
    ensure_idle(pid)
    previous=0
    for c in cues:
        try: start,end=float(c['start']),float(c['end'])
        except (KeyError,ValueError,TypeError): raise HTTPException(400,'Invalid timing')
        if not isinstance(c.get('text'),str) or not math.isfinite(start) or not math.isfinite(end) or not 0<=previous<=start<end: raise HTTPException(400,'Invalid or overlapping timing')
        previous=float(c['end'])
        c['start'],c['end']=start,end
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8')); v.update(cues=cues,edited=True); save(p,v)
    return v

@app.post('/api/projects/{pid}/reflow')
def flow(pid: str, settings: dict):
    ensure_idle(pid)
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8'))
    if v.get('edited'): raise HTTPException(409,'Manual edits exist. Automatic reflow requires realignment, which is not yet available.')
    try: limit=int(settings.get('limit',8))
    except (ValueError,TypeError): raise HTTPException(400,'Invalid word limit')
    if not 1<=limit<=30: raise HTTPException(400)
    v['cues']=reflow(v['words'],limit); save(p,v); return v

def stamp(seconds):
    ms=round(float(seconds)*1000); s,ms=divmod(ms,1000); m,s=divmod(s,60); h,m=divmod(m,60)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

@app.get('/api/projects/{pid}/srt')
def export(pid: str):
    p=project(pid); v=json.loads((p/'project.json').read_text(encoding='utf-8'))
    if not v['cues']: raise HTTPException(400,'Generate subtitles before exporting.')
    out=p/'subtitles.srt'
    out.write_text('\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(v['cues'],1))+'\n',encoding='utf-8')
    return FileResponse(out,filename=Path(v['name']).stem+'.srt')

@app.get('/api/projects/{pid}/vtt')
def export_vtt(pid: str):
    v=get_project(pid)
    if not v['cues']: raise HTTPException(400,'Generate subtitles before exporting.')
    text='WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start']).replace(',','.')} --> {stamp(c['end']).replace(',','.')}\n{c['text']}" for c in v['cues'])+'\n'
    return Response(text,media_type='text/vtt')

@app.get('/api/projects/{pid}/txt')
def export_text(pid: str):
    v=get_project(pid)
    if not v['cues']: raise HTTPException(400,'Generate subtitles before exporting.')
    return Response('\n'.join(c['text'] for c in v['cues'])+'\n',media_type='text/plain')

app.mount('/assets',StaticFiles(directory=ROOT/'assets', check_dir=False),name='assets')
app.mount('/',StaticFiles(directory=ROOT/'web',html=True),name='web')
