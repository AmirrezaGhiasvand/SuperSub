# SuperSub

Local video-to-SRT subtitle studio with an English interface, Persian subtitles, a timeline editor, light/dark themes and saved projects. Media and inference stay on your PC.

## Set up on a new Windows PC

1. Install **64-bit Python 3.11 or newer** from [python.org](https://www.python.org/downloads/windows/), enabling **Add Python to PATH**. Python 3.14 is the version tested on the development PC.
2. Clone this repository, or download its ZIP and extract it. Private repository access requires signing in with an authorized GitHub account.
3. Double-click **Setup.cmd**. It installs dependencies into `.venv` and creates local folders. Internet is needed for packages. **Setup never downloads models.**
4. Double-click **Start.cmd**. Keep its console open. The app opens at **http://127.0.0.1:8765**.
5. In Settings, click **Locate local model → Browse folders…**. Select an existing **CTranslate2 Whisper model folder**, choose its profile and click **Use this model**. You can paste its full path if the folder dialog is unavailable.
6. Select a short Persian video, choose Persian as the video language, and click **Generate subtitles**. Review the output, then **Download SRT**.

No Node.js, GPU, cloud API key or separate FFmpeg installation is needed to run the app. Codec support is bundled through imageio-ffmpeg. A large model still needs several GB of available system memory; CPU processing can take time.

### PowerShell setup

```powershell
git clone https://github.com/AmirrezaGhiasvand/SuperSub.git
cd SuperSub
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

If Python is not on PATH, choose its executable when creating the environment:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1 -Python "C:\Path\To\Python\python.exe"
```

Setup can be rerun. Starting the app does not reinstall packages. Stop with **Ctrl+C** in its console.

## Bring your own model

The selected folder must contain `model.bin`, `config.json`, `tokenizer.json` and the model's original vocabulary/preprocessing files. Do not select a Transformers or ONNX checkpoint. Folder checks confirm required files exist; compatibility is validated when inference loads the model.

- **Multilingual Whisper:** use for standard Whisper models, including Large V3 Turbo.
- **Persian specialist:** use for Persian-only fine-tunes; select Persian as video language.
- **Nava:** registration is possible, but generation is disabled until its separate alignment pipeline is implemented.

Weights remain in their original location. Paths are remembered in ignored `data/local-models.json`; model selection is remembered by the browser. If a folder moves, locate it again. Standard folders under `models/` are also discovered automatically.

Optional manual downloads are available through `install_models.py`; they are never run by setup or generation:

```powershell
.\.venv\Scripts\python.exe install_models.py turbo
# Optional Persian conversion requires extra packages:
.\.venv\Scripts\python.exe -m pip install transformers torch
.\.venv\Scripts\python.exe install_models.py persian
```

The Persian download uses [Givia Persian Turbo](https://huggingface.co/givia/whisper-large-v3-turbo-persian). Review its model card and attribution terms before redistributing weights.

Once packages and models are present, generation uses local-only model loading. Verify offline operation with a short clip before relying on it.

## Generate, edit and export

### Model and timeline controls

Use **Load model** to keep the selected model ready in a separate process; **Unload** releases its process and model memory. Generation reuses a matching loaded model. With no loaded model, generation still loads temporarily and releases it afterward. Wait for loading to finish, and unload or switch models before generating with a different selection. Loading/unloading is blocked during generation; cancelling a resident job unloads that worker. Keeping a model loaded consumes memory until explicitly unloaded or the server exits.

The expanded timeline is the subtitle editor. Click a block to open text, start/end, previous/next, playback and cue deletion controls. Edits autosave. There is no bottom subtitle list. Global **Shift all forward/backward** adjusts saved cue times by the chosen number of seconds, updates playback captions and SRT, and preserves spacing/durations; backward shifts stop at time zero.

The player uses a fixed 16:9 frame with letterboxing rather than stretching source video. Native caption tracks keep subtitles visible in native video fullscreen; the Fullscreen button also expands the whole player. The dark palette uses distinct background, panel and raised-control shades, with consistent button states and focus outlines.

New audio extraction and preview conversion preserve delayed-audio leading silence through timestamp-aware resampling. New preview caches use preview-v2.mp4. Existing saved subtitle times are not silently rewritten: regenerate or use the global shift controls where needed. Model word alignment can still be imperfect; this is not a forced-alignment guarantee.

**Automatic — follow speech pauses** is enabled by default. It chooses cue word counts from timestamp gaps of at least **0.45 seconds**; the threshold is adjustable from 0.1–2 seconds. Punctuation and a six-second readability limit also split cues. Turn automatic mode off to use a manual maximum of 1–30 words. Use 1 for word-by-word captions. Glossary hints help recognition but do not guarantee exact spellings.

Generation displays a loading screen with phase, elapsed time, progress and cancellation, followed by a completion dialog. Preview conversion happens separately and may take time. Imported media receives a browser-compatible H.264/AAC MP4 preview; original files are unchanged.

The timeline shows the media track, subtitle blocks and playhead. Click to seek, zoom for precision, drag blocks to move them, or drag edges to trim without crossing adjacent cues. Subtitle text is overlaid on the video during each cue. The overlay is for preview; the app does not export burned-in video.

Text and timing edits autosave. Resolve save errors before leaving. SRT download flushes pending edits and exports the saved cues. Existing projects keep their timings until edited or explicitly regenerated.

**New project** clears the workspace without deleting saved work. The left Projects panel can be collapsed independently, and the whole sidebar can be minimized. Selecting a project restores its media, settings, saved subtitles and timeline. History begins after at least one successful generated subtitle; later removing all cues does not remove the project.

## Local files, memory and updates

Projects, copied media, preview files and diagnostics live under `data/`. Delete project removes its local folder; the originally selected file outside this folder is untouched. Empty working imports can remain on disk even though they do not appear in history.

Inference runs in a separate process using CPU INT8, two threads and greedy decoding. It is disposable by default; explicit Load model keeps it resident until unloading. Audio is read in windows of at most 60 seconds, favoring quiet boundaries. This reduces memory growth and releases model memory when the worker exits. Saved results are replaced only after a successful run. Chunk boundaries and greedy decoding may affect recognition; review output before publishing.

To update a cloned installation:

```powershell
# Stop the running server with Ctrl+C first.
git pull --ff-only
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

Then press **Ctrl+F5** in the browser. With a ZIP installation, extract the update separately and copy local project data only while both apps are stopped. Do not overwrite a working installation with an older data backup.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| Python missing / installation fails | Install 64-bit Python, enable PATH and reopen the console. Check internet access. Python 3.11 is an alternative if wheels are unavailable for your version. |
| Model unavailable | Locate its folder again; setup does not fetch weights. |
| `mkl_malloc` / allocation failure | Close duplicate model/server processes and memory-heavy apps. Keep the Windows page file system-managed or select a smaller model. SuperSub does not change OS settings. |
| `metadata_errors` | Update and restart the server. The current PCM pipeline bypasses the incompatible PyAV decoder. |
| Endpoint Not Found after updating | Stop the old server, restart Start.cmd and hard-refresh the browser. |
| Port 8765 in use | Run `powershell -File .\start.ps1 -Port 8766`. |
| Browser does not open | Visit the local URL manually. `-NoBrowser` disables automatic opening. |
| Video does not play | Wait for preview conversion; inspect the message below the player if conversion fails. |
| No speech / save error | Check that the file has audio; fix invalid or overlapping cue timings. Saved results are preserved on failed retries. |

## Development and current limits

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m py_compile app.py inference.py media_tools.py local_models.py model_picker.py install_models.py
.\.venv\Scripts\python.exe -m pip check
# Optional development-only Node.js checks:
node --test tests/timeline.test.mjs
node --check web/app.js
```

Verified: **24 Python tests**, **4 Node timeline tests**, DOM checks, FFmpeg conversion, and actual local Turbo inference on an eight-second speech sample. Full browser visual QA, long-video stress testing, offline validation and Persian accuracy benchmarking remain outstanding. GPU inference, separate forced alignment, Nava enablement, batch processing and burned-in export are not implemented. Cancellation terminates inference workers; audio extraction and independent preview conversion can still finish their current step.

Git contains code, scripts, tests and documentation. **Data, assets, models, virtual environments, credentials and caches are excluded.** Optional local logos can be placed in `assets/mansvolve-black.png` and `assets/mansvolve-white.png`.

See [project context](context/README.md), [setup guide](context/setup.md), [infrastructure](context/infra.md) and [current status](context/current-status.md). `requirements.txt` drives installation; `requirements-lock.txt` is the captured original Windows environment, not a cross-platform lock.
