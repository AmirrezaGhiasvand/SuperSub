# Infrastructure

Windows-first, loopback-only FastAPI application. A static browser frontend is served by the same process at port 8765. faster-whisper uses local CTranslate2 models, CPU INT8 and speech detection. PyAV decodes source audio. One in-process thread runs transcription at a time; cancellation occurs between yielded segments. Restart loses active job status. Project JSON is atomically replaced; concurrent edits during transcription are not supported.

Data: `data/<uuid>/source.<extension>`, `project.json`, and exported `subtitles.srt`. JSON stores source metadata, original word timestamps, cue edits and transcription settings. Source media is copied; project deletion removes the copy. No cloud storage.

API: GET /api/models and /api/projects; POST /api/projects multipart file; GET /api/projects/{id}/media and /srt; POST /run, /cancel, /reflow; GET /status; PUT /cues; DELETE project. Run accepts model, language, limit and glossary. Cues contain start/end seconds and text. Status uses running/complete/failed/cancelled/idle with optional progress/error.

Detected hardware: NVIDIA GTX 1630, 4096 MiB, driver 566.36. Python 3.14 and Node 24 installed; FFmpeg not on PATH. Planned upgrade: Python 3.11, React/TypeScript frontend, separate worker process, SQLite, GPU compatibility detection, forced alignment and browser preview proxies.
