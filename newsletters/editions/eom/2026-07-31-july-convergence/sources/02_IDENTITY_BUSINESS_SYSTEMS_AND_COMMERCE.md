# AeroVista Identity, Business Systems, and Commerce Report — July 2026

## Executive Summary

July established the clearest business-system architecture AeroVista has had to date.

Public identity is now live. AVCC is positioned as the canonical commercial and operational core. Profit Compass has become a credible private-pilot product. The shared commerce backend is implemented and tested, while Gear remains protected as the live production baseline.

The remaining work is less about adding features and more about enforcing permissions, serializing unsafe mutations, protecting fulfillment workflows, and completing controlled production release paths.

## Public Identity Foundation

Current request path:

```text
aerovista.us/account/*
→ Firebase Auth
→ identity-api.aerovista.us
→ Cloudflare Tunnel
→ NXCore identity gateway
→ AVCC canonical identity records
```

### Responsibility split

- Firebase: credentials, verification, recovery, token issuance.
- Identity Gateway: public security boundary.
- AVCC: canonical person, profile, provider links, account state, roles, badges, preferences.
- Individual services: exact resource membership and action permissions.

### Public routes

- `/account`
- `/account/login`
- `/account/register`
- `/account/verify`
- `/account/recovery`

Cold signup is enabled.

Verified free signup grants `aerovista.member` but does not automatically grant builder, creator, operator, or administrative access.

Existing AVCC people should be linked to provider identities instead of duplicated.

## AVCC as the Business Core

AVCC is now defined as the canonical owner of:

- Accounts and contacts.
- Opportunities and quotes.
- Engagements and contracts.
- Projects and work orders.
- Tasks and milestones.
- Work records and costs.
- Billing entries.
- Invoices and payments.
- Profitability.
- Executive visibility.
- Commercial audit and approval evidence.

AeroCore OS owns technical execution and shared services. Division Workspaces own specialized production.

## Three-Ledger Architecture

### Activity Ledger

Records what happened:

- Tool launch.
- File upload.
- Worker completion.
- Deployment.
- Approval.
- Revision request.
- Flight completion.
- Course publication.

### Work Ledger

Converts activity into accountable work:

- Time.
- Deliverables.
- Field sessions.
- Worker usage.
- Expenses.
- Materials.
- Rework.
- Internal cost.

### Billing Ledger

Contains approved invoice candidates only.

This prevents the system from turning every click, render, or open tool into a charge.

## Billing Classifications

- hourly
- fixed_fee
- milestone
- retainer_included
- retainer_overage
- usage_based
- pass_through_expense
- internal
- warranty
- rework_non_billable
- complimentary
- written_off

Internal cost and client charge must remain separate.

## Profit Compass

### Product purpose

Profit Compass is a private member-business financial tool. It is not:

- AeroVista corporate accounting.
- AVCC accounting.
- Art Localized accounting.
- Tax preparation.
- A direct Bigcapital interface.

### Current capabilities

- Business creation.
- Member authorization.
- Income and expense tracking.
- Product and event profitability.
- CSV import.
- Validation and duplicate handling.
- Transaction corrections.
- YTD cash-basis P&L.
- Report snapshots.
- CSV and PDF export.
- Audit history.
- Export and deletion requests.
- Terms and privacy acknowledgement.
- Signed Workspace sessions.
- Pilot invitations.
- Temporary support access.
- Cash Commitment Map.

### Current verified state

- Tests: 43/43 passing.
- API healthy.
- PostgreSQL persistent.
- Frontend and database restart-protected.
- Signing secret removed from source and rotated.
- Bigcapital clean, disabled, and untouched.

### Critical unresolved controls

1. Serialize whole-store read-modify-write mutations.
2. Approve and enforce RBAC.
3. Require authorized support for export/deletion fulfillment.

### Premium roadmap

1. Source-transaction drill-down.
2. Management Report Packs and Financial Story.
3. Decision Lab.
4. Cash Compass expansion.

## AeroVista Commerce

### Gear

Gear remains the protected live storefront baseline.

July confirmed:

- Live catalog.
- Working checkout.
- Production separation.
- Dedicated operator credential.
- No sandbox disruption to Gear.

### Commerce backend

Implemented and verified:

- Store-aware catalog.
- Cart quote.
- Sandbox checkout.
- Webhooks.
- Persistent rate limiting.
- PostgreSQL.
- Store isolation.
- Rollback rehearsal.
- Safe operator tooling.

### Test state

- 58 backend tests passed.
- Dependency audit clean.
- Migrations verified.
- Production catalog unchanged.

### Remaining release gate

Production `/v1` remains intentionally offline.

A public same-URL `301` loop remains unresolved at the ingress boundary.

## Commercial Architecture Direction

The storefront model was refined:

- Share the commerce engine.
- Share API contracts.
- Share cart and checkout.
- Allow independent brand-specific frontends.

Gear remains a conventional retail experience.

Horizon becomes a gallery-first art-buying experience.

## August Handoff

1. Add Profit Compass mutation queue.
2. Approve and enforce RBAC.
3. Gate export/deletion fulfillment.
4. Add contract and browser E2E tests.
5. Resolve commerce ingress loop.
6. Complete source transaction drill-down after stabilization.
7. Confirm repository remote and backup strategy.
