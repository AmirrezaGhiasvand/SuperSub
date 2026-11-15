# Current status

## Local model selection update

Setup now installs dependencies only, with no model downloads. Added native folder browse and full-path fallback, CTranslate2 file checks, explicit multilingual/Persian/Nava profiles and persistent registration under ignored data/local-models.json. Model weights stay in the selected folder. Missing models disable generation; relocated folders need re-registration. Nava remains disabled. The optional install_models.py downloader is manual only. This supersedes earlier setup download notes below.

Validation: seven unit tests, Python compilation, JavaScript syntax and isolated HTTP checks for model registration/restart persistence. Native dialog interaction and real-model inference still need manual QA.

## Portable setup update

Added Setup.cmd/setup.ps1 and Start.cmd/start.ps1. Setup creates a venv, installs version-pinned direct dependencies and downloads Turbo separately; SkipModel supports existing local weights. Launch does not install dependencies. Assets are optional and ignored by Git along with models/data/venv/tools. README documents clean-device installation. requirements-lock.txt records the current Windows Python 3.14 environment; setup uses requirements.txt to permit compatible transitive dependencies on other Python versions.

Verified: setup with SkipModel, dependency consistency, three unit tests, installer CLI help, and clean-checkout HTTP startup without assets/models/data. Full model download, inference and new-PC installation remain untested. Previous notes below describe the initial delivery and may predate these checks.

Initial implementation created. Backend, browser interface, launcher, model downloader and documentation exist. Existing Turbo files were inspected but not inference-tested. Model downloads and runtime dependency installation have not been completed. No model accuracy claims are verified.

Implemented: import, persisted local JSON projects, model/language/word controls, glossary prompt, CPU transcription, native word timestamps, pause/punctuation reflow, cue editing, seek/highlight, SRT export, deletion, light/dark theme.

Remaining against accepted plan: React/TypeScript/Tailwind migration, SQLite migration, separate worker with robust cancellation/restart tracking, system-theme mode, bundled Persian fonts, full language list, forced alignment and Nava enablement, GPU inference, codec preview proxies, cue-limit export warnings, edit realignment, real model comparisons, browser QA and end-to-end inference tests. Import does not yet validate audio streams in advance. Overlapping edit/transcription operations should be avoided. Project history buttons show the last fetched state; refresh after saving if needed.
