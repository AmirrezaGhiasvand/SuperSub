# Current status

## Decoder compatibility and loading screen

Fixed actual generation failure caused by faster-whisper 1.2.1 passing removed metadata_errors to PyAV 19. Normalized WAV is now read through Python wave into float32 NumPy samples and passed directly to transcribe, bypassing PyAV decoding. Added a modal generation loading screen with elapsed time, mirrored phase/progress and cancellation, plus a persistent sidebar minimize/expand button. Endpoint 404 errors include restart guidance; /api/health identifies this build. Existing running servers must be restarted.

Validation: 12 tests pass, including a regression asserting the engine receives samples rather than a filename. Actual installed Turbo loaded and transcribed a silent one-second sample with av.open forbidden; completed successfully with zero segments. This verifies the decoder fix, not Persian recognition accuracy. JavaScript syntax passes; browser interaction still needs manual QA.

## Playback and generation fixes

Added bundled-FFmpeg preview conversion to H.264/AAC with MP4 faststart and 16 kHz mono extraction for inference. Central workspace owns media selection, generation/cancellation and editor actions; the sidebar contains configuration only. Generation has immediate busy state, phase labels, progress and completion dialogs. History requires generated nonempty cues. Added per-project retrieval so incomplete projects remain accessible without appearing in history. Export saves pending edits first and supports SRT/VTT/text. Editing/reflow while generation runs is blocked. Invalid timings and word limits receive useful errors; no-speech runs preserve previous results. Setup remains dependencies-only.

Validation: 12 passing unit/integration tests, including actual FFmpeg MKV→MP4/audio conversion, mocked ASR success/silence/failure/cancel and history/export rules; JavaScript syntax check. Browser interaction and real-model Persian inference remain manual QA. Cancellation still waits for the active decoding/loading step; preview preparation is separate and not cancelled by the generation cancel button.

Reviewed reference README and UI source: https://huggingface.co/spaces/mehrshadjavid/jcutpersiansub . Adopted its select/generate/review workflow and added VTT/text exports; no reference code was copied. These notes supersede older playback/history/export limitations below.

## Local model selection update

Setup now installs dependencies only, with no model downloads. Added native folder browse and full-path fallback, CTranslate2 file checks, explicit multilingual/Persian/Nava profiles and persistent registration under ignored data/local-models.json. Model weights stay in the selected folder. Missing models disable generation; relocated folders need re-registration. Nava remains disabled. The optional install_models.py downloader is manual only. This supersedes earlier setup download notes below.

Validation: seven unit tests, Python compilation, JavaScript syntax and isolated HTTP checks for model registration/restart persistence. Native dialog interaction and real-model inference still need manual QA.

## Portable setup update

Added Setup.cmd/setup.ps1 and Start.cmd/start.ps1. Setup creates a venv, installs version-pinned direct dependencies and downloads Turbo separately; SkipModel supports existing local weights. Launch does not install dependencies. Assets are optional and ignored by Git along with models/data/venv/tools. README documents clean-device installation. requirements-lock.txt records the current Windows Python 3.14 environment; setup uses requirements.txt to permit compatible transitive dependencies on other Python versions.

Verified: setup with SkipModel, dependency consistency, three unit tests, installer CLI help, and clean-checkout HTTP startup without assets/models/data. Full model download, inference and new-PC installation remain untested. Previous notes below describe the initial delivery and may predate these checks.

Initial implementation created. Backend, browser interface, launcher, model downloader and documentation exist. Existing Turbo files were inspected but not inference-tested. Model downloads and runtime dependency installation have not been completed. No model accuracy claims are verified.

Implemented: import, persisted local JSON projects, model/language/word controls, glossary prompt, CPU transcription, native word timestamps, pause/punctuation reflow, cue editing, seek/highlight, SRT export, deletion, light/dark theme.

Remaining against accepted plan: React/TypeScript/Tailwind migration, SQLite migration, separate worker with robust cancellation/restart tracking, system-theme mode, bundled Persian fonts, full language list, forced alignment and Nava enablement, GPU inference, codec preview proxies, cue-limit export warnings, edit realignment, real model comparisons, browser QA and end-to-end inference tests. Import does not yet validate audio streams in advance. Overlapping edit/transcription operations should be avoided. Project history buttons show the last fetched state; refresh after saving if needed.
