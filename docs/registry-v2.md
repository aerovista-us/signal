# Signal Registry v2 — publishing and migration

## Purpose

The Registry v2 layer is the authoritative inventory for formal reports, publications, dispatches, and standalone media. Existing Signal pages and URLs remain delivery surfaces.

## Classification

Every record has one top-level `contentClass`:

- `report`
- `publication`
- `dispatch`
- `media`

Reports additionally use `reportClass` such as `eod`, `eow`, `mtd`, `eom`, `audit`, `incident`, or `milestone`.

Audience and format are independent dimensions. ByteCast is normally a format/owned asset of a report or publication, not a competing top-level report type.

## New report workflow

1. Create or finalize the report content and all companion files.
2. Keep all new report-owned files in one directory when practical.
3. Add a record under `registry/records/reports/`.
4. List every owned file in `files[]` with role, path, media type, size, and Git blob SHA-1 when available.
5. Use `relationship: owned` for files that must travel with the report.
6. Use `relationship: referenced` for external evidence that should remain a link/reference.
7. Set `package.mode: directory` and `package.strict: true` for self-contained packages.
8. Run `python scripts/registry_v2.py check`.
9. Commit the record and generated `registry/indexes/` updates.
10. Update the existing Signal UI catalog only as a presentation step.

## Formal report rule

A finalized formal report must have:

- stable `AV-RPT-...` ID
- report class
- reporting period or effective timestamp
- issued date
- final status
- audience
- canonical URL
- package declaration
- complete owned-file manifest

## Package movement rule

To move/archive/export a report:

- copy every `owned` file in its manifest;
- preserve every `referenced` identifier/link;
- keep the registry record with the package;
- validate destination size/hash data before deleting the source;
- preserve old public URLs with redirects when applicable.

## Legacy migration

Do not reorganize legacy live content first. Register current paths first. Once a legacy record is complete and validated, it can be normalized into a dedicated package directory in a later migration.

## Current pilot records

- `AV-RPT-EOM-2026-08` — August 2026 EOM (legacy flat package)
- `AV-RPT-EOM-2026-07` — July 2026 EOM (strict directory package)
- `AV-RPT-EOD-2026-07-05` — July 5 EOD (strict directory package)

The July EOM is intentionally the stress-test record because it contains HTML report sections, six MP3s, ByteCast transcripts, images, scripts/styles, metadata, and source evidence.
