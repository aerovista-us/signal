# Signal Registry v2 — publishing, integrity, and migration

## Purpose

Signal Registry v2 is the authoritative inventory for AeroVista formal reports, publications, dispatches, and standalone media. Existing Signal HTML pages remain delivery surfaces; `js/signals-catalog.json` is now a **generated UI view**, not an independent source of truth.

## Classification model

Every record has one top-level `contentClass`:

- `report` — formal EOD, EOW, MTD, EOM, milestone, audit, incident, compliance, etc.
- `publication` — newsletters, shareholder briefs, research/intelligence, pilot notes.
- `dispatch` — short or mutable operating/topic updates.
- `media` — genuinely standalone media.

Audience and format are independent dimensions. ByteCast, HTML, PDF, images, transcripts, and dashboards describe delivery formats/assets; they do not compete with EOD/EOW/EOM as report classes.

## Formal report contract

A finalized report must carry:

- stable `id` and matching `reportId` in the `AV-RPT-...` namespace;
- `reportClass`;
- reporting `period` (start/end or effective timestamp);
- `issuedAt`;
- `status`;
- `audience`;
- `title`, `summary`, and `owner`;
- repository-relative `canonicalPath`;
- absolute public `canonicalUrl`;
- `tags`;
- package declaration;
- complete `files[]` manifest.

The semantic validator additionally requires a valid date order, prevents a final report from being issued before its reporting period ends, and requires the canonical path to be an owned primary file.

## File manifest and portability

Every file entry identifies:

- `relationship`: `owned` or `referenced`;
- stable file ID and role;
- filename;
- file type/extension;
- MIME type;
- repository-relative path;
- byte size;
- Git blob SHA-1;
- SHA-256.

### Relationship rules

- **owned** — the file is part of the record package and must move with it.
- **referenced** — the record points to external/shared evidence but does not claim ownership or automatically move it.

A file may be owned by only one registry record. Shared material must be referenced by the other records.

## Strict packages

For a self-contained report/publication directory:

```json
{
  "package": {
    "mode": "directory",
    "root": "newsletters/editions/eom/2026-07-31-july-convergence",
    "strict": true,
    "portable": true
  }
}
```

Strict validation fails when:

- an actual file inside the package is absent from the manifest;
- an owned manifest path points outside the package;
- a file is missing;
- byte size differs;
- Git blob SHA-1 differs;
- SHA-256 differs.

This makes a directory package independently movable and verifiable.

## Generated views

Canonical records live under:

```
registry/records/
  reports/
  publications/
  dispatches/
  media/
```

Generated indexes live under:

```
registry/indexes/
  all.json
  reports.json
  publications.json
  dispatches.json
  media.json
  current.json
```

The Internal Signals UI presentation source is:

```
registry/presentation/signals-catalog.json
```

It contains UI-specific ordering, badges, section placement, and `recordId` links. The generator resolves those record IDs against Registry v2 and writes:

```
js/signals-catalog.json
```

Do **not** hand-edit `js/signals-catalog.json` as an authority record.

## Commands

Validate current records and regenerate views:

```bash
python scripts/registry_v2.py check
```

Refresh manifests from the repository, calculate/refresh byte sizes, Git blob SHA-1, and SHA-256, then validate and rebuild generated views:

```bash
python scripts/registry_v2.py refresh
```

Run regression tests:

```bash
python scripts/test_registry_v2.py
```

## New report workflow

1. Create/finalize the report and all companion assets.
2. Prefer one self-contained directory for new reports.
3. Create the Registry v2 record under `registry/records/reports/`.
4. Set its report metadata, canonical path/URL, package declaration, and seed file manifest.
5. Mark external/shared evidence as `referenced`.
6. Run `python scripts/registry_v2.py refresh` to inventory strict packages and calculate integrity values.
7. Run `python scripts/test_registry_v2.py`.
8. Commit the report/package, registry record, indexes, presentation source when needed, and generated UI catalog.
9. CI reruns `check` and fails if any generated view is stale.

## Package movement rule

To move/archive/export a record:

1. copy every `owned` file;
2. preserve every `referenced` identifier/link;
3. keep the registry record with the package;
4. verify destination size and SHA-256 before source deletion;
5. preserve old public URLs with redirects when applicable.

## Legacy content

Legacy flat files are registered in place first with `package.mode: legacy-flat`. They can be normalized into dedicated package directories later without sacrificing provenance.

Mutable `current` pages are classified as dispatches/views rather than immutable formal reports.

## Backfill status — September 9, 2026

Registry v2 currently governs **26 records**:

- 10 formal reports;
- 10 dispatches;
- 5 publications;
- 1 standalone media record.

The formal-report lineage includes the August EOM, August MTD, July EOM, July 5 EOD, June 15/21/28 EOWs, EchoVerse milestone, and May 23/29 EOW reports. The registry also covers the existing newsletter/shareholder editions, topic dispatches, Art Localized pilot publication, Vespera Macro Rails package, War Loop package, and EP02 media.

The July EOM is a useful stress test: its strict package includes the interactive report, six MP3s, ByteCast scripts/transcripts, report sections, images, styles/scripts, metadata, and source evidence, with every owned file carrying SHA-256.
