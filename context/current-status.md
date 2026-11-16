# Current status

Updated 2026-11-15. This snapshot replaces obsolete chronological implementation notes.

## Implemented

Latest editor placement: cue editing reuses the browse/generate slot as an overlay without resizing the preview or timeline. Background media controls become inert while the editor is open; closing restores them. DOM interaction and startup checks pass; visual browser verification remains pending.

Latest timeline interaction update: edge/playhead snapping with zoom-aware 8px threshold capped at .35s, visible guide, persistent toggle and Alt bypass. Left/Right navigates boundaries; Shift arrows nudge .1s; Space plays/pauses; Enter edits; Escape closes. Single-click cue playback is distinguished from double-click editing. Editor is a non-modal right-side workspace panel, inline on small windows, with start/end-at-playhead actions. Trim/move snapping respects adjacent cue limits; pointer cancellation restores the original cue. Autosave and video preview remain live during edits.

Latest layout adjustment: removed the video-name lane and reduced the subtitle timeline to 180px to increase preview space. Native captions use 50% horizontal/vertical coordinates with centered line alignment, and the HTML fallback is centered too. This applies to normal/fullscreen playback.


Compact desktop pass: viewport-height workspace, smaller 16:9 preview alongside media controls, unchanged timeline height, tight toolbars/footer and internally scrolling settings. Flat minimal button styling replaces raised gradients/hover motion. Small/short windows retain normal scrolling for access. DOM interaction checks pass; real-browser viewport layout verification remains pending because the browser host is unavailable.

Frontend startup hotfix: a cached unversioned timeline.mjs lacked shiftCues and prevented the entire app module from initializing. The geometry import is now versioned, a classic bootstrap dynamically fetches a fresh entry module and surfaces import failures, and frontend responses use explicit JavaScript MIME/no-store without 304 reuse. Added real module-linkage and HTTP static-response regression tests. favicon.ico returns 204 to avoid unrelated console noise. Browser console evidence confirmed the stale-module failure.

Latest studio update (2026-11-16): explicit model load/status/unload with a persistent isolated worker, matching-model reuse and release on unload/cancel/server shutdown. Generation without a loaded model remains disposable. The larger timeline owns double-click cue editing in a non-modal right-side panel; the bottom subtitle list is removed. Added autosaved global forward/backward shifts, fixed 16:9 letterboxed playback, native captions for fullscreen and a contrasted charcoal palette/button system. Timestamp-aware audio resampling preserves delayed-stream leading silence; preview caches are versioned. Existing project timings require manual shift/regeneration rather than silent migration.

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

26 Python tests and 10 Node startup/timeline tests pass. DOM checks cover overlay gaps, serialized autosave, reset, project restoration/settings and removed controls. Actual FFmpeg conversion/audio extraction passed. Installed Turbo passed isolated silence and an eight-second speech sample producing 11 timed words. This confirms operation, not accuracy or long-file reliability.

## Remaining

Browser preview tooling failed to initialize: real-browser visual/responsive/accessibility QA remains pending. Full offline tests, long-file memory/stress testing, speech quality at chunk boundaries and comparative Persian benchmarks remain incomplete. Large models can still exceed available memory.

Preview conversion and audio extraction can finish their current step after cancellation; restart does not resume active jobs. Empty imports may remain on disk outside history. No batch queue, GPU inference, forced alignment/Nava inference, burned-in export, full language list or system-theme mode.

Runtime is FastAPI/static JavaScript and JSON persistence. React/TypeScript/Tailwind/SQLite were original plan choices, not shipped prerequisites. Assets/data/models are excluded from Git.
