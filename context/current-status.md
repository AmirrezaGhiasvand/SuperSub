# Current status

Updated 2026-11-16. Current code is on main; this snapshot replaces historical implementation notes.

## Implemented

- Dependency-only Windows setup. Models are chosen locally; optional manual downloads/conversion never run during setup.
- Resident Load/Unload and disposable CPU INT8 inference with 2 threads, bounded <=60s windows, original timeline offsets and native-memory-failure recovery.
- FFmpeg browser preview and normalized PCM, delayed-audio leading-silence preservation, direct samples bypassing PyAV metadata_errors.
- Navbar project name/Generate/Cancel, browse only for new workspaces, left history/settings and default-open right inspector.
- Editor follows the cue under the playhead; gaps retain selection. Text/timing focus pauses playback and protects edits until focus leaves.
- Subtitle-only 180px timeline: zoom, drag/trim, snapping, boundary buttons, Alt bypass and start/end-at-playhead controls. Left/Right .1s, Shift arrows 1s, Up/Down subtitle starts. Single-click plays/selects; Enter/double-click edits; Escape clears selection.
- Autosave, project reset/restoration/deletion, SRT download and global forward/backward sync shifts.
- Default automatic word counts based on pauses (.45s, configurable .1–2s), optional manual limit, punctuation and 6s readability limits.
- Centered native fullscreen captions, fixed 16:9 letterboxing, compact desktop layout and Mansvolve-inspired monochrome/pill UI. Inter/Vazirmatn/Martian Mono fonts and OFL licenses are bundled.
- Versioned module startup/no-store responses prevent stale export failures.
- README now has verified comparison/download/file-role tables and exact Persian source conversion instructions, checked 2026-11-16. No model weights were downloaded for documentation verification.

## Verified

26 Python tests and 10 JavaScript startup/timeline tests pass. DOM checks cover active-cue following, navbar, hidden browsing, default-open editor, keyboard/snapping, autosave and project restoration. Actual Turbo passed load/reuse/unload, silence and an eight-second speech sample yielding 11 timed words. FFmpeg conversion and delayed-audio fixtures pass.

File listings verified: Small, Medium, Large V3 Turbo, Large V3, Givia Persian source and Nava CT2. Only existing Turbo has local inference smoke results; other models are not accuracy/runtime benchmarks.

## Remaining

Real-browser visual/fullscreen/responsive/accessibility QA, full offline checks, long-file stress tests and comparative Persian accuracy/timing benchmarks remain outstanding. Large models can exceed system memory; greedy decoding/chunk cuts may affect recognition. Pause segmentation is not forced alignment.

Preview/audio extraction can finish the active step after cancellation. Restart does not resume jobs; empty imports can remain outside history. No GPU inference, Nava/forced alignment, batch queue, burned-in export, translation or diarization.

Runtime is FastAPI/static JS/JSON. React/TypeScript/Tailwind/SQLite were original proposals, not installation prerequisites. Data/assets/models/venv/tools/secrets are excluded from Git; licensed fonts in web/fonts are shipped source dependencies.
