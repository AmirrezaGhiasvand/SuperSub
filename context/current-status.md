# Current status

Updated 2026-11-15. This snapshot replaces obsolete chronological implementation notes.

## Implemented

Latest studio update (2026-11-16): explicit model load/status/unload with a persistent isolated worker, matching-model reuse and release on unload/cancel/server shutdown. Generation without a loaded model remains disposable. The larger timeline owns click-to-edit cue dialogs; the bottom subtitle list is removed. Added autosaved global forward/backward shifts, fixed 16:9 letterboxed playback, native captions for fullscreen and a contrasted charcoal palette/button system. Timestamp-aware audio resampling preserves delayed-stream leading silence; preview caches are versioned. Existing project timings require manual shift/regeneration rather than silent migration.

Validation for this update: actual installed Turbo loaded, was reused for inference in the same process, and unloaded successfully. Added delayed-audio fixture, global-shift tests, model lifecycle tests and DOM checks for native caption tracks/inspector/fullscreen target. Real browser fullscreen/visual QA remains unverified; model alignment quality remains variable.

- Windows dependency-only setup/launch scripts; no automatic model download, local model picker/path entry, optional manual download helper.
- English light/dark UI with minimized sidebar and independently collapsible Projects.
- Local media import, bundled FFmpeg H.264/AAC preview conversion and mono PCM extraction.
- Disposable inference process: CPU INT8, two compute threads, greedy decoding, <=60s quiet-boundary audio windows and original timeline offsets. Native memory failures are recoverable; cancellation terminates the inference child.
- Generation phases, elapsed time, progress, loading and completion dialogs.
- Default-on automatic word counts from speech pauses (.45s default, .1–2s configurable). Manual cap 1–30 available when disabled. Punctuation and 6s duration limits apply.
- Zoomable timeline, playhead, cue move/trim, video overlay, autosaved text/timing edits and SRT export.
- New project reset and persisted project restoration. History starts after generated subtitles and retains generated projects even after cues are removed.

## Validation

24 Python tests and 4 Node timeline tests pass. DOM checks cover overlay gaps, serialized autosave, reset, project restoration/settings and removed controls. Actual FFmpeg conversion/audio extraction passed. Installed Turbo passed isolated silence and an eight-second speech sample producing 11 timed words. This confirms operation, not accuracy or long-file reliability.

## Remaining

Browser preview tooling failed to initialize: real-browser visual/responsive/accessibility QA remains pending. Full offline tests, long-file memory/stress testing, speech quality at chunk boundaries and comparative Persian benchmarks remain incomplete. Large models can still exceed available memory.

Preview conversion and audio extraction can finish their current step after cancellation; restart does not resume active jobs. Empty imports may remain on disk outside history. No batch queue, GPU inference, forced alignment/Nava inference, burned-in export, full language list or system-theme mode.

Runtime is FastAPI/static JavaScript and JSON persistence. React/TypeScript/Tailwind/SQLite were original plan choices, not shipped prerequisites. Assets/data/models are excluded from Git.
