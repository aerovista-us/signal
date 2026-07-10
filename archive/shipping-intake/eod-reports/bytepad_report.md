# BytePad (formerly Sticky Notes) — Consolidated Findings

Last updated: 2025-09-29

## Canonical name and aliases
- Canonical: BytePad
- Also known as: Sticky Notes, BytePad+, Bytepad.bamf

## Known locations (paths) discovered
- D:\AeroCore\tools\Bytepad\
  - index.html
  - main.js
  - preload.js
  - bytepad-style.css
- D:\AeroCore\tools\BytePad+\
  - style.css
  - renderer.js
  - tools.json
  - core\notes.js
  - core\enhancers\
  - utils\enhancers\
  - standalone\ (includes style.css, renderer.js, .gitignore)
- D:\AeroCore\tools\Bytepad.bamf\
  - index.html
  - main.js
  - bytepad-style.css
  - create-data-structure.js
  - bytepad-config.json
- D:\AeroCore\app\Andy's\V4\src\renderer\Tools\StickyNotes\
  - index.html
  - Bytepad.css
  - Bytepad.js

## Variants and lineage
- Sticky Notes appears to be the earlier name; BytePad is the current branding.
- Multiple distributions exist:
  - BytePad (base) under tools\Bytepad
  - BytePad+ (enhanced) with core/notes, enhancers, utils
  - Bytepad.bamf packaging variant with config and data structure scripts
  - StickyNotes tool embedding BytePad assets in an app tool path

## Components suggested by master data
- Frontend: HTML/CSS/JS (index.html, main.js, css variants)
- Electron-related presence: preload.js (implies Electron usage in some variants)
- Domain modules: core\\notes.js, enhancers, utils/enhancers
- Setup/data scripts: create-data-structure.js, bytepad-config.json

## Classification (from master tagging context)
- Appears under Web Apps & Tools with HTML/JS detected
- Consistently categorized as a tool in master mentions

## Initial takeaways
- BytePad is a notes/sticky-notes style tool that has evolved through several packaging variants.
- The "BytePad+" tree suggests modular architecture (core, enhancers, utils) beyond a simple single-file app.
- StickyNotes paths that import BytePad assets indicate backward compatibility or embedding for legacy tools.

## Open questions
- Which variant is the current production entry point? (BytePad vs BytePad+ vs .bamf)
- Where is the authoritative configuration for data paths and storage? (bytepad-config.json?)
- Does the Electron variant (preload.js) coexist with a pure-web build, or are they separate targets?
- What is the intended migration path from Sticky Notes to BytePad across apps?

## Next steps (ongoing updates planned)
1. Pull all matching rows from master CSVs to capture full context (topics, categories, co-mentioned tools).
2. Inventory BytePad+ core and enhancer modules to map features and dependencies.
3. Identify current entry points and runtime (web vs Electron) and document startup flow.
4. Trace data model and storage (create-data-structure.js, config) for persistence and migration.
5. Add cross-links to related tools discovered in the same contexts.

---

Notes: This report will be continuously appended as further evidence is gathered from `MemoryMapping/master` and source trees.

## Key Features & Capabilities (from master data)
- **Privacy-focused**: Local-only storage with instant search and tagging
- **Multiple note formats**: Plain text, code, checklist support
- **Color-coded notes**: Visual organization system
- **Export/import functionality**: Data portability
- **Real-time sync**: Firebase integration for collaborative features
- **Offline resilience**: Local backup with cloud sync
- **Geometry persistence**: Note positioning, sizing, and z-index management
- **Team boards**: Collaborative workspace functionality
- **Media support roadmap**: Planned image/video display and music support
- **Built-in media player**: Future enhancement planned

## Technical Architecture
- **Desktop version**: Electron-based with IPC communication
- **Mobile version**: Firebase sync with password-only access
- **Hybrid model**: Local storage + cloud collaboration
- **Conflict resolution**: Built-in sync conflict handling
- **Backup strategy**: Periodic and emergency backup systems
- **Firebase integration**: Real-time Firestore sync with offline fallback

## Current Issues & CSP Problems
Based on your console output, BytePad is experiencing:
- **Content Security Policy violations**: Firebase auth token requests blocked
- **Network connectivity issues**: "Could not reach Cloud Firestore backend"
- **CSP directive conflicts**: `connect-src` restrictions preventing Firebase API calls
- **Offline mode operation**: App falling back to local-only mode due to network restrictions

## Co-mentioned Tools & Projects
From master CSV analysis, BytePad is frequently mentioned alongside:
- **AeroCoreOS**: Integration planned for sticky notes and task linking
- **AeroDash**: Project overview integration
- **RydeSync**: Real-time syncing logic sharing
- **VaultMaster**: File tree integration
- **FantasyForge**: Development context
- **ICETAP/Rake & Shake**: Audit and compliance platform
- **AeroVista**: LLC ecosystem integration

## Development Context
- **Long-term goals**: Robust desktop features → mobile web version
- **Strategic approach**: Gradual enhancement incorporation
- **Integration focus**: AeroCoreOS redesign with BytePad integration
- **True path standardization**: System tool interaction improvements needed

## Update log
- 2025-09-29: Added consolidated paths and variants; initiated CSV and filesystem scans for additional BytePad/StickyNotes references.
- 2025-09-30: Added comprehensive feature analysis, technical architecture, current CSP issues, and co-mentioned tools from master CSV data.


