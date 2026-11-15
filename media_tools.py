"""Bundled FFmpeg provides codecs without changing system-wide codec packs."""
import subprocess
import imageio_ffmpeg

def convert(source, target, preview=False):
    args=[imageio_ffmpeg.get_ffmpeg_exe(),'-nostdin','-y','-v','error','-i',str(source)]
    if preview:
        args += ['-map','0:v:0?','-map','0:a:0?','-vf',"scale='trunc(min(1280,iw)/2)*2':-2",'-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart']
    else:
        args += ['-vn','-map','0:a:0','-ar','16000','-ac','1','-c:a','pcm_s16le']
    result=subprocess.run(args+[str(target)],capture_output=True,timeout=3600,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if result.returncode:
        raise ValueError('Cannot decode media. Check that the file is valid and contains a supported audio/video stream. '+result.stderr.decode(errors='replace')[-600:])
