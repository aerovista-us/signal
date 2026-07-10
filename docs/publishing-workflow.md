# Publishing workflow

How to ship a new internal Signal edition.

## Choose the type

| Type | Use for | Example path |
|------|---------|--------------|
| `eod` | Daily operating truth, company status | `editions/eod/2026-07-05-company-status/` |
| `weekly` | Weekly EOW ByteCast, full audio + visuals | `editions/weekly/2026-06-21-better-machine/` |
| `shareholder` | Shareholder briefs, positioning | `editions/shareholder/2026-07-08-seeing-the-system/` |
| `milestone` | Platform / division milestone ByteCast | `editions/milestone/2026-06-16-echoverse/` |

**Dispatch vs edition:** Short EOW summaries live in `dispatches/eow/`. Full audio editions live in `newsletters/editions/`.

## Option A — Pipeline (recommended for standard ByteCast)

1. Copy `signal_pipeline_echoverse_starter/content/echoverse-platform-update.json`
2. Set `editionType`, `date`, `folderSlug`, `catalogTitle`, `tags`, content sections
3. Drop `assets/audio.mp3` source file in `signal_pipeline_echoverse_starter/assets/`
4. Run `python scripts/build_signal.py content/YOUR.json`
5. Add entry to `js/signals-catalog.json` (or run catalog sync)
6. Deploy per [github-pages-deploy.md](./github-pages-deploy.md)

## Option B — Hand-crafted HTML

1. Create `newsletters/editions/{type}/{slug}/index.html`
2. Put media in `newsletters/editions/{type}/{slug}/assets/`
3. Use absolute paths: `/favicon.svg`, `/js/site-paths.js`, `/dispatches/internal-signals.html`
4. Add `meta.json` beside `index.html`
5. Add catalog entry to `js/signals-catalog.json`
6. If replacing a legacy flat file, leave a redirect stub at the old path

## Catalog entry

Add to `js/signals-catalog.json` under `editions` and optionally `now`:

```json
{
  "id": "weekly-2026-06-21",
  "section": "weekly",
  "title": "A Better Machine",
  "badges": [{ "type": "eow", "label": "EOW" }],
  "dateEm": "Jun 21",
  "dateYear": "2026",
  "href": "/newsletters/editions/weekly/2026-06-21-better-machine/",
  "types": ["eow", "bytecast"],
  "tags": "june 21 2026 weekly",
  "summary": "One-line description for the hub."
}
```

Filter counts and hub rows update automatically via `render-signals-hub.js`.

## Deploy checklist

1. Sync `newsletters/editions/`, `js/signals-catalog.json`, redirect stubs, `dispatches/`
2. `git push origin main`
3. Verify canonical URL + legacy stub URL (see deploy doc table)
4. Hard-refresh [Internal Signals](https://thesignal.aerovista.us/dispatches/internal-signals.html)
