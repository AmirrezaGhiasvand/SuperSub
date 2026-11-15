"""Local-only model registration; never downloads or copies weights."""
from pathlib import Path
import hashlib
import json
import threading

ROOT = Path(__file__).parent
REGISTRY = ROOT / 'data' / 'local-models.json'
GUARD = threading.Lock()
BUILTINS = {
    'turbo': dict(path=str(ROOT/'models'/'whisper-large-v3-turbo'), name='Whisper Large V3 Turbo', profile='multilingual'),
    'persian': dict(path=str(ROOT/'models'/'givia-persian'), name='Givia Persian Turbo', profile='persian'),
    'nava': dict(path=str(ROOT/'models'/'nava-ct2'), name='Nava (alignment pending)', profile='nava'),
}

def valid_folder(folder):
    return folder.is_dir() and all((folder/name).is_file() for name in ('model.bin','config.json','tokenizer.json'))

def catalog():
    result = {k:dict(v) for k,v in BUILTINS.items()}
    if REGISTRY.exists():
        result.update(json.loads(REGISTRY.read_text(encoding='utf-8')))
    return result

def register(path, profile):
    folder = Path(path.strip().strip('"')).expanduser()
    if not folder.is_absolute() or not valid_folder(folder):
        raise ValueError('Select a full local folder path containing model.bin, config.json and tokenizer.json (CTranslate2 Whisper format).')
    if profile not in ('multilingual','persian','nava'):
        raise ValueError('Select a supported model profile.')
    folder = folder.resolve()
    if 'nava' in folder.name.lower(): profile = 'nava'
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
