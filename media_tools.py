"""Bundled FFmpeg provides codecs without changing system-wide codec packs."""
import subprocess
import imageio_ffmpeg
import wave
import numpy as np

def iter_audio(path, seconds=60):
    """Read bounded windows, favoring a quiet boundary in their last 8 seconds."""
    with wave.open(str(path),'rb') as audio:
        rate=audio.getframerate()
        if rate!=16000 or audio.getnchannels()!=1 or audio.getsampwidth()!=2:
            raise ValueError('Expected 16 kHz mono 16-bit PCM audio.')
        total=audio.getnframes();position=0
        while position<total:
            audio.setpos(position)
            samples=np.frombuffer(audio.readframes(min(rate*seconds,total-position)),dtype='<i2').astype(np.float32)
            samples*=1/32768.0
            count=len(samples)
            if position+count<total and count>rate*10:
                window=rate//5;start=count-rate*8
                tail=samples[start:start+((count-start)//window)*window].reshape(-1,window)
                quiet=int(np.argmin(np.mean(tail*tail,axis=1)))
                count=start+(quiet+1)*window
                samples=samples[:count]
            yield position/rate,samples,total/rate
            position+=count

def load_audio(path):
    """Read our normalized PCM directly, avoiding PyAV-version decoder APIs."""
    with wave.open(str(path),'rb') as audio:
        if audio.getframerate()!=16000 or audio.getnchannels()!=1 or audio.getsampwidth()!=2:
            raise ValueError('Expected 16 kHz mono 16-bit PCM audio.')
        return np.frombuffer(audio.readframes(audio.getnframes()),dtype='<i2').astype(np.float32)/32768.0

def convert(source, target, preview=False):
    args=[imageio_ffmpeg.get_ffmpeg_exe(),'-nostdin','-y','-v','error','-threads','2','-i',str(source)]
    if preview:
        args += ['-map','0:v:0?','-map','0:a:0?','-vf',"scale='trunc(min(1280,iw)/2)*2':-2",'-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart']
    else:
        args += ['-vn','-map','0:a:0','-ar','16000','-ac','1','-c:a','pcm_s16le']
    result=subprocess.run(args+['-threads','2',str(target)],capture_output=True,timeout=3600,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if result.returncode:
        raise ValueError('Cannot decode media. Check that the file is valid and contains a supported audio/video stream. '+result.stderr.decode(errors='replace')[-600:])
