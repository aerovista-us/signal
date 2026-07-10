# Site structure

Canonical layout for [thesignal.aerovista.us](https://thesignal.aerovista.us).

## Root

| Path | Role |
|------|------|
| `index.html` | Public homepage |
| `signal-public-theme.css` | Canonical theme (dispatches load `/signal-public-theme.css`) |
| `css/signal-public-theme.css` | Mirror — keep in sync with root |
| `js/site-paths.js` | Path registry (`SIGNAL_PATHS`) |
| `js/site-config.js` | Site URL, OG image, analytics |
| `js/signals-catalog.json` | Internal Signals hub catalog data |
| `js/render-signals-hub.js` | Hub renderer + search/filter |
| `newsletter-current.html` | Redirect → Internal Signals |
| `player-swamphop.html` | SwampHop player (legacy spaced filename redirects here) |

## Newsletters — editions

```
newsletters/
  editions/
    weekly/{YYYY-MM-DD-slug}/
    eod/{YYYY-MM-DD-slug}/
    bytecast/...
    shareholder/...
    milestone/...
      index.html      # canonical page
      meta.json       # catalog metadata
      assets/         # audio.mp3, infographic.png, ...
  *.html              # redirect stubs → editions/...
```

**Naming:** `{type}/{date}-{kebab-slug}/` — ISO dates, kebab-case.

**Legacy flat URLs** (`newsletters/aerovista_signal_weekly_2026-06-15.html`, etc.) remain as meta-refresh redirect stubs.

## Dispatches

```
dispatches/
  internal-signals.html    # hub (do not move URL)
  current-updates.html     # redirect stub
  eod/current-operating-note.html
  eow/current-stakeholder-update.html
  eow/2026-06-28-weekend-report.html
  topics/cindy-connect-launch-status.html
  ...
  eod-current-operating-note.html   # redirect stub
```

## Redirect stub template

```html
<meta http-equiv="refresh" content="0; url=editions/weekly/2026-06-15-systems-becoming-products/" />
<link rel="canonical" href="https://thesignal.aerovista.us/newsletters/editions/weekly/2026-06-15-systems-becoming-products/" />
```

## Safe edits on large HTML

See [large-edition-files.md](./large-edition-files.md).

## Migration scripts

- `scripts/migrate-newsletters.ps1` — one-time edition folder migration
- `scripts/migrate-dispatches.ps1` — dispatch subfolder migration
