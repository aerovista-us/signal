# Vespera.call.to.action.update

**Date:** 2026-07-13 (thread continued through follow-ups)  
**Scope:** Art Localized booth CTAs, Digimart / Cindy launch polish, modes visibility, commerce overrides, market featured booths  
**Primary project:** `aerovista.us`

---

## Thread goal (started as)

Update Vespera’s public call-to-action to point at:

`https://aerovista.us/vespera/`

That request expanded into a broader booth launch/content pass for Digimart and Connect with Cindy, plus platform fixes for modes and commerce links.

---

## 1. Vespera CTA

### What happened
- Initial CTA lived in `src/data/creator-configs/vespera.json` under links:
  - Label: **Start a brand sprint**
  - Was incorrectly edited to `/start?division=aerovista.us/vespera/showcase`
- Corrected to absolute URL:

```json
{
  "label": "Start a brand sprint",
  "href": "https://aerovista.us/vespera/"
}
```

### Notes
- `media.cta` in creator configs is **label-only** for classic booths; it does not drive the destination URL.
- Vespera **Launch Story** featured item still pointed at the old Lumina `/start?...` intake URL (left for a later decision).

**File:** `src/data/creator-configs/vespera.json`

---

## 2. Completeness audit — Digimart & Connect with Cindy

### Connect with Cindy (~mostly complete)
**Strengths:** profile, hero, links, theme, media copy, booking link present in `links`.

**Gaps found:**
- Featured pieces used Setup Wizard field `url` instead of renderer field `href` → public “View →” links silently dead.
- No featured images (gradient cards only).
- `media.cta` unused by classic mode CTA buttons.

### Digimart (not launch-complete at audit time)
**Gaps found:**
- Featured piece had empty `url`, not `href`.
- No product images.
- `mode: "listening-room"` not in `availableModes` and no `modeMedia` audio → listening-room UI broken/incoherent.
- Thin links (YouTube only).
- `media.cta: "Open Setup"` leftover operator copy.

**Publish gate (`validateBoothConfig`) can pass while public featured/mode UX is still incomplete.**

---

## 3. Digimart storefront content (Gumroad)

### Source of truth for products
[https://corrick7.gumroad.com/](https://corrick7.gumroad.com/)

### Updates in `digimart.json`
- Main CTA / shop link → Gumroad store
- Four featured tools with real `href` + local cover images:
  1. **Sing Karaoke Studio** → `/l/waabt`
  2. **SING LRC Maker** → `/l/zolldn`
  3. **Guitar Studio Notebook** → `/l/svnnz`
  4. **Beats Mixer Studio** → `/l/gexrbw`
- Mode set toward storefront/showcase cleanup; later locked to public showcase with modes hidden
- Media copy aligned to Gumroad pitch; CTA label → “Shop Digimart”
- Product covers saved under:
  - `public/assets/art-localized/booths/digimart/`

**File:** `src/data/creator-configs/digimart.json`

---

## 4. Storefront mode audit (why placeholders / AeroVista forms appear)

Screenshot showed Digimart storefront with:
- Global copy: “Sell without marketplace noise.”
- Placeholder chips: Product grid / Merch table / Commission intake / Drop announcements
- Buttons: **Visit storefront** / **Ask about commissions** → AeroVista `/start` and `/contact`

### Source map (classic public path)

| UI piece | Source | In creator JSON? |
|----------|--------|------------------|
| STOREFRONT card copy + highlight chips | `src/data/boothModes.js` → `BOOTH_MODES.storefront` | No |
| Visit / Ask button **labels** | same `boothModes.js` | No |
| Visit / Ask button **URLs** | `src/config/booth-intake.js` → `boothModeIntakeUrl()` | No (hardwired intake) |
| digimart media label/title/blurb | `digimart.json` → `media` | Yes |
| Gumroad shop + product cards | `digimart.json` → `links` / `featuredWork` | Yes |
| `media.cta` | present in JSON | **Unused** by classic mode media buttons |

**Conclusion:** creator JSON owns profile/media/links/featured work; storefront mode UI is shared scaffold + Lumina intake forms. Config alone could not retarget Visit Storefront to Gumroad without a code change (or hiding modes).

---

## 5. Hide modes from public view (`modesPublic`)

### Platform change
Added creator-config flag:

```json
"modesPublic": false
```

Merged in `applyCreatorConfig` (`src/data/creatorConfigs.js`).

### Public behavior when `modesPublic === false`
- Classic booth **skips** `BoothModePanel` (placeholder mode card + Visit/Ask intake)
- Hides mode chip in hero (`BoothHero`)
- Hides “· {mode} mode” on Booth Story (`BoothPage`)
- `mode` / `availableModes` remain for Manage/Setup background work

### Applied to
- **Digimart** — `mode: "showcase"`, `modesPublic: false`
- **Connect with Cindy** — same (`mode` had incorrectly been set to `false`; restored to `"showcase"`)

### Build break & fix
Nested JSDoc `/** ... */` inside the `CreatorConfig` typedef prematurely closed the comment and broke Vite import analysis in `creatorConfigs.js`. Nested comment removed; build restored.

**Docs updated:**
- `docs/ART_LOCALIZED_USER_MANUAL.md`
- `docs/DIGIMART_E2E_RUNBOOK.md`

---

## 6. Commerce sidebar CTA override

### Problem
Sidebar button like:

`Connect with Cindy` → `/contact?division=lumina&booth=connect-with-cindy&source=art_localized`

came from **platform registry**, not creator-config:

- `src/data/boothsRegistry.js` → `commerce`
- Rendered by `src/components/BoothTools.jsx`

### Platform change
Creator configs can now override `commerce`:

```json
"commerce": [
  { "label": "Book a Consultation", "href": "https://cindysanti.com/#booking", "variant": "primary" }
]
```

Wired through:
- `CreatorConfig` typedef
- `applyCreatorConfig` merge
- `creatorConfigFromBooth` export/round-trip preservation

### Applied
| Booth | Commerce CTA |
|-------|----------------|
| Connect with Cindy | Book a Consultation → `https://cindysanti.com/#booking` |
| Digimart | Shop Digimart → `https://corrick7.gumroad.com/` |

**Docs:** `docs/ART_LOCALIZED_USER_MANUAL.md`

---

## 7. Market featured booths

### Request
Featured row should show only:
1. **Connect with Cindy** — *Warm truth · grounded guidance · practical transformation.*
2. **Digimart** — *Apps for making noise.*

Remove prior featured rotation (EchoVerse / Horizon / etc. from that section; they remain elsewhere in the market).

### Implementation
- Added pin list in `src/data/founderBoothCatalog.js`:

```js
export const MARKET_FEATURED_BOOTH_SLUGS = ['connect-with-cindy', 'digimart'];
```

- `pickFeaturedBooths` / `partitionFeaturedBooths` in `src/data/marketBrowsingPrefs.js` prefer the pin over weight/session rotation.
- Catalog entries added for Cindy + Digimart (template label **Builder Booth**, interest tags, bridge links).

**Docs:** `docs/ART_LOCALIZED_USER_MANUAL.md` (Featured booths section)

---

## Known remaining gaps (not fully closed in this thread)

1. **Cindy featured work** still uses Setup field `url` instead of renderer `href` — public featured “View →” may still be dead until renamed/`href` added (+ optional images).
2. **Vespera Launch Story** featured href may still point at Lumina `/start?...`.
3. **Storefront mode CTAs** still globally intake-driven when modes are public; Digimart/Cindy hide modes for now instead of per-booth CTA URL overrides for mode panel buttons.
4. **Deploy** required for live site to pick up creator-config + code changes (`deploy:hosting` / booth promote flow as applicable).

---

## Key files touched

| Area | Paths |
|------|--------|
| Vespera CTA | `src/data/creator-configs/vespera.json` |
| Digimart content | `src/data/creator-configs/digimart.json`, `public/assets/art-localized/booths/digimart/*` |
| Cindy content | `src/data/creator-configs/connect-with-cindy.json` |
| Modes hide | `src/data/creatorConfigs.js`, `src/pages/BoothPage.jsx`, `src/components/BoothHero.jsx`, `src/data/boothsRegistry.js` (typedef) |
| Commerce override | `src/data/creatorConfigs.js` + Cindy/Digimart JSON |
| Featured market | `src/data/founderBoothCatalog.js`, `src/data/marketBrowsingPrefs.js` |
| Docs | `docs/ART_LOCALIZED_USER_MANUAL.md`, `docs/DIGIMART_E2E_RUNBOOK.md`, this file |

---

## Operator cheat sheet

| Intent | Setting |
|--------|---------|
| Vespera brand sprint CTA | `vespera.json` → links “Start a brand sprint” → `https://aerovista.us/vespera/` |
| Hide public modes | `"modesPublic": false` (+ keep `availableModes` for Manage) |
| Re-show modes later | `"modesPublic": true` or remove flag |
| Sidebar Commerce button | `"commerce": [{ "label", "href", "variant" }]` |
| Market featured pin | `MARKET_FEATURED_BOOTH_SLUGS` in `founderBoothCatalog.js` |

---

## Outcome

Thread started as a Vespera CTA URL fix and ended with:
- Correct Vespera CTA
- Digimart Gumroad-backed featured products + shop CTA
- Public modes hidden for Digimart and Cindy while mode work continues offline
- Creator-config `commerce` override so booths are not stuck on Lumina contact forms
- Market featured row pinned to Cindy + Digimart
