# Decisions

- Local-only processing, English UI, dark/light themes and Mansvolve inspiration were requested.
- Dependency-only setup; explicit model folder selection leaves weights in place. Manual downloads are optional. No data/assets/models in Git.
- Preserve colloquial Persian. User chose the current CTranslate2 engine and ready-to-load models only. Conversion-only Givia source and unavailable Nava were removed from recommendations and installer choices; existing compatible local models remain usable.
- Automatic word counts follow pauses by default; manual cap optional; punctuation and six-second readability boundaries remain.
- Autosave replaces Save/Reflow/Add cue controls. Visible export is SRT; New project resets workspace; history restores latest saved state.
- Bundled FFmpeg preview conversion supplies codec support; no OS codec pack or burned-in-video export.
- Disposable CPU INT8 worker, limited threads, greedy decoding and quiet-boundary windows reduce memory pressure. Native crashes do not take down the editor. No OS page-file changes are automatic.
- FastAPI/static JS/JSON are implemented. React/TypeScript/Tailwind/SQLite were original future architecture choices, not setup prerequisites.
