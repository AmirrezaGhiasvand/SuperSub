# Setup and handoff

Updated 2026-11-16. See the root README for the complete installation and troubleshooting walkthrough.

Model downloads: [comparison](../README.md#model-choices), [exact files](../README.md#manual-download-exact-files). Small/Medium use vocabulary.txt; Turbo/Large V3 use vocabulary.json and preprocessor_config.json. Do not mix repositories, rename vocabulary files or select unconverted source checkpoints. Listings checked 2026-11-16; setup still downloads no weights.

Current workspace: Generate/Cancel and project name live in the navbar; browsing is hidden once media is selected. The right editor stays open and follows playback. Left/Right moves .1s, Shift arrows 1s, Up/Down subtitle starts. Font files/licenses ship under web/fonts, with no runtime Google Fonts dependency.

1. Install 64-bit Python 3.11+ with PATH enabled (development tested Python 3.14).
2. Clone https://github.com/AmirrezaGhiasvand/SuperSub.git or extract its ZIP. Private repository access requires an authorized account.
3. Run Setup.cmd: creates .venv, installs requirements.txt and checks imports. **No model downloads.**
4. Run Start.cmd: opens http://127.0.0.1:8765 after readiness. Keep the console open; Ctrl+C stops it.
5. Locate a local CTranslate2 model folder in Settings, select its profile, then Use this model. Required files include model.bin, config.json, tokenizer.json and original vocabulary/preprocessing files. Paste the path if Browse folders is unavailable.
6. Generate a short clip, review the timeline, edit, wait for autosave and export SRT.

No Node.js, GPU, cloud API key or separate FFmpeg install is needed. Setup needs internet for packages. Models remain in their original directories; absolute paths persist in ignored data/local-models.json. Moving weights requires re-registration. Nava generation is disabled until alignment exists.

PowerShell:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

setup.ps1 supports -Python with an executable path when creating a venv. start.ps1 supports -Port and -NoBrowser. There is no SkipModel flag. Optional install_models.py downloads are manual only, with choices small, medium, turbo and large-v3. All are ready-to-load CTranslate2; conversion is not offered.

To update: stop server, git pull --ff-only, rerun Setup.cmd, launch Start.cmd and Ctrl+F5. Back up data while stopped; external model folders need separate backup. ZIP users should extract updates separately and carefully transfer backed-up data. Absolute model paths are device-specific.

For memory failures, close duplicate servers/models and memory-heavy apps, use a system-managed page file or a smaller model. No OS settings are altered automatically. worker.log in each project retains diagnostics. For Not Found or metadata_errors after updating, restart the old server before refreshing. Verify offline operation and long-file performance before relying on them.

Git excludes data/, assets/, models/, .venv/, .tools/, credentials and caches. Optional local logos work without being distributed in Git.
