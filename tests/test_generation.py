import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import app

class ImmediateThread:
    def __init__(self,target,**kwargs): self.target=target
    def start(self): self.target()

class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.pid='abc123'; self.p=self.root/self.pid;self.p.mkdir()
        app.save(self.p,dict(id=self.pid,name='test.mkv',source='source.mkv',words=[],cues=[]))
        self.patches=[patch.object(app,'DATA',self.root),patch.object(app.threading,'Thread',ImmediateThread),patch.object(app.local_models,'catalog',return_value={'test':dict(path=str(self.root),profile='multilingual')}),patch.object(app.local_models,'valid_folder',return_value=True),patch.object(app.media_tools,'convert'),patch.object(app.media_tools,'load_audio',return_value=__import__('numpy').zeros(16000,dtype='float32'))]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        app.jobs.clear();self.tmp.cleanup()
    def engine(self,words):
        def transcribe(samples,**kwargs):
            self.assertIsInstance(samples,__import__('numpy').ndarray)
            self.assertEqual(samples.dtype.name,'float32')
            return iter([SimpleNamespace(words=words,end=1)]),SimpleNamespace(duration=1)
        return SimpleNamespace(transcribe=transcribe)
    def test_history_only_after_subtitle_and_exports(self):
        self.assertEqual(app.projects(),[])
        word=SimpleNamespace(word='سلام',start=0,end=1)
        with patch('faster_whisper.WhisperModel',return_value=self.engine([word])):
            result=app.run(self.pid,dict(model='test',limit=8))
        self.assertEqual(result['status'],'complete')
        self.assertEqual(len(app.projects()),1)
        self.assertIn(b'WEBVTT',app.export_vtt(self.pid).body)
        self.assertIn('سلام',app.export_text(self.pid).body.decode())
    def test_no_speech_not_added_to_history(self):
        with patch('faster_whisper.WhisperModel',return_value=self.engine([])):
            result=app.run(self.pid,dict(model='test',limit=8))
        self.assertEqual(result['status'],'empty');self.assertEqual(app.projects(),[])
    def test_failed_run_releases_lock(self):
        with patch('faster_whisper.WhisperModel',side_effect=RuntimeError('bad model')):
            result=app.run(self.pid,dict(model='test',limit=8))
        self.assertEqual(result['status'],'failed');self.assertFalse(app.lock.locked())
    def test_cancellation_before_load(self):
        with patch.object(app.media_tools,'convert',side_effect=lambda *a,**k:app.jobs[self.pid].update(cancel=True)),patch('faster_whisper.WhisperModel') as loader:
            result=app.run(self.pid,dict(model='test',limit=8))
        self.assertEqual(result['status'],'cancelled');loader.assert_not_called()
