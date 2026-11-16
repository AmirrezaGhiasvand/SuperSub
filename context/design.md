# Design

Brand reference: https://amirrezaghiasvand.github.io/mansvolve_landing/ . Inspected source uses monochrome panels, rounded cards, pill buttons, dotted backgrounds, Vazirmatn and Martian Mono. SuperSub adapts those elements for an English editing app without copying analytics or remote font loading.

Dark palette: #080808 background, #131313 panels, #202020 raised surfaces, #343434 borders, white text. Light mode uses white/gray surfaces with black primary buttons. Yellow #f5ed03 marks playhead/snapping. Buttons are compact pills with visible focus, restrained contrast and no moving hover effects.

Inter is the English UI font; Vazirmatn supports Persian editing/captions; Martian Mono labels navigation/time. Variable TTFs and original OFL licenses ship in web/fonts. Optional Mansvolve logo assets remain local and outside Git.

Navbar: project name, Generate/Cancel, theme and brand. Left: Projects/New project/history and settings with collapse support. Center: compact fixed-16:9 preview, subtitle-only timeline, SRT/Delete and status footer. Right: always-visible inspector once media is selected or a project opens, showing a selected cue or an empty state. Browse appears only for new workspaces. Selecting/deselecting cues does not change preview width.

Desktop >=901px width and >=700px height uses viewport-height layout. Subtitle timeline is 180px; settings/editor scroll internally. Narrow/short windows retain accessible normal flow. Captions use native 50% horizontal/vertical positioning and centered fallback for fullscreen.

Single-click plays/selects a cue; double-click/Enter selects for editing. Left/Right nudges playhead .1s, Shift arrows 1s, Up/Down jumps subtitle starts. Escape clears selection. Inputs retain native editing keys. Snapping uses a zoom-aware threshold, visual guide, toggle and Alt bypass.

Real browser visual/responsive/accessibility QA remains outstanding; DOM/interaction checks pass.
