"""Explicit, online model installation. Run inside the application venv."""
from pathlib import Path
import argparse
from huggingface_hub import snapshot_download

root=Path(__file__).parent/'models'
p=argparse.ArgumentParser()
p.add_argument('model', choices=['turbo','persian','nava'])
a=p.parse_args()
if a.model=='turbo':
    snapshot_download('mobiuslabsgmbh/faster-whisper-large-v3-turbo',local_dir=root/'whisper-large-v3-turbo')
elif a.model=='nava':
    snapshot_download('Nimruz/Nava-ct2',local_dir=root/'nava-ct2')
else:
    from ctranslate2.converters import TransformersConverter
    source=snapshot_download('givia/whisper-large-v3-turbo-persian')
    TransformersConverter(source,copy_files=['tokenizer.json','preprocessor_config.json']).convert(str(root/'givia-persian'),quantization='int8')
