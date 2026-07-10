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
