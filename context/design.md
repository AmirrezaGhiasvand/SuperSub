# Design

Compact desktop layout (2026-11-16): at >=901px width and >=700px height, header/main use a viewport-height grid with no page scrolling. The 16:9 preview shrinks to its available top-row space next to media/generation controls. The timeline retains its 310px height; controls and export/save footer are compact. Settings use internal overflow; smaller windows retain accessible page flow. Buttons use flat fills and subtle borders, without gradients, shadows or moving hover effects. Focus rings remain visible.

Inspiration: https://amirrezaghiasvand.github.io/mansvolve_landing/ . Monochrome surfaces, rounded panels, pill actions and compact timeline labels. Dark background #070707/panels #111/borders #303030; light background #f6f6f6/white panels. Optional local Mansvolve logos accompany SuperSub. Current fonts are system fonts; no remote frontend resources.

Left: collapsible Projects/New project/history, then model/language/pause/word/glossary settings. Entire sidebar minimizes. Center: media/generate, video with subtitle overlay, zoomable media/subtitle tracks, cue editor, SRT download and Delete project.

Loading/completion dialogs show phases, elapsed time and cancellation. Timeline has a warm playhead and trim handles. Subtitle text uses auto direction in overlay and RTL editor fields. Edits autosave with visible status/error feedback. No Save/Reflow/Add cue/VTT/Text controls.

Theme/panel state persists in browser; reduced-motion disables spinner animation. Full visual/responsive/keyboard/accessibility QA is pending. Overlay is preview-only.
