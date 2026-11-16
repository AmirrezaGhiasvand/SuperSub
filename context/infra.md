# Infrastructure

## Runtime and setup

Resident lifecycle: GET /api/models/status; POST /api/models/load accepts model ID; POST /api/models/unload releases the child. inference.py --serve keeps one engine in data/model-runtime and accepts atomic command files. Matching generation reuses it; other loaded models/loading states reject generation until resolved. Lifecycle operations share the generation lock. Cancellation unloads resident jobs; temporary inference remains available without preloading. Runtime files are ignored data, not source.

Media v2 conversion uses aresample=async=1:first_pts=0 for both preview/extracted PCM to preserve delayed audio. preview-v2.mp4 avoids reusing old conversion caches. Frontend rebuilds a native VTTCue track from saved cues for normal/fullscreen captions; CSS locks player frame to 16:9 with object-fit containment. Timeline cue selection opens an autosaved inspector. Global shifts mutate the same saved cues exported as SRT, clamping backward movement uniformly at zero.

FastAPI/uvicorn serves static HTML/JS on loopback port 8765. setup.ps1 installs requirements.txt into .venv without model downloads. start.ps1 checks imports and opens the browser. requirements-lock.txt is the captured original Windows environment, not the installation input.

Frontend: web/index.html, web/app.js, web/timeline.mjs. Timeline and subtitle export use the same cue data. Autosave requests serialize and flush before project navigation/export. Settings/panel preferences persist in the browser.

## Processing and memory

Import copies source media and starts independent FFmpeg H.264/AAC MP4 preview conversion (faststart, <=1280px width). /preview reports preparing/ready/failed; /media serves preview when ready with byte-range support.

Generation extracts 16kHz mono PCM WAV. inference.py runs as a separate process with thread limits set before native imports: CPU INT8, two threads, one worker, beam/best-of 1. A wave/NumPy reader streams <=60s audio windows, choosing quiet boundaries near the end. Word timestamps receive original offsets. Passing samples bypasses PyAV's incompatible metadata_errors decoder call.

Parent controller polls atomic worker status JSON every 200ms, terminates on cancel and reports native memory exits. Model memory is released when the child exits. FFmpeg uses two threads. A global lock allows one generation job. Saved cues are replaced only on successful nonempty recognition.

Cue boundaries: pause .1–2s (default .45), punctuation, 6s duration; automatic_words=true omits the manual word cap, false applies limit 1–30. Active jobs are not resumed after restart.

## Persistence and APIs

data/<id>/ stores source, preview.mp4, project.json, exported SRT and worker.log. Temporary WAV and worker request/state/result JSON are cleaned after generation. JSON project state stores words/cues/settings/duration/generated flag. data/local-models.json stores external CTranslate2 paths/profiles; registration checks required files, inference checks compatibility. Native picker runs model_picker.py separately.

- GET /api/health, /api/models; POST /api/models/register and /api/models/browse.
- GET /api/projects lists previously generated projects; POST imports multipart file.
- GET /api/projects/{id} restores saved state; DELETE removes copied local project data.
- Project routes: GET /preview, /media, /status, /srt; POST /run and /cancel; PUT /cues.
- /vtt, /txt and /reflow remain backend routes but have no UI controls.

Run input: model, language, glossary, limit, pause, automatic_words. Cues: start/end seconds and text. Status: running/complete/empty/failed/cancelled/idle, phase, nullable progress, optional error. Backend blocks edits during generation and invalid/overlapping timing. No SQL migration exists. Data/models/assets/venv/tools/credentials/caches stay outside Git.
