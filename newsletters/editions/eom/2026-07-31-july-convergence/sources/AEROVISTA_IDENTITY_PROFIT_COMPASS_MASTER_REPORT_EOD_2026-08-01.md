# AeroVista Identity, Workspace, and Profit Compass Master Report

**Reporting date:** August 1, 2026  
**Thread EOD cutoff:** 1:37 AM Pacific Time  
**Status:** Combined architecture, implementation, handoff, risk, roadmap, and end-of-day report

---

## 1. Executive Summary

AeroVista now has two major platform pieces operating in a complementary way:

1. **A live public identity foundation**
   - Firebase Auth handles credentials, verification, recovery, and token issuance.
   - `identity-api.aerovista.us` is the public identity boundary running through Cloudflare Tunnel to NXCore.
   - AVCC remains the canonical identity authority for people, provider links, account state, profiles, preferences, access badges, roles, and audit.
   - Public cold signup is enabled at the canonical `/account/*` routes.
   - Existing AVCC people should be linked to Firebase identities through `identity_auth_links`, not recreated.

2. **A live, hardened Profit Compass private-pilot system**
   - Profit Compass is a standalone member-business tool, not AeroVista corporate accounting.
   - It supports income, expenses, products, events, CSV imports, YTD cash-basis P&L, exports, snapshots, corrections, audit history, invitations, policy acknowledgement, support grants, and controlled export/deletion workflows.
   - The Cash Commitment Map now adds cash-on-hand, upcoming commitments, expected payments, overdue detection, and a conservative safe-to-spend number.
   - The latest handoff reports `43/43` tests passing, clean builds, a healthy systemd API, persistent PostgreSQL, and restart-protected frontend and database services.
   - A hardcoded session-signing secret found during audit was rotated out of source and into a protected systemd drop-in.
   - Bigcapital remains clean, disabled, and untouched.

The current product is beyond a basic prototype. It is a credible controlled private-pilot candidate. Before increasing member count or adding heavy premium functionality, three decisions should be resolved:

1. Serialize whole-store read-modify-write operations to prevent lost updates.
2. Define and enforce the business-role permission matrix.
3. Require a separate authorized support/operator path for export and deletion fulfillment.

After those controls, the planned premium sequence is:

```text
1. Drill-down to source transactions
2. Management Report Packs + Financial Story Report
3. Decision Lab
4. Cash Compass expansion
```

---

## 2. Platform Purpose and Boundaries

### 2.1 AeroVista Workspace

AeroVista Workspace is the common front door for independently owned tools and division workspaces.

The preferred future public structure is:

```text
https://workspace.aerovista.us/
https://workspace.aerovista.us/lumina/
https://workspace.aerovista.us/lumina/image-studio/
https://workspace.aerovista.us/member-business/
https://workspace.aerovista.us/member-business/profit-compass/
```

The Workspace portal may display multiple tools, but each tool keeps its own source repository, runtime, deployment, data authority, and security boundary.

Raw LAN ports may remain available for internal operations and debugging, but members should use canonical named routes.

### 2.2 Profit Compass

Profit Compass is for AeroVista members operating their own independent businesses.

It is not currently:

- AeroVista corporate accounting
- AVCC financial reporting
- Art Localized accounting
- Division accounting
- Tax preparation
- A direct Bigcapital interface
- A bank, payment processor, or money-transmission service

### 2.3 Core storage and deployment boundary

```text
AeroVista Workspaces
└── Compiled member-facing frontend only

AeroVistaCore
└── API, financial logic, PostgreSQL, audit, private data, exports, backups,
    identity adapter, and accounting-provider boundary
```

Canonical locations:

```text
Source:
/srv/ACOS/AeroVistaCore/source/profit-compass

API runtime:
/srv/ACOS/AeroVistaCore/services/profit-compass-api

Member-finance runtime boundary:
/srv/ACOS/AeroVistaCore/services/member-finance-core

Authoritative data:
/srv/ACOS/AeroVistaCore/data/profit-compass

Static Workspace deployment:
/srv/ACOS/workspaces/member-business/profit-compass
```

Required request flow:

```text
Member browser
→ Profit Compass frontend
→ Profit Compass Member API
→ business authorization
→ accounting-provider adapter
→ current local accounting provider
```

Prohibited direct paths:

```text
Frontend → PostgreSQL
Frontend → Bigcapital
Frontend → AVCC invoice routes
Bigcapital → AVCC SQLite
Member financial data → AeroVista executive reporting
```

---

## 3. AeroVista Authentication and Authorization Model

### 3.1 Eleven layers

| Layer | Purpose | Examples |
|---|---|---|
| 1. Public access | No login required | AeroVista website, Art Localized market, booth pages |
| 2. Cloudflare edge | Protects public traffic | DNS, TLS, proxy, WAF, rate limiting, DDoS protection |
| 3. Cloudflare Tunnel | Connects domains to NXCore without exposing ports | Identity API, AVCC services, Art Localized APIs |
| 4. Cloudflare Access | Coarse entrance control for protected browser applications | Creator Console, collaborators, protected admin pages |
| 5. Tailscale | Private network perimeter | SSH, SMB, NXCore administration, internal APIs |
| 6. Application authentication | Establishes the active application session | Signed Workspace session, bearer token |
| 7. AVCC Identity | Defines the canonical person or principal | Person, email, provider links, account status |
| 8. Roles and capabilities | Defines broad authority | Founder, operator, admin, creator, reviewer |
| 9. Resource-specific grants | Defines exact scope | Booth, business, project, catalog, division |
| 10. Action-level permissions | Defines allowed operations | View, edit, publish, approve, delete, manage members |
| 11. Audit and compliance | Records sensitive activity | Login, grant changes, imports, exports, admin access |

### 3.2 Public request flow

```text
Internet user
→ Cloudflare edge
→ Cloudflare Tunnel
→ Cloudflare Access when required
→ application session
→ AVCC Identity
→ broad capability check
→ exact resource grant or service-owned membership
→ action permission
→ allow or deny
→ audit
```

### 3.3 Internal request flow

```text
Trusted user or device
→ Tailscale
→ private NXCore service
→ application session
→ AVCC Identity
→ service authorization
```

### 3.4 Clean responsibility split

```text
Cloudflare
= public perimeter

Tailscale
= private network perimeter

Application session
= proves the active login

AVCC Identity
= defines the person and broad access state

Resource grant or service membership
= defines the exact resource

Action permission
= defines what may be done

Audit
= records what actually happened
```

Cloudflare and Tailscale safely deliver a user to the application. They are not final business authorization.

---

## 4. Public Identity Stack: Current State

### 4.1 Live architecture

```text
aerovista.us /account/*
→ Firebase Auth
→ identity-api.aerovista.us
→ Cloudflare Tunnel
→ NXCore identity-gateway on port 3110
→ internal AVCC Identity API
→ AVCC SQLite identity records
```

Ownership:

| Concern | Authority |
|---|---|
| Credentials, verification, recovery, token issuance | Firebase Auth |
| Public API security boundary | NXCore Identity Gateway |
| Canonical person, profile, provider links, badges, roles, preferences | AVCC |
| Exact service resource access | Owning service, mirrored to AVCC where appropriate |

### 4.2 Public account routes

```text
/account
/account/login
/account/register
/account/verify
/account/recovery
```

Legacy Art Localized account routes redirect to the canonical account routes.

### 4.3 Current identity status

- Public identity gateway is live and healthy.
- Firebase Admin is active on NXCore.
- Cold signup is enabled.
- Profile and preference changes persist through the gateway into AVCC.
- Verified bootstrap creates or links the canonical AVCC identity.
- Verified free signup grants `aerovista.member`; it does not allow self-selected roles.
- Existing AVCC users should be linked, not duplicated.
- Social Engine remains on a separate NextAuth Credentials login until Firebase SSO is completed.

### 4.4 Identity taxonomy

```text
Identity
= the person or principal

Relationship
= how the person relates to AeroVista

System role
= protected administrative authority

Access badge
= broad service capability

Resource grant
= exact service-owned scope
```

Relevant access badges include:

```text
aerovista.member
profitcompass.pilot
artlocalized.builder
echoverse.private_catalog
summit.facilitator
```

Profit Compass should use AVCC’s canonical identity ID and broad pilot/access capability, while keeping exact business membership and financial permissions inside Profit Compass.

---

## 5. Profit Compass Current Product State

### 5.1 Latest authoritative handoff

```text
Source repo:
/srv/ACOS/AeroVistaCore/source/profit-compass

Workspace repo:
/srv/ACOS/workspaces

Latest source commit:
8671c3a
fix: close mass-assignment/idempotency gaps, harden frontend, document the system

Latest Workspace commit:
f31082e
chore(workspaces): deploy Profit Compass audit-pass frontend fixes

Working trees:
Clean

Tests:
43/43 passing
```

The latest source commit is described as a squashed commit. It includes the audit fixes plus an earlier UX round involving landing pages, faster inputs, autocomplete, form-draft autosave, and the Workspace navigation update.

### 5.2 Runtime status

```text
API health:
http://127.0.0.1:54131/v1/health → {"ok":true}

API service:
profit-compass-api → active, running, enabled

PostgreSQL:
restart: unless-stopped

Workspace nginx frontend:
restart: unless-stopped
```

### 5.3 Current member capabilities

A member can currently:

- Create and access a private business.
- Record income.
- Record direct costs and operating expenses.
- Manage products and services.
- Manage events and booths.
- Link activity to products and events.
- Correct posted transactions using reversal/replacement behavior.
- Import CSV transactions through preview, validation, confirm, and commit.
- Detect duplicate and idempotent imports.
- Generate a YTD cash-basis P&L through a custom period end.
- Export CSV and a real minimal PDF.
- Preserve report snapshots that remain unchanged after later corrections.
- Request a business JSON export.
- Request business deletion.
- Accept versioned Terms and Privacy.
- Use signed Workspace-session identity.
- Reject expired or revoked sessions.
- Enter through single-use, expiring pilot invitations.
- Use temporary support/admin access grants with reason, ticket, target, and time limits.
- View the Cash Commitment Map.

### 5.4 Cash Commitment Map

The Cash Commitment Map answers a different question than the P&L:

> What is actually safe to spend after known commitments?

It includes:

- Cash on hand
- Bills
- Payroll
- Taxes
- Subscriptions
- Other recurring commitments
- 30-, 60-, and 90-day projection
- Recurrence
- Overdue detection
- Expected customer payments
- Conservative safe-to-spend calculation

This is the first working slice of the broader Cash Compass concept.

### 5.5 UX and infrastructure improvements

The latest UX and infrastructure pass added:

- Real landing pages for `income/`, `expenses/`, and `imports/`
- Fast-typing date and amount inputs
- Autocomplete from recent vendors, customers, categories, payees, and locations
- Form-draft autosave
- A navigation link back to AeroVista Workspaces
- Restart protection for PostgreSQL
- Frontend error handling for session and network failures
- Missing-business-ID guards
- Escaping on previously unsafe HTML rendering paths

---

## 6. Private Pilot Identity and Launch Controls

Implemented controls include:

- Signed Workspace-session validation
- Signature, issuer, audience, expiration, revocation, and known-member checks
- Production startup refusal when development identity is enabled
- Explicit local-only opt-ins:

```text
PROFIT_COMPASS_DEV_IDENTITY=true
PROFIT_COMPASS_DEV_SESSION_BOOTSTRAP=true
```

- Single-use, expiring invitations
- Hashed stored invitation tokens
- Invite redemption that creates the invited member business and membership
- Export fulfillment state and temporary download expiration
- Deletion fulfillment state with review-oriented status
- Time-limited support/admin grants
- Terms and Privacy acknowledgement
- Administrative-access logging
- Pilot release and hardening documentation

### Production rule

Development identity and development session bootstrap must remain disabled for a real external-member deployment.

The local LAN preview may use development session bootstrap only when intentionally enabled and clearly treated as local development.

---

## 7. Security and Audit Work Completed

The audit fixed:

- Cross-business mass assignment on PATCH operations
- Missing idempotency on product, event, and commitment creation
- Unauthorized invite revocation
- Fragile transaction-correction replay logic
- Unguarded frontend promise rejections
- Missing-business-ID handling
- Two unescaped HTML paths
- A hardcoded live session-signing secret
- Test cleanup failures related to new cash tables

The signing secret was rotated to a random value stored only in:

```text
/etc/systemd/system/profit-compass-api.service.d/override.conf
```

Old sessions stopped working after restart, and a fresh session successfully completed an authenticated request.

---

## 8. Known Risks Requiring Decisions

### 8.1 Whole-store concurrency

Current mutations use:

```text
read entire data model
→ modify in memory
→ write entire data model
```

There is no lock around the sequence.

Two concurrent requests can read the same old state and overwrite each other. This can also defeat idempotency checks.

Recommended immediate fix:

```text
One API process
→ one in-process async mutex or mutation queue
→ serialize every read-modify-write cycle
```

This should be completed before multiple API processes or meaningful multi-member concurrency.

### 8.2 RBAC is stored but not enforced

Business roles exist:

```text
owner
bookkeeper
contributor
viewer
```

The current membership guard checks only whether membership exists. It does not enforce role permissions.

Consequently, a viewer may currently perform actions intended for an owner or bookkeeper.

A product decision is needed before implementation.

Recommended initial matrix:

| Action | Owner | Bookkeeper | Contributor | Viewer |
|---|:---:|:---:|:---:|:---:|
| View dashboard and reports | Yes | Yes | Yes | Yes |
| Add income and expense | Yes | Yes | Yes | No |
| Correct transactions | Yes | Yes | No | No |
| Import transactions | Yes | Yes | No | No |
| Manage products and events | Yes | Yes | Yes | No |
| Export reports | Yes | Yes | No | Optional |
| Manage members | Yes | No | No | No |
| Request deletion | Yes | No | No | No |
| Fulfill export/deletion | No; operator path | No | No | No |

The exact matrix should be formally approved before enforcement.

### 8.3 Export and deletion self-fulfillment

The documented pilot policy calls for reviewed fulfillment. Current code allows an ordinary business member to fulfill their own export or deletion request.

Recommended decision:

```text
Requesting member
→ creates request

Authorized support/operator
→ receives temporary support grant
→ reviews request
→ fulfills request
→ audit records completion
```

### 8.4 Performance risks

Two future scaling bottlenecks are documented:

1. `providerFor()` replays the full transaction history on frequent calls.
2. PostgreSQL writes delete and reinsert data across approximately twenty tables on each mutation.

These are not urgent at current pilot volume, but they will be the first major performance problems as transaction count and tenant count grow.

### 8.5 Other open items

- Contract tests are not yet implemented.
- End-to-end test directories are empty.
- The source and Workspace repositories have no remote configured.
- Session revocation uses a static environment list requiring process restart.
- The frontend hardcodes the API port rather than using `build.json`.
- The literal `[businessId]` directory is not a dynamic route; business context comes from query parameters or local storage.
- Deployment requires separate build, migration, and API-restart steps.

---

## 9. Bigcapital Position

Bigcapital remains:

```text
Cloned and pinned
Clean working tree
Disabled
Not started
Not modified
Not exposed
```

Profit Compass does not currently need Bigcapital to deliver its member value.

The future value of Bigcapital is in deeper accounting:

- Double-entry ledger
- Chart of accounts
- Balance sheet
- Cash-flow statement
- General ledger
- Trial balance
- Accounts receivable
- Accounts payable
- Invoicing
- Vendor bills
- Bank reconciliation
- Inventory valuation
- Accrual accounting
- Multi-currency

The member-facing Profit Compass interface should remain AeroVista-owned and simple even if Bigcapital later becomes a private provider.

No Bigcapital integration should begin until:

- Whole-store concurrency is safe.
- RBAC is enforced.
- Current local reports reconcile reliably.
- Backup and restore remain proven.
- The provider adapter can run shadow comparisons without making Bigcapital authoritative.

---

## 10. Premium Feature Roadmap

### 10.1 Milestone 1 — Drill-down to Source Transactions

Goal:

Every financial total should reveal the records that created it.

Member flow:

```text
P&L total
→ category breakdown
→ source transactions
→ transaction detail
→ import, product, event, correction, and receipt context
```

Required work:

- Clickable P&L lines
- Category drill-down
- Product and event drill-down
- Transaction detail drawer
- Source metadata
- Correction and reversal visibility
- Detailed export appendix
- Reconciliation tests

Acceptance:

- Every displayed total reconciles to source records.
- Corrected and reversed entries remain visible.
- Cross-business access remains denied.
- Exported details match report totals.

### 10.2 Milestone 2 — Management Report Packs + Financial Story Report

Goal:

Turn the P&L into a polished, explainable business report.

Suggested structure:

```text
Cover
Executive business snapshot
YTD P&L
Monthly revenue and profit trend
Comparison period
Top products
Event profitability
Largest expense categories
Cash outlook
Financial Story
Owner notes
Transaction appendix
Unaudited disclaimer
```

Financial Story v1 should use deterministic rules, not unconstrained AI.

Example:

> Revenue increased while direct costs increased faster, reducing gross margin for the period.

Every narrative statement must link to its supporting values.

Required work:

- Report templates
- Saved immutable report-pack snapshots
- Deterministic commentary rules
- Branded PDF generation
- Summary and detailed formats
- Report history
- Source links and audit evidence

### 10.3 Milestone 3 — Decision Lab

Goal:

Allow members to test decisions without changing real financial records.

Initial drivers:

- Selling price
- Units sold
- Material cost
- Production cost
- Operating expense
- Number of events
- Average event revenue
- Booth fees
- Advertising spend

Result:

```text
Current baseline
vs.
Scenario projection

Revenue
Direct costs
Gross profit
Operating expenses
Net profit
Margin
Difference from baseline
```

Required rules:

- Scenarios never post transactions.
- Money uses exact integer minor-unit calculations.
- Assumptions and results are stored separately.
- At least three scenarios can be compared side by side.

### 10.4 Milestone 4 — Cash Compass Expansion

The Cash Commitment Map is the foundation.

Cash Compass should add:

- Starting available cash
- Expected inflows
- Planned purchases
- Recurring cash rules
- Tax reserve
- Owner withdrawals
- Confidence levels
- 30-, 90-, and 180-day outlook
- Lowest projected balance
- Runway
- Low-cash dates
- Threshold alerts
- Drill-down to the items causing the warning

Required disclaimer:

> Estimated cash outlook based on balances and expected activity entered by the member.

Cash projections must remain distinct from the P&L and must not alter posted accounting records.

---

## 11. Recommended Implementation Order

### Immediate stabilization

```text
1. Add in-process mutation queue
2. Approve the RBAC matrix
3. Enforce action permissions
4. Gate export/deletion fulfillment to authorized support
5. Add contract and end-to-end tests
6. Decide repository remote and backup strategy
```

### Premium expansion

```text
7. Build source-transaction drill-down
8. Build management report packs
9. Add deterministic Financial Story
10. Build Decision Lab
11. Expand Cash Commitment Map into Cash Compass
12. Evaluate Bigcapital in shadow mode
```

---

## 12. Commit and Milestone History

The thread recorded the following major checkpoints:

| Milestone | Source commit | Workspace commit |
|---|---|---|
| Import, YTD reports, and exports | `0932cd3` | `9cd9cf6` |
| Private-pilot identity hardening | `ffffed1` | `f92d553` |
| Controlled private-pilot launch controls | `cf875b6` | Workspace unchanged |
| Cash Commitment Map | `907b7fc` | `a187926` |
| Audit, security, UX, docs, and current handoff state | `8671c3a` | `f31082e` |

Earlier development also established:

- Workspace placement and repository boundaries
- Persistent PostgreSQL records
- Transaction corrections
- Product and event profitability
- Import batches and report snapshots
- Tenant isolation
- Signed Workspace sessions
- Terms and Privacy
- Invitations
- Export and deletion request controls
- Temporary support access

The latest handoff and commit pair should be treated as current authority. Earlier commits remain useful as milestone history.

---

## 13. End-of-Day Report for This Conversation Thread

### Date

August 1, 2026, through 1:37 AM Pacific Time.

### Purpose of the thread

This report thread reviewed Profit Compass’s current architecture and implementation, aligned it with the AeroVista identity system, evaluated Bigcapital’s future role, identified premium P&L features, created the next feature roadmap, and reconciled the latest handoff and EOD evidence.

### Accomplished in the conversation

#### Architecture and routing

- Confirmed `workspace.aerovista.us` as the preferred future Workspace domain.
- Established the canonical route family for Lumina and Member Business.
- Preserved raw LAN ports for operations while naming public Workspace routes as canonical.
- Reaffirmed that one Workspace portal may host multiple independently owned tools.

#### Bigcapital strategy

- Clarified what Bigcapital could eventually add:
  - Double-entry accounting
  - General ledger
  - AR/AP
  - Invoicing and bills
  - Bank reconciliation
  - Inventory accounting
  - Balance sheet and cash flow
- Confirmed that Bigcapital should remain private, disabled, and untouched while the local provider proves the member experience.

#### Identity integration

- Mapped Profit Compass to the existing AeroVista auth layers.
- Confirmed that no second Profit Compass login platform should be built.
- Defined the ownership split:
  - Firebase for credentials
  - Identity gateway for the public boundary
  - AVCC for canonical identity and broad access
  - Profit Compass for business membership and financial permissions
- Produced a developer build brief covering session validation, capabilities, business membership, action permissions, support access, audit, route protection, environment rules, and tests.

#### Controlled private pilot

Development progress reported during the thread included:

- Trusted Workspace-session checks
- Production fail-closed protection
- Explicit development-only identity flags
- Single-use expiring invitations
- Hashed invitation tokens
- Business and membership provisioning
- Export and deletion workflow state
- Time-limited support grants
- Release and hardening documentation
- Passing migrations, tests, lint, build, and LAN smoke tests

#### Premium product direction

The thread identified the most valuable premium P&L features as those that explain, forecast, and support decisions rather than merely calculating a P&L.

A focused four-feature plan was created:

```text
Drill-down
→ Report Packs and Financial Story
→ Decision Lab
→ Cash Compass
```

#### Current-state reconciliation

The uploaded handoff and EOD documents updated the current state beyond the earlier thread milestones:

- Cash Commitment Map shipped.
- Full UX and infrastructure pass shipped.
- Full security and audit pass shipped.
- Session signing secret rotated.
- Test count increased to `43/43`.
- Latest authoritative commits became `8671c3a` and `f31082e`.
- Three critical unresolved decisions were documented.

### Current status at EOD

```text
Public AeroVista identity:
Live

Cold signup:
Enabled

AVCC canonical identity:
Live

Profit Compass API:
Healthy

Profit Compass tests:
43/43 passing

PostgreSQL:
Persistent and restart-protected

Workspace frontend:
Running and restart-protected

Cash Commitment Map:
Live

Private pilot controls:
Implemented

Bigcapital:
Clean, disabled, untouched

Repositories:
Clean, local-only, no remote configured
```

### Decisions made

1. Use AeroVista’s existing identity foundation; do not build a second login platform.
2. Keep member financial data out of AVCC.
3. Keep exact business authorization inside Profit Compass.
4. Keep Bigcapital disabled until the local provider and operational controls are mature.
5. Address locking, RBAC, and fulfillment authority before expanding pilot scale.
6. Build premium features in the order:
   - drill-down
   - report packs and Financial Story
   - Decision Lab
   - Cash Compass
7. Use `workspace.aerovista.us` as the preferred future canonical Workspace domain.

### Watch items

- Public registration is open and should be monitored for abuse.
- Social Engine still uses a separate password system.
- Existing AVCC identity conflicts require linking, not recreation.
- Profit Compass’s current data-store pattern is unsafe under meaningful concurrency.
- Business roles are not yet enforced.
- Export and deletion fulfillment authority conflicts with the documented review process.
- Contract and end-to-end test tiers remain empty.
- Profit Compass repositories have no remote.

### Recommended next session

```text
1. Implement the in-process mutation queue.
2. Approve and enforce the Profit Compass RBAC matrix.
3. Require authorized support grants for export/deletion fulfillment.
4. Add contract and browser end-to-end pilot tests.
5. Confirm a remote/backup strategy for both repositories.
6. Begin source-transaction drill-down after stabilization passes.
```

---

## 14. Overall Read

Profit Compass has crossed the line from a basic bookkeeping prototype into a useful private business-operating tool.

Its strongest current qualities are:

- Clear member-focused scope
- Strong tenant separation
- Useful P&L and import workflow
- Immutable snapshots and correction history
- Controlled pilot identity
- Increasingly credible operational controls
- A differentiated cash-commitment view
- A clean provider boundary for future accounting depth

Its main weakness is no longer missing features. It is that the underlying mutation and permission models need to catch up with the product’s growing capability.

The best strategic move is therefore:

> Stabilize concurrency and permissions first, then make the numbers deeply traceable, present them as a polished financial story, and add decision and cash-planning tools.

That path preserves the simplicity of Profit Compass while capturing the most valuable features of expensive financial-planning software.

---

## Source Basis

This combined report was grounded in the supplied project files and the implementation history reported in the conversation, including:

- `HANDOFF_EOD_2026-07-31_IDENTITY.md`
- `IDENTITY_FREE_ACCOUNT_MILESTONE.md`
- `WO-NX-018_ACCOUNT_ROUTES.md`
- `IDENTITY_AUTH_ARCHITECTURE.md`
- Profit Compass `HANDOFF.md`
- Profit Compass `KNOWN_ISSUES.md`
- `EOD_REPORT_2026-08-01.md`
- `PROFIT_COMPASS_BUILD_PROCESS.md`
- `BYTEPAD_WORKSPACE.md`
- AVCC operator handoff and documentation index

Where an earlier thread milestone differed from the newest handoff, the newest handoff was treated as the current operational authority and the earlier information was retained as historical build evidence.

---

## Appendix A — Adjacent AeroVista Platform Notes

### BytePad Workspace

The supplied BytePad workspace handoff records a production deployment of the dock-and-canvas experience. The dock can be maximized to nearly fill AVCC, while the full BytePad launcher embeds the same application full-bleed. The latest fixes separated zoom transformation from the sticky-note overlay and corrected service-worker behavior that had served AVCC `index.html` into the BytePad iframe. These changes are adjacent to Profit Compass rather than dependencies of it, but they reinforce the wider Workspace pattern: independently deployed tools can appear inside a shared AeroVista operating shell.

### AVCC operating role

AVCC remains AeroVista’s operational and identity authority rather than the accounting ledger for member businesses. Its relevant responsibilities include canonical identity, profiles, roles, badges, service capability resolution, audit, operational projects, tasks, clients, and internal integrations. Profit Compass should integrate with AVCC identity through a narrow adapter and should not reuse AVCC’s prototype invoice or SQLite financial paths for member accounting.

### Social Engine

The Social Engine is running on NXCore but still uses NextAuth Credentials with its own password system. The agreed direction is Firebase SSO using the same `aerovista-us` identity project, followed by a canonical public hostname and corrected source/deployment path. It should not become a second permanent identity authority.
