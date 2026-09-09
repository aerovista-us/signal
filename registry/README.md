# Signal Registry v2

Signal Registry v2 is the canonical content-record layer for The Signal.

## Authority model

One registry system, multiple content classes:

- `report` — formal EOD/EOW/MTD/EOM, audit, incident, milestone, etc.
- `publication` — newsletter, research, shareholder/public publication.
- `dispatch` — short operational or topical update.
- `media` — standalone media only. Companion ByteCast/audio stays attached to its parent record.

Presentation catalogs such as `js/signals-catalog.json` remain UI data. They are not the authoritative record.

## Layout

```
registry/
  schema/content-record.schema.json
  records/
    reports/*.json
    publications/*.json
    dispatches/*.json
    media/*.json
  indexes/
    all.json
    reports.json
    publications.json
    dispatches.json
    media.json
    current.json
```

Each record owns a complete file manifest. A directory package with `package.strict: true` must list every file under its package root. This makes the package movable and auditable as a unit.

## File relationships

- `owned` — travels with the record during export/migration/archive.
- `referenced` — external evidence or linked material; preserve the reference but do not copy it automatically.

## Validation and index generation

Run:

```bash
python scripts/registry_v2.py validate
python scripts/registry_v2.py build
python scripts/registry_v2.py check
```

`check` validates records, checks owned file existence/size/Git blob SHA-1 when provided, verifies strict package completeness, then regenerates the index views.

## Migration rule

Do not move legacy live files merely to register them. First create a valid registry record with their current paths. Physical package normalization can happen later with redirects preserving live URLs.

## Formal report minimum

A final formal report must include a stable ID, report class, reporting period/effective time, issue date, status, audience, package declaration, and complete owned-file manifest.
