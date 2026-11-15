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

def execute(request, report):
    import media_tools
    from faster_whisper import WhisperModel
    report({'phase':'Loading model (low memory)','progress':None})
    engine=WhisperModel(request['model'],device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
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

if __name__=='__main__':
    request_path=Path(sys.argv[1]);folder=request_path.parent
    try:
        value=execute(json.loads(request_path.read_text(encoding='utf-8')),lambda s:write_json(folder/'worker-state.json',s))
        write_json(folder/'worker-result.json',value)
    except MemoryError:
        print(MEMORY_HELP,file=sys.stderr);sys.exit(1)
    except Exception as e:
        print(str(e),file=sys.stderr);sys.exit(1)
