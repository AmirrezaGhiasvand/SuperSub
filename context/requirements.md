# Requirements

Windows-local video-to-SRT app with English layout, Persian editing, light/dark themes and persisted projects. No cloud inference/account/API key is required. Setup installs dependencies only; users register local CTranslate2 weights.

Workflow: New project/select media → configure → generate with phases → review video/timeline → autosave → SRT download. Project history is collapsible on the left; selection fetches latest saved media/settings/cues. The sidebar can minimize.

Controls: model, language, glossary, pause threshold .1–2s (default .45), default-on Automatic — follow speech pauses. Manual words 1–30 (default 8) is enabled only when automatic mode is off. Punctuation and six-second readability boundaries apply. Preserve spoken Persian with conservative character normalization.

Timeline supports seek/zoom/move/trim and synchronized video text. No Save/Reflow/Add cue/VTT/Text buttons. New project retains saved work and model configuration. Delete project removes copied data only.

Excluded: batch queue, translation, diarization, burned-in video and cloud services. Nava needs future alignment; no perfect accuracy/speed guarantee.
