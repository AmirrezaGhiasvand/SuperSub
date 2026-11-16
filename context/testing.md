# Testing

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m py_compile app.py inference.py media_tools.py local_models.py model_picker.py install_models.py
.\.venv\Scripts\python.exe -m pip check
node --experimental-vm-modules --test tests/startup.test.mjs tests/timeline.test.mjs
node --check web/app.js
```

Node.js is development-only. Latest verified: 26 Python tests and 10 Node tests. Covers model registration, pause/duration limits, automatic/manual grouping, history/export/persistence, worker failure/cancellation, bounded chunks/offsets, native allocation error reporting, real FFmpeg conversion and timeline geometry/overlay gaps.

Additional local DOM checks passed autosave serialization, reset, project reopening/settings and removed controls. The harness lives in ignored .tools/ and is not part of portable tests. Actual Turbo passed silence and an eight-second existing-media sample (11 timed words); no accuracy score is claimed.

Manual release checks still needed:
- Clean Windows installation with no weights/assets in Git; model selection without copies and persistence after restart.
- Real-browser playback, seeking, drag/trim, overlay timing, Persian/English text, autosave recovery and SRT comparison.
- New/reset/reopen/delete, both themes, hidden panels, keyboard access and small screens.
- Long/noisy media, silence, moved models, memory pressure, cancelled extraction and speech across chunk boundaries.
- Offline runtime, interrupted startup and repeated jobs confirming child processes exit.

Visual browser QA, comprehensive offline validation, long-file stress tests and Persian benchmarks remain outstanding.
