# Vespera × AeroVista — The Signal · VXP-MR-01

This repository includes a **multi-file publication spine** for issue **VXP-MR-01** (*Tokenized Rails, Collateral Systems, and the Physical Internet of Money*).

## Location

All publication assets live under:

`publications/VXP-MR-01-macro-rails-intelligence/`

## Files

| File | Role |
|------|------|
| `vespera_publication_meta.yaml` | Issue metadata, volume IDs, appendices, HTML route, footer strings |
| `vespera_toc.md` | Human-readable table of contents |
| `volume_01_regulatory_rails.md` … `volume_06_ai_energy_physical_rails.md` | Volume narratives and cluster specs |
| `signals_appendix.md` | Placeholder for canonical signal definitions (to be filled from the briefing) |
| `micro_infographic_pack.md` | Index of slide-ready infographic specs (detail in each volume) |
| `signals_briefing.html` | Web briefing: “Signals to Watch” + “How to Use This”, with publication wrapper and footer |
| `magazine.html` + `magazine.mjs` | Mobile-first PNG magazine: realistic page curl (StPageFlip via `page-flip` on jsDelivr), one page per screen in portrait, swipe and corner peel |
| `pages-manifest.json` | Optional root `title`, `partner`, `issue`; ordered `pages` (strings and/or `{ "src", "title", "note", "links" }` and/or placeholders) |
| `pages/README.txt` | Where to drop PNGs and how to reference them in the manifest |

## PNG magazine (`magazine.html`)

Open in a browser (local file or static host):

`publications/VXP-MR-01-macro-rails-intelligence/magazine.html`

1. Add PNG files (same folder as `magazine.html` or under `pages/`).
2. Edit `pages-manifest.json`: set `pages` to an ordered array (optional root `title` for the header line). The active issue uses five spreads — `cover.png`, `02_signal_clusters_deep_dive.png`, `03_05_convergence_architecture.png`, `06_07_strategic_outlook.png`, `back_cover.png` — with per-spread `title`, `note`, and `links`. Conventions are in [`pages/README.txt`](../publications/VXP-MR-01-macro-rails-intelligence/pages/README.txt). Optional motion teaser: [`media/brief-teaser.mp4`](../publications/VXP-MR-01-macro-rails-intelligence/media/brief-teaser.mp4).
3. Reload. The app loads **`page-flip` 2.0.7** from jsDelivr (global `St.PageFlip`), builds one HTML leaf per image, and initializes portrait single-page spreads with shadows and slower flips for a heavier feel.

**Local testing:** Some browsers block `fetch()` for `pages-manifest.json` under the `file://` protocol. Use any static HTTP server from the issue folder (for example `npx serve .`) and open `/magazine.html`.

**Docker Compose:** From the repo root run `docker compose up`, then open `http://localhost:9888/publications/VXP-MR-01-macro-rails-intelligence/magazine.html` (override the host port with `PORT=3000 docker compose up` if 9888 is taken). Config: [`docker-compose.yml`](../docker-compose.yml) and [`docker/nginx/default.conf`](../docker/nginx/default.conf).

**Tracking Prevention / Edge:** Avoid loading the library with `<script src="https://cdn…">`. `magazine.mjs` **fetches** the bundle and runs it from a **blob: URL**. By default it tries the **CDN first**, then optional `./vendor/page-flip.browser.min.js`, so an empty `vendor/` folder does **not** produce a 404. To load vendor first (e.g. offline LAN), set `"preferLocalPageFlip": true` in [`pages-manifest.json`](../publications/VXP-MR-01-macro-rails-intelligence/pages-manifest.json) and install the file via [`scripts/pull-page-flip.ps1`](../publications/VXP-MR-01-macro-rails-intelligence/scripts/pull-page-flip.ps1) — see [`vendor/README.txt`](../publications/VXP-MR-01-macro-rails-intelligence/vendor/README.txt).

**Layout (immersive):** `#book` fills the entire safe viewport; the **header and chin are overlays** (frosted gradients, high `z-index`) so the flip canvas gains the vertical space that used to sit under flex chrome. Spreads still scroll and support pinch-zoom; prev/next and chin stay tappable above the page layer.

**Chrome:** A top **header** shows partner, optional issue title (from manifest `title`, else issue code), issue id + spread index, and the current spread title. The bottom **chin** has prev/next and a tappable center strip that expands a **notes & links** panel (per-spread copy from the manifest, plus buttons for same-origin URLs). The panel collapses when you flip to another spread.

**Placeholders:** Any manifest entry can be `{ "placeholder": true, "label": "Cluster title" }` instead of a PNG path. Those spreads render an in-page “Coming soon” card (no network request, no duplicate of page 1). Replace with a string path when the asset exists.

**Touch / resize:** PageFlip runs with `mobileScrollSupport: true` (helps some mobile browsers deliver gestures over `overflow: hidden` shells). After images load and when `#book` resizes (`ResizeObserver`, `resize`, `visualViewport`), the UI layer calls `getUI().update()` so framing stays correct.

**Single-page manifest:** If `pages-manifest.json` lists only one spread, swipe and corners do not advance. Open the chin (center tap) to read the short hint in the notes panel.

**Tuning** (in `magazine.mjs`, `CONFIG`): `swipeDistance` (horizontal swipe sensitivity vs vertical drift), `flippingTime`, `maxShadowOpacity`. With `prefers-reduced-motion: reduce`, flip duration is shortened automatically.

**Navigation**: corner drag and horizontal swipe (library); on-screen prev/next when there is a previous/next page.

**DevTools:** Chromium may log `[Violation] Added non-passive event listener to a scroll-blocking 'touchstart'` from the bundled page-flip library; it does not block magazine behavior unless you patch vendor code.

## Related

- Root `signal.html` is an earlier standalone briefing using the same visual language; the publication HTML is the issue-wrapped version intended for route `/vespera/macro/signals-briefing` per metadata.

## Next steps (optional)

- Expand `signals_appendix.md` with metrics, sources, cadence, and owners per cluster.
- Promote any volume to a long-form PDF-style narrative with charts.
