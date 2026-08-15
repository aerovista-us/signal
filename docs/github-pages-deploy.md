# Deploying to GitHub Pages ([aerovista-us/signal](https://github.com/aerovista-us/signal))

Production at [thesignal.aerovista.us](https://thesignal.aerovista.us) serves from the **`main`** branch of this repo. If a file exists on your Collab share but not on GitHub, the live site will 404.

Site layout: [site-structure.md](./site-structure.md) · Publishing: [publishing-workflow.md](./publishing-workflow.md)

## Theme CSS

- **Canonical:** `signal-public-theme.css` (repo root) — dispatches use `/signal-public-theme.css`
- **Mirror:** `css/signal-public-theme.css` — keep in sync with root
- **`index.html`** inlines theme in `<style>` (no external CSS required on Pages)

## Umami

Set `analytics.websiteId` in [`js/site-config.js`](../js/site-config.js). Checklist: [umami-analytics.md](./umami-analytics.md).

## Full sync checklist (local → GitHub)

Copy from `\\100.115.9.61\Collab\mini.shops\thesignal` into your clone of [aerovista-us/signal](https://github.com/aerovista-us/signal), then:

```bash
git add index.html signal-public-theme.css css/signal-public-theme.css js/ dispatches/ newsletters/
git add publications/ docs/ scripts/ favicon.svg signal.png signal.html player-swamphop.html
git add signal_pipeline_echoverse_starter/ archive/orphans/
git status
git commit -m "Sync site structure: editions, dispatches subfolders, catalog hub."
git push origin main
```

Wait 1–2 minutes for GitHub Pages to rebuild, then hard-refresh.

## Redirect policy

Moved files keep **redirect stub HTML** at the old URL (meta refresh + canonical). Verify both stub and new canonical URL return **200**.

## Internal Signals hub

- Hub: [`dispatches/internal-signals.html`](../dispatches/internal-signals.html)
- Catalog data: [`js/signals-catalog.json`](../js/signals-catalog.json)
- Renderer: [`js/render-signals-hub.js`](../js/render-signals-hub.js)

Legacy redirects: [`newsletter-current.html`](../newsletter-current.html), [`dispatches/current-updates.html`](../dispatches/current-updates.html)

## Adding a new Internal Signals entry (checklist)

Every new edition (EOD, EOW, ByteCast, milestone, MTD, etc.) touches **the report file itself plus up to three other files**. Missing any of these is why a newly-added entry "isn't showing up" even after a successful deploy.

1. **The report/edition file(s)** — copy the actual HTML (and any assets it doesn't self-embed) into `newsletters/` or `newsletters/editions/<type>/<slug>/`. If this file isn't in the git repo, its link will 404 even though the catalog references it.

2. **`js/signals-catalog.json`** — the data source for the hub page:
   - Add an object to **`editions[]`** (section, badges, dateEm, dateYear, href, types, tags, summary) — this is what populates the type-specific catalog list (Daily EOD / Weekly EOW / ByteCast / Milestones / Archive / EOM). `section` must be one of `eod`, `eom`, `weekly`, `bytecast`, `milestones`, `archive`.
   - Add an object to **`now[]`** (id, typeLabel, title, summary, href, types, tags) if it should appear as a "Right Now" card.
   - If this is the newest/headline entry, update **`featured`** (label, title, summary, href, stats) — this drives the big hero box at the top of the hub.
   - Bump the top-level **`updated`** date.

3. **`dispatches/internal-signals.html`** — static fallback markup that renders before/without JS. The renderer (`render-signals-hub.js`) overwrites the hero's `h2`, `p`, `.pulse-stat` values, and the button's `href`/`data-copy` from `featured` — but it does **not** rewrite the `<a class="btn">` link text (e.g. "Open EOD edition") or the header's "Updated …" / "N editions indexed" text. Update these by hand to match:
   - `.hub-meta strong` (Updated date) and the editions-indexed count
   - `.featured-label`, `h2`, `p` text (optional — JS will overwrite on load, but keep in sync for no-JS/first-paint)
   - `.btn` link text + `href`, and the `copy-btn` `data-copy` URL
   - the three `.pulse-stat` blocks

4. **`index.html`** — the "Internal Signals" card under `#dispatches` has a **hardcoded summary paragraph** ("Latest: …") that is not driven by the catalog JSON at all. Update it by hand or it will keep pointing at whatever was last typed there.

Then follow the standard sync/push flow below, adding only the files you actually touched (don't blindly `git add` the whole tree if you only changed one entry):

```bash
git add newsletters/<new-file-or-folder> js/signals-catalog.json dispatches/internal-signals.html index.html
git status
git commit -m "Publish <edition name> to Internal Signals"
git push origin main
```

## Verify after deploy

### Core

- https://thesignal.aerovista.us/ — homepage, no console 404
- https://thesignal.aerovista.us/signal-public-theme.css — CSS 200
- https://thesignal.aerovista.us/js/signals-catalog.json — catalog JSON 200
- https://thesignal.aerovista.us/dispatches/internal-signals.html — hub loads catalog rows

### Canonical editions

- https://thesignal.aerovista.us/newsletters/editions/eod/2026-07-05-company-status/
- https://thesignal.aerovista.us/newsletters/editions/shareholder/2026-07-08-seeing-the-system/
- https://thesignal.aerovista.us/newsletters/editions/weekly/2026-06-28-resilience-weekend/
- https://thesignal.aerovista.us/newsletters/editions/milestone/2026-06-16-echoverse/

### Legacy stubs (must still 200 → redirect)

- https://thesignal.aerovista.us/newsletters/aerovista_bytecast_status_player.html
- https://thesignal.aerovista.us/newsletters/bytecast_shareholder_seeing_the_system.html
- https://thesignal.aerovista.us/newsletters/aerovista_signal_weekly_2026-06-15.html
- https://thesignal.aerovista.us/dispatches/eod-current-operating-note.html
- https://thesignal.aerovista.us/dispatches/topics/cindy-connect-launch-status.html

### Assets (new paths)

- https://thesignal.aerovista.us/newsletters/editions/eod/2026-07-05-company-status/assets/audio.mp3
- https://thesignal.aerovista.us/newsletters/editions/shareholder/2026-07-08-seeing-the-system/assets/audio.mp3

### Link preview

- https://thesignal.aerovista.us/signal.png — OG image 200
