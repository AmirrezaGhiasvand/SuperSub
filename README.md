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

Select a video, model, video language and maximum words per cue (default 8). Add optional glossary hints, then generate. Review the video and edit subtitle text or timing. Double-click a cue to seek. **Save edits before Download SRT**; downloads reflect the saved project.

Reflow changes cue length using original word timestamps without rerunning transcription. Reflow refuses saved manual edits because their word alignment may no longer match. Cancellation takes effect between generated segments.

Projects and copied media are stored under `data/`. Delete a project in the UI to remove its local copy. Source files selected outside the project folder are untouched.

## What is included

Source code, tests, setup/launch scripts and project context. **`data/`, `assets/`, `models/`, `.venv/`, credentials and caches are excluded from Git.** The interface works without logos. For local branding, optionally place `mansvolve-black.png` and `mansvolve-white.png` in `assets/`.

## Troubleshooting

- **Python not found:** install Python, enable PATH and reopen the console.
- **Dependency installation fails:** check internet access and 64-bit Python. For incompatible wheels use Python 3.11 in a fresh checkout or virtual environment.
- **Model unavailable:** click Locate local model and select its existing folder again. Rerunning setup does not download weights. Optional downloads via `install_models.py` are manual only.
- **Port in use:** run `start.ps1 -Port 8766`.
- **Browser does not open:** visit the printed local URL manually. Use `start.ps1 -NoBrowser` when desired.
- **Preview cannot play a codec:** transcription may still work; preview transcoding is not implemented.
- **No speech / transcription error:** check that the input has a supported audio stream. Errors are displayed in the workspace.

## Development and status

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m py_compile app.py install_models.py
.\.venv\Scripts\python.exe -m pip check
```

This is an initial FastAPI/static-web implementation. GPU inference, forced alignment, React/SQLite migration, robust worker cancellation and benchmarked Persian accuracy remain planned. Browser and real-audio inference QA are not yet complete. See [context](context/README.md), [infrastructure](context/infra.md), and [current status](context/current-status.md).
