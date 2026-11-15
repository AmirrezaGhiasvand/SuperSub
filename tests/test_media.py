import tempfile
import subprocess
import unittest
from pathlib import Path
import media_tools

class MediaTests(unittest.TestCase):
    def test_incompatible_source_converted_and_audio_extracted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'sample.mkv'
            subprocess.run([media_tools.imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','lavfi','-i','testsrc=size=160x120:rate=10','-f','lavfi','-i','sine=frequency=400','-t','1','-c:v','ffv1','-c:a','pcm_s16le',str(source)],check=True,capture_output=True)
            media_tools.convert(source,root/'preview.mp4',preview=True)
            media_tools.convert(source,root/'audio.wav')
            self.assertGreater((root/'preview.mp4').stat().st_size,100)
            import wave
            with wave.open(str(root/'audio.wav')) as audio:
                self.assertEqual(audio.getframerate(),16000);self.assertEqual(audio.getnchannels(),1)
