"""Explicit downloads of ready-to-load CTranslate2 models; no conversion."""
from pathlib import Path
import argparse
from huggingface_hub import snapshot_download

MODELS = {
    'small': ('Systran/faster-whisper-small', 'whisper-small', ['model.bin','config.json','tokenizer.json','vocabulary.txt']),
    'medium': ('Systran/faster-whisper-medium', 'whisper-medium', ['model.bin','config.json','tokenizer.json','vocabulary.txt']),
    'turbo': ('dropbox-dash/faster-whisper-large-v3-turbo', 'whisper-large-v3-turbo', ['model.bin','config.json','tokenizer.json','vocabulary.json','preprocessor_config.json']),
    'large-v3': ('Systran/faster-whisper-large-v3', 'whisper-large-v3', ['model.bin','config.json','tokenizer.json','vocabulary.json','preprocessor_config.json']),
}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',choices=MODELS)
    args=parser.parse_args()
    repo,folder,files=MODELS[args.model]
    snapshot_download(repo,local_dir=Path(__file__).parent/'models'/folder,allow_patterns=files)
    print('Download complete. Locate this folder in SuperSub and choose Multilingual Whisper.')

if __name__=='__main__':main()
