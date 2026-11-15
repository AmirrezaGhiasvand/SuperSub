import tempfile
import unittest
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import media_tools
import inference

class InferenceTests(unittest.TestCase):
    def test_chunks_cover_audio_with_bounded_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'audio.wav'
            with wave.open(str(p),'wb') as f:
                f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000)
                for _ in range(125):f.writeframes(np.zeros(16000,dtype='<i2').tobytes())
            chunks=list(media_tools.iter_audio(p))
            self.assertGreater(len(chunks),2)
            self.assertEqual(sum(len(c[1]) for c in chunks),125*16000)
            self.assertTrue(all(len(c[1])<=60*16000 for c in chunks))
            for a,b in zip(chunks,chunks[1:]):self.assertAlmostEqual(a[0]+len(a[1])/16000,b[0])
    def test_offsets_and_low_memory_settings(self):
        sample=np.zeros(16000,dtype='float32')
        word=SimpleNamespace(start=.1,end=.8,word='سلام')
        segment=SimpleNamespace(end=1,words=[word])
        engine=SimpleNamespace(transcribe=lambda *a,**k:None)
        def transcribe(samples,**kw):
            self.assertEqual(kw['beam_size'],1);self.assertEqual(kw['best_of'],1)
            self.assertIsInstance(samples,np.ndarray)
            return iter([segment]),None
        engine.transcribe=transcribe
        with patch('faster_whisper.WhisperModel',return_value=engine) as model,patch.object(media_tools,'iter_audio',return_value=iter([(0,sample,61),(60,sample,61)])):
            result=inference.execute({'model':'local','audio':'audio.wav','settings':{}},lambda s:None)
        self.assertEqual(model.call_args.kwargs['cpu_threads'],2)
        self.assertAlmostEqual(result['words'][1]['start'],60.1)
        self.assertAlmostEqual(result['duration'],61)
    def test_crashed_worker_becomes_memory_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            def launch(*a,**kw):
                kw['stderr'].write(b'mkl_malloc: failed to allocate memory\n')
                return SimpleNamespace(poll=lambda:1,returncode=1)
            with patch.object(inference.subprocess,'Popen',side_effect=launch):
                with self.assertRaisesRegex(RuntimeError,'Not enough system memory'):
                    inference.run_isolated(tmp,'local',{},lambda s:None,lambda:False)
    def test_cancel_terminates_worker(self):
        with tempfile.TemporaryDirectory() as tmp:
            from unittest.mock import Mock
            process=Mock();process.poll.return_value=None
            with patch.object(inference.subprocess,'Popen',return_value=process):
                with self.assertRaises(inference.Cancelled):inference.run_isolated(tmp,'local',{},lambda s:None,lambda:True)
            process.terminate.assert_called_once();process.wait.assert_called_once()
