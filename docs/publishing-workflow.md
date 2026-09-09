# Publishing workflow

How to ship a new internal Signal edition.

> **Registry v2 rule:** For formal reports and other governed Signal content, the registry record is authoritative. `js/signals-catalog.json` is a presentation index only. See [registry-v2.md](./registry-v2.md).

## Choose the type

| Type | Use for | Example path |
|------|---------|--------------|
| `eod` | Daily operating truth, company status | `editions/eod/2026-07-05-company-status/` |
| `eom` | End-of-month rollup, everything that shipped | `editions/eom/2026-07-31-july-convergence/` |
| `weekly` | Weekly EOW ByteCast, full audio + visuals | `editions/weekly/2026-06-21-better-machine/` |
| `shareholder` | Shareholder briefs, positioning | `editions/shareholder/2026-07-08-seeing-the-system/` |
| `milestone` | Platform / division milestone ByteCast | `editions/milestone/2026-06-16-echoverse/` |

**Dispatch vs edition:** Short EOW summaries live in `dispatches/eow/`. Full audio editions live in `newsletters/editions/`.

**Classification vs format:** EOD/EOW/EOM/milestone describe report class. ByteCast, HTML, PDF, image, or dashboard describe delivery format. Do not create a separate ByteCast registry record when the audio belongs to a report.

## Formal report package first

Before publishing a formal report:

1. Create/finalize the report and every companion asset.
2. Prefer one self-contained directory per new report.
3. Create `registry/records/reports/AV-RPT-....json`.
4. List **every owned file** in the record manifest.
5. Mark external evidence as `referenced`, not `owned`.
6. For a self-contained directory set `package.mode: "directory"` and `package.strict: true`.
7. Run `python scripts/registry_v2.py check`.
8. Commit the report package, registry record, and generated `registry/indexes/`.
9. Then update the Internal Signals presentation catalog/UI.

For legacy flat reports, register existing paths first with `package.mode: "legacy-flat"`; normalize/move them later.

## Existing edition authoring

### Option A — Pipeline

1. Copy the edition content starter.
2. Set edition type/date/slug/title/tags/content.
3. Add audio and visual assets.
4. Build the edition.
5. Create/update the Registry v2 record and validate it.
6. Add/update `js/signals-catalog.json`.
7. Deploy per [github-pages-deploy.md](./github-pages-deploy.md).

### Option B — Hand-crafted HTML

1. Create `newsletters/editions/{type}/{slug}/index.html`.
2. Put all owned media/support files inside that report directory when practical.
3. Use absolute site paths where required by the page shell.
4. Add `meta.json` beside `index.html`.
5. Create the Registry v2 record and complete file manifest.
6. Run the registry validator.
7. Add the catalog presentation entry.
8. If replacing a legacy flat file, leave a redirect stub at the old path.

## Catalog entry

`js/signals-catalog.json` drives the Internal Signals UI. It may contain featured/now/section presentation metadata, but it must not be treated as the formal records database.

## Deploy checklist

1. Validate: `python scripts/registry_v2.py check`
2. Sync the report/edition package and registry files.
3. Update the UI catalog and any redirect stubs.
4. Push to `main`.
5. Verify canonical URL + legacy stub URL.
6. Hard-refresh Internal Signals.
