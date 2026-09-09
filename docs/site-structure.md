# Site structure

Canonical layout for [thesignal.aerovista.us](https://thesignal.aerovista.us).

## Registry v2 — authoritative records

```
registry/
  schema/
    content-record.schema.json
  records/
    reports/
    publications/
    dispatches/
    media/
  indexes/
    all.json
    reports.json
    publications.json
    dispatches.json
    media.json
    current.json
```

The registry is the authoritative content inventory. `js/signals-catalog.json` remains the presentation catalog for the Internal Signals hub.

A formal report record contains the complete manifest for every owned HTML, MP3/AAC/WAV, image, transcript, source, data, script/style, metadata, and attachment file belonging to that report.

See [registry-v2.md](./registry-v2.md).

## Root

| Path | Role |
|------|------|
| `index.html` | Public homepage |
| `signal-public-theme.css` | Canonical theme |
| `css/signal-public-theme.css` | Theme mirror |
| `js/site-paths.js` | Path registry |
| `js/site-config.js` | Site URL, OG image, analytics |
| `js/signals-catalog.json` | Internal Signals presentation/catalog data |
| `js/render-signals-hub.js` | Hub renderer + search/filter |
| `newsletter-current.html` | Redirect → Internal Signals |
| `player-swamphop.html` | SwampHop player |

## Newsletters — editions

```
newsletters/
  editions/
    weekly/{YYYY-MM-DD-slug}/
    eod/{YYYY-MM-DD-slug}/
    eom/{YYYY-MM-DD-slug}/
    bytecast/...
    shareholder/...
    milestone/...
      index.html
      meta.json
      assets/
  *.html
```

**Naming:** `{type}/{date}-{kebab-slug}/` — ISO dates, kebab-case.

Legacy flat URLs remain redirect stubs when migrated.

## Dispatches

```
dispatches/
  internal-signals.html
  current-updates.html
  eod/current-operating-note.html
  eow/current-stakeholder-update.html
  eow/2026-06-28-weekend-report.html
  topics/cindy-connect-launch-status.html
```

## Redirect policy

Moved files keep redirect stubs at old public URLs. Registry records should preserve both canonical URL and legacy references where useful.

## Validation

```bash
python scripts/registry_v2.py check
```

For strict directory packages, validation fails if the package contains an owned file not listed in the manifest.

## Migration scripts

- `scripts/migrate-newsletters.ps1`
- `scripts/migrate-dispatches.ps1`
- `scripts/fix-dispatch-stubs.ps1`

## Safe edits on large HTML

See [large-edition-files.md](./large-edition-files.md).
