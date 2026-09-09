# Signal Registry v2

Signal Registry v2 is the canonical content-record layer for The Signal.

## Authority model

One registry system, multiple content classes:

- `report` — formal EOD/EOW/MTD/EOM, audit, incident, milestone, etc.
- `publication` — newsletter, research, shareholder/public publication.
- `dispatch` — short operational or topical update.
- `media` — standalone media only. Companion ByteCast/audio stays attached to its parent record.

The registry records are authoritative. `registry/presentation/signals-catalog.json` holds presentation choices tied to registry `recordId` values, and `js/signals-catalog.json` is generated from those choices plus canonical registry metadata.

## Layout

```
registry/
  schema/content-record.schema.json
  records/
    reports/*.json
    publications/*.json
    dispatches/*.json
    media/*.json
  presentation/
    signals-catalog.json
  indexes/
    all.json
    reports.json
    publications.json
    dispatches.json
    media.json
    current.json
```

Each record carries a complete file manifest. A directory package with `package.strict: true` must list every file under its package root. This makes the package movable and auditable as a unit.

## File relationships

- `owned` — canonical package material that travels with the record during export, migration, or archive.
- `referenced` — related material that is not part of the canonical package, including external evidence and local legacy aliases/duplicates.

Local legacy aliases are still recorded with filename, role, path, file type, MIME type, size, Git blob SHA-1, and SHA-256. During migration they must be deliberately preserved, redirected, or retired; they must not disappear simply because the canonical package moves.

## Integrity

The registry refresh computes SHA-256 and Git blob SHA-1 for local files. Final owned files must have SHA-256 integrity data. Validation also checks file sizes, paths, duplicate IDs, duplicate ownership, reporting-period ordering, required classifications, canonical paths, and strict-package completeness.

## Validation and index generation

Run:

```bash
python scripts/registry_v2.py refresh
python scripts/registry_v2.py validate
python scripts/registry_v2.py build
python scripts/registry_v2.py check
```

- `refresh` expands strict package manifests and recalculates file metadata and hashes.
- `validate` verifies the authoritative records.
- `build` regenerates indexes and the UI catalog.
- `check` validates and regenerates generated views so CI can detect drift.

## Migration rule

Do not move legacy live files merely to register them. Register current canonical and legacy paths first. Physical normalization can happen later with redirects preserving live URLs and registry references recording every legacy asset that must be handled.

## Formal report minimum

A final formal report must include a stable `reportId`, report class, reporting period or effective time, issue date, status, audience, title, summary, owner, canonical URL/path, tags, package declaration, and complete file manifest.
