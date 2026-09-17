# Signal Access & Personalization Plan

Status: implementation started
Date: 2026-09-15

## Goal
Evolve Signal from a public publication surface into a governed publication system that can also deliver Staff, Client, Creator/Collaborator, and other entitled material through AV Account without breaking existing public URLs.

## Governing principles
- Existing public material remains public unless an explicit later migration is separately approved.
- Registry metadata is descriptive before it becomes enforcement policy.
- AV Account is identity authority; Signal does not invent a second identity store.
- Capability/entitlement resolution determines protected delivery, not UI hiding.
- Agreement acceptance can become an entitlement prerequisite, but agreement records and content access remain separate concepts.
- Creator/Collaborator is a first-class audience/relationship; tax classification is not an authorization role.

## Phase 1 — Reports/Publications taxonomy + Registry contract
1. Keep `contentClass` authoritative: `report`, `publication`, `dispatch`, `media`.
2. Reports require `reportId`, `reportClass`, and reporting `period`.
3. Publications require `publicationClass` and are not forced into reporting-period semantics.
4. Registry records remain the source of truth; generated indexes/presentation are derived.
5. Preserve canonical paths and redirects during normalization.
6. Validate duplicate IDs, invalid classes/periods, missing assets, broken paths, and integrity drift.

Acceptance gate: every governed report/publication validates against Registry v2 and can be regenerated without hand-maintained catalog drift.

## Phase 2 — Audience/access metadata, non-enforcing
Add optional `access` metadata to Registry records:
- `mode`: `public`, `authenticated`, or `entitled`
- `capabilities[]`
- `accountRoles[]`
- `entitlements[]`
- `agreementRequirements[]`

Extend audience vocabulary with `creator` and `collaborator`.

During Phase 2, access metadata MUST NOT make currently public material private. It exists to make future policy explicit and testable before enforcement.

Acceptance gate: registry validation passes; current public URLs and generated public catalog remain unchanged; representative future protected records can be modeled without being published publicly.

## Phase 3 — AV Account identity + capability resolution
Integrate Signal with the existing AV Account/Identity Gateway contract. Signal consumes resolved identity/capabilities and does not maintain passwords or parallel roles.

Define normalized Signal access context:
- account identity
- role/relationship
- capabilities
- entitlements
- accepted agreement versions where required

Acceptance gate: authenticated test identities resolve to deterministic Signal access context while anonymous public access behaves exactly as before.

## Phase 4 — Protected content delivery
Introduce server-side protected delivery for Staff and entitled Clients first, then Creator/Collaborator audiences as governed packages are approved.

Rules:
- Protected files must not remain reachable from an unguarded public static path.
- UI filtering is not authorization.
- Deny by default when a protected record requires unresolved capability/entitlement/agreement state.
- Audit protected-content access decisions at an appropriate summary level.
- Public records continue through the existing public delivery path.

Acceptance gate: anonymous users cannot fetch protected assets directly; entitled identities can; public regression suite remains green.

## Phase 5 — My Signal
Build a personalized `My Signal` surface from Registry records filtered by resolved access context.

My Signal may combine:
- public reports/publications
- authenticated-member material
- Staff material
- Client-specific or client-capability material
- Creator/Collaborator material
- agreement-gated material

The Registry remains canonical. My Signal is a personalized view, not a separate content catalog.

Acceptance gate: test identities see exactly the records their access context permits, no more and no less; direct protected delivery enforces the same decision.

## Fold-in: Creator/Collaborator program
The creator collaboration plan fits into this rollout rather than becoming a separate Signal architecture:
- Phase 1: creator-produced material uses the same report/publication taxonomy and provenance/file manifest rules.
- Phase 2: `creator`/`collaborator` audiences and future capability/entitlement/agreement requirements become declarative metadata.
- Phase 3: AV Account resolves Creator/Collaborator identity and capability packages.
- Phase 4: creator workspaces, private briefs, statements, commission-related publications, or collaboration materials can use protected delivery when appropriate.
- Phase 5: My Signal becomes the personalized communication/publication surface for each collaborator.

The 1099/W-9, commission ledger, creator agreement, IP/license, and non-cash capability-value work remain governed commercial/compliance concerns outside Signal. Signal consumes their resulting entitlement/agreement state; it does not become the tax or payment authority.

## Immediate implementation slice
1. Add additive `access` schema and Creator/Collaborator audience vocabulary.
2. Add schema validation fixtures for public and future entitled records.
3. Audit current records for taxonomy drift without changing public visibility.
4. Document mapping from AV Account capability resolution to Registry `access` fields.
5. Only after those gates pass, begin identity integration.
