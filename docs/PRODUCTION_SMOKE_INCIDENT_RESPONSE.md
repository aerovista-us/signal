# Signal production-smoke incident response

The GitHub Actions workflow `.github/workflows/production-smoke.yml` is the owned incident route for failed production-smoke checks.

## Ownership and targets

- Primary acknowledgment owner: `@aerovista-us`
- Backup: AeroVista founder/operator using the repository Actions and Issues views (current single-maintainer fallback)
- Acknowledgment target: 4 hours from the first incident issue entry
- Restoration target: 24 hours from detection
- Incident destination: a deduplicated GitHub issue titled `[Incident] Signal production smoke failure`

A second distinct maintainer should replace the single-maintainer backup when one is available.

## Evidence captured automatically

Each failure entry records:

- workflow run URL;
- tested commit/deployment SHA;
- production origin;
- triggering event;
- failed stage;
- UTC observation time;
- final smoke assertion/output.

Repeated failures update the existing open incident instead of creating duplicates. The next successful production-smoke run adds restoration evidence and closes the incident.

## Controlled verification

A repository operator can test routing without changing production content by either:

1. manually dispatching the workflow with `force_failure: true`; or
2. temporarily merging a branch containing `.github/CONTROLLED_SMOKE_FAILURE`.

After confirming the incident was delivered, remove the marker or dispatch normally. Record both the failing run and restored passing run in issue #12 before closing it.

The production-smoke incident route is separate from the pre-merge `validate-registry` required check.
