# Design

Editor placement update: the inspector now overlays a fixed media-actions slot, covering Browse/Generate while editing. It no longer adds a workspace column or changes preview/timeline geometry. Background controls are invisible and inert until Close/Escape restores them. The editor scrolls internally when necessary; video remains visible.

Timeline editor is now a non-modal panel on the right of the workspace, not a dialog. Single cue clicks play; double clicks open the editor. Snap targets use a mint guide, with a toggle in the toolbar and boundary navigation buttons. Keyboard controls are documented in README/tooltips. Panel and preview share space; narrower desktops hide the import controls while editing, and small windows place the editor inline. Escape or Close restores the workspace.

Compact desktop layout (2026-11-16): at >=901px width and >=700px height, header/main use a viewport-height grid with no page scrolling. The 16:9 preview shrinks to its available top-row space next to media/generation controls. The subtitle-only timeline uses 180px height, returning the removed video-name lane space to the preview; controls and export/save footer are compact. Settings use internal overflow; smaller windows retain accessible page flow. Buttons use flat fills and subtle borders, without gradients, shadows or moving hover effects. Focus rings remain visible.

Inspiration: https://amirrezaghiasvand.github.io/mansvolve_landing/ . Monochrome surfaces, rounded panels, pill actions and compact timeline labels. Dark background #070707/panels #111/borders #303030; light background #f6f6f6/white panels. Optional local Mansvolve logos accompany SuperSub. Current fonts are system fonts; no remote frontend resources.

Left: collapsible Projects/New project/history, then model/language/pause/word/glossary settings. Entire sidebar minimizes. Center: media/generate, video with subtitle overlay, zoomable media/subtitle tracks, cue editor, SRT download and Delete project.

Loading/completion dialogs show phases, elapsed time and cancellation. Timeline has a warm playhead and trim handles. Subtitle text uses auto direction in overlay and RTL editor fields. Edits autosave with visible status/error feedback. No Save/Reflow/Add cue/VTT/Text controls.

Theme/panel state persists in browser; reduced-motion disables spinner animation. Full visual/responsive/keyboard/accessibility QA is pending. Overlay is preview-only.

Captions use native percentage positioning at 50% horizontally/vertically, with centered multiline alignment. The HTML fallback also centers at 50%. The video-name lane is removed from DOM and timeline rendering.
