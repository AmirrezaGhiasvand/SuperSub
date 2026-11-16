"""Local-only model registration; never downloads or copies weights."""
from pathlib import Path
import hashlib
import json
import threading

ROOT = Path(__file__).parent
REGISTRY = ROOT / 'data' / 'local-models.json'
GUARD = threading.Lock()
BUILTINS = {
    'small': dict(path=str(ROOT/'models'/'whisper-small'), name='Whisper Small', profile='multilingual'),
    'medium': dict(path=str(ROOT/'models'/'whisper-medium'), name='Whisper Medium', profile='multilingual'),
    'turbo': dict(path=str(ROOT/'models'/'whisper-large-v3-turbo'), name='Whisper Large V3 Turbo', profile='multilingual'),
    'large-v3': dict(path=str(ROOT/'models'/'whisper-large-v3'), name='Whisper Large V3', profile='multilingual'),
}

def valid_folder(folder):
    return folder.is_dir() and all((folder/name).is_file() for name in ('model.bin','config.json','tokenizer.json'))

def catalog():
    result = {k:dict(v) for k,v in BUILTINS.items()}
    legacy=ROOT/'models'/'givia-persian'
    if valid_folder(legacy):
        result['persian']=dict(path=str(legacy),name='Local Persian model',profile='persian')
    if REGISTRY.exists():
        result.update({k:v for k,v in json.loads(REGISTRY.read_text(encoding='utf-8')).items() if v.get('profile')!='nava' and 'nava' not in Path(v['path']).name.lower()})
    return result

def register(path, profile):
    folder = Path(path.strip().strip('"')).expanduser()
    if not folder.is_absolute() or not valid_folder(folder):
        raise ValueError('Select a full local folder path containing model.bin, config.json and tokenizer.json (CTranslate2 Whisper format).')
    if profile not in ('multilingual','persian'):
        raise ValueError('Select a supported model profile.')
    folder = folder.resolve()
    if 'nava' in folder.name.lower(): raise ValueError('This model is not supported for subtitle generation. Choose a supported model from the README.')
    key = 'local-' + hashlib.sha256(str(folder).casefold().encode()).hexdigest()[:16]
    entry = dict(path=str(folder), name=folder.name, profile=profile)
    with GUARD:
        saved = json.loads(REGISTRY.read_text(encoding='utf-8')) if REGISTRY.exists() else {}
        saved[key] = entry
        REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        temporary = REGISTRY.with_suffix('.tmp')
        temporary.write_text(json.dumps(saved, ensure_ascii=False),encoding='utf-8')
        temporary.replace(REGISTRY)
    return key, entry
