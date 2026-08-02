# Art Localized — Full Audit Report

**Document:** `full.audit.report.md`  
**Scope:** Conversation / engineering thread covering DigiMart go-live friction, Approve & Launch, and Gallery add-on  
**Primary codebase:** `C:\AeroCoreOS\aerovista.us`  
**NXCore API:** `\\100.115.9.61\acos\services\artlocalized-api`  
**Report date:** 2026-08-01  
**Related prior work window:** 2026-07-10 → 2026-07-12 (implementation), continued review through this report

---

## 1. Executive summary

This thread moved Art Localized from a fragile **creator Publish → operator promote “latest”** handoff to a **revision-pinned Approve & Launch** pipeline, then closed a DigiMart creator friction gap by shipping a **Gallery add-on tool** so uploaded images can appear on classic public booths beyond the hero.

| Theme | Outcome |
|-------|---------|
| DigiMart stale / mismatch risk | Mitigated: Request Review pins `submittedRevisionId`; Approve & Launch exports that exact revision; promote prefers `--revision` / `--export` |
| Creator Publish step | Removed for artists (`publish_disabled`); creators use Save Draft + Request Review only |
| Operator go-live | `/review` → **Approve & Launch** → copy `batch:complete-booth --revision …` |
| Uploads beyond hero | Gallery add-on: Enable → curate from media library → `addOns.gallery` → classic `BoothPage` Gallery section |
| Docs / operator runbooks | Updated (`BOOTH_SETUP_AND_EDIT`, onboarding, CHANGELOG, WO-NX-010, launch-complete email) |
| Deploy | Hosting redeployed after UI ships; art-api rebuilt on NXCore when API changed |

---

## 2. Thread timeline (high level)

1. **Finish / DigiMart / batch ops context** (earlier in same long thread)  
   - Smoke, DigiMart promote/live, launch-kit fixes, analytics ingest notes, batch tooling, friction docs, registry sync for new booths in Setup dropdown.

2. **DigiMart “deploy didn’t update” clarification**  
   - Deploy alone does not promote. Correct path: save → review → (old) publish → **promote** → deploy. This motivated the Approve & Launch redesign.

3. **Duplicate DigiMart block-layout files**  
   - Provision wrote `{slug}-builder-booth.js`; promote wrote `{slug}-booth.js` + brittle hints. Fixed with shared register helper; canonical DigiMart layout file kept.

4. **Approve & Launch plan** (`.cursor/plans/approve_and_launch_932f9722.plan.md`)  
   - Implemented end-to-end (API + CLI + UI + docs). Plan later annotated with shipped drifts.

5. **DigiMart image usability question**  
   - Confirmed: classic DigiMart + Setup media library → effectively **hero-only** for creators.

6. **Gallery as creator-selectable add-on** (`.cursor/plans/gallery_add-on_tool_55ec124b.plan.md`)  
   - Implemented: tool registry + `addOns.gallery` + builder UI + public Gallery section + docs; hosting deployed.

---

## 3. Problem statements addressed

### 3.1 Stale / wrong export on go-live

**Before:** request review → approve → creator publish → operator promote using date-named exports and often “latest,” while creators could keep editing after approval.

**After:** Request Review pins an immutable `versionId` as `submittedRevisionId` (+ checksum). Approve & Launch exports **only that version payload**. Workstation runner promotes that file by `--revision`.

### 3.2 Creator Publish confusion

Creators believed Publish = live. Publish only created an NXCore export; live required promote + deploy.

**After:** Artists cannot `POST /publish`. Copy and UI emphasize Save Draft + Request Review; operator launches.

### 3.3 DigiMart images unused beyond hero

Media library only offered **Use as hero**. Featured work / media UI were text-only. Classic DigiMart (`publicView: classic`, often `listening-room`) ignored modeMedia showcase galleries.

**After:** Opt-in Gallery add-on writes `addOns.gallery` and renders on classic `BoothPage` independent of booth mode.

---

## 4. Approve & Launch — what shipped

### 4.1 Target flow

```text
Creator Save Draft
  → Request Review (pins submittedRevisionId)
  → Operator /review → Approve & Launch
  → Exact export {slug}-{revisionId}.json + launch job
  → Workstation: npm run batch:complete-booth -- --slug X --revision Y
  → promote + deploy + launch-kit + verify + launch-complete
  → launchStatus: live
  → Operator sends completion email
```

Firebase deploy from NXCore remained **out of scope**; laptop CLI is still required for promote/deploy.

### 4.2 NXCore (artlocalized-api)

| Piece | Location / behavior |
|-------|---------------------|
| Revision pin | `POST …/request-review` — may auto-record `draft_saved` with `source: 'request_review_pin'` if needed |
| Clear on save | Draft save sets `launchStatus: 'draft'`, clears submission/approval pins |
| Artist publish block | `POST …/publish` → `403 publish_disabled` unless founder/operator (emergency date-named export retained) |
| Approve & Launch | `POST …/approve-and-launch` — checksum check, export from **version payload**, launch job, returns CLI `command` |
| Launch complete | `POST …/launch-complete` — sets `live` / `launch_failed` + `deployedRevisionId` |
| Jobs | `src/lib/launchJobs.js` → `data/launch-jobs/` |
| Status projection | `booths-status` includes `launchStatus`, revision ids, `exportFilename`, etc. |

**Filename sanitize:** non `[A-Za-z0-9._-]` chars in revision id → `_` via `exportFilenameForRevision`.

**Accept states for launch:** `review_requested` / `needs_review`, and also already-`approved` (approve-only advanced path).

### 4.3 CLI (`aerovista.us`)

| Script | Change |
|--------|--------|
| `scripts/batch-complete-booth.mjs` | `--revision` / `--export`; prefers LAN share; calls launch-complete; prints completion email body + template pointer |
| `scripts/promote-booth.mjs` | `--revision`; share-first resolve; warns if falling back to “latest”; strips launch/review keys from creator-config |

Silent “latest” was **deprecated with warning**, not hard-blocked (drift from original “must require” wording).

### 4.4 Frontend

| Surface | Change |
|---------|--------|
| Setup (`CreatorSetupConsolePage.jsx`) | Publish removed; Request Review; launch status / revision strip |
| Manage (`BoothManagePage.jsx`) | Same; no artist Publish |
| Review (`OperatorReviewQueuePage.jsx`) | Primary **Approve & Launch**; revision + checksum; copy launch command; Approve-only + Mark failed under Advanced |
| API client | `postApproveAndLaunch`, `postLaunchComplete`; extended `BoothStatusRow` |
| Assign checklists | `operatorWorkflowSteps.js` prefers `batch:complete-booth --revision` |

### 4.5 Docs / email

- `docs/BOOTH_SETUP_AND_EDIT.md` — streamlined Approve & Launch + CLI
- `docs/BUILDER_ONBOARDING.md`, `docs/COLLABORATOR_ONBOARDING.md`
- `docs/CHANGELOG.md`
- `docs/templates/art-localized-launch-kit/email/launch-complete-email.template.md`

### 4.6 Known drifts / oddities (from plan annotations)

- Request-review may compare full draft checksum (including meta) to version payload → extra `draft_saved` snapshots possible (harmless noise).
- Leftover `*.bak-wo0*` files under art-api `src/` from earlier WO work.
- art-api **image** is built (not bind-mounted `src/`); API changes need `docker compose up -d --build` on NXCore (`glyph@100.115.9.61`).
- Pre-ship **approved** drafts without `submittedRevisionId` need a fresh Request Review.

---

## 5. Gallery add-on — what shipped

### 5.1 Data

```js
addOns: {
  gallery: {
    enabled: true,
    items: [{ title: string, image: string, caption?: string }]
  }
}
```

- Merged in `creatorConfigs.js` (`applyCreatorConfig`, `creatorConfigFromBooth`)
- Included in `collectAssetRefs` for asset checks / promote rewrite awareness
- **Not** stripped by `promote-booth.mjs` NXCore-only key list

### 5.2 Toolkit

- Tool id `gallery` on `DEFAULT_CREATOR_BOOTH_TOOLS` (DigiMart, Cindy, Everyday Method, etc.)
- Component: `src/components/booth-tools/CdaGalleryBuilder.jsx`
- Registered in `boothToolComponents.js`

### 5.3 Creator UX

- Setup Step 6: Enable / Disable / Manage Gallery (embedded)
- Media library: **Add to gallery** when enabled (Setup Step 4 + Manage + inside builder)
- Soft cap: **12** images
- Standalone tool route can Save Gallery to draft when not embedded

### 5.4 Public classic booth

- `BoothPage.jsx` renders `GalleryViewer` when `addOns.gallery.enabled && items.length`
- Mode-independent (works for DigiMart `listening-room`)
- `BoothTools` sidebar chip → `#gallery` when present
- `GalleryViewer` CTAs/header made optional for add-on use

### 5.5 Docs

- `docs/WO-NX-010_ASSET_REGISTRY.md` — Gallery path marked shipped
- Setup / collaborator onboarding notes
- CHANGELOG entry (2026-07-12 · Gallery creator add-on tool)

---

## 6. DigiMart-specific findings

| Item | State during thread |
|------|---------------------|
| Slug | `digimart` |
| Creator | Jeanette / `jlcorrickandco@gmail.com` |
| Public view | `classic` |
| Mode (draft observed) | `listening-room` |
| Live promote | Done earlier in thread (2026-07-10 era) with later revision work |
| Image UX before Gallery | Hero usable; featured work text-only; extra uploads not public |
| Block layout | Canonical `digimart-builder-booth.js` after duplicate-file fix; public URL still classic |

**Operator note after Gallery ship:** Creator enables Gallery, applies images, saves, Request Review; operator Approve & Launch with `--revision` so gallery asset URLs are pulled/rewritten like hero.

---

## 7. Architecture decisions (locked)

1. **Approve & Launch is split:** NXCore = authority/immutability/export/job; workstation = promote/Firebase/kit/verify.  
2. **Reuse `versionId` as revisionId** — no parallel ID scheme.  
3. **Gallery is opt-in `addOns.gallery`**, not forced onto `modeMedia.showcase.gallery` (would miss DigiMart listening-room).  
4. **Tools remain registry-provisioned catalogs**; “selectable” for Gallery means Enable on draft, not a marketplace.

---

## 8. Key file index

### Approve & Launch

| Area | Path |
|------|------|
| API routes | `\\100.115.9.61\acos\services\artlocalized-api\src\routes\booths.js` |
| Launch jobs | `…\artlocalized-api\src\lib\launchJobs.js` |
| Status | `…\artlocalized-api\src\routes\builderWorkflow.js` |
| Batch CLI | `aerovista.us/scripts/batch-complete-booth.mjs` |
| Promote CLI | `aerovista.us/scripts/promote-booth.mjs` |
| Review UI | `aerovista.us/src/pages/OperatorReviewQueuePage.jsx` |
| Setup / Manage | `CreatorSetupConsolePage.jsx`, `BoothManagePage.jsx` |
| Workflow API | `aerovista.us/src/api/builderWorkflowApi.js` |
| Plan (+ drifts) | `AeroCoreOS/.cursor/plans/approve_and_launch_932f9722.plan.md` |

### Gallery

| Area | Path |
|------|------|
| Builder | `aerovista.us/src/components/booth-tools/CdaGalleryBuilder.jsx` |
| Assets | `aerovista.us/src/components/builder/BoothAssetManager.jsx` |
| Public | `aerovista.us/src/pages/BoothPage.jsx`, `GalleryViewer.jsx`, `BoothTools.jsx` |
| Config merge | `aerovista.us/src/data/creatorConfigs.js` |
| Validation refs | `aerovista.us/src/lib/boothValidation.js` |
| Registry | `aerovista.us/src/data/boothToolsRegistry.js` |
| Plan | `Users/trcam/.cursor/plans/gallery_add-on_tool_55ec124b.plan.md` |

### Process docs

- `docs/BOOTH_SETUP_AND_EDIT.md`
- `docs/BUILDER_ONBOARDING.md`
- `docs/COLLABORATOR_ONBOARDING.md`
- `docs/CHANGELOG.md`
- `docs/WO-NX-010_ASSET_REGISTRY.md`
- `docs/DIGIMART_E2E_RUNBOOK.md` / `docs/CREATOR_BATCH_V1_TRACKER.md` (batch context)

---

## 9. Acceptance checklist (thread outcomes)

### Approve & Launch

- [x] Artist cannot create production exports via Publish  
- [x] Request Review stores immutable `submittedRevisionId`  
- [x] Approve & Launch exports only that revision  
- [x] Post-approval draft edits clear submission  
- [x] `batch:complete-booth --revision` path documented and implemented  
- [x] Docs updated; plan annotated with drifts  

### Gallery

- [x] DigiMart (and other DEFAULT toolkit booths) can Enable Gallery in Setup  
- [x] Library images addable when enabled  
- [x] Disabled / empty gallery shows nothing public  
- [x] Hero-only flow unchanged if Gallery never enabled  
- [x] `addOns` survives promote strip list; asset refs collected  

---

## 10. Open follow-ups (not done in this thread)

| Item | Notes |
|------|-------|
| Server-side Firebase from Approve & Launch | Needs Firebase token + repo checkout on NXCore/CI |
| Hard-require `--revision`/`--export` on promote | Still soft-warn + latest fallback |
| Featured work image picker | Schema supports `featuredWork[].image`; Setup still text-first |
| Block-layout gallery sync | Out of scope; classic-first |
| CF Access bypass for public analytics ingest | Documented earlier; ops may still need Zero Trust policy |
| DigiMart public share confirmation | Tracker had creator share as pending at times |
| Everyday Method assignment email | Earlier note of possible wrong email — verify if still open |
| Clean art-api `.bak-wo0*` leftovers | Optional hygiene |

---

## 11. Operator quick commands (current)

```powershell
cd C:\AeroCoreOS\aerovista.us

# After /review Approve & Launch:
npm run batch:complete-booth -- --slug <slug> --revision <revisionId>

# Fallback:
npm run promote:booth -- --slug <slug> --revision <revisionId> --deploy
npm run launch-kit -- --slug <slug> --verify
npm run verify:booth-live -- --slug <slug>

# Rebuild art-api after API changes:
ssh glyph@100.115.9.61 "cd /srv/ACOS/services/artlocalized-api && docker compose up -d --build"
```

Creator Gallery path: `https://artists.aerovista.us/setup?booth=<slug>` → Step 6 → Gallery.

---

## 12. Verdict

This conversation delivered two production-shaped platform upgrades for Art Localized Batch v1:

1. **Trustworthy go-live** via revision-pinned Approve & Launch (fixes DigiMart-class stale promote risk).  
2. **Usable creator media** via an opt-in Gallery add-on on classic booths (fixes hero-only upload trap).

Both are documented, UI-deployed (as of ship), and aligned with the chosen split between NXCore authority and workstation Firebase deploy. Remaining work is mostly automation (server-side deploy), media polish (featured-work images), and batch ops follow-through.
