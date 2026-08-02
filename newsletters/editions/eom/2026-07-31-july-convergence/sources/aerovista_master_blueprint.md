# AeroVista Master Blueprint

Source: https://chatgpt.com/c/6a5a7b8a-3ce4-83e8-aa9c-37b088877502

## USER
Review both conversations in this project and create the master blueprint architecture build plan complete with to do list and phase roll up optimize for cursor including for the rules and skills know that we already have AV skill set

## ASSISTANT
I’m consolidating the two workspace threads into one implementation blueprint: system architecture, shared contracts, division model, packaging strategy, Cursor rules, AV-Skillset integration, phased delivery, and an executable backlog.

## ASSISTANT
Below is the consolidated master blueprint from both Workspace project conversations. It treats AeroCore OS as the shared operating layer, AeroVista Main as the organizational shell, and each division workspace as a permission-controlled operating environment rather than a simple dashboard.

 
# AeroVista Workspace Platform
## Master Architecture Blueprint, Build Plan, Cursor Rules, and Phase Roll-Up

**Working platform name:** AeroVista Workspace 
**Core operating layer:** AeroCore OS 
**Primary deployment forms:** PWA, desktop shell, portable workstation bundle, tablet mode 
**Primary engineering environment:** Cursor using AV-Skillset 
**Document status:** Master implementation blueprint 
**Operating mode:** Full Engineering / Controlled Change

---

# 1. Executive Vision

AeroVista Workspace is a unified digital work environment for AeroVista Main and its divisions.

It is not merely:

- A collection of links
- A dashboard
- A launcher
- A browser bookmark page
- A wrapper around third-party applications

It is a modular operating workspace where authorized users can:

- Enter the divisions they are permitted to access
- Work with files, projects, media, tools, tasks, agents, and backend services
- Open browser-based editors and locally installed applications
- Launch portable applications without complex installation
- Send long-running work to AeroCore backend workers
- Move projects between browser, desktop, tablet, and server environments
- Use the same project identity, metadata, permissions, storage, and workflow state everywhere
- Install new capabilities through adapters and capability packages
- Operate within one dependable system contract

The intended experience is:

> Sign in once, enter the appropriate division, open a project, and have the correct files, tools, agents, workflows, permissions, and backend resources already available.

---

# 2. Core Product Structure

## 2.1 AeroVista Main

AeroVista Main is the organizational workspace above all divisions.

It provides:

- Executive overview
- Cross-division project visibility
- AVCC integration
- Shared announcements
- Shared document library
- User and team management
- Division access control
- Organization-wide search
- Shared assets and brand resources
- Operational health
- Release visibility
- Shared AI agents
- Shared service catalog
- Workspace administration
- Cross-division intake and routing
- Audit and compliance reporting

AeroVista Main should not automatically expose every division to every user.

It acts as the entry point and command layer.

---

## 2.2 Division Workspaces

Each division receives its own workspace configuration, tools, routes, project types, storage scopes, agents, and workflow templates.

The architecture must not hard-code the number of divisions.

Instead, divisions are loaded from a versioned **Division Registry**.

This resolves the current planning discrepancy between:

- “Seven divisions plus AeroVista Main”
- The broader current AeroVista organizational roster

The platform should initially support the approved launch roster while allowing Frontier or future divisions to be enabled through configuration rather than architectural changes.

Likely registry entries include:

- Nexus TechWorks
- Lumina Creative Media
- EchoVerse Audio
- Horizon Aerial & Visual
- Vespera Publishing
- Summit Learning
- SkyForge Creative Studios
- Frontier Outdoor & Adventure, when approved for workspace activation

---

# 3. Product Principles

## 3.1 Workspace, Not Link Farm

Every division page must enable actual work.

A division workspace should include:

- Active projects
- Recent files
- Division tools
- Embedded editors
- Local application launchers
- Backend processing jobs
- Templates
- Workflow stages
- Team activity
- Agent access
- Project health
- Publishing and delivery actions

---

## 3.2 Capability-Based Architecture

The platform should not assume every tool is an internal web application.

A capability may be implemented as:

- Native AeroVista web module
- Embedded browser application
- Self-hosted open-source service
- Portable desktop application
- Installed desktop application
- Tauri desktop command
- Electron desktop command
- Android application
- PWA feature
- Server-side worker
- Containerized processor
- External SaaS integration
- AI agent or workflow
- Command-line tool
- Remote desktop application

All capabilities must appear through a common capability contract.

---

## 3.3 Permission-Controlled Composition

Users should see only:

- Divisions they can access
- Projects they are assigned to
- Tools allowed by their role
- Files allowed by their storage scope
- Actions permitted by policy
- Backend jobs appropriate for their role
- Administrative controls they are authorized to use

The workspace UI must be composed dynamically from effective permissions.

Do not merely hide navigation while leaving APIs exposed.

Both frontend and backend must enforce authorization.

---

## 3.4 Local-First, Server-Assisted

Routine creative work should continue even if some backend services are temporarily unavailable.

Local-first capabilities include:

- File browsing
- Draft editing
- Project notes
- Selected browser tools
- Cached project metadata
- Portable applications
- Queued uploads
- Queued backend jobs
- Offline PWA shell
- Local preview generation

Server-assisted capabilities include:

- Rendering
- Transcoding
- AI inference
- Media analysis
- Batch conversion
- Publishing
- Search indexing
- Backups
- Shared collaboration
- Automation
- Compliance scanning
- Large-file processing

---

## 3.5 One Project Identity Everywhere

A project must keep the same identity across:

- PWA
- Desktop shell
- Portable app bundle
- Tablet
- Server workers
- Shared storage
- AVCC
- Division workflows
- Publishing systems
- Audit records

A user should never need to manually reconcile multiple unrelated project folders representing the same project.

---

# 4. High-Level System Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│ USER SURFACES │
├──────────────────────────────────────────────────────────────┤
│ PWA │ Tauri Desktop │ Electron Fallback │ Tablet │ Mobile │
│ Browser │ Portable Workstation │ Installed Desktop Apps │
└───────────────────────────┬──────────────────────────────────┘
 │
┌───────────────────────────▼──────────────────────────────────┐
│ WORKSPACE EXPERIENCE │
├──────────────────────────────────────────────────────────────┤
│ AeroVista Main Shell │
│ Division Workspaces │
│ Project Workbench │
│ Tool Dock / Launcher │
│ File and Asset Browser │
│ Workflow Board │
│ Agent Panel │
│ Job Center │
│ Search and Command Palette │
│ Notifications │
└───────────────────────────┬──────────────────────────────────┘
 │
┌───────────────────────────▼──────────────────────────────────┐
│ AEROCORE PLATFORM SERVICES │
├──────────────────────────────────────────────────────────────┤
│ Identity and Access │
│ Workspace Composition │
│ Division Registry │
│ Project Registry │
│ Capability Registry │
│ Tool Adapter Gateway │
│ Workflow Engine │
│ Job Orchestrator │
│ Event Bus │
│ Search and Indexing │
│ File and Asset Services │
│ Agent Gateway │
│ Notification Service │
│ Audit and Compliance │
│ Health and Observability │
│ Release and Configuration Service │
└───────────────────────────┬──────────────────────────────────┘
 │
┌───────────────────────────▼──────────────────────────────────┐
│ EXECUTION AND STORAGE │
├──────────────────────────────────────────────────────────────┤
│ NXCore Containers │
│ Worker Pools │
│ GPU / AI Workers │
│ Portable Applications │
│ Local Desktop Applications │
│ Object Storage │
│ Shared Project Storage │
│ Databases │
│ Redis / Queues │
│ Search Index │
│ Backup and Archive │
└───────────────────────────┬──────────────────────────────────┘
 │
┌───────────────────────────▼──────────────────────────────────┐
│ EXTERNAL AND DIVISION SYSTEMS │
├──────────────────────────────────────────────────────────────┤
│ AVCC │ Art Localized │ EchoVerse │ GitHub │ Cloudflare │
│ Firebase │ Publishing Services │ Email │ Calendar │
│ Drone and Media Systems │ Learning Platforms │ AI Providers │
└──────────────────────────────────────────────────────────────┘
```

---

# 5. Primary User Surfaces

## 5.1 Progressive Web Application

The PWA should be the default workspace client.

Responsibilities:

- Authentication
- Division routing
- Project dashboards
- Embedded browser editors
- File previews
- Workflow controls
- Agent access
- Backend job submission
- Notifications
- Tablet operation
- Offline shell
- Installable browser experience

The PWA should not attempt to reproduce every advanced desktop editor.

It should coordinate tools and provide the central project context.

---

## 5.2 Tauri Desktop Shell

Tauri is the preferred desktop shell because it offers:

- Smaller bundles than Electron
- Lower idle memory use
- Rust-backed system integration
- Secure command boundaries
- File-system access
- Local application launching
- Deep-link registration
- Update support
- Sidecar process support

The Tauri application should wrap the workspace PWA while providing a controlled desktop bridge.

Desktop-only functions may include:

- Open local project folder
- Launch registered portable application
- Launch installed application
- Reveal asset in file manager
- Watch project directories
- Register file handlers
- Open terminal in project context
- Sync files
- Manage portable bundles
- Start approved local services
- Send local files to server workers
- Receive rendered outputs
- Check tool installation health

---

## 5.3 Electron Fallback

Electron should remain a supported fallback, not the default.

Use Electron when:

- A required Node-native integration is materially easier
- A target plugin depends on Electron
- Existing code can accelerate delivery
- Tauri compatibility blocks a critical capability
- A specialized division application requires Chromium-specific behavior

The core workspace API contracts must remain independent of either desktop shell.

---

## 5.4 Portable Workstation Bundle

The portable workstation is a deployment package for Windows workstations.

It should contain:

```text
AeroVista-Workspace/
├── AeroVista Workspace Launcher.exe
├── apps/
│ ├── graphics/
│ ├── video/
│ ├── audio/
│ ├── publishing/
│ ├── development/
│ ├── utilities/
│ └── division-specific/
├── runtime/
├── config/
├── cache/
├── logs/
├── projects/
├── templates/
├── updates/
└── workspace-manifest.json
```

The bundle should:

- Run without administrative installation where technically possible
- Detect available portable tools
- Register them with the local capability bridge
- Update individual tool packages independently
- Maintain checksums and versions
- Avoid storing credentials in plaintext
- Store user-specific data outside immutable application folders
- Support USB, network-share, or local SSD deployment
- Provide repair and verification commands

Portable applications must not be copied blindly into one massive package.

They should be installed as versioned capability packs.

---

## 5.5 Tablet Mode

Tablet mode should prioritize:

- Reviewing projects
- Approvals
- Notes and annotations
- Lightweight image edits
- Audio and video review
- File upload
- Camera capture
- Task handling
- Agent interaction
- Job monitoring
- Publishing approval
- Dashboard access

Tablet mode should not promise parity with desktop applications.

When a desktop-only function is selected, the system should offer:

- Send to desktop queue
- Send to backend worker
- Open remote workstation
- Create task for an authorized operator

---

# 6. Core Workspace Modules

## 6.1 Main Shell

The shared shell contains:

- Organization switcher
- Division switcher
- Project switcher
- Global command palette
- Search
- Notifications
- User profile
- Connection status
- Sync state
- Job state
- Help
- Workspace settings

---

## 6.2 Project Workbench

The Project Workbench is the center of daily work.

Each project page should display:

- Project identity
- Division
- Project type
- Owner
- Team
- Current workflow stage
- Recent files
- Active tasks
- Available tools
- Current jobs
- Outputs
- Approvals
- Activity history
- Notes
- Linked systems
- Agent context
- Delivery status

Suggested routes:

```text
/workspace
/workspace/main
/workspace/divisions/:divisionSlug
/workspace/projects/:projectId
/workspace/projects/:projectId/files
/workspace/projects/:projectId/tools
/workspace/projects/:projectId/workflow
/workspace/projects/:projectId/jobs
/workspace/projects/:projectId/activity
/workspace/projects/:projectId/settings
```

---

## 6.3 Tool Dock

The Tool Dock presents capabilities relevant to the current division and project.

Tool groups:

- Create
- Edit
- Review
- Convert
- Analyze
- Collaborate
- Publish
- Deliver
- Automate
- Administer

A tool tile should clearly show:

- Name
- Capability type
- Launch target
- Availability
- Local or remote execution
- Required permissions
- Compatible file types
- Current version
- Health state
- Whether installation is required
- Whether it can run on the current device

---

## 6.4 Unified File and Asset Browser

The asset browser should present a virtual project view while supporting several storage backends.

Sources may include:

- Project folders
- NXCore shared storage
- Local device storage
- Uploaded assets
- Generated outputs
- Template libraries
- Division asset libraries
- Archive storage
- External cloud storage
- Published assets

Core operations:

- Preview
- Open
- Download
- Upload
- Move
- Copy
- Rename
- Version
- Tag
- Comment
- Lock
- Approve
- Send to tool
- Send to worker
- Publish
- Archive

---

## 6.5 Job Center

Long-running processes should never be hidden behind a frozen interface.

The Job Center provides:

- Queued jobs
- Running jobs
- Completed jobs
- Failed jobs
- Progress
- Logs
- Inputs
- Outputs
- Retry
- Cancel
- Rerun with changes
- Open result
- Assign operator
- Worker health

Example jobs:

- Video rendering
- Audio analysis
- Transcoding
- Image enhancement
- Document conversion
- OCR
- AI generation
- Dataset processing
- Static site build
- Application build
- Deployment
- Backup
- Publishing
- Thumbnail generation
- Archive inspection

---

# 7. Canonical Domain Model

## 7.1 Organization

```json
{
 "organization_id": "av",
 "name": "AeroVista LLC",
 "status": "active"
}
```

---

## 7.2 Division

```json
{
 "division_id": "lumina",
 "display_name": "Lumina Creative Media",
 "status": "active",
 "workspace_route": "/workspace/divisions/lumina",
 "capability_sets": [
 "shared-core",
 "visual-design",
 "social-media",
 "marketing-production"
 ],
 "storage_scope": "divisions/lumina",
 "default_project_templates": [
 "campaign",
 "social-package",
 "brand-kit"
 ]
}
```

---

## 7.3 Project

```json
{
 "project_id": "prj_01JXYZ",
 "slug": "downtown-cda-booth-campaign",
 "title": "Downtown CDA Booth Campaign",
 "division_id": "lumina",
 "project_type": "campaign",
 "status": "active",
 "workflow_stage": "production",
 "owner_user_id": "usr_123",
 "team_ids": ["team_lumina"],
 "storage_root": "projects/prj_01JXYZ",
 "created_at": "ISO-8601",
 "updated_at": "ISO-8601"
}
```

---

## 7.4 Asset

```json
{
 "asset_id": "ast_01JXYZ",
 "project_id": "prj_01JXYZ",
 "name": "hero-image-v3.png",
 "media_type": "image/png",
 "asset_type": "image",
 "version": 3,
 "storage_provider": "aerocore",
 "storage_key": "projects/prj_01JXYZ/assets/hero-image-v3.png",
 "checksum": "sha256:...",
 "created_by": "usr_123",
 "status": "working"
}
```

---

## 7.5 Capability

```json
{
 "capability_id": "image.raster.edit",
 "name": "Raster Image Editing",
 "category": "edit",
 "supported_asset_types": ["image/png", "image/jpeg", "image/webp"],
 "execution_modes": [
 "web",
 "portable",
 "installed",
 "worker"
 ],
 "required_permissions": ["asset.read", "asset.write"],
 "adapter_contract_version": "1.0"
}
```

---

## 7.6 Tool Registration

```json
{
 "tool_id": "gimp-portable",
 "name": "GIMP Portable",
 "provides": ["image.raster.edit"],
 "adapter_type": "desktop-launch",
 "platforms": ["windows"],
 "launch": {
 "executable": "apps/graphics/gimp/GIMPPortable.exe",
 "arguments": ["{{asset.local_path}}"]
 },
 "health_check": {
 "type": "file-exists",
 "path": "apps/graphics/gimp/GIMPPortable.exe"
 }
}
```

---

## 7.7 Job

```json
{
 "job_id": "job_01JXYZ",
 "job_type": "media.video.transcode",
 "project_id": "prj_01JXYZ",
 "requested_by": "usr_123",
 "status": "queued",
 "priority": "normal",
 "inputs": [
 {
 "asset_id": "ast_source"
 }
 ],
 "parameters": {
 "format": "mp4",
 "resolution": "1080p"
 },
 "outputs": [],
 "worker_pool": "media",
 "created_at": "ISO-8601"
}
```

---

# 8. Shared Naming Standards

Use predictable identifiers throughout the platform.

## 8.1 Identifier Prefixes

```text
org_ Organization
div_ Division
usr_ User
team_ Team
role_ Role
prj_ Project
ast_ Asset
cap_ Capability
tool_ Tool registration
job_ Job
wfl_ Workflow
tsk_ Task
evt_ Event
rel_ Release
pkg_ Capability package
agt_ Agent
sec_ Secret reference
```

Human-readable slugs may omit prefixes.

Database identifiers should remain opaque and immutable.

---

## 8.2 Event Naming

Use dot-separated past-tense event names:

```text
project.created
project.updated
project.archived
asset.uploaded
asset.versioned
asset.approved
asset.published
job.queued
job.started
job.completed
job.failed
tool.launched
workflow.transitioned
release.deployed
capability.installed
```

---

## 8.3 Capability Naming

Use hierarchical capability names:

```text
image.raster.edit
image.vector.edit
image.background.remove
image.batch.resize
image.slice
audio.waveform.edit
audio.multitrack.edit
audio.analyze
video.nonlinear.edit
video.transcode
document.layout.edit
document.pdf.edit
document.convert
code.repository.edit
code.application.build
site.static.publish
drone.flight.plan
drone.media.process
learning.course.author
publishing.book.layout
```

This makes tools interchangeable.

For example, multiple applications may provide `image.raster.edit`.

---

# 9. Adapter Architecture

Every external application or service must connect through an adapter.

## 9.1 Adapter Types

- Web embed adapter
- Web redirect adapter
- Desktop launch adapter
- Portable application adapter
- Local service adapter
- REST API adapter
- GraphQL adapter
- Command-line adapter
- Container worker adapter
- Queue worker adapter
- Storage adapter
- Publishing adapter
- Authentication adapter
- AI provider adapter
- Remote desktop adapter

---

## 9.2 Required Adapter Contract

Every adapter must declare:

- Unique adapter ID
- Contract version
- Tool or service version
- Capabilities provided
- Input asset types
- Output asset types
- Supported platforms
- Required permissions
- Configuration requirements
- Secret references
- Health check
- Launch or execution behavior
- Error mapping
- Logging behavior
- Cleanup behavior
- Update behavior
- Rollback behavior

---

## 9.3 Adapter Lifecycle

```text
discovered
→ registered
→ configured
→ tested
→ enabled
→ healthy
→ degraded
→ disabled
→ retired
```

Do not label an adapter “complete” merely because code exists.

Track these states separately:

- Implemented
- Tested
- Packaged
- Deployed
- Configured
- Enabled
- Verified
- Operationally accepted

---

# 10. Capability Package System

Portable tools, templates, adapters, and supporting runtimes should be distributed as capability packages.

Example:

```text
pkg-image-foundation/
├── package.json
├── manifest.json
├── checksums.json
├── adapters/
├── apps/
├── templates/
├── licenses/
├── icons/
├── install/
├── uninstall/
├── verify/
└── README.md
```

Manifest example:

```json
{
 "package_id": "pkg-image-foundation",
 "version": "1.0.0",
 "platforms": ["windows-x64"],
 "provides": [
 "image.raster.edit",
 "image.vector.edit",
 "image.batch.resize",
 "image.slice"
 ],
 "dependencies": [],
 "tools": [
 "gimp-portable",
 "inkscape-portable",
 "imagemagick"
 ]
}
```

Each package must support:

- Installation
- Verification
- Repair
- Upgrade
- Rollback
- Removal
- License inventory
- Checksum validation

---

# 11. Division Workspace Capability Model

## 11.1 Shared Core for All Divisions

Every division receives:

- Project management
- File and asset browser
- Notes
- Team activity
- Workflow stages
- Tasks
- Calendar links
- Messaging links
- AI assistant
- Document editor
- PDF viewer
- Image preview
- Media preview
- Archive utilities
- Search
- Job submission
- Publishing handoff
- Audit history
- Templates
- Basic conversion tools

---

## 11.2 Lumina Creative Media

Primary work:

- Brand design
- Campaign development
- Social media production
- Marketing assets
- Photography enhancement
- Graphic packages
- Promotional video
- Creative review

Capabilities:

- Raster editing
- Vector editing
- Layout design
- Background removal
- Image generation
- Image slicing
- Batch resize
- Color correction
- Social format conversion
- Video editing
- Motion graphics
- Brand kit management
- Campaign packaging
- Approval boards

Candidate open-source and free tools:

- GIMP
- Inkscape
- Krita
- Photopea as browser fallback
- Penpot
- Blender
- Kdenlive
- Shotcut
- OpenShot
- ImageMagick
- FFmpeg
- Upscayl
- Excalidraw
- Scribus
- darktable
- RawTherapee

---

## 11.3 Nexus TechWorks

Primary work:

- Software development
- Infrastructure
- Security
- Automation
- Application operations
- System integration
- Repository maintenance

Capabilities:

- Repository management
- Browser IDE
- Local IDE launch
- Terminal
- Container management
- API testing
- Database administration
- Architecture diagrams
- Log analysis
- Deployment
- Monitoring
- Security scanning
- Documentation
- AI coding agents

Candidate tools:

- Cursor
- VS Code Portable
- VSCodium
- Git
- GitHub CLI
- Docker
- Podman
- Bruno
- Hoppscotch
- DBeaver
- SQLite Browser
- Redis Insight
- Portainer
- Grafana
- Prometheus
- Loki
- Gitea or Forgejo
- Mermaid
- Excalidraw
- Draw.io
- OpenTofu
- Ansible
- Nmap for authorized network diagnostics only
- OWASP ZAP for approved application testing

---

## 11.4 EchoVerse Audio

Primary work:

- Music cataloging
- Metadata enrichment
- Audio analysis
- Editing
- Streaming
- Playlist production
- Voice and narration
- Publishing

Capabilities:

- Waveform editing
- Multitrack editing
- Audio playback
- Metadata editing
- Catalog browsing
- BPM and key analysis
- Loudness analysis
- Transcription
- Stem processing
- Batch normalization
- Cover art
- Playlist management
- Distribution preparation

Candidate tools:

- Audacity
- Ardour
- Tenacity
- LMMS
- Mixxx
- FFmpeg
- SoX
- MusicBrainz Picard
- Kid3
- Whisper
- Demucs
- Essentia
- librosa
- EchoVerse native applications

The workspace should integrate existing EchoVerse services rather than duplicate them.

---

## 11.5 Horizon Aerial & Visual

Primary work:

- Drone operations
- Aerial photography
- Inspection media
- Mapping
- Video production
- Client delivery

Capabilities:

- Flight planning
- Mission records
- Media ingest
- Geotagging
- Photogrammetry handoff
- Panorama creation
- Image processing
- Video editing
- Map review
- Client galleries
- Compliance records
- Equipment tracking

Candidate tools:

- WebODM
- OpenDroneMap
- QGIS
- CloudCompare
- Blender
- Kdenlive
- FFmpeg
- ExifTool
- darktable
- RawTherapee
- MeshLab

Flight and regulatory records require stricter permissions and audit retention.

---

## 11.6 Vespera Publishing

Primary work:

- Books
- Reports
- Digital publications
- Manuscript development
- Layout
- EPUB and PDF creation

Capabilities:

- Manuscript editing
- Version comparison
- Layout
- Citation handling
- Proofing
- EPUB generation
- PDF production
- Cover design
- Publishing checklists
- Metadata preparation

Candidate tools:

- LibreOffice Writer
- OnlyOffice
- Scribus
- Sigil
- Calibre
- Pandoc
- LanguageTool
- Zotero
- GIMP
- Inkscape
- Typst
- LaTeX tooling

---

## 11.7 Summit Learning

Primary work:

- Course creation
- Training materials
- Employee onboarding
- Learning delivery
- Assessments
- Certification

Capabilities:

- Course authoring
- Video lessons
- Narration
- Slide production
- Quizzes
- SCORM packaging
- Learning records
- Training templates
- Completion reporting

Candidate tools:

- Moodle
- H5P
- OBS Studio
- OpenShot or Kdenlive
- Audacity
- Excalidraw
- LibreOffice Impress
- Xerte
- Adapt Learning
- Whisper
- FFmpeg

---

## 11.8 SkyForge Creative Studios

Primary work:

- Advanced visual production
- 3D
- Animation
- Cinematic media
- Interactive environments
- Game and virtual experiences

Capabilities:

- 3D modeling
- Animation
- Rendering
- Compositing
- Texture production
- Game project management
- Asset pipelines
- Virtual production
- Interactive previews

Candidate tools:

- Blender
- Godot
- Unreal Engine launcher integration
- Unity launcher integration
- Krita
- GIMP
- Inkscape
- Natron
- Material Maker
- ArmorPaint alternatives where licensing permits
- MeshLab
- FFmpeg

---

## 11.9 Frontier Outdoor & Adventure

When enabled:

- Field projects
- Equipment records
- Route planning
- Outdoor media
- Product evaluation
- Expedition documentation
- Vehicle and e-bike projects

Capabilities:

- Offline project packs
- Maps
- GPS imports
- Equipment checklists
- Maintenance records
- Field media ingest
- Route documentation
- Weather and risk briefs
- Vehicle build records

Potential tools:

- QGIS
- Organic Maps
- GPXSee
- Viking GPS
- ExifTool
- LibreOffice
- Local PWA field forms

---

# 12. AeroCore Backend Services

## 12.1 Identity and Access Service

Responsibilities:

- User identity
- Session management
- Organization membership
- Division access
- Role assignments
- Project membership
- Capability permissions
- Device registration
- Service accounts
- API tokens
- Audit identity

Recommended model:

- OIDC-compatible identity
- Cloudflare Access for protected external entry points
- Internal AeroCore authorization service
- Short-lived access tokens
- Server-side permission checks
- Device trust for desktop bridges

---

## 12.2 Workspace Composition Service

Returns the UI composition for a user.

Example:

```http
GET /api/workspace/me
```

Response includes:

- Accessible divisions
- Recent projects
- Available capabilities
- Installed tools
- Current device features
- Notifications
- Active jobs
- Assigned tasks
- Administrative options

---

## 12.3 Division Registry Service

Canonical source for:

- Division identities
- Routes
- branding
- capability sets
- templates
- storage scopes
- workflow definitions
- integration bindings

The registry should be stored in Git as versioned configuration and loaded into the service.

---

## 12.4 Project Registry Service

Canonical source for:

- Project identity
- ownership
- team
- division
- state
- workflow
- linked storage
- linked repositories
- linked publishing targets
- associated assets
- project configuration

---

## 12.5 Capability Registry

The Capability Registry answers:

- What can this workspace do?
- Which tools provide the capability?
- Which execution modes are available?
- Is the tool installed?
- Is the backend healthy?
- Does the user have permission?
- Is the current device compatible?

---

## 12.6 Job Orchestrator

Recommended initial stack:

- API service
- Redis-backed queue
- Worker pools
- PostgreSQL job records
- WebSocket or Server-Sent Events progress updates
- Object or shared storage for inputs and outputs

Potential implementations:

- BullMQ for Node-first jobs
- Celery for Python-heavy processing
- Temporal later for complex durable workflows
- NATS or RabbitMQ when cross-service event volume justifies it

Do not introduce Temporal during the first foundation phase unless workflow durability requirements already exceed a simpler queue.

---

## 12.7 Event Bus

Start with a simple internal event contract.

Possible initial implementation:

- Redis Streams
- NATS JetStream
- PostgreSQL outbox pattern

Every state-changing service should emit events after durable persistence.

Avoid services silently mutating one another’s databases.

---

## 12.8 Search and Indexing

Search targets:

- Projects
- Assets
- Documents
- Metadata
- Tasks
- Activity
- Jobs
- Division resources
- Tool catalog
- Templates

Initial implementation may use PostgreSQL full-text search.

Move to Meilisearch or OpenSearch when indexing scale or relevance requires it.

---

## 12.9 Audit and Compliance

Audit events must include:

- Actor
- Action
- Target
- Timestamp
- Project
- Division
- Device
- Result
- Request correlation ID
- Relevant before and after state
- Policy decision where applicable

Audit records should be append-only.

Sensitive actions include:

- Permission changes
- Publishing
- Deletion
- External delivery
- Tool installation
- Secret use
- Administrative actions
- Compliance exports
- Drone regulatory records
- Production deployments

---

# 13. Storage Architecture

## 13.1 Logical Layout

```text
/aerocore/
├── organizations/
│ └── av/
├── divisions/
│ ├── lumina/
│ ├── nexus/
│ └── ...
├── projects/
│ └── prj_*/
│ ├── project.json
│ ├── source/
│ ├── working/
│ ├── assets/
│ ├── outputs/
│ ├── exports/
│ ├── delivery/
│ ├── cache/
│ └── archive/
├── shared/
│ ├── brand/
│ ├── templates/
│ ├── fonts/
│ ├── stock/
│ └── references/
└── system/
 ├── packages/
 ├── manifests/
 ├── logs/
 ├── backups/
 └── quarantine/
```

---

## 13.2 Storage Rules

- Project IDs, not display names, identify storage roots.
- File names may change without changing asset identity.
- Asset metadata is stored in the database.
- Important files use checksums.
- Generated outputs reference their source assets.
- Applications may use temporary working copies.
- Temporary files must not become canonical assets automatically.
- Publishing creates an immutable delivery record.
- Deletion initially means soft deletion.
- Archive and purge are separate controlled operations.

---

## 13.3 Local Synchronization

The desktop bridge should support:

- Project checkout
- Selective folder sync
- Conflict detection
- Upload queue
- Download queue
- Checksum verification
- Working copy state
- Explicit publish or commit
- Offline changes
- Retry after reconnect

Do not attempt a full Dropbox replacement in Phase 1.

Begin with explicit project checkout and sync operations.

---

# 14. Security Architecture

## 14.1 Trust Boundaries

Treat these as separate trust zones:

- Public browser
- Authenticated browser
- Desktop shell
- Portable application
- Local machine
- Tailnet
- NXCore service network
- Worker containers
- External SaaS
- Publishing targets

---

## 14.2 Desktop Bridge Rules

The PWA must not receive unrestricted local system access.

Use a strict allowlist of commands.

Examples:

```text
workspace.openProjectFolder
workspace.launchTool
workspace.revealAsset
workspace.checkoutProject
workspace.syncProject
workspace.submitLocalFile
workspace.getInstalledCapabilities
workspace.verifyCapabilityPackage
```

Every command must validate:

- Authenticated user
- Device registration
- Permission
- Project scope
- Allowed path
- Tool registration
- Argument format

Never expose arbitrary shell execution to the web interface.

---

## 14.3 Secrets

Secrets must be referenced, not copied into project files.

Use:

- Environment-specific secret stores
- Docker secrets where suitable
- Encrypted server configuration
- OS credential storage for desktop tokens
- Short-lived credentials
- Rotation procedures

Never place production secrets in:

- Git repositories
- capability manifests
- portable bundles
- frontend environment files
- project exports
- Cursor rules
- logs

---

# 15. Repository Architecture

Recommended monorepo:

```text
aerovista-workspace/
├── AGENTS.md
├── README.md
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
├── apps/
│ ├── workspace-web/
│ ├── workspace-desktop-tauri/
│ ├── workspace-desktop-electron/
│ ├── admin-console/
│ └── package-manager/
├── services/
│ ├── workspace-api/
│ ├── identity-policy/
│ ├── project-registry/
│ ├── capability-registry/
│ ├── job-orchestrator/
│ ├── file-service/
│ ├── event-service/
│ ├── search-service/
│ ├── audit-service/
│ └── notification-service/
├── workers/
│ ├── media-worker/
│ ├── image-worker/
│ ├── audio-worker/
│ ├── document-worker/
│ ├── build-worker/
│ └── ai-worker/
├── packages/
│ ├── ui/
│ ├── contracts/
│ ├── config/
│ ├── auth/
│ ├── events/
│ ├── storage/
│ ├── observability/
│ ├── tool-adapters/
│ └── testing/
├── divisions/
│ ├── lumina/
│ ├── nexus/
│ ├── echoverse/
│ ├── horizon/
│ ├── vespera/
│ ├── summit/
│ ├── skyforge/
│ └── frontier/
├── capability-packs/
│ ├── shared-foundation/
│ ├── image-foundation/
│ ├── video-foundation/
│ ├── audio-foundation/
│ ├── publishing-foundation/
│ ├── development-foundation/
│ └── field-foundation/
├── infrastructure/
│ ├── compose/
│ ├── traefik/
│ ├── cloudflare/
│ ├── monitoring/
│ ├── backup/
│ └── scripts/
├── docs/
│ ├── architecture/
│ ├── contracts/
│ ├── operations/
│ ├── decisions/
│ ├── testing/
│ └── runbooks/
└── scripts/
 ├── bootstrap/
 ├── verify/
 ├── release/
 └── maintenance/
```

---

# 16. Technology Baseline

## Frontend

- React
- TypeScript
- Next.js or Vite-based React shell
- Tailwind CSS
- TanStack Query
- Zustand or equivalent lightweight UI state
- Zod for contract validation
- Workbox or framework-native PWA support
- Storybook for shared components

Next.js is appropriate when server-rendered routes and integrated backend-for-frontend behavior are valuable.

A Vite SPA is appropriate if the PWA is primarily an authenticated application behind AeroCore APIs.

Recommended decision:

- Use Next.js for the main workspace and admin shell.
- Keep shared packages framework-neutral.
- Use client-side workbench modules where interaction is intensive.

## Backend

- TypeScript
- Node.js
- Fastify or NestJS
- PostgreSQL
- Redis
- S3-compatible object storage where appropriate
- Shared NXCore storage for large working media
- OpenAPI
- Zod or JSON Schema contracts

## Desktop

- Tauri
- Rust command layer
- TypeScript frontend
- Signed update manifests
- Capability discovery service

## Workers

- Python for AI, media intelligence, and scientific processing
- Node.js for general orchestration
- FFmpeg and ImageMagick sidecars
- Container isolation for risky or conflicting toolchains

## Infrastructure

- Docker Compose during initial deployment
- Traefik
- Cloudflare Tunnel and Access
- Tailscale
- Prometheus
- Grafana
- Loki
- OpenTelemetry
- Automated backup verification

Kubernetes is not required for the initial AeroCore deployment.

Introduce it only when workload scale, multi-node scheduling, or operational needs justify the additional complexity.

---

# 17. Cursor and AV-Skillset Integration

The AV-Skillset already exists and must be treated as the governing engineering workflow layer.

Do not create a competing skill system inside this repository.

## 17.1 Repository Bootstrap

At repository root:

```text
AGENTS.md
.cursor/
├── rules/
│ ├── 00-project-foundation.mdc
│ ├── 10-architecture.mdc
│ ├── 20-contracts.mdc
│ ├── 30-security.mdc
│ ├── 40-testing.mdc
│ ├── 50-deployment.mdc
│ ├── 60-documentation.mdc
│ └── 70-controlled-change.mdc
└── commands/
 ├── plan-feature.md
 ├── audit-service.md
 ├── implement-adapter.md
 ├── verify-release.md
 └── create-capability-pack.md
```

`AGENTS.md` should point Cursor and other coding agents to AV-Skillset and explain when each AeroVista skill is mandatory.

---

## 17.2 Required Skill Activation

Before major work, agents should use the applicable AV-Skillset skills.

Minimum expected sequence for feature work:

1. `using-superpowers`
2. `aerovista-operating-mode`
3. `aerovista-system-mapping`
4. `brainstorming`
5. `writing-plans`
6. `using-git-worktrees`, when repository conditions allow
7. `test-driven-development`
8. `aerovista-deployment-safety`
9. `aerovista-verification`
10. `verification-before-completion`
11. `aerovista-operational-review`, for production-impacting work

The agent must not merely mention the skills.

It must follow their required workflow and produce the corresponding evidence.

---

## 17.3 Cursor Rule: Operating State Language

Cursor must use the following status vocabulary precisely:

- Proposed
- Planned
- Implementing
- Implemented
- Tested
- Packaged
- Deployed
- Configured
- Enabled
- Verified
- Operationally accepted
- Rolled back
- Retired

Forbidden vague completion phrases include:

- Done
- Finished
- All set
- Production ready

unless the specific state and verification evidence are also provided.

---

## 17.4 Cursor Rule: No Unapproved Architecture Drift

Cursor must not:

- Initialize Git in a non-Git production directory without approval
- Replace existing deployment topology without a migration plan
- Introduce a new database when an existing canonical service owns the data
- Duplicate existing EchoVerse, AVCC, or Art Localized functionality
- Add a new framework without documenting the reason
- Change exposed ports without updating architecture and runbooks
- Hard-code NXCore addresses where configuration is appropriate
- silently modify production configuration
- place secrets in source control
- claim deployment from local tests
- remove compatibility paths without a rollback plan

---

## 17.5 Cursor Rule: Contract-First Development

Before implementing a service or adapter:

1. Define the contract.
2. Add schemas.
3. Add contract tests.
4. Define failure responses.
5. Define authorization requirements.
6. Define observability.
7. Implement the smallest compliant behavior.
8. Verify integration.
9. Update documentation.

Shared contracts belong in:

```text
packages/contracts/
```

Services should import canonical contracts rather than redefining them.

---

## 17.6 Cursor Rule: Repository Preflight

Before editing:

```text
1. Read AGENTS.md.
2. Read relevant Cursor rules.
3. Identify repository root.
4. Check Git status.
5. Identify deployment environment.
6. Find existing tests.
7. Find existing contracts.
8. Search for existing implementations.
9. Identify service ownership.
10. State the planned change boundary.
```

---

## 17.7 Cursor Rule: Controlled Change Output

Every significant Cursor implementation report should include:

```text
Mode:
Scope:
Repositories changed:
Services changed:
Contracts changed:
Configuration changed:
Tests executed:
Builds executed:
Deployment performed:
Verification performed:
Rollback path:
Known limitations:
Next safe action:
```

---

## 17.8 Cursor Rule: Completion Evidence

A feature is not considered verified until Cursor provides evidence such as:

- Test output
- Build output
- Health endpoint output
- API response
- UI route verification
- Screenshot where visually necessary
- Worker job result
- Database record
- Log correlation
- Deployment manifest
- Rollback verification

---

# 18. API Contract Baseline

Initial endpoints:

```text
GET /api/health
GET /api/workspace/me

GET /api/divisions
GET /api/divisions/:divisionId

GET /api/projects
POST /api/projects
GET /api/projects/:projectId
PATCH /api/projects/:projectId

GET /api/projects/:projectId/assets
POST /api/projects/:projectId/assets
GET /api/assets/:assetId
POST /api/assets/:assetId/versions

GET /api/capabilities
GET /api/tools
POST /api/tools/:toolId/launch-request

GET /api/jobs
POST /api/jobs
GET /api/jobs/:jobId
POST /api/jobs/:jobId/cancel
POST /api/jobs/:jobId/retry

GET /api/workflows/:workflowId
POST /api/projects/:projectId/transitions

GET /api/activity
GET /api/notifications
POST /api/notifications/:notificationId/read
```

Desktop bridge:

```text
GET /desktop/capabilities
POST /desktop/tools/:toolId/launch
POST /desktop/projects/:projectId/checkout
POST /desktop/projects/:projectId/sync
POST /desktop/assets/:assetId/open
POST /desktop/verify
```

---

# 19. Workflow Model

Each project type uses a versioned workflow definition.

Example creative workflow:

```text
intake
→ planning
→ production
→ internal_review
→ client_review
→ approved
→ publishing
→ delivered
→ archived
```

Example software workflow:

```text
intake
→ mapped
→ planned
→ implementing
→ tested
→ staged
→ deployed
→ verified
→ operational
```

Transitions should support:

- Required permissions
- Required fields
- Required approvals
- Automated jobs
- Notifications
- Webhooks or internal events
- Rollback transition
- Audit record

---

# 20. Operational Controls

## 20.1 Feature Flags

Feature flags should control:

- Division activation
- Experimental tools
- New adapters
- Desktop bridge functions
- Publishing integrations
- AI providers
- Beta workflows

Flags must be environment-aware and auditable.

---

## 20.2 Release Channels

Use:

- Development
- Internal
- Pilot
- Stable

Portable capability packs and desktop applications should support channels independently.

---

## 20.3 Health States

Each service, adapter, and tool should report:

- Healthy
- Degraded
- Unavailable
- Misconfigured
- Update required
- Unsupported on device
- Permission denied

---

## 20.4 Backup Requirements

Back up:

- PostgreSQL
- Division registry
- Project registry
- Capability registry
- Workflow definitions
- Audit data
- Critical project assets
- Capability package manifests
- Deployment configuration

Verify restores, not just backup creation.

---

# 21. Phased Build Plan

## Phase 0 — Architecture Lock and Repository Preflight

### Objective

Establish the canonical roster, repository, contracts, rules, deployment boundaries, and decision record before implementation begins.

### Tasks

- [ ] Confirm official launch division roster
- [ ] Decide whether Frontier launches now or remains registry-disabled
- [ ] Confirm canonical product name
- [ ] Confirm monorepo location
- [ ] Confirm production compose root
- [ ] Inventory existing AeroCore, AVCC, EchoVerse, and Art Localized services
- [ ] Identify reusable authentication
- [ ] Identify reusable file and job services
- [ ] Create system context diagram
- [ ] Create deployment topology diagram
- [ ] Create repository ownership map
- [ ] Create port and hostname registry
- [ ] Create ADR directory
- [ ] Add AGENTS.md from AV-Skillset
- [ ] Add Cursor rules
- [ ] Create environment matrix
- [ ] Define implementation, deployment, and verification states
- [ ] Record out-of-scope items

### Exit Gate

- Architecture decisions are recorded.
- No unresolved ownership conflict exists for foundation services.
- Cursor preflight rules are active.
- The first implementation slice has a defined contract and rollback boundary.

---

## Phase 1 — Workspace Foundation

### Objective

Create the functional AeroVista shell, authentication boundary, division registry, and basic permission-controlled navigation.

### Deliverables

- Workspace web application
- AeroVista Main shell
- Division switcher
- User session
- Division registry
- Role-based navigation
- Initial design system
- Health endpoint
- Development environment
- CI validation

### Tasks

- [ ] Scaffold monorepo
- [ ] Configure TypeScript
- [ ] Configure package workspace
- [ ] Add linting and formatting
- [ ] Add test framework
- [ ] Add shared contracts package
- [ ] Add shared UI package
- [ ] Implement workspace shell
- [ ] Implement authentication adapter
- [ ] Implement `/api/workspace/me`
- [ ] Implement division registry schema
- [ ] Load division registry configuration
- [ ] Implement division navigation
- [ ] Implement permission middleware
- [ ] Add unauthorized-state UI
- [ ] Add health and version display
- [ ] Add OpenTelemetry foundation
- [ ] Add structured logging
- [ ] Add CI contract, test, and build checks

### Exit Gate

An authenticated user can enter AeroVista Main and see only authorized divisions.

---

## Phase 2 — Project Registry and Workbench

### Objective

Make the platform useful for real project work.

### Deliverables

- Project creation
- Project registry
- Project dashboard
- Team assignments
- Workflow state
- Recent activity
- Project templates

### Tasks

- [ ] Define project contract
- [ ] Define project membership rules
- [ ] Implement project database
- [ ] Implement project API
- [ ] Implement project list
- [ ] Implement project creation
- [ ] Implement project workbench
- [ ] Add division-specific project templates
- [ ] Add project roles
- [ ] Add activity records
- [ ] Add project search
- [ ] Add project archive state
- [ ] Add project export manifest
- [ ] Add contract tests
- [ ] Add permission tests

### Exit Gate

An authorized user can create, open, update, and manage a division project with a stable project identity.

---

## Phase 3 — Files and Asset Foundation

### Objective

Connect projects to actual working files and generated assets.

### Deliverables

- Asset registry
- Upload
- Download
- Preview
- Version records
- Project folder mapping
- Basic local checkout design

### Tasks

- [ ] Define asset contract
- [ ] Define storage adapter contract
- [ ] Implement storage abstraction
- [ ] Implement shared-storage adapter
- [ ] Implement object-storage adapter if needed
- [ ] Implement upload API
- [ ] Implement download API
- [ ] Implement asset browser
- [ ] Add previews for common formats
- [ ] Add checksum creation
- [ ] Add asset versioning
- [ ] Add soft deletion
- [ ] Add quarantine state
- [ ] Add source-output relationships
- [ ] Add storage reconciliation command
- [ ] Add backup coverage

### Exit Gate

Project files can be safely uploaded, viewed, versioned, retrieved, and audited.

---

## Phase 4 — Capability Registry and Tool Dock

### Objective

Make tools discoverable and interchangeable through shared capability contracts.

### Deliverables

- Capability registry
- Tool registry
- Tool Dock
- Device compatibility reporting
- Initial browser tool adapters
- Initial backend tool adapters

### Tasks

- [ ] Define capability schema
- [ ] Define tool registration schema
- [ ] Define adapter contract
- [ ] Implement capability registry service
- [ ] Implement tool registry service
- [ ] Implement Tool Dock UI
- [ ] Add capability filtering by division
- [ ] Add capability filtering by project type
- [ ] Add permission filtering
- [ ] Add platform compatibility
- [ ] Add tool health state
- [ ] Add installation-required state
- [ ] Add launch request audit
- [ ] Implement first five adapters
- [ ] Create adapter development template
- [ ] Add adapter contract test suite

### Initial Adapter Targets

- [ ] Excalidraw
- [ ] Penpot
- [ ] Photopea or equivalent browser editor
- [ ] EchoVerse
- [ ] AVCC
- [ ] Art Localized
- [ ] Internal file preview
- [ ] Backend FFmpeg worker

### Exit Gate

A project presents the correct tools based on division, file type, device, role, and availability.

---

## Phase 5 — Job Orchestrator and Worker Platform

### Objective

Provide dependable asynchronous processing with visible progress and recoverable outputs.

### Deliverables

- Job API
- Queue
- Worker registration
- Job Center
- Progress events
- Retry and cancellation
- Output asset registration

### Tasks

- [ ] Define job contract
- [ ] Select initial queue technology
- [ ] Implement job database
- [ ] Implement queue producer
- [ ] Implement worker consumer
- [ ] Implement progress updates
- [ ] Implement Job Center
- [ ] Implement retry policy
- [ ] Implement cancellation where supported
- [ ] Implement dead-letter handling
- [ ] Implement worker heartbeats
- [ ] Add job logs
- [ ] Add input and output relationships
- [ ] Register outputs as assets
- [ ] Add resource limits
- [ ] Add worker pool routing
- [ ] Add failure notifications
- [ ] Add job audit events

### Initial Worker Jobs

- [ ] Image resize
- [ ] Image conversion
- [ ] Image slicing
- [ ] Thumbnail generation
- [ ] Video transcode
- [ ] Audio transcode
- [ ] Document conversion
- [ ] Archive inspection

### Exit Gate

A user can submit a long-running job, observe its progress, and receive a registered output asset.

---

## Phase 6 — Tauri Desktop Bridge

### Objective

Connect the secure workspace to local files and desktop applications.

### Deliverables

- Tauri shell
- Device registration
- Local capability discovery
- Secure tool launching
- Local project checkout
- Sync foundation
- Deep links

### Tasks

- [ ] Scaffold Tauri application
- [ ] Wrap authenticated workspace
- [ ] Define desktop command allowlist
- [ ] Implement device registration
- [ ] Implement secure token storage
- [ ] Implement capability discovery
- [ ] Implement local tool verification
- [ ] Implement approved tool launch
- [ ] Implement open folder
- [ ] Implement reveal asset
- [ ] Implement file handoff
- [ ] Implement project checkout
- [ ] Implement explicit project sync
- [ ] Add local logs
- [ ] Add desktop health screen
- [ ] Add deep-link handling
- [ ] Add signed update design
- [ ] Perform desktop security review

### Exit Gate

An authorized desktop user can open a project asset in an approved local application without exposing arbitrary operating-system execution.

---

## Phase 7 — Portable Application Packages

### Objective

Deliver a repeatable AeroVista workstation kit.

### Deliverables

- Capability package format
- Package manager
- Image foundation pack
- Video foundation pack
- Audio foundation pack
- Publishing pack
- Development pack

### Tasks

- [ ] Finalize package manifest
- [ ] Create checksum format
- [ ] Create package signing plan
- [ ] Implement package install
- [ ] Implement package verify
- [ ] Implement package repair
- [ ] Implement package upgrade
- [ ] Implement rollback
- [ ] Implement package removal
- [ ] Build shared foundation pack
- [ ] Build Lumina pack
- [ ] Build EchoVerse pack
- [ ] Build Nexus pack
- [ ] Build Vespera pack
- [ ] Build Summit pack
- [ ] Build Horizon pack
- [ ] Build SkyForge pack
- [ ] Add license inventory
- [ ] Add portable data-location rules
- [ ] Add workstation bootstrap command

### Exit Gate

A clean Windows workstation can receive an approved capability pack and pass automated tool verification.

---

## Phase 8 — Division Workspace Rollout

### Objective

Transform the generic foundation into real division work environments.

Recommended sequence:

1. Lumina
2. Nexus
3. EchoVerse
4. Vespera
5. Summit
6. Horizon
7. SkyForge
8. Frontier when enabled

### Per-Division Checklist

- [ ] Confirm project types
- [ ] Confirm roles
- [ ] Confirm workflow stages
- [ ] Confirm capability sets
- [ ] Confirm browser tools
- [ ] Confirm portable tools
- [ ] Confirm backend jobs
- [ ] Confirm templates
- [ ] Confirm storage rules
- [ ] Confirm publishing targets
- [ ] Confirm audit requirements
- [ ] Build division landing page
- [ ] Build project template
- [ ] Build division capability pack
- [ ] Test with real project
- [ ] Record operator feedback
- [ ] Complete operational acceptance

### Exit Gate

Each launched division can complete one representative project from intake to delivery.

---

## Phase 9 — Workflow Automation and Agents

### Objective

Add controlled AI and automation without bypassing human ownership.

### Deliverables

- Agent registry
- Project-aware agent context
- Workflow actions
- Approval gates
- Agent activity history
- Automation templates

### Tasks

- [ ] Define agent contract
- [ ] Define allowed agent actions
- [ ] Implement agent gateway
- [ ] Implement project context assembly
- [ ] Add agent permission checks
- [ ] Add human approval gates
- [ ] Add agent audit events
- [ ] Add prompt and tool version records
- [ ] Add execution cost records
- [ ] Add agent result attachments
- [ ] Add division agent profiles
- [ ] Add automation templates
- [ ] Add safe failure handling
- [ ] Add manual override
- [ ] Add agent evaluation suite

### Agent Categories

- Workspace assistant
- Project planner
- Asset librarian
- Metadata assistant
- Publishing assistant
- Compliance checker
- Development agent
- Media processing assistant
- Training content assistant
- Executive summary agent

### Exit Gate

Agents can assist within a project while every action remains permission-controlled, attributable, and reviewable.

---

## Phase 10 — Operational Hardening

### Objective

Prepare the platform for dependable daily use.

### Tasks

- [ ] Threat model
- [ ] Desktop bridge penetration review
- [ ] Permission matrix review
- [ ] Backup restore drill
- [ ] Worker failure drill
- [ ] Queue recovery drill
- [ ] Storage reconciliation drill
- [ ] Service restart test
- [ ] Network interruption test
- [ ] Offline PWA test
- [ ] Desktop update rollback test
- [ ] Capability package rollback test
- [ ] Audit export verification
- [ ] Load test
- [ ] Large-file test
- [ ] Browser compatibility test
- [ ] Tablet usability test
- [ ] Logging review
- [ ] Alert thresholds
- [ ] Runbook completion
- [ ] Operator training
- [ ] Pilot support process

### Exit Gate

The platform passes recovery, security, permission, backup, deployment, and operational verification gates.

---

## Phase 11 — Pilot and Production Rollout

### Pilot Group

Start with a small internal group representing:

- AeroVista Main
- Lumina
- Nexus
- EchoVerse

### Tasks

- [ ] Define pilot users
- [ ] Provision roles
- [ ] Register devices
- [ ] Deploy PWA
- [ ] Deploy desktop client
- [ ] Install capability packs
- [ ] Import representative projects
- [ ] Observe real workflows
- [ ] Record missing capabilities
- [ ] Record friction points
- [ ] Fix critical issues
- [ ] Complete production readiness review
- [ ] Promote stable release
- [ ] Begin remaining division rollout

### Exit Gate

Pilot users complete real work without falling back to undocumented manual processes.

---

# 22. Consolidated Master To-Do List

## Architecture and Governance

- [ ] Lock canonical division roster
- [ ] Lock platform naming
- [ ] Approve monorepo structure
- [ ] Create ADRs
- [ ] Create service ownership map
- [ ] Create environment matrix
- [ ] Create port and hostname registry
- [ ] Establish release state vocabulary
- [ ] Establish architecture review process

## Cursor and AV-Skillset

- [ ] Add root AGENTS.md
- [ ] Link repository workflow to AV-Skillset
- [ ] Add Cursor rules
- [ ] Add Cursor commands
- [ ] Add preflight checklist
- [ ] Add controlled-change report template
- [ ] Add verification report template
- [ ] Add adapter implementation template
- [ ] Add capability-pack template

## Shared Contracts

- [ ] Organization schema
- [ ] Division schema
- [ ] User and role schema
- [ ] Project schema
- [ ] Asset schema
- [ ] Capability schema
- [ ] Tool schema
- [ ] Adapter schema
- [ ] Job schema
- [ ] Workflow schema
- [ ] Event schema
- [ ] Audit schema
- [ ] Error schema

## Core Services

- [ ] Workspace API
- [ ] Identity and policy integration
- [ ] Division Registry
- [ ] Project Registry
- [ ] Asset Service
- [ ] Capability Registry
- [ ] Tool Registry
- [ ] Job Orchestrator
- [ ] Worker Registry
- [ ] Event Service
- [ ] Audit Service
- [ ] Notification Service
- [ ] Search Service

## Web Workspace

- [ ] Main shell
- [ ] Division switcher
- [ ] Project switcher
- [ ] Project Workbench
- [ ] File browser
- [ ] Tool Dock
- [ ] Workflow board
- [ ] Job Center
- [ ] Agent panel
- [ ] Activity timeline
- [ ] Notifications
- [ ] Admin pages
- [ ] Offline shell
- [ ] Tablet layout

## Desktop

- [ ] Tauri shell
- [ ] Device registration
- [ ] Secure credential storage
- [ ] Capability discovery
- [ ] Tool launch
- [ ] File handoff
- [ ] Project checkout
- [ ] Project sync
- [ ] Deep links
- [ ] Update mechanism
- [ ] Repair and diagnostics
- [ ] Electron fallback decision gate

## Portable Applications

- [ ] Package standard
- [ ] Package signing
- [ ] Package manager
- [ ] Shared pack
- [ ] Image pack
- [ ] Video pack
- [ ] Audio pack
- [ ] Publishing pack
- [ ] Development pack
- [ ] Field pack
- [ ] License records
- [ ] Checksums
- [ ] Repair workflows
- [ ] Rollback workflows

## Workers

- [ ] Image worker
- [ ] Video worker
- [ ] Audio worker
- [ ] Document worker
- [ ] Build worker
- [ ] AI worker
- [ ] Worker health
- [ ] Resource limits
- [ ] Retry policy
- [ ] Dead-letter handling
- [ ] Output registration

## Security and Operations

- [ ] Authorization matrix
- [ ] Desktop command allowlist
- [ ] Secret management
- [ ] Audit retention
- [ ] Backup policy
- [ ] Restore drills
- [ ] Monitoring
- [ ] Alerting
- [ ] Central logs
- [ ] Correlation IDs
- [ ] Deployment runbooks
- [ ] Rollback runbooks
- [ ] Incident response
- [ ] Package vulnerability review

---

# 23. Recommended First Vertical Slice

The first build should not attempt every division or every tool.

Build one complete vertical slice using Lumina.

## Vertical Slice

```text
User signs in
→ sees AeroVista Main
→ enters Lumina
→ creates a campaign project
→ uploads an image
→ opens the asset in a browser editor
→ submits an image resize job
→ receives output
→ opens output locally through Tauri
→ marks asset approved
→ exports a delivery package
→ audit history records the process
```

This slice validates:

- Identity
- Permissions
- Division composition
- Projects
- Assets
- Capabilities
- Browser tools
- Workers
- Desktop bridge
- Workflow state
- Delivery
- Audit

Once this succeeds, other divisions become configuration and capability expansion rather than speculative architecture work.

---

# 24. Initial Build Tickets for Cursor

## Epic AVW-001 — Repository Foundation

- AVW-001-01 Create monorepo
- AVW-001-02 Add AGENTS.md and AV-Skillset references
- AVW-001-03 Add Cursor rules
- AVW-001-04 Add shared TypeScript configuration
- AVW-001-05 Add CI pipeline
- AVW-001-06 Add architecture documentation structure
- AVW-001-07 Add environment validation script

## Epic AVW-002 — Shared Contracts

- AVW-002-01 Organization and division schemas
- AVW-002-02 Project schema
- AVW-002-03 Asset schema
- AVW-002-04 Capability and tool schemas
- AVW-002-05 Job schema
- AVW-002-06 Event and audit schemas
- AVW-002-07 Shared error contract
- AVW-002-08 Contract test harness

## Epic AVW-003 — Workspace Shell

- AVW-003-01 Main layout
- AVW-003-02 Authentication boundary
- AVW-003-03 Division switcher
- AVW-003-04 Permission-aware navigation
- AVW-003-05 Command palette
- AVW-003-06 Health and connection state
- AVW-003-07 Tablet-responsive shell

## Epic AVW-004 — Lumina Vertical Slice

- AVW-004-01 Lumina registry configuration
- AVW-004-02 Campaign project template
- AVW-004-03 Project Workbench
- AVW-004-04 Asset upload and preview
- AVW-004-05 Browser editor adapter
- AVW-004-06 Image resize worker
- AVW-004-07 Job Center
- AVW-004-08 Approval transition
- AVW-004-09 Delivery export
- AVW-004-10 End-to-end verification

## Epic AVW-005 — Desktop Bridge

- AVW-005-01 Tauri bootstrap
- AVW-005-02 Device registration
- AVW-005-03 Capability discovery
- AVW-005-04 Secure local launch
- AVW-005-05 Project checkout
- AVW-005-06 Asset handoff
- AVW-005-07 Sync prototype
- AVW-005-08 Security review

---

# 25. Definition of Done

A work item is complete only when all applicable conditions are met:

- Contract exists
- Authorization is defined
- Implementation exists
- Unit tests pass
- Contract tests pass
- Integration tests pass
- Build passes
- Logs are structured
- Health reporting exists
- Error behavior is defined
- Documentation is updated
- Deployment state is identified
- Verification evidence is captured
- Rollback path is documented
- Known limitations are recorded
- AV-Skillset completion requirements are satisfied

---

# 26. Explicit Non-Goals for Initial Release

Do not include in the initial foundation unless required by the vertical slice:

- Full cloud-drive replacement
- Real-time collaborative editing for every file type
- Kubernetes migration
- Custom replacements for GIMP, Blender, Audacity, or other mature editors
- Fully autonomous agents
- Arbitrary local command execution
- Full mobile parity with desktop
- Every division workflow
- Every portable application
- Public marketplace for capability packages
- Cross-company multi-tenancy
- Complex billing
- Plugin execution from untrusted third parties

---

# 27. Key Architecture Decisions

## Decision 1

AeroCore OS is the service and orchestration layer, not a custom desktop operating system.

## Decision 2

The PWA is the universal client.

## Decision 3

Tauri is the preferred desktop bridge.

## Decision 4

Electron remains an exception path.

## Decision 5

Portable tools are distributed through versioned capability packages.

## Decision 6

Capabilities are canonical; individual applications are interchangeable providers.

## Decision 7

Projects, assets, jobs, workflows, and divisions use shared contracts.

## Decision 8

Division access is registry- and policy-driven.

## Decision 9

Long-running processing runs through visible jobs and workers.

## Decision 10

Existing AeroVista systems are integrated, not silently rebuilt.

## Decision 11

AV-Skillset governs agent behavior and engineering process.

## Decision 12

The first implementation is a complete Lumina vertical slice.

---

# 28. Immediate Next Execution Order

1. Create the AeroVista Workspace repository.
2. Install the root AGENTS.md from AV-Skillset.
3. Add the Cursor rules described in this blueprint.
4. Create the architecture decision records.
5. Inventory existing reusable AeroCore services.
6. Lock the division registry launch roster.
7. Build the shared contracts package.
8. Scaffold the workspace shell and API.
9. Implement identity and division composition.
10. Build the Lumina vertical slice.
11. Add the first image worker.
12. Add the Tauri desktop bridge.
13. Create the first portable image capability pack.
14. Run operational verification.
15. Roll the proven pattern into the remaining divisions.

---

# 29. Final Target State

The completed system should allow AeroVista to deploy a dependable workspace to nearly any supported machine through one of four paths:

```text
Browser
PWA installation
Tauri desktop installation
Portable workstation bundle
```

Every path connects to the same:

- User identity
- Division permissions
- Project records
- Asset identities
- Workflow states
- Tool capabilities
- Backend jobs
- Audit history
- AeroCore services

The result is one operating environment with multiple execution surfaces—not a loose collection of applications pretending to be a platform.
:::

The strongest move is to make this the repository’s canonical `MASTER_ARCHITECTURE_BLUEPRINT.md`, then derive a smaller `IMPLEMENTATION_ROADMAP.md`, Cursor rule files, ADRs, and ticket-ready phase plans from it.

## USER
Consider AVCC can become the commercial and operational core of AeroCore OS.

The best fit is not to turn AVCC into every division’s editor. Instead:

AeroCore OS manages identity, permissions, assets, tools, devices, jobs, handoffs, and shared infrastructure.

AVCC manages contacts, customers, projects, tasks, work records, costs, quotes, invoices, payments, profitability, and executive visibility.

Division workspaces perform the specialized work and report structured activity back to AVCC.


AVCC as the Business Core of AeroCore OS

1. Final platform relationship

 AEROCORE OS
 Identity · Permissions · Devices · Platform APIs
 │
 ┌───────────────────────┼────────────────────────┐
 │ │ │
 ▼ ▼ ▼
 AVCC Division Workspaces Shared Services
Business operations Specialized production Assets, jobs, tools,
and billing and delivery handoffs, notifications
 │ │ │
 └───────────────────────┴────────────────────────┘
 │
 ▼
 WORK LEDGER
 │
 Time · Deliverables · Costs · Usage
 │
 ▼
 Quotes · Invoices · Payments

AVCC becomes the place where AeroVista answers:

- Who is the client?
- What did they request?
- What did AeroVista agree to deliver?
- Which division owns the work?
- Who performed it?
- How much time and infrastructure did it consume?
- What is billable?
- What has been approved?
- What should appear on the invoice?
- Has the invoice been paid?
- Was the project profitable?

---

2. What AVCC should own

AVCC should become the canonical source for the commercial and operational side of AeroVista.

Customer and relationship management

- Organizations
- Contacts
- Leads
- Prospects
- Clients
- Vendors
- Contractors
- Partners
- Communication history
- Relationship owners
- Client portals
- Contact permissions

Sales and engagement records

- Opportunities
- Service inquiries
- Estimates
- Quotes
- Statements of work
- Contracts
- Retainers
- Purchase orders
- Service packages
- Accepted terms

Project operations

- Projects
- Project owners
- Participating divisions
- Work orders
- Tasks
- Milestones
- Deadlines
- Dependencies
- Assigned staff
- Project status
- Client status
- Internal notes
- Risks and blockers

Financial operations

- Rate cards
- Fixed-price services
- Hourly rates
- Retainers
- Expenses
- Materials
- External costs
- Infrastructure usage
- Discounts
- Taxes
- Credits
- Invoice drafts
- Approved invoices
- Payment status
- Profitability

Executive and compliance records

- Release readiness
- Project health
- Delivery evidence
- Audit history
- Approval history
- Division performance
- Revenue by service and division
- Unbilled work
- Overdue invoices
- Scope changes
- Write-offs

---

3. What AVCC should not own

AVCC should reference these systems, but it should not become their primary storage or editing environment:

- Layered image files
- Audio masters
- Raw drone footage
- Game-engine projects
- Source-code repositories
- Large media proxies
- Manuscript working files
- Photogrammetry datasets
- Application build artifacts
- Detailed audio-analysis data
- Tool-specific project formats

Those remain in:

- AeroCore Vault
- Git repositories
- EchoVerse Catalog
- Horizon media storage
- Publishing systems
- Game repositories
- Specialized division services

AVCC stores the business reference:

{
 "deliverable_id": "del_campaign_hero",
 "asset_id": "ast_campaign_hero",
 "approved_version_id": "av_campaign_hero_004",
 "status": "client_approved",
 "billing_status": "ready_to_invoice"
}

It does not need to store the actual 2 GB layered source file.

---

4. The connected business lifecycle

The complete lifecycle should become:

Contact
→ Opportunity
→ Quote
→ Engagement
→ Project
→ Work Order
→ Tasks
→ Production activity
→ Deliverables
→ Approval
→ Billing entries
→ Invoice
→ Payment
→ Project closeout

Contact

A person or organization enters AVCC.

Examples:

- Local business
- Artist
- Real-estate agent
- Construction company
- Author
- Training client
- Internal AeroVista division

Opportunity

AVCC records what they may purchase.

Examples:

- Brand package
- Aerial photo session
- Website build
- Audio production
- Training course
- Book production
- Game prototype

Quote

The opportunity becomes a priced offer.

The quote contains:

- Service items
- Deliverables
- Assumptions
- Exclusions
- Schedule
- Billing method
- Deposit requirements
- Revision limits
- Usage rights

Engagement

When accepted, AVCC creates an engagement or contract record.

The engagement establishes:

- Customer
- Billing terms
- Rate card
- Contract dates
- Responsible division
- Payment schedule
- Approved services

Project

The engagement creates one or more AeroCore projects.

AVCC engagement ID: eng_...
AeroCore project ID: prj_...

Both systems retain the relationship.

Work Order

A work order defines a specific bounded assignment inside the project.

Examples:

- Capture 30 aerial property images
- Produce three social-media videos
- Design one landing page
- Mix and master five tracks
- Create six training modules

Tasks

Tasks break the work order into assignable activities.

Each task must include:

- Division
- Owner
- Billing classification
- Estimated effort
- Deliverable
- Completion criteria
- Due date
- Client-visible or internal status

Production activity

Division workspaces perform the work.

AeroCore sends structured events to AVCC as activity occurs.

Deliverable approval

A specific deliverable version is approved internally or by the client.

That approval can trigger:

- Milestone completion
- Invoice eligibility
- Revenue recognition
- Final delivery
- Project closeout

---

5. The three-ledger model

AVCC should not turn every click or saved file into an invoice line.

Use three related ledgers.

Activity Ledger

Captures what happened.

Examples:

- User launched Krita
- Horizon uploaded 42 images
- FFmpeg completed a render
- Lumina submitted a layout
- Client approved version 4
- Nexus deployed a service

Activity events are detailed and auditable, but usually not directly billable.

Work Ledger

Converts meaningful activity into accountable work records.

Examples:

- 2.5 hours of Lumina design
- One Horizon field-capture session
- Three video renders
- One client revision cycle
- One website deployment
- 50 GB of project storage
- One photogrammetry processing job

Work records may be:

- Billable
- Included in fixed price
- Internal
- Warranty
- Rework
- Non-billable
- Written off

Billing Ledger

Contains only approved invoice candidates.

Examples:

Lumina brand package $1,500
Horizon aerial capture session $450
Additional revision — 1.5 hours $180
Video processing and delivery $75
Hosting and maintenance — July $95

An invoice should be built only from approved billing-ledger entries.

---

6. Billing classifications

Every work order, task, time entry, job, and deliverable should have a billing classification.

hourly
fixed_fee
milestone
retainer_included
retainer_overage
usage_based
pass_through_expense
internal
warranty
rework_non_billable
complimentary
written_off

This prevents AeroCore from assuming that all recorded activity should be charged.

Example

A Lumina designer works three hours on a fixed-price brand package.

AVCC records:

Actual labor: 3.0 hours
Internal cost: $120
Client billing: Included in fixed $1,500 package
Invoice addition: $0 hourly line
Profit analysis: Labor cost still counted

That distinction is crucial.

---

7. Service catalog

AVCC needs a company-wide service and product catalog.

Each service should have:

- Service ID
- Public name
- Internal name
- Owning division
- Supporting divisions
- Description
- Standard deliverables
- Default pricing model
- Default rate
- Expected effort
- Required tools
- Standard handoff route
- Revision allowance
- Tax category
- Revenue account
- Active or retired status

Example services

LUM-BRAND-STARTER
Lumina Brand Starter Package
Fixed fee: $1,500

HOR-AERIAL-REALESTATE
Horizon Real Estate Aerial Session
Fixed fee: $450

NEX-WEB-MAINT
Nexus Website Maintenance
Recurring: $95/month

ECH-MASTER-SINGLE
EchoVerse Single-Track Mastering
Fixed fee: $150

VES-EDITORIAL-10K
Vespera Developmental Edit — up to 10,000 words
Fixed fee or per-word

SUM-CUSTOM-MODULE
Summit Custom Training Module
Milestone billing

SKY-PROTOTYPE
SkyForge Interactive Prototype
Milestone billing

A quote selects services from this catalog. Accepted services create work-order templates automatically.

---

8. Division workspaces feeding AVCC

Each workspace should report business-relevant events through an AVCC Operations Adapter.

Lumina examples

lumina.brief.approved
lumina.concept.approved
lumina.revision.requested
lumina.deliverable.submitted
lumina.deliverable.approved

Horizon examples

horizon.mission.scheduled
horizon.flight.completed
horizon.capture.ingested
horizon.reshoot.required
horizon.delivery.approved

EchoVerse examples

echoverse.recording.completed
echoverse.mix.submitted
echoverse.master.approved
echoverse.track.released

Nexus examples

nexus.build.completed
nexus.deployment.completed
nexus.support.started
nexus.incident.resolved

Summit examples

summit.module.completed
summit.assessment.approved
summit.course.published
summit.learner.certified

Vespera examples

vespera.draft.submitted
vespera.edit.completed
vespera.proof.approved
vespera.edition.published

SkyForge examples

skyforge.prototype.completed
skyforge.playtest.completed
skyforge.build.promoted
skyforge.release.approved

AVCC translates selected events into milestone, work, or billing records.

---

9. Tool sessions and time tracking

AeroCore LaunchPad can help track real work without spying on employees.

When a user opens a tool for an assigned task:

Task selected
→ Tool session begins
→ User works
→ Session pauses or ends
→ User confirms time classification
→ AVCC receives work entry

The platform should not blindly bill application-open time.

A session may contain:

- Active time
- Paused time
- User-confirmed billable time
- Internal time
- Notes
- Output references

Example:

{
 "task_id": "tsk_lumina_hero",
 "tool_session_id": "tls_krita_123",
 "elapsed_minutes": 104,
 "submitted_minutes": 90,
 "billing_classification": "fixed_fee",
 "notes": "Hero image layout and first revision",
 "outputs": ["av_campaign_hero_004"]
}

This gives AVCC cost visibility without creating unreliable automatic billing.

---

10. Backend-worker billing

NXCore processing can also create cost records.

Examples:

- Video-render minutes
- GPU image generation
- Whisper transcription duration
- Photogrammetry processing
- Storage usage
- Large delivery packages
- External AI API calls
- External map or data services

Each worker result can include:

{
 "job_id": "job_...",
 "project_id": "prj_...",
 "cpu_seconds": 840,
 "gpu_seconds": 320,
 "memory_peak_mb": 6144,
 "storage_output_bytes": 4382882011,
 "external_cost_usd": 1.42,
 "billing_code": "MEDIA_RENDER",
 "billing_classification": "included"
}

AVCC records:

- Actual platform cost
- Client charge where applicable
- Whether included in a package
- Project margin impact

This creates real profitability data.

---

11. Invoice generation

An invoice should be generated through a controlled process:

Completed work and milestones
→ Work Ledger
→ Billing review
→ Invoice candidates
→ Draft invoice
→ Project owner review
→ Financial approval
→ Invoice issued
→ Payment recorded

Invoice sources

An invoice may contain:

- Fixed-fee services
- Completed milestones
- Approved hourly work
- Retainer overages
- Reimbursable expenses
- Materials
- Usage charges
- Recurring hosting or support
- Credits
- Discounts
- Taxes

Required protections

- No duplicate billing of the same ledger entry
- Every invoice line links to its source
- Changes after issue create credit or adjustment records
- Issued invoices are immutable
- Void and replacement are auditable
- Internal costs remain separate from client charges

---

12. Retainers and recurring services

AVCC should support recurring relationships from the start.

Examples:

- Monthly content production
- Website maintenance
- Audio hosting
- Catalog management
- Training-platform access
- Ongoing drone progress capture
- Technical support
- Brand-management retainers

A retainer should track:

Monthly included hours
Included deliverables
Included infrastructure usage
Overage rate
Rollover policy
Renewal date
Cancellation terms

Tasks and work entries consume the retainer allowance before generating overage billing.

---

13. Scope-change controls

One of AVCC’s most valuable roles should be preventing invisible scope creep.

When a request falls outside the approved work order:

New client request
→ Task flagged as out of scope
→ Change request created
→ Cost and schedule impact calculated
→ Client approves or declines
→ Work order updated
→ Work becomes billable

The division workspace should show:

This request exceeds the approved revision allowance.

[ Create change request ]
[ Mark complimentary ]
[ Return to project owner ]

A specialist should not have to negotiate billing directly with the client.

---

14. Internal AeroVista work

Not every AeroCore project has an external customer.

AVCC should support internal project accounts:

AeroVista Corporate
Lumina Internal
Nexus Internal
EchoVerse Internal
SkyForge Internal
Summit Internal
Vespera Internal
Horizon Internal

Internal projects still record:

- Labor
- Worker usage
- Asset production
- Division contributions
- Opportunity cost
- Strategic value
- Completion evidence

They produce no external invoice, but they help reveal where AeroVista’s time and infrastructure are going.

---

15. Contacts and access relationships

AVCC contacts should connect to AeroCore identities where appropriate.

AVCC Contact
 │
 ├── No AeroCore account
 ├── Client portal identity
 ├── Contractor identity
 ├── Employee identity
 └── Partner identity

A contact record may exist without login access.

When portal access is granted:

- AVCC remains the relationship record.
- AeroCore Identity creates the account.
- The project grants scoped access.
- AVCC records portal status and expiration.

Do not make contact records and user identities the same database object.

---

16. Recommended shared IDs

AVCC and AeroCore should share immutable cross-system IDs.

Account: acc_...
Contact: con_...
Opportunity: opp_...
Quote: quo_...
Engagement: eng_...
Project: prj_...
Work Order: wor_...
Task: tsk_...
Work Entry: wen_...
Billing Entry: ben_...
Invoice: inv_...
Payment: pay_...

The same "prj_" identifier should appear in:

- AVCC
- Division workspace
- Asset Vault
- Tool sessions
- Worker jobs
- Handoffs
- Reviews
- Release records
- Invoice source records

---

17. AVCC modules inside AeroCore OS

AVCC can become a modular foundation.

My Work

- Assigned tasks
- Time and work entries
- Reviews
- Handoffs
- Deadlines
- Recently used projects

Contacts

- Organizations
- People
- Relationship history
- Portal access
- Communications

Sales

- Leads
- Opportunities
- Quotes
- Service packages
- Contracts

Projects

- Projects
- Work orders
- Tasks
- Milestones
- Division routes
- Health and blockers

Work Ledger

- Time
- Deliverables
- Worker usage
- Expenses
- Materials
- Rework
- Internal costs

Billing

- Rate cards
- Billing entries
- Retainers
- Invoice drafts
- Issued invoices
- Credits
- Payments

Operations

- Releases
- Incidents
- Service status
- Job usage
- Support work

Executive

- Revenue
- Profitability
- Unbilled work
- Division performance
- Project health
- Cash flow
- Overdue payments

Access to each module remains permissioned.

---

18. Architectural choice

AVCC should become two things:

AVCC Core Services

Reusable backend services:

AVCC Contact Service
AVCC Opportunity Service
AVCC Engagement Service
AVCC Project Service
AVCC Work Service
AVCC Billing Service
AVCC Invoice Service
AVCC Payment Service
AVCC Reporting Service

AVCC Command Workspace

The executive and business-management interface used by authorized users.

This avoids making every AeroCore user open the full AVCC application.

Division users only see relevant pieces inside their own workspace:

- Assigned tasks
- Current work order
- Billing classification
- Time submission
- Scope warning
- Milestone status

Executives and finance users see the larger AVCC Command Workspace.

---

19. Recommended event flow

Division action
→ AeroCore event
→ AVCC Operations Adapter
→ Activity Ledger
→ Rule evaluation
→ Work Ledger candidate
→ Human or automatic approval
→ Billing Ledger candidate
→ Invoice draft

Example:

Horizon flight completed
→ horizon.flight.completed
→ Activity record created
→ Work order marked fieldwork complete
→ Fixed-fee milestone becomes eligible
→ Project owner verifies deliverables
→ $450 billing entry created
→ Included in next invoice

Another example:

Lumina revision submitted
→ lumina.revision.submitted
→ Revision count increases from 2 to 3
→ Contract includes 2 revisions
→ Scope warning created
→ Project owner creates $120 change request
→ Client approves
→ New billing entry becomes eligible

---

20. What should be reused from the current AVCC

Architecturally, the existing AVCC can provide the starting foundation for:

- User-facing operating dashboards
- Project and task records
- Release-board concepts
- Evidence tracking
- Cross-project reporting
- Operational status
- Publisher and integration patterns

Before using it as the AeroCore base, perform a code and data audit to identify:

- Which AVCC entities are stable
- Which are presentation-only
- Which schemas can become canonical
- Which services are tightly coupled
- Which data is duplicated elsewhere
- Which modules should be extracted
- Which fields need new identifiers
- Which components can become shared workspace components

The correct move is likely evolution and extraction, not a total rewrite and not blindly renaming AVCC to AeroCore OS.

---

21. Recommended build sequence

Phase 1 — Map AVCC

- Inventory current entities
- Inventory APIs
- Inventory publishers
- Identify contacts, projects and task structures
- Identify release and evidence structures
- Identify duplicated data
- Define migration boundaries

Phase 2 — Add commercial entities

- Accounts
- Contacts
- Opportunities
- Quotes
- Engagements
- Work orders
- Rate cards
- Work entries
- Billing entries
- Invoices
- Payments

Phase 3 — Connect AeroCore contracts

- Shared project IDs
- Project Context
- Tool sessions
- Worker jobs
- Asset versions
- Handoffs
- Reviews
- Audit events

Phase 4 — Build Work Ledger

- Manual time entry
- Tool-session submission
- Worker-cost records
- Fixed-fee milestone eligibility
- Billing classification
- Approval workflow

Phase 5 — Invoice pipeline

- Invoice candidate review
- Draft generation
- Taxes and discounts
- Issuance
- Payment tracking
- Credits and adjustments
- Accounting export

Phase 6 — Division integration

Begin with the Horizon-to-Lumina pilot:

Client contact in AVCC
→ Quote approved
→ Project and work orders created
→ Horizon mission completed
→ Lumina campaign produced
→ Work and costs recorded
→ Client approval captured
→ Invoice generated
→ Payment tracked

---

22. Final role of AVCC

AeroCore OS
= platform foundation

AVCC
= business, project, work and financial operating system

Division Workspaces
= where specialized work is performed

AeroCore Vault
= where canonical assets and versions live

AeroCore Workers
= where heavy processing runs

AeroCore Relay
= where responsibility moves between divisions

AVCC Billing
= where approved work becomes invoices

AVCC Executive
= where outcomes, profitability and risk become visible

The strongest final definition is:

«AVCC is the commercial and operational brain of AeroCore OS. It connects contacts, agreements, projects, tasks, production activity, deliverables, costs, invoices and payments—while AeroCore OS provides the secure platform, specialized workspaces, assets, tools and processing infrastructure used to perform the work.»The next architecture pass should audit AVCC’s current project, task, publisher, and release-board schemas against the AeroCore contract pack, then define exactly which AVCC modules are promoted into shared AeroCore services and which remain inside the executive workspace.

## ASSISTANT
This is the right correction. AVCC should sit **inside AeroCore OS as its commercial and operational core**, not beside it as another loosely connected application.

The earlier blueprint made the Project Registry, workflow ownership, and operational records too platform-centric. Those responsibilities now need to be split cleanly:

- **AeroCore OS owns platform execution and technical governance.**
- **AVCC owns business intent, accountable work, commercial records, and financial outcomes.**
- **Division workspaces own specialized production.**

 
# AeroVista Workspace Master Blueprint
## Architecture Amendment: AVCC as the Commercial and Operational Core of AeroCore OS

**Amendment status:** Architecture direction locked 
**Affected systems:** AeroCore OS, AVCC, Division Workspaces, Vault, Workers, Relay, LaunchPad 
**Change classification:** Major domain ownership clarification 
**Preferred implementation strategy:** Evolution and service extraction from existing AVCC

---

# 1. Revised Platform Definition

The AeroVista platform should be organized into three primary operating layers.

```text id="yn7dgj"
┌──────────────────────────────────────────────────────────────┐
│ AEROCORE OS │
│ Identity · Permissions · Devices · APIs · Events · Security │
│ Tools · Assets · Workers · Handoffs · Shared Infrastructure │
└──────────────────────────────┬───────────────────────────────┘
 │
 ┌───────────────────────┼────────────────────────┐
 │ │ │
 ▼ ▼ ▼
┌──────────────┐ ┌───────────────────┐ ┌─────────────────┐
│ AVCC │ │ Division │ │ Shared AeroCore │
│ Business and │ │ Workspaces │ │ Services │
│ Operations │ │ Specialized Work │ │ Vault, Workers, │
│ Core │ │ and Delivery │ │ Relay, LaunchPad│
└──────┬───────┘ └─────────┬─────────┘ └────────┬────────┘
 │ │ │
 └────────────────────────┼───────────────────────┘
 ▼
 STRUCTURED ACTIVITY
 │
 ▼
 ACTIVITY LEDGER
 │
 ▼
 WORK LEDGER
 │
 ▼
 BILLING LEDGER
 │
 ▼
 INVOICES · PAYMENTS · MARGIN
```

---

# 2. Final Responsibility Boundaries

## 2.1 AeroCore OS Owns

AeroCore OS is the secure technical platform.

It owns:

- Authentication
- User identities
- Service identities
- Device registration
- Sessions and tokens
- Roles and technical permissions
- Division access enforcement
- Project-access enforcement
- Tool permissions
- Local desktop bridge
- Portable application packages
- Capability Registry
- Tool Registry
- Asset identity
- Asset storage and versioning
- File transfer
- Backend jobs
- Worker registration
- Worker execution
- Technical usage measurements
- Event transport
- Notifications
- Handoffs
- Platform health
- Shared search infrastructure
- Technical auditing
- Secret handling
- Infrastructure
- Deployment plumbing
- Backup systems

AeroCore OS answers:

- Who may access this?
- Which device is being used?
- Which tools are available?
- Where is the canonical asset?
- Which version was opened?
- Which worker processed it?
- How much infrastructure was consumed?
- Which system currently holds responsibility?
- Did the operation technically succeed?

---

## 2.2 AVCC Owns

AVCC is the canonical commercial and operational system.

It owns:

- Accounts and organizations
- Contacts
- Leads
- Prospects
- Customers
- Vendors
- Contractors
- Partners
- Opportunities
- Quotes
- Estimates
- Contracts
- Engagements
- Statements of work
- Retainers
- Purchase orders
- Service packages
- Projects as business engagements
- Participating divisions
- Work orders
- Tasks
- Milestones
- Deadlines
- Assignment records
- Operational status
- Client-visible status
- Scope
- Scope changes
- Rate cards
- Work records
- Labor cost
- Expenses
- Materials
- Infrastructure cost attribution
- Billing classifications
- Billing candidates
- Invoices
- Credits
- Payments
- Profitability
- Executive reporting
- Commercial audit history
- Approval evidence
- Delivery evidence
- Release readiness
- Project risk
- Unbilled work
- Write-offs

AVCC answers:

- Who is the client?
- What was requested?
- What did AeroVista agree to do?
- What is in scope?
- Which division owns the work?
- Who is assigned?
- What was completed?
- What did it cost AeroVista?
- What is billable?
- What requires approval?
- What belongs on the invoice?
- Has the client paid?
- Was the engagement profitable?

---

## 2.3 Division Workspaces Own

Division Workspaces own specialized execution.

Examples:

- Lumina edits visual campaigns.
- Horizon performs flights and processes aerial media.
- EchoVerse analyzes, edits, and publishes audio.
- Nexus builds and deploys software.
- Summit creates training content.
- Vespera develops publications.
- SkyForge creates interactive and 3D experiences.

They own:

- Specialized production interfaces
- Division-specific workflows
- Tool integrations
- Production notes
- Working views
- Domain-specific validation
- Specialized metadata
- Production outputs
- Delivery preparation
- Division-level operational events

They do not own:

- Customer master records
- Commercial agreements
- Canonical invoices
- Payment records
- Company-wide rate cards
- Final profitability calculations
- Global identities
- Global asset storage policies
- Cross-division commercial reporting

---

# 3. Revised Project Ownership Model

The prior blueprint treated the AeroCore Project Registry as the canonical project system.

That should be changed.

## 3.1 AVCC Project

The AVCC project is the canonical business and operational project record.

It contains:

```json id="1ecrw1"
{
 "project_id": "prj_01JXYZ",
 "engagement_id": "eng_01JABC",
 "account_id": "acc_01JCLIENT",
 "title": "Downtown CDA Campaign",
 "project_owner_id": "usr_123",
 "participating_divisions": [
 "horizon",
 "lumina"
 ],
 "commercial_status": "active",
 "operational_status": "production",
 "billing_method": "fixed_fee",
 "contract_value_usd": 4500,
 "target_margin_percent": 45
}
```

AVCC owns the project lifecycle:

```text id="1atdxq"
proposed
→ quoted
→ accepted
→ active
→ delivery
→ billing
→ paid
→ closed
```

---

## 3.2 AeroCore Project Context

AeroCore should maintain a **Project Context**, not a competing business project record.

The Project Context contains technical and workspace bindings:

```json id="s0smwu"
{
 "project_id": "prj_01JXYZ",
 "avcc_project_url": "/projects/prj_01JXYZ",
 "workspace_routes": [
 "/workspace/divisions/horizon/projects/prj_01JXYZ",
 "/workspace/divisions/lumina/projects/prj_01JXYZ"
 ],
 "vault_root": "projects/prj_01JXYZ",
 "repository_ids": [],
 "enabled_capability_sets": [
 "aerial-production",
 "visual-design"
 ],
 "worker_policies": [
 "media-standard"
 ],
 "retention_policy": "client-standard"
}
```

The shared `prj_...` identifier prevents two project identities from developing.

AVCC owns the business project.

AeroCore owns the technical context needed to execute it.

---

# 4. Revised Task Ownership

AVCC should own canonical tasks because tasks represent accountable work.

A task may reference AeroCore execution resources.

```json id="g0wcrx"
{
 "task_id": "tsk_lumina_hero",
 "project_id": "prj_01JXYZ",
 "work_order_id": "wor_brand_campaign",
 "division_id": "lumina",
 "owner_user_id": "usr_456",
 "title": "Produce campaign hero image",
 "billing_classification": "fixed_fee",
 "estimated_minutes": 180,
 "completion_criteria": [
 "Desktop and mobile formats complete",
 "Internal approval captured",
 "Final version linked"
 ],
 "due_at": "ISO-8601",
 "status": "in_progress",
 "asset_refs": [
 "ast_campaign_hero"
 ]
}
```

Division workspaces display and update permitted portions of the AVCC task.

They should not create isolated local task systems unless the records are subordinate production steps linked to the canonical AVCC task.

---

# 5. Contact and Identity Separation

Contacts and identities must remain distinct.

## AVCC Contact

Represents a business relationship.

```json id="s5asqf"
{
 "contact_id": "con_01JXYZ",
 "account_id": "acc_01JCLIENT",
 "name": "Jane Smith",
 "relationship_type": "client",
 "email": "jane@example.com",
 "relationship_owner_id": "usr_av_owner",
 "portal_status": "active"
}
```

## AeroCore Identity

Represents an authenticated actor.

```json id="ac66w1"
{
 "user_id": "usr_01JXYZ",
 "identity_type": "external_client",
 "status": "active",
 "authentication_provider": "oidc"
}
```

## Relationship Binding

```json id="6cv4n2"
{
 "contact_id": "con_01JXYZ",
 "user_id": "usr_01JXYZ",
 "access_scope": "client_portal",
 "expires_at": null
}
```

A contact does not require a login.

A login does not automatically create a commercial relationship.

---

# 6. Canonical Commercial Lifecycle

```text id="8g8hpc"
Account or Contact
→ Opportunity
→ Quote
→ Engagement
→ Project
→ Work Order
→ Task
→ Production Activity
→ Deliverable
→ Approval
→ Work Record
→ Billing Entry
→ Invoice
→ Payment
→ Closeout
```

## 6.1 Opportunity

Represents potential business.

## 6.2 Quote

Represents a priced offer with scope and conditions.

## 6.3 Engagement

Represents accepted commercial terms.

## 6.4 Project

Represents the managed body of work.

## 6.5 Work Order

Represents a bounded assignment that one or more divisions can execute.

## 6.6 Task

Represents assignable, measurable work.

## 6.7 Deliverable

Represents an expected client or internal output.

## 6.8 Approval

Establishes that a version or milestone has been accepted.

## 6.9 Billing Entry

Represents approved commercial value eligible for invoicing.

---

# 7. Three-Ledger Architecture

## 7.1 Activity Ledger

The Activity Ledger records what occurred.

Examples:

- Tool launched
- File uploaded
- Worker completed
- Build deployed
- Deliverable submitted
- Approval recorded
- Client requested revision
- Flight completed
- Course published

Activity records are detailed, immutable, and auditable.

They are not automatically invoice lines.

Suggested record:

```json id="f35b4s"
{
 "activity_id": "act_01JXYZ",
 "project_id": "prj_01JXYZ",
 "task_id": "tsk_01JXYZ",
 "event_type": "lumina.deliverable.submitted",
 "actor_id": "usr_456",
 "occurred_at": "ISO-8601",
 "source_system": "lumina-workspace",
 "references": {
 "asset_id": "ast_campaign_hero",
 "asset_version_id": "av_campaign_hero_004"
 }
}
```

---

## 7.2 Work Ledger

The Work Ledger converts meaningful activity into accountable work.

```json id="9z66a3"
{
 "work_entry_id": "wen_01JXYZ",
 "project_id": "prj_01JXYZ",
 "work_order_id": "wor_01JXYZ",
 "task_id": "tsk_01JXYZ",
 "division_id": "lumina",
 "performed_by": "usr_456",
 "work_type": "design",
 "quantity": 1.5,
 "unit": "hour",
 "billing_classification": "fixed_fee",
 "internal_cost_usd": 60,
 "client_charge_usd": 0,
 "status": "approved",
 "source_activity_ids": [
 "act_01JABC",
 "act_01JDEF"
 ]
}
```

Work records may be:

- Draft
- Submitted
- Approved
- Rejected
- Corrected
- Written off
- Converted to billing

---

## 7.3 Billing Ledger

The Billing Ledger contains controlled invoice candidates.

```json id="85z61b"
{
 "billing_entry_id": "ben_01JXYZ",
 "project_id": "prj_01JXYZ",
 "account_id": "acc_01JCLIENT",
 "source_type": "milestone",
 "source_id": "mil_01JXYZ",
 "description": "Lumina Brand Starter Package",
 "quantity": 1,
 "unit_price_usd": 1500,
 "subtotal_usd": 1500,
 "tax_category": "professional_service",
 "status": "approved_for_invoice",
 "invoice_id": null
}
```

Once attached to an issued invoice, a billing entry cannot be reused.

---

# 8. Billing Classification Contract

The following values become part of the shared AeroCore–AVCC contract:

```text id="pgtd52"
hourly
fixed_fee
milestone
retainer_included
retainer_overage
usage_based
pass_through_expense
internal
warranty
rework_non_billable
complimentary
written_off
```

These classifications apply to:

- Work orders
- Tasks
- Tool sessions
- Time entries
- Worker jobs
- Deliverables
- Expenses
- Billing entries

The classification may be inherited but must remain overridable through an audited approval process.

---

# 9. Service Catalog Ownership

The service catalog belongs to AVCC.

A service definition should include:

```json id="mbctds"
{
 "service_id": "LUM-BRAND-STARTER",
 "public_name": "Lumina Brand Starter Package",
 "internal_name": "Brand Starter V1",
 "owning_division": "lumina",
 "supporting_divisions": [],
 "description": "Foundation brand package",
 "pricing_model": "fixed_fee",
 "default_price_usd": 1500,
 "expected_internal_cost_usd": 600,
 "default_work_order_template_id": "wot_lum_brand_starter",
 "default_deliverables": [
 "Primary logo",
 "Secondary mark",
 "Color palette",
 "Typography guidance"
 ],
 "included_revision_cycles": 2,
 "revenue_account": "creative_services",
 "tax_category": "professional_service",
 "status": "active"
}
```

Accepted quote items should generate work orders from templates.

This reduces manual setup and creates consistency between sales promises and production execution.

---

# 10. AeroCore Operations Adapter

Each division should send events through a shared adapter contract.

## 10.1 Adapter Responsibilities

The AVCC Operations Adapter should:

- Validate event structure
- Verify project and task relationships
- Verify the source division
- Deduplicate repeated events
- Persist activity records
- Run commercial and operational rules
- Update milestone eligibility
- Create work-entry candidates
- Create scope warnings
- Update task state where authorized
- Record processing results
- Emit follow-up events

---

## 10.2 Event Envelope

```json id="6fkiqj"
{
 "event_id": "evt_01JXYZ",
 "event_type": "horizon.flight.completed",
 "event_version": "1.0",
 "occurred_at": "ISO-8601",
 "source_system": "horizon-workspace",
 "organization_id": "av",
 "division_id": "horizon",
 "project_id": "prj_01JXYZ",
 "work_order_id": "wor_01JXYZ",
 "task_id": "tsk_01JXYZ",
 "actor_id": "usr_01JXYZ",
 "correlation_id": "cor_01JXYZ",
 "payload": {}
}
```

---

## 10.3 Event Processing Result

```json id="g351wq"
{
 "event_id": "evt_01JXYZ",
 "processing_status": "accepted",
 "activity_id": "act_01JXYZ",
 "rules_triggered": [
 "mark_fieldwork_complete",
 "create_milestone_candidate"
 ],
 "work_entry_candidates": [
 "wen_01JXYZ"
 ],
 "billing_entry_candidates": [],
 "warnings": []
}
```

---

# 11. Tool Sessions and Work Confirmation

AeroCore LaunchPad owns the technical tool session.

AVCC owns the submitted work record.

```text id="dyxzij"
AVCC task selected
→ AeroCore LaunchPad starts tool session
→ User performs work
→ AeroCore records technical session
→ User reviews elapsed time and output
→ User submits accountable work
→ AVCC creates Work Ledger entry
```

## Technical Session

```json id="t1zmpo"
{
 "tool_session_id": "tls_01JXYZ",
 "project_id": "prj_01JXYZ",
 "task_id": "tsk_01JXYZ",
 "tool_id": "krita-portable",
 "user_id": "usr_456",
 "started_at": "ISO-8601",
 "ended_at": "ISO-8601",
 "elapsed_minutes": 104,
 "active_minutes_estimate": 92,
 "output_asset_version_ids": [
 "av_campaign_hero_004"
 ]
}
```

## Submitted Work Entry

```json id="4qmy9f"
{
 "tool_session_id": "tls_01JXYZ",
 "submitted_minutes": 90,
 "billing_classification": "fixed_fee",
 "notes": "Hero image layout and initial revision",
 "status": "submitted"
}
```

Tool-session data should inform the user, not silently determine pay, performance, or client billing.

---

# 12. Worker Cost Flow

AeroCore Workers measure technical resource usage.

AVCC determines accounting and billing treatment.

```text id="drqi8q"
Worker job completes
→ AeroCore records technical usage
→ Usage event sent to AVCC
→ AVCC determines internal cost
→ Contract rules determine client treatment
→ Work Ledger records cost
→ Billing Ledger receives charge only when applicable
```

Worker result:

```json id="b8l4an"
{
 "job_id": "job_01JXYZ",
 "project_id": "prj_01JXYZ",
 "task_id": "tsk_01JXYZ",
 "job_type": "media.video.render",
 "cpu_seconds": 840,
 "gpu_seconds": 320,
 "memory_peak_mb": 6144,
 "storage_output_bytes": 4382882011,
 "external_cost_usd": 1.42,
 "billing_code": "MEDIA_RENDER"
}
```

AVCC enrichment:

```json id="m57gps"
{
 "work_entry_id": "wen_01JXYZ",
 "source_job_id": "job_01JXYZ",
 "internal_cost_usd": 4.72,
 "billing_classification": "fixed_fee",
 "client_charge_usd": 0,
 "margin_impact_usd": -4.72
}
```

---

# 13. Scope-Control Architecture

Scope management belongs in AVCC but must surface inside division workspaces.

When production exceeds contract rules:

```text id="0t8vn8"
Production event
→ AVCC evaluates engagement rules
→ Scope threshold exceeded
→ Scope warning created
→ Task may continue or pause according to policy
→ Project owner chooses treatment
```

Available treatments:

- Create change request
- Charge as approved overage
- Mark as complimentary
- Mark as warranty
- Mark as internal rework
- Return request to client
- Escalate for project-owner review

Every treatment should preserve:

- Original request
- Contract rule
- Decision maker
- Financial impact
- Schedule impact
- Approval evidence

---

# 14. Invoice Architecture

## 14.1 Invoice Pipeline

```text id="v605nk"
Approved billing entries
→ Invoice candidate review
→ Draft invoice
→ Project-owner approval
→ Finance approval
→ Invoice issuance
→ Delivery to customer
→ Payment tracking
→ Reconciliation
```

## 14.2 Protections

- Each billing entry may be invoiced once.
- Issued invoices are immutable.
- Corrections use credits, adjustments, voids, or replacements.
- Invoice lines link to billing entries.
- Billing entries link to work, milestones, expenses, or services.
- Internal cost remains separate from customer charge.
- Invoice numbering is controlled.
- Tax treatment is recorded.
- Currency is explicit.
- Payment allocation is auditable.
- Partial payments are supported.
- Overpayments and credits are supported.

---

# 15. AVCC Service Architecture

AVCC should evolve into independently understandable domain services.

```text id="5v1n23"
services/
├── avcc-account-service/
├── avcc-contact-service/
├── avcc-opportunity-service/
├── avcc-quote-service/
├── avcc-engagement-service/
├── avcc-project-service/
├── avcc-work-order-service/
├── avcc-task-service/
├── avcc-activity-ledger/
├── avcc-work-ledger/
├── avcc-billing-ledger/
├── avcc-invoice-service/
├── avcc-payment-service/
├── avcc-service-catalog/
├── avcc-retainer-service/
├── avcc-scope-change-service/
├── avcc-reporting-service/
└── avcc-operations-adapter/
```

These do not initially need to become separate deployed microservices.

They may begin as clearly bounded modules in a modular monolith.

Extraction should occur only when justified by:

- Scaling
- Security boundary
- Deployment independence
- Ownership
- Failure isolation
- Reuse
- Integration demand

---

# 16. AVCC Command Workspace

AVCC Command Workspace is the business-facing interface.

## Modules

### My Work

- Assigned tasks
- Due dates
- Reviews
- Work-entry submission
- Handoffs
- Recent projects

### Contacts

- Accounts
- Contacts
- Relationship history
- Portal access
- Vendors
- Contractors
- Partners

### Sales

- Leads
- Opportunities
- Quotes
- Services
- Contracts
- Engagements

### Projects

- Projects
- Work orders
- Tasks
- Milestones
- Scope
- Risks
- Participating divisions
- Delivery status

### Work Ledger

- Submitted time
- Approved work
- Worker usage
- Expenses
- Materials
- Rework
- Internal costs
- Write-offs

### Billing

- Rate cards
- Billing candidates
- Retainers
- Draft invoices
- Issued invoices
- Credits
- Payments

### Operations

- Releases
- Incidents
- Support work
- Service health
- Processing usage
- Deployment evidence

### Executive

- Revenue
- Margin
- Cash flow
- Unbilled work
- Overdue balances
- Project health
- Division contribution
- Capacity
- Scope changes
- Internal investment

---

# 17. Revised AeroCore Workspace Modules

The AeroCore Workspace remains the unified entry surface, but AVCC modules are consumed according to permission.

## Ordinary Division User

Sees:

- Assigned AVCC tasks
- Work-order scope
- Billing classification
- Completion criteria
- Milestone status
- Scope warnings
- Work-entry submission
- Relevant project and client context

Does not automatically see:

- Customer financial history
- Profitability
- Other employees’ costs
- Invoice controls
- Payment details
- Company-wide sales pipeline

## Project Owner

Also sees:

- Budget
- Estimated versus actual effort
- Billing candidates
- Scope changes
- Milestone approvals
- Division coordination
- Client approvals
- Delivery readiness

## Finance User

Also sees:

- Rate cards
- Invoice drafts
- Credits
- Payments
- Tax information
- Aging
- Reconciliation

## Executive

Also sees:

- Portfolio health
- Revenue
- Margin
- Cash flow
- Division performance
- Risk
- Unbilled work
- Strategic internal investment

---

# 18. Shared Identifier Standard

The shared identifier set should be expanded and standardized.

```text id="gckmu1"
acc_ Account
con_ Contact
usr_ AeroCore identity
opp_ Opportunity
quo_ Quote
eng_ Engagement
svc_ Service
prj_ Project
wor_ Work order
tsk_ Task
mil_ Milestone
del_ Deliverable
ast_ Asset
av_ Asset version
tls_ Tool session
job_ Worker job
act_ Activity entry
wen_ Work entry
ben_ Billing entry
inv_ Invoice
crd_ Credit
pay_ Payment
ret_ Retainer
chg_ Scope change
evt_ Event
cor_ Correlation
```

The same IDs should travel through all relevant systems.

No service should generate a replacement project ID merely because it stores a local projection of the project.

---

# 19. Revised Repository Layout

```text id="teoejg"
aerocore-platform/
├── AGENTS.md
├── apps/
│ ├── aerocore-workspace/
│ ├── avcc-command-workspace/
│ ├── aerocore-admin/
│ ├── aerocore-desktop-tauri/
│ └── capability-package-manager/
├── domains/
│ ├── aerocore/
│ │ ├── identity/
│ │ ├── access/
│ │ ├── devices/
│ │ ├── assets/
│ │ ├── capabilities/
│ │ ├── tools/
│ │ ├── jobs/
│ │ ├── relay/
│ │ └── notifications/
│ └── avcc/
│ ├── accounts/
│ ├── contacts/
│ ├── opportunities/
│ ├── quotes/
│ ├── engagements/
│ ├── projects/
│ ├── work-orders/
│ ├── tasks/
│ ├── activity-ledger/
│ ├── work-ledger/
│ ├── billing-ledger/
│ ├── invoices/
│ ├── payments/
│ ├── retainers/
│ ├── service-catalog/
│ ├── scope-changes/
│ └── reporting/
├── divisions/
│ ├── lumina/
│ ├── horizon/
│ ├── nexus/
│ ├── echoverse/
│ ├── summit/
│ ├── vespera/
│ ├── skyforge/
│ └── frontier/
├── packages/
│ ├── aerocore-contracts/
│ ├── avcc-contracts/
│ ├── shared-identifiers/
│ ├── event-contracts/
│ ├── operations-adapter-sdk/
│ ├── ui/
│ ├── auth/
│ ├── observability/
│ └── testing/
├── workers/
├── capability-packs/
├── infrastructure/
└── docs/
```

This is a logical target layout.

The existing AVCC repository should not be moved into this structure until its current repository, deployment, and ownership conditions are audited.

---

# 20. Revised Cursor Rules

## Rule: Respect Domain Ownership

Cursor must determine the canonical owner before adding a field or service.

- Business relationship data belongs to AVCC.
- Commercial project data belongs to AVCC.
- Tasks and work orders belong to AVCC.
- Asset binaries and versions belong to AeroCore Vault.
- Tool execution belongs to AeroCore LaunchPad.
- Worker execution belongs to AeroCore Workers.
- Cross-division handoffs belong to AeroCore Relay.
- Financial records belong to AVCC.
- Division-specific production metadata belongs to the division service.

Cursor must not create duplicate canonical entities.

---

## Rule: Project Is One Shared Identity

All systems use the same `prj_...` identifier.

Local systems may maintain projections, but they may not generate independent replacement project identities.

---

## Rule: Activity Is Not Billing

Cursor must never implement logic that turns every activity, tool session, or worker job directly into an invoice line.

The required progression is:

```text id="3i5qtz"
Activity
→ Work candidate
→ Work approval
→ Billing candidate
→ Billing approval
→ Invoice
```

---

## Rule: Cost and Charge Are Separate

Every cost-capable record should distinguish:

- Internal cost
- Client charge
- Billing classification
- Included amount
- Margin impact

Never use one monetary field to represent both cost and price.

---

## Rule: Issued Financial Records Are Immutable

Issued invoices, applied payments, and posted credits may not be silently edited.

Corrections require explicit financial adjustment records.

---

## Rule: Audit Existing AVCC Before Extraction

Cursor must not begin decomposing AVCC until it has:

1. Located the current repository and deployment.
2. Read AVCC’s AGENTS.md and project instructions.
3. Mapped entities.
4. Mapped APIs.
5. Mapped publishers.
6. Mapped release-board structures.
7. Mapped storage.
8. Mapped duplicated data.
9. Identified production consumers.
10. Produced an extraction and compatibility plan.

---

# 21. Revised Build Phases

## Phase 0 — AVCC and AeroCore System Mapping

### Objective

Establish exactly what exists before redefining ownership.

### Tasks

- [ ] Locate AVCC repository or repositories
- [ ] Locate AVCC deployment compose roots
- [ ] Identify AVCC databases
- [ ] Inventory current entities
- [ ] Inventory current APIs
- [ ] Inventory publishers
- [ ] Inventory release-board schemas
- [ ] Inventory evidence structures
- [ ] Inventory project structures
- [ ] Inventory task structures
- [ ] Inventory user-facing views
- [ ] Identify data duplicated in other systems
- [ ] Identify integrations consuming AVCC data
- [ ] Identify AVCC data currently sourced from other systems
- [ ] Map AVCC permissions
- [ ] Map operational health and deployment state
- [ ] Produce current-state architecture
- [ ] Produce ownership-conflict report
- [ ] Produce migration-risk report

### Exit Gate

Every proposed canonical AVCC entity has been compared against the existing implementation.

---

## Phase 1 — Contract and Ownership Pack

### Objective

Define shared contracts before changing production code.

### Tasks

- [ ] Shared identifier contract
- [ ] Account contract
- [ ] Contact contract
- [ ] Opportunity contract
- [ ] Quote contract
- [ ] Engagement contract
- [ ] Project contract
- [ ] AeroCore Project Context contract
- [ ] Work-order contract
- [ ] Task contract
- [ ] Deliverable contract
- [ ] Activity contract
- [ ] Work-entry contract
- [ ] Billing-entry contract
- [ ] Invoice contract
- [ ] Payment contract
- [ ] Tool-session contract
- [ ] Worker-usage contract
- [ ] Scope-change contract
- [ ] Event-envelope contract
- [ ] Error contract
- [ ] Authorization rules
- [ ] Contract tests

### Exit Gate

AVCC and AeroCore can exchange valid project, task, activity, work, billing, asset, job, and approval records without schema ambiguity.

---

## Phase 2 — Stabilize AVCC Core

### Objective

Promote stable current AVCC structures into clearly bounded domain modules.

### Tasks

- [ ] Classify existing schemas as canonical, transitional, or presentation-only
- [ ] Normalize identifiers
- [ ] Add compatibility mappings
- [ ] Isolate project domain
- [ ] Isolate task domain
- [ ] Isolate release and evidence domain
- [ ] Add API versioning
- [ ] Add event outbox
- [ ] Add authorization enforcement
- [ ] Add audit records
- [ ] Preserve existing AVCC views
- [ ] Preserve current publisher behavior
- [ ] Add migration tests
- [ ] Document rollback

### Exit Gate

Current AVCC functions continue operating while stable domain boundaries exist beneath them.

---

## Phase 3 — Add Commercial Domains

### Objective

Extend AVCC into the full commercial lifecycle.

### Tasks

- [ ] Accounts
- [ ] Contacts
- [ ] Opportunities
- [ ] Service catalog
- [ ] Quotes
- [ ] Quote approval
- [ ] Engagements
- [ ] Contracts and terms references
- [ ] Work-order templates
- [ ] Rate cards
- [ ] Retainers
- [ ] Scope-change records
- [ ] Customer portal relationships

### Exit Gate

An opportunity can become an accepted engagement, project, and structured set of work orders without manual re-entry.

---

## Phase 4 — AeroCore Project Integration

### Objective

Connect business projects to the technical platform.

### Tasks

- [ ] Shared project-ID enforcement
- [ ] AeroCore Project Context
- [ ] Vault project root
- [ ] Division workspace routes
- [ ] Capability policies
- [ ] Device access
- [ ] Project-scoped assets
- [ ] Project-scoped jobs
- [ ] Project-scoped handoffs
- [ ] Project-scoped notifications
- [ ] AVCC task projection into workspaces
- [ ] Workspace status updates to AVCC

### Exit Gate

A project created from an engagement appears in the correct division workspaces with the correct tasks, tools, permissions, and storage.

---

## Phase 5 — Activity and Work Ledgers

### Objective

Create dependable operational cost and effort records.

### Tasks

- [ ] Activity Ledger
- [ ] Event deduplication
- [ ] Operations Adapter
- [ ] Manual work entry
- [ ] Tool-session work submission
- [ ] Worker-cost ingestion
- [ ] Work approval
- [ ] Billing classification
- [ ] Internal cost calculation
- [ ] Fixed-fee inclusion rules
- [ ] Warranty and rework rules
- [ ] Write-off handling
- [ ] Work-entry corrections
- [ ] Project effort reporting

### Exit Gate

AVCC can explain who performed work, what resources were used, what it cost internally, and how it should be commercially classified.

---

## Phase 6 — Billing and Invoice Pipeline

### Objective

Turn approved commercial value into controlled financial records.

### Tasks

- [ ] Billing Ledger
- [ ] Billing-entry approval
- [ ] Fixed-fee milestone billing
- [ ] Hourly billing
- [ ] Usage billing
- [ ] Retainer consumption
- [ ] Overage calculation
- [ ] Pass-through expenses
- [ ] Discounts
- [ ] Taxes
- [ ] Draft invoices
- [ ] Financial approval
- [ ] Invoice issuance
- [ ] Invoice delivery
- [ ] Credits
- [ ] Voids
- [ ] Replacement invoices
- [ ] Payment recording
- [ ] Partial payments
- [ ] Outstanding balance
- [ ] Accounting export

### Exit Gate

An approved engagement can progress from completed work to issued invoice and recorded payment with complete source traceability.

---

## Phase 7 — Scope and Profitability Controls

### Objective

Expose scope creep, margin, and operational risk before losses become invisible.

### Tasks

- [ ] Revision counting
- [ ] Scope-rule evaluation
- [ ] Change-request workflow
- [ ] Complimentary-work approval
- [ ] Warranty classification
- [ ] Rework attribution
- [ ] Estimated versus actual effort
- [ ] Worker-cost attribution
- [ ] Division cost allocation
- [ ] Project margin
- [ ] Service margin
- [ ] Client profitability
- [ ] Unbilled-work reporting
- [ ] Write-off reporting
- [ ] Internal-project cost reporting

### Exit Gate

AVCC can show whether work is in scope, what it costs, what will be billed, and whether the project remains profitable.

---

## Phase 8 — Division Operations Adapters

Recommended order:

1. Horizon
2. Lumina
3. Nexus
4. EchoVerse
5. Summit
6. Vespera
7. SkyForge
8. Frontier

### Per-Division Tasks

- [ ] Define event namespace
- [ ] Define milestone mappings
- [ ] Define work-entry mappings
- [ ] Define billing rules
- [ ] Define scope thresholds
- [ ] Define required approvals
- [ ] Implement adapter
- [ ] Add deduplication tests
- [ ] Add project/task validation
- [ ] Add activity-ledger tests
- [ ] Add representative workflow
- [ ] Complete operational acceptance

### Exit Gate

Each division can report production activity into AVCC without giving AVCC ownership of specialized working data.

---

## Phase 9 — Command Workspace and Embedded Views

### Objective

Deliver appropriate AVCC functions to each user without exposing the entire business system.

### Tasks

- [ ] AVCC Command Workspace
- [ ] My Work module
- [ ] Contacts module
- [ ] Sales module
- [ ] Projects module
- [ ] Work Ledger module
- [ ] Billing module
- [ ] Operations module
- [ ] Executive module
- [ ] Embedded task panel
- [ ] Embedded work-order panel
- [ ] Embedded time submission
- [ ] Embedded scope warning
- [ ] Embedded milestone state
- [ ] Permission-aware financial views
- [ ] Client portal views

### Exit Gate

Users see only the AVCC capabilities necessary for their role and current workspace context.

---

## Phase 10 — Horizon-to-Lumina Commercial Pilot

### Pilot Flow

```text id="fdrxb8"
Client contact
→ Opportunity
→ Quote
→ Engagement
→ Shared project ID
→ Horizon work order
→ Lumina work order
→ Horizon flight and delivery
→ Lumina campaign production
→ Work and worker costs
→ Client approval
→ Billing entries
→ Invoice
→ Payment
→ Profitability report
```

### Pilot Verification

- [ ] Contact created
- [ ] Quote generated
- [ ] Quote accepted
- [ ] Engagement created
- [ ] Project created
- [ ] Project Context created
- [ ] Work orders created
- [ ] Tasks routed
- [ ] Division permissions verified
- [ ] Assets stored in Vault
- [ ] Horizon events processed
- [ ] Relay handoff processed
- [ ] Lumina events processed
- [ ] Tool sessions submitted
- [ ] Worker costs recorded
- [ ] Approval captured
- [ ] Billing entries reviewed
- [ ] Invoice issued
- [ ] Payment recorded
- [ ] Margin calculated
- [ ] Full audit chain verified

### Exit Gate

A real multi-division engagement completes from contact through payment without undocumented duplicate records or manual financial reconstruction.

---

# 22. New Priority Audit Deliverable

The next implementation artifact should be:

```text id="tfhbsm"
AVCC_AEROCORE_DOMAIN_AUDIT.md
```

It should contain:

1. Current AVCC repository inventory 
2. Current deployment topology 
3. Current database and storage inventory 
4. Existing entity catalog 
5. Existing API catalog 
6. Publisher and integration catalog 
7. Project schema analysis 
8. Task schema analysis 
9. Release-board schema analysis 
10. Evidence and audit schema analysis 
11. Current permission model 
12. Duplicate-data analysis 
13. Proposed canonical ownership 
14. Shared AeroCore contract comparison 
15. Required identifier migrations 
16. Compatibility risks 
17. Extraction candidates 
18. Modules that should remain in AVCC 
19. Modules that should become shared services 
20. Recommended first safe change 

---

# 23. Updated Immediate Execution Order

1. Audit the current AVCC codebase and data model.
2. Audit current AVCC publishers and Release Board.
3. Map AVCC projects and tasks against the proposed shared contracts.
4. Map AVCC evidence records against Activity, Work, and Billing Ledger needs.
5. Identify existing stable modules.
6. Identify presentation-only or duplicated structures.
7. Lock shared identifiers.
8. Define the AVCC–AeroCore contract pack.
9. Add compatibility mappings before schema replacement.
10. Stabilize AVCC as a modular core.
11. Add commercial entities.
12. Create AeroCore Project Context.
13. Build the Operations Adapter.
14. Build Activity and Work Ledgers.
15. Build Billing and invoice flow.
16. Run the Horizon-to-Lumina pilot.
17. Expand division adapters after the pilot is verified.

---

# 24. Final System Definition

## AeroCore OS

The secure technical foundation that provides identity, permissions, devices, assets, tools, processing, events, handoffs, notifications, and infrastructure.

## AVCC

The commercial and operational brain that connects customers, agreements, services, projects, work, costs, billing, payments, profitability, approvals, and executive oversight.

## Division Workspaces

The specialized environments where AeroVista teams perform production work.

## AeroCore Vault

The canonical store for project assets and versions.

## AeroCore LaunchPad

The controlled bridge between project context and local or browser-based tools.

## AeroCore Workers

The processing layer for media, AI, builds, analysis, conversion, and automation.

## AeroCore Relay

The cross-division handoff and responsibility-routing layer.

## AVCC Ledgers

The accountable progression from activity to work to approved billing.

## AVCC Executive

The decision layer for commercial health, operational health, profitability, risk, and organizational visibility.

---

# 25. Locked Architecture Statement

> AVCC is the commercial and operational brain of AeroCore OS. It owns the business relationship, the agreement, the accountable project, the work structure, the cost records, the approved billing, the invoice, the payment, and the profitability view.

> AeroCore OS provides the secure platform used to perform that work: identities, permissions, devices, assets, tools, worker infrastructure, handoffs, technical events, and specialized division workspaces.

> Division systems retain ownership of specialized production data while reporting structured activity, deliverables, costs, approvals, and milestones back to AVCC.
:::

The biggest practical change is that the next phase should **not** begin by scaffolding a new Project Registry. It should begin by auditing AVCC and determining whether its existing project, task, publisher, evidence, and Release Board structures can become the canonical operational foundation without breaking current deployments.

## USER
check project files for avcc audit docs

## ASSISTANT
I checked the AVCC audit package. It is substantial and mostly complete.

## Files present

### Core audit and planning documents

- `avcc_audit.md` — the original read-only audit brief and success criteria. 
- `AVCC_CURRENT_SYSTEM_MAP.md` — verified production architecture, authentication, data flows, filesystem coupling, and deployment boundaries. 
- `AVCC_COMPONENT_INVENTORY.md` — runtime components, paths, deployment state, dependencies, and ownership gaps. 
- `AVCC_ENTITY_CATALOG.md` — 2026-07-17 SQLite snapshot, entity counts, relationships, missing entities, and data-quality findings. 
- `AVCC_API_CATALOG.md` — comprehensive route inventory with authentication, effects, and cross-cutting API risks. 
- `AVCC_PUBLISHER_CATALOG.md` — Art Localized, EchoVerse, Gear, NXCal, and Work Order publisher analysis. 
- `AVCC_DATA_OWNERSHIP_MATRIX.md` — current and recommended sources of truth across AVCC and AeroCore. 
- `AVCC_PERMISSION_MODEL.md` — current authentication model and the missing project-, division-, record-, and financial-scope authorization controls. 
- `AVCC_RELEASE_EVIDENCE_AUDIT.md` — confirms the Release Board is presentation-only and should be replaced with a durable Release/Evidence service. 
- `AVCC_FINANCIAL_READINESS.md` — correctly classifies AVCC as operational tracking, not billing-capable. 
- `AVCC_AEROCORE_GAP_ANALYSIS.md` — capability-by-capability gap, risk, complexity, and phase mapping. 
- `AVCC_MODULE_CLASSIFICATION.md` — identifies what to promote, keep, refactor, retain temporarily, or retire. 
- `AVCC_MIGRATION_RECOMMENDATION.md` — recommends a strangler migration with new versioned business services beside AVCC. 
- `AVCC_NEXT_IMPLEMENTATION_PLAN.md` — defines the safety/contracts slice and the first contact-to-draft-invoice proof. 

### Machine-readable inventories

- `avcc-components.json` 
- `avcc-entities.json` 
- `avcc-publishers.json` 
- `avcc-capabilities.json` 
- `avcc-gaps.json` 

## Missing from the requested audit deliverables

Three expected files are not present in the uploaded package:

1. `AVCC_AUDIT_EXECUTIVE_SUMMARY.md`
2. `AVCC_OPERATIONAL_RISK_REGISTER.md`
3. `avcc-api-routes.json`

Those are meaningful omissions.

The executive summary should contain the blunt final recommendation, top risks, reusable assets, blocking gaps, first implementation slice, and evidence table.

The risk register should consolidate severity, likelihood, operational impact, mitigation, owner, dependency, and blocking status. Those risks currently exist across several files, but they are not yet centralized.

The API catalog exists in Markdown and is detailed, but the requested machine-readable route inventory has not been included.

## Main conclusions supported by the audit

The audit strongly supports:

> **Yes — AVCC is suitable after modular extraction.**

The recommended role is:

> **AVCC should be split into shared business services plus an AVCC Command Workspace.**

The current AVCC cannot safely support the full lifecycle:

```text
Contact
→ Project
→ Work
→ Approval
→ Invoice
```

without a new business-services layer beside the current application.

The strongest reusable foundations are:

- Current project and task CRUD
- Identity profiles, sessions, badges, and capability concepts
- Context Broker and publisher ingestion
- NXCal integration
- Executive context and reporting interfaces
- Existing AVCC user experience
- Work Order compatibility paths

The largest blockers are:

- No organization/contact separation
- No engagement or quote model
- No Service Catalog
- No canonical Work Ledger
- No Billing Ledger
- Unsafe invoice money representation
- Mutable and deletable invoices
- No payments or reconciliation ledger
- No business mutation audit trail
- Weak authorization beyond authentication
- Two competing Work Order implementations
- Presentation-only Release Board
- No reliable publisher idempotency, replay, retry, or dead-letter handling

## One ownership issue to resolve

The audit’s ownership matrix assigns Projects, Tasks, Work Orders, and the Work Ledger to shared **AeroCore services**. 

That differs slightly from the latest architecture direction, where AVCC is the canonical commercial and operational owner of projects, work orders, tasks, and ledgers while AeroCore owns their technical execution context.

This is not a major technical conflict, but the final blueprint should normalize the naming:

- `AVCC Project Service`, exposed as an AeroCore shared business service
- `AVCC Task Service`, exposed through AeroCore contracts
- `AVCC Work Order Service`
- `AVCC Work Ledger`
- `AVCC Billing Ledger`
- `AeroCore Project Context`, assets, tools, jobs, and devices

That preserves AVCC’s business ownership while still making its services reusable across AeroCore OS.

## Recommended next action

Before implementation, complete the three missing deliverables and revise the ownership matrix/module classification to use the final AVCC-versus-AeroCore ownership language. After that, the package is strong enough to become the authoritative audit baseline for Cursor.

## USER
let's update and build out the ultimate AeroVista Workspace Master Blueprint
Architecture Amendment: AVCC as the Commercial and Operational Core of AeroCore OS

## ASSISTANT
I’m turning the architecture amendment and completed AVCC audit into one authoritative blueprint, resolving ownership conflicts and replacing speculative phases with evidence-backed implementation gates.

## ASSISTANT
The audit changes the build order in an important way: we will preserve the live AVCC façade, add versioned business modules beside it, and migrate through projections—not attempt a rewrite or a premature microservice split.

## ASSISTANT
# Ultimate AeroVista Workspace Master Blueprint

The updated blueprint is complete:

[Download `AEROVISTA_WORKSPACE_MASTER_BLUEPRINT_V2.md`](sandbox:/mnt/data/AEROVISTA_WORKSPACE_MASTER_BLUEPRINT_V2.md)

It contains a 14-phase implementation roll-up, complete architecture, ownership rules, Cursor/AV-Skillset controls, migration strategy, security model, priority backlog, exit gates, and definition of done.

## Major improvements

### AVCC ownership is now explicit

The blueprint locks the final relationship:

- **AVCC owns:** customers, contacts, opportunities, services, quotes, engagements, projects, work orders, accountable tasks, ledgers, invoices, payments, scope, profitability, and executive reporting.
- **AeroCore OS owns:** identity, access, devices, Vault assets, tools, workers, technical events, Relay handoffs, release evidence, and infrastructure.
- **Division Workspaces own:** specialized production data and execution.

AVCC business modules may be exposed as shared AeroCore APIs, but that does not transfer their canonical ownership to the platform layer.

### The current audit is built into the plan

The blueprint now reflects the verified production state rather than designing around assumptions:

- AVCC currently has useful project, task, identity, Context Broker, NXCal, reporting, and executive foundations. 
- The database contains 22 projects, 19 tasks, nine clients, two prototype invoices, and 1,039 Context Broker events. 
- Nineteen projects lack a client, eleven tasks lack a project, and both existing invoices lack project relationships. 
- Most business APIs authenticate users but do not enforce project-, division-, ownership-, or capability-scoped authorization. 
- Current invoice storage is not billing-safe because money uses SQLite `REAL`, invoices remain mutable, and payments, reconciliation, duplicate-billing prevention, taxes, and financial audit history are missing. 
- The current Release Board is duplicated static presentation data rather than a durable release system. 

### The build order has been corrected

The first step is no longer “build a new workspace and Project Registry.”

The new order begins with:

1. Production Git and release provenance
2. Backup and restore evidence
3. Copied-database contract testing
4. Canonical IDs and versioned contracts
5. Exact-money and audit rules
6. Scoped authorization
7. AVCC modular boundaries and compatibility façade
8. Contact-to-draft-invoice vertical proof
9. AeroCore execution integration
10. Division adapters and worker costs
11. Full invoice and payment capability
12. Horizon-to-Lumina commercial pilot

This follows the audit’s recommended strangler strategy: new versioned modules beside AVCC, legacy projections through an outbox, and read cutover only after reconciliation and rollback rehearsal. 

### The first implementation slice is fully defined

The blueprint’s first commercial proof is:

```text
Organization
→ Contact
→ Service Catalog Item
→ Project
→ Work Order
→ Task
→ Division Activity
→ Work Entry
→ Deliverable
→ Approval
→ Billing Entry
→ Draft Invoice
```

Its acceptance gates include:

- Exact integer-minor-unit totals
- Actor and timestamp on every transition
- Project- and capability-scoped permissions
- Append-only corrections
- Duplicate-billing prevention
- Complete audit traceability
- No Square submission
- No production-data mutation

That aligns with the audit’s recommended next implementation slice. 

### Cursor is given enforceable operating rules

The document includes:

- Required AV-Skillset activation sequence
- Repository and deployment preflight
- Canonical-owner checks
- Contract-first development
- Controlled-change reporting
- Migration requirements
- Forbidden architecture drift
- Precise implementation status language
- Verification and operational-acceptance gates
- Rules against premature microservice decomposition
- Rules against converting activity directly into billing

### The blueprint is now implementation-ready

It includes:

- Locked architecture decisions
- Evidence-backed current state
- Canonical data ownership
- Business lifecycle
- Three-ledger model
- Service Catalog
- Project Context
- Workspace UX
- Division capabilities
- PWA, Tauri, Electron, and portable-app strategy
- Shared services
- API baseline
- Identifier standard
- Security model
- Financial integrity requirements
- Migration and backfill rules
- Repository layout
- Fourteen implementation phases
- P0–P3 backlog
- Exit gates
- Non-goals
- Top architecture risks
- Definition of done

This should now become the canonical `MASTER_ARCHITECTURE_BLUEPRINT.md` for the AeroVista Workspace and AeroCore OS program.

## USER
create cursor rules

## ASSISTANT
I’m converting the blueprint into a ready-to-drop `.cursor/rules` package with ownership, contracts, security, financial integrity, migration, testing, deployment, and AV-Skillset enforcement built in.

## ASSISTANT
Created the complete Cursor rules package.

[Download `AEROVISTA_CURSOR_RULES_V1.zip`](sandbox:/mnt/data/AEROVISTA_CURSOR_RULES_V1.zip)

It includes:

- 13 `.cursor/rules/*.mdc` files
- 5 reusable `.cursor/commands/*.md` workflows
- Package manifest
- Installation README

The rule set covers:

- AeroCore OS and AVCC ownership boundaries
- AV-Skillset enforcement
- Contract-first development
- Shared IDs and lifecycle states
- Capability-plus-scope permissions
- Financial integrity
- Activity, Work, and Billing Ledgers
- Reliable event processing
- Strangler migration and compatibility
- Testing and verification
- Deployment safety
- Documentation and release evidence
- Controlled-change reporting

Place the included `.cursor` directory at the repository root beside the AV-Skillset-based `AGENTS.md`.

## USER
what else should we do before sending this job over to cursor?

## ASSISTANT
Before handing this to Cursor, I would do **one final packaging pass**. The architecture is strong; the remaining risk is Cursor receiving too much material without a precise first assignment.

## 1. Do not send Cursor the entire build as one job

The master blueprint is the program plan, not a single implementation ticket.

Cursor’s first assignment should be limited to:

> **Phase 0: repository provenance, safety harness, contracts, and implementation readiness.**

Do not let the first job include:

- Production schema changes
- New customer records
- Invoice migration
- Square integration
- Full workspace scaffolding
- Microservice extraction
- Legacy route retirement
- Production deployment

The existing AVCC production directory is not a Git worktree, which makes provenance the first real blocker. 

---

## 2. Confirm the actual working location

Cursor needs explicit paths for:

- Current AVCC production directory
- Safe development repository
- Docker Compose root
- SQLite production database
- Copied test database location
- Audit documents
- AV-Skillset location
- Intended output directory

Known production paths include:

```text
AVCC production:
/srv/ACOS/aerovista-command-center

AVCC database:
/srv/ACOS/aerovista-command-center/_data/sql/aerovista.db

File Work Orders:
/srv/avcc/workorders
```

Cursor must not assume the production directory is the development repository.

Before the job begins, decide whether Cursor should:

1. Work in an existing Git repository,
2. Create a new governed repository outside production, or
3. Produce only a migration/repository bootstrap plan.

Do **not** tell Cursor to initialize Git inside `/srv/ACOS/aerovista-command-center` unless that is deliberately approved.

---

## 3. Add the root `AGENTS.md`

The Cursor rules package refers to the AV-Skillset, but the target repository still needs the actual root `AGENTS.md`.

Confirm that it:

- Points to the AV-Skillset location
- Requires the relevant skills
- Defines operating modes
- Defines production safety expectations
- Explains repository versus deployed-directory boundaries
- Requires verification evidence
- Requires controlled-change reporting

The `.cursor/rules` files reinforce AV-Skillset use; they do not replace it.

---

## 4. Create a single handoff folder

Cursor should receive one obvious package rather than files scattered across locations.

Recommended structure:

```text
cursor-handoff/
├── JOB_BRIEF.md
├── AGENTS.md
├── MASTER_ARCHITECTURE_BLUEPRINT.md
├── CURRENT_STATE.md
├── ACCEPTANCE_GATES.md
├── PATHS_AND_ENVIRONMENTS.md
├── RISK_REGISTER.md
├── audit/
│ ├── AVCC_CURRENT_SYSTEM_MAP.md
│ ├── AVCC_COMPONENT_INVENTORY.md
│ ├── AVCC_ENTITY_CATALOG.md
│ ├── AVCC_API_CATALOG.md
│ ├── AVCC_PERMISSION_MODEL.md
│ ├── AVCC_FINANCIAL_READINESS.md
│ ├── AVCC_DATA_OWNERSHIP_MATRIX.md
│ ├── AVCC_MODULE_CLASSIFICATION.md
│ ├── AVCC_MIGRATION_RECOMMENDATION.md
│ └── AVCC_NEXT_IMPLEMENTATION_PLAN.md
└── .cursor/
 ├── rules/
 └── commands/
```

Avoid giving Cursor every JSON inventory unless the first task needs it. Too much context can make the agent wander.

---

## 5. Complete the remaining audit artifacts

Three requested audit deliverables were still missing:

- `AVCC_AUDIT_EXECUTIVE_SUMMARY.md`
- `AVCC_OPERATIONAL_RISK_REGISTER.md`
- `avcc-api-routes.json`

The first two matter before implementation.

The API JSON can wait until Cursor’s contract and route inventory work, but the Risk Register should exist before any architectural change.

At minimum, it should track:

```text
Risk
Severity
Likelihood
Affected system
Current evidence
Required mitigation
Blocking phase
Owner
Verification method
Status
```

Priority risks should include:

- Production not under Git provenance
- Weak business authorization
- Unsafe money representation
- Hard deletion
- Duplicate Work Order persistence
- Publisher idempotency gaps
- Broad filesystem mounts
- Missing customer/project mappings
- Uninventoried API consumers
- Static Release Board truth

---

## 6. Lock the first implementation boundary

The safest first Cursor job is not the full contact-to-invoice build.

It should produce the foundation that makes that build safe:

### First Cursor job

- Verify repository and deployment topology
- Establish Git/tag provenance plan
- Create copied-database test harness
- Add shared contracts package skeleton
- Add identifier, money, timestamp, status, and error contracts
- Add contract tests
- Add architecture decision records
- Add migration compatibility map
- Add backup/restore verification script or documented procedure
- Produce the next implementation plan

### Explicitly out of scope

- Production mutation
- Database migration
- New production routes
- Financial record conversion
- Square calls
- Deployment
- Removing old routes
- Altering existing AVCC records

---

## 7. Define acceptance gates before Cursor starts

Cursor should know exactly what counts as success.

For the first job:

- [ ] No production files or data changed
- [ ] Git status and repository boundaries documented
- [ ] Production-to-source provenance gap documented
- [ ] Copied SQLite database can be opened read-only
- [ ] Database integrity test runs
- [ ] Existing tables are validated against contract assumptions
- [ ] Canonical ID contract exists
- [ ] Exact-money contract exists
- [ ] Timestamp and timezone contract exists
- [ ] Status normalization contract exists
- [ ] Error contract exists
- [ ] Idempotency contract exists
- [ ] Capability-plus-scope authorization contract exists
- [ ] Contract tests pass
- [ ] Migration compatibility approach is documented
- [ ] Backup and restore evidence is documented
- [ ] Rollback path exists
- [ ] No deployment performed

---

## 8. Tell Cursor what not to trust

Cursor should treat the following as evidence that needs verification, not implementation truth:

- Static Release Board percentages
- UI labels suggesting financial readiness
- “Paid” invoice statuses without payment records
- Free-text project and division names
- Empty Work Order tables
- Documentation pointing to old paths
- Restore-staging directories
- Existing Square adapter behavior
- Unverified Portable Apps Bridge deployment
- Unversioned APIs as permanent contracts

The Release Board is explicitly presentation-only. 

The current invoice system is operational tracking, not billing-capable. 

---

## 9. Give Cursor a required output format

This prevents a long implementation session ending with “done.”

Require:

```text
Mode
Objective
Current-state findings
Repository boundary
Production boundary
Files created
Files changed
Contracts created
Tests executed
Test results
Production changes
Deployment status
Risks discovered
Assumptions
Rollback path
Known limitations
Recommended next slice
Exact state of each deliverable
```

---

## 10. Recommended Cursor handoff prompt

Use this as the actual first job:

 
# Cursor Job: AeroVista Workspace Phase 0 — AVCC Foundation Readiness

## Operating mode

Controlled Change — Read-Only Production / Development-Only Implementation

Use the repository’s root `AGENTS.md`, all applicable `.cursor/rules`, and the existing AV-Skillset.

Activate the relevant AV-Skillset workflows before making changes.

## Objective

Prepare the AVCC and AeroCore OS codebase for the first commercial vertical slice without mutating production data, deploying services, or changing the current AVCC runtime.

The next commercial slice will eventually prove:

Contact 
→ Service 
→ Project 
→ Work Order 
→ Task 
→ Activity 
→ Work Entry 
→ Deliverable Approval 
→ Billing Entry 
→ Draft Invoice

This job does not implement that lifecycle. It creates the safe engineering, contract, provenance, test, and migration foundation required to implement it correctly.

## Required reading

Read before acting:

1. `AGENTS.md`
2. `.cursor/rules/*`
3. `MASTER_ARCHITECTURE_BLUEPRINT.md`
4. `AVCC_CURRENT_SYSTEM_MAP.md`
5. `AVCC_COMPONENT_INVENTORY.md`
6. `AVCC_ENTITY_CATALOG.md`
7. `AVCC_API_CATALOG.md`
8. `AVCC_PERMISSION_MODEL.md`
9. `AVCC_FINANCIAL_READINESS.md`
10. `AVCC_DATA_OWNERSHIP_MATRIX.md`
11. `AVCC_MODULE_CLASSIFICATION.md`
12. `AVCC_MIGRATION_RECOMMENDATION.md`
13. `AVCC_NEXT_IMPLEMENTATION_PLAN.md`

## Safety restrictions

Do not:

- Modify the production AVCC directory.
- Modify the production SQLite database.
- Run database migrations.
- Deploy or restart services.
- Change production configuration.
- Initialize Git inside a production directory.
- Call Square or another payment provider.
- Create customers, invoices, payments, or test financial records in production.
- Remove or modify legacy APIs.
- Move current production files.
- Treat static Release Board data as durable release truth.
- Split the application into microservices.

Use a copied database for all schema and contract testing.

## Required work

### 1. Repository and provenance preflight

Document:

- Actual development repository root
- Current Git state
- Production deployment path
- Docker Compose root
- Build and deployment path
- Production database path
- Safe copied-database path
- Existing backup and restore mechanisms
- Gaps between source, build artifact, and deployed runtime

Do not create or change the production repository structure.

### 2. Architecture decisions

Create ADRs for:

- AVCC as the commercial and operational core
- AeroCore OS technical ownership
- Modular-monolith-first strategy
- Strangler migration
- Shared project identity
- Three-ledger model
- Exact-money representation
- Capability-plus-scope authorization
- Outbox-based compatibility projections
- Immutable financial corrections

### 3. Shared contract foundation

Create or scaffold canonical contracts for:

- Identifiers
- Money and currency
- Timestamps and timezone
- Status and lifecycle
- Error responses
- Idempotency
- Optimistic concurrency
- Authorization scope
- Business audit events
- Event envelope

Do not duplicate contract definitions in multiple services.

### 4. Copied-database test harness

Create a test workflow that:

- Operates only on a copied AVCC SQLite database
- Verifies SQLite integrity
- Inspects existing schema safely
- Validates known entity assumptions
- Detects unsafe `REAL` financial fields
- Detects hard-delete behavior in current CRUD where testable
- Captures current table and relationship baselines
- Produces deterministic test output

### 5. Migration compatibility mapping

Document:

- Legacy IDs to preserve
- New canonical IDs
- Project and task relationship gaps
- Client-to-account/contact review requirements
- Work Order duplication
- Legacy invoice treatment
- Static release import treatment
- Status mapping requirements
- Legacy API compatibility period
- Cutover gates
- Rollback behavior

Do not perform the migration.

### 6. Security contract

Define capability-plus-scope authorization for:

- Contacts
- Projects
- Work Orders
- Tasks
- Work Ledger
- Billing
- Payments
- Releases
- Audit

Default deny.

Separate system administration from sensitive business-content access.

### 7. Verification

Run all newly created tests and validation scripts.

Provide actual output or captured evidence.

## Deliverables

Produce:

- Repository and deployment boundary report
- ADR set
- Shared contract package or package skeleton
- Contract tests
- Copied-database validation harness
- Migration compatibility document
- Authorization capability matrix
- Backup and restore readiness report
- Phase 1 implementation plan
- Controlled Change report

## Acceptance gates

This job is complete only when:

- Production remains unchanged.
- No deployment occurred.
- Repository and production boundaries are explicit.
- Contract tests pass.
- Copied-database validation passes.
- Exact-money rules are documented and tested.
- Shared identifiers are documented and tested.
- Authorization scopes are explicit.
- Migration risks and compatibility requirements are documented.
- Backup and restore readiness is evidenced.
- Rollback is documented.
- The next implementation slice has explicit acceptance tests.

## Required final report

Report:

- Mode
- Objective
- Repository inspected
- Production path inspected
- Files created
- Files changed
- Contracts created
- Tests executed
- Test results
- Production changes
- Deployment status
- Risks discovered
- Assumptions
- Rollback path
- Known limitations
- Recommended next safe action

Use precise lifecycle states. Do not report “done” or “production ready.”
:::

## My strongest recommendation

Before launching Cursor, create the handoff folder and explicitly identify the **safe Git development repository**. That is the only decision I would not leave for Cursor to infer.

Everything after that can proceed through the Phase 0 job above.