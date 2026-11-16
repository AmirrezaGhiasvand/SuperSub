"""Bounded-memory inference in a disposable child process."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

MEMORY_HELP='Not enough system memory for this model. Close other model/server processes and memory-heavy apps, keep the Windows page file system-managed, or select a smaller local Whisper model. Saved subtitles are unchanged.'

class Cancelled(Exception): pass

def write_json(path, value):
    path=Path(path);temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8');temporary.replace(path)

def create_engine(model):
    from faster_whisper import WhisperModel
    return WhisperModel(model,device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)

def execute(request, report, engine=None):
    import media_tools
    if engine is None:
        report({'phase':'Loading model (low memory)','progress':None})
        engine=create_engine(request['model'])
    words=[];duration=0
    for offset,samples,total in media_tools.iter_audio(request['audio']):
        duration=total
        report({'phase':'Recognizing speech (low memory)','progress':min(99,round(offset/max(total,.001)*100))})
        segments,_=engine.transcribe(samples,language=request['settings'].get('language') or None,word_timestamps=True,vad_filter=True,beam_size=1,best_of=1,temperature=0,condition_on_previous_text=False,initial_prompt=request['settings'].get('glossary') or None)
        for segment in segments:
            for w in segment.words or []:
                text=w.word.strip().replace('ي','ی').replace('ك','ک')
                if text:
                    words.append(dict(start=min(total,offset+w.start),end=min(total,offset+w.end),word=text))
            report({'phase':'Recognizing speech (low memory)','progress':min(99,round((offset+segment.end)/max(total,.001)*100))})
    return {'words':words,'duration':duration}

def run_isolated(folder, model, settings, report, cancelled):
    if resident.matches(model):return resident.run(folder,model,settings,report,cancelled)
    folder=Path(folder);request=folder/'worker-request.json';state=folder/'worker-state.json';result=folder/'worker-result.json';log=folder/'worker.log'
    for p in (state,result):p.unlink(missing_ok=True)
    write_json(request,dict(audio=str(folder/'audio.wav'),model=model,settings=settings))
    env=dict(os.environ,OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_DYNAMIC='FALSE',PYTHONIOENCODING='utf-8')
    process=None
    try:
        with log.open('wb') as output:
            process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),str(request)],stdout=output,stderr=output,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            while True:
                if cancelled():raise Cancelled()
                if state.exists():
                    try:report(json.loads(state.read_text(encoding='utf-8')))
                    except (OSError,ValueError):pass
                if process.poll() is not None:break
                time.sleep(.2)
        if cancelled():raise Cancelled()
        if process.returncode or not result.exists():
            text=log.read_text(encoding='utf-8',errors='replace')[-3000:]
            if any(term in text.lower() for term in ('mkl_malloc','memory','bad_alloc','allocate')):raise RuntimeError(MEMORY_HELP)
            raise RuntimeError('Transcription worker stopped unexpectedly. '+MEMORY_HELP if not text.strip() else text[-1000:])
        return json.loads(result.read_text(encoding='utf-8'))
    finally:
        if process is not None and process.poll() is None:
            process.terminate();process.wait(timeout=15)
        for p in (request,state,result):p.unlink(missing_ok=True)

class ResidentModel:
    def __init__(self):
        self.process=None;self.model=None;self.folder=None;self.output=None
    def status(self):
        if self.process is None:return {'status':'unloaded'}
        if self.process.poll() is not None:
            return {'status':'failed','path':self.model,'error':MEMORY_HELP+' Check data/model-runtime/worker.log.'}
        return {'status':'loaded' if (self.folder/'ready.json').exists() else 'loading','path':self.model}
    def matches(self,model):
        return self.status()['status']=='loaded' and Path(self.model).resolve()==Path(model).resolve()
    def load(self,model,folder):
        self.unload();self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        for name in ('ready.json','command.json'):(self.folder/name).unlink(missing_ok=True)
        self.model=str(Path(model).resolve());write_json(self.folder/'model.json',{'model':self.model})
        self.output=(self.folder/'worker.log').open('wb')
        env=dict(os.environ,OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_DYNAMIC='FALSE')
        self.process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--serve',str(self.folder)],stdout=self.output,stderr=self.output,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        return self.status()
    def unload(self):
        if self.process is not None and self.process.poll() is None:self.process.terminate();self.process.wait(timeout=15)
        if self.output is not None:self.output.close()
        self.process=None;self.model=None
        return {'status':'unloaded'}
    def run(self,folder,model,settings,report,cancelled):
        folder=Path(folder).resolve();state=folder/'worker-state.json';result=folder/'worker-result.json'
        for p in (state,result):p.unlink(missing_ok=True)
        write_json(self.folder/'command.json',dict(audio=str(folder/'audio.wav'),model=model,settings=settings,folder=str(folder)))
        try:
            while not result.exists():
                if cancelled():self.unload();raise Cancelled()
                if self.status()['status']!='loaded':raise RuntimeError(MEMORY_HELP)
                if state.exists():
                    try:report(json.loads(state.read_text(encoding='utf-8')))
                    except (OSError,ValueError):pass
                time.sleep(.2)
            value=json.loads(result.read_text(encoding='utf-8'))
            if 'error' in value:raise RuntimeError(value['error'])
            return value
        finally:
            for p in (state,result):p.unlink(missing_ok=True)

resident=ResidentModel()
import atexit
atexit.register(resident.unload)

def serve(folder):
    folder=Path(folder);model=json.loads((folder/'model.json').read_text(encoding='utf-8'))['model']
    engine=create_engine(model);write_json(folder/'ready.json',{'ready':True})
    while True:
        command=folder/'command.json'
        if not command.exists():time.sleep(.2);continue
        request=json.loads(command.read_text(encoding='utf-8'));command.unlink()
        target=Path(request['folder'])
        try:value=execute(request,lambda s:write_json(target/'worker-state.json',s),engine)
        except Exception as e:value={'error':MEMORY_HELP if isinstance(e,MemoryError) else str(e)}
        write_json(target/'worker-result.json',value)

if __name__=='__main__' and sys.argv[1]=='--serve':
    serve(sys.argv[2])
elif __name__=='__main__':
    request_path=Path(sys.argv[1]);folder=request_path.parent
    try:
        value=execute(json.loads(request_path.read_text(encoding='utf-8')),lambda s:write_json(folder/'worker-state.json',s))
        write_json(folder/'worker-result.json',value)
    except MemoryError:
        print(MEMORY_HELP,file=sys.stderr);sys.exit(1)
    except Exception as e:
        print(str(e),file=sys.stderr);sys.exit(1)
