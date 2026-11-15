# SuperSub

A local video-to-SRT subtitle studio with an English interface, Persian text editing, light/dark themes, and saved projects. Audio stays on your computer.

## Quick setup on Windows

1. Install **64-bit Python 3.11 or newer** from [python.org](https://www.python.org/downloads/windows/). Enable **Add Python to PATH**. Python 3.14 passes the current dependency/import tests; actual model inference has not yet been verified.
2. Clone this repository with Git, or download and extract its ZIP. Open the extracted folder.
3. Double-click **Setup.cmd**. It installs application dependencies into a local `.venv`. Internet is required for packages. **No model is downloaded.**
4. Double-click **Start.cmd**. The browser opens at **http://127.0.0.1:8765** once the server is ready.
5. Click **Locate local model**, then **Browse folders…** (or paste its full path). Select the model profile and click **Use this model**.
6. Keep the console open while using SuperSub. Press **Ctrl+C** there to stop.

No Node.js, GPU, API key, account, or separate FFmpeg installation is required for the current application. Inference runs on CPU INT8; large videos may take considerable time.

### PowerShell alternative

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

To choose an installed Python executable:

```powershell
.\setup.ps1 -Python "C:\Path\To\Python\python.exe"
```

Setup is safe to rerun and stops on installation failures. Launching does not reinstall packages.

## Models and offline use

Setup installs dependencies only. Bring your own local **CTranslate2 Whisper model folder**, wherever it is stored on your PC. The folder must contain `model.bin`, `config.json` and `tokenizer.json`, plus the original model vocabulary/preprocessing files. Registration checks the folder structure; the inference engine validates model compatibility when loading it.

Use **Locate local model → Browse folders… → Use this model**. Choose **Multilingual Whisper** for the existing Turbo model, or **Persian specialist** for Persian-only fine-tunes. No copying is required. Paths are remembered locally in `data/local-models.json`; the selected model is remembered in this browser. If you move a folder, locate it again. On systems without Tk folder-dialog support, paste the full folder path. Do not select an unconverted Transformers checkpoint. Existing standard folders under `models/` are still discovered automatically.

Once dependencies and model weights are installed, local Turbo transcription can run without internet. The initial speech detector cache may be populated by the installed runtime; verify offline use with a short clip before relying on it.

Optional Persian specialist (experimental):

```powershell
.\.venv\Scripts\python.exe -m pip install transformers torch
.\.venv\Scripts\python.exe install_models.py persian
```

This downloads and converts [Givia Persian Turbo](https://huggingface.co/givia/whisper-large-v3-turbo-persian). Select Persian as the language. Consult its model card and attribution terms before redistributing weights.

`install_models.py nava` downloads [Nava CTranslate2](https://huggingface.co/Nimruz/Nava-ct2), but Nava transcription is disabled until separate word alignment is implemented. It is not needed for setup.

## Using SuperSub

### Timeline workspace

**Automatic — follow speech pauses** chooses each cue's word count from speech pauses by default. Turn it off to use the manual word limit. Both modes retain punctuation and a six-second readability limit.

Inference uses a disposable child process, CPU INT8, two compute threads and greedy decoding. Audio is streamed in windows of at most 60 seconds, favoring quiet cut points near window ends; global timestamps are retained. This limits memory growth for long files and releases model memory after each job. Chunk boundaries and greedy decoding can change recognition relative to the previous full-audio/beam-search pipeline. If memory is still insufficient, close other running model/server instances and memory-heavy apps, use a system-managed Windows page file, or choose a smaller model. SuperSub does not alter OS memory settings automatically.

Subtitles appear over the video and as timed blocks on a scrollable timeline. Click the ruler or a block to seek, adjust zoom for detail, drag a subtitle to move it, or drag its edges to trim. Trims cannot cross neighboring cues. The playhead and overlay follow playback; subtitle text disappears during gaps. This is a preview overlay, not a burned-in video export.

Text/timing edits save automatically after a short delay. A save-status indicator reports errors; fix invalid or overlapping times before switching projects. The editor has no Save, Reflow, Add cue, VTT or Text buttons. SRT download and Delete project remain. New project clears the current media, editor and timeline while retaining saved work and model configuration. Projects are listed in a collapsible left panel; selecting one fetches its latest saved cues/settings and rebuilds the timeline and preview. A project remains in history once it has generated subtitles, even if its cues are later removed.

New generation automatically splits cues at detected word-timestamp gaps (default 0.45 seconds, configurable from 0.1–2 seconds). Punctuation, maximum words and a six-second duration limit also create boundaries. Existing projects keep their saved timings until explicitly regenerated. Pause quality depends on the recognition model's word alignment; this does not add a separate alignment model.

Generation opens a loading screen with phase, elapsed time and cancellation. The settings panel can be minimized with its arrow button; this preference is remembered. After updating code, stop the server with Ctrl+C, restart Start.cmd and hard-refresh the page (Ctrl+F5). A running server does not reload changes automatically.

The inference pipeline reads FFmpeg-normalized PCM into float32 samples directly. This avoids the faster-whisper 1.2.1 / PyAV 19 `metadata_errors` incompatibility without modifying installed third-party packages.

The left panel contains settings only. Select media and generate from the central workspace. Generation immediately enters a loading state and reports audio preparation, model loading, speech recognition, and subtitle building. A completion dialog appears when the saved subtitles are ready. Processing percentage is approximate; preparation and loading use an indeterminate indicator.

FFmpeg codecs are bundled through imageio-ffmpeg; no system codec pack is required. Imported videos receive a local H.264/AAC MP4 preview (up to 1280 px wide). Preparation can take time for large files; the original file remains unchanged. Seeking and playback use the completed preview. Decode errors appear below the player.

History includes projects only after successful generation of at least one subtitle. Empty imports, silent clips, failures and cancellations do not create history entries; previously generated results are preserved on failed retries. Working media can remain in data until deleted. SRT download saves pending edits first. Set maximum words to 1 for word-by-word cues.

Select a video, model, video language and maximum words per cue (default 8). Add optional glossary hints, then generate. Review the video and edit subtitle text or timing. Click a cue's play button or its timeline block to seek. Wait for the save-status indicator before closing the browser; SRT download flushes pending edits automatically.

Cancellation takes effect between processing steps or generated segments. Regeneration replaces existing cues only after confirmation and successful recognition.

Projects and copied media are stored under `data/`. Delete a project in the UI to remove its local copy. Source files selected outside the project folder are untouched.

## What is included

Source code, tests, setup/launch scripts and project context. **`data/`, `assets/`, `models/`, `.venv/`, credentials and caches are excluded from Git.** The interface works without logos. For local branding, optionally place `mansvolve-black.png` and `mansvolve-white.png` in `assets/`.

## Troubleshooting

- **Python not found:** install Python, enable PATH and reopen the console.
- **Dependency installation fails:** check internet access and 64-bit Python. For incompatible wheels use Python 3.11 in a fresh checkout or virtual environment.
- **Model unavailable:** click Locate local model and select its existing folder again. Rerunning setup does not download weights. Optional downloads via `install_models.py` are manual only.
- **Port in use:** run `start.ps1 -Port 8766`.
- **Browser does not open:** visit the printed local URL manually. Use `start.ps1 -NoBrowser` when desired.
- **Preview cannot play:** wait for local preview conversion to finish. If it fails, check the error under the player and try a valid file. Rerun Setup.cmd if bundled FFmpeg is missing.
- **No speech / transcription error:** check that the input has a supported audio stream. Errors are displayed in the workspace.

## Development and status

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m py_compile app.py install_models.py
.\.venv\Scripts\python.exe -m pip check
```

This is an initial FastAPI/static-web implementation. GPU inference, forced alignment, React/SQLite migration, robust worker cancellation and benchmarked Persian accuracy remain planned. Browser and real-audio inference QA are not yet complete. See [context](context/README.md), [infrastructure](context/infra.md), and [current status](context/current-status.md).
