# Create Account Integration

Source: https://chatgpt.com/c/6a6aacb8-51b8-83e8-a912-e2941d7ef18a

## USER
looking at the services overall.. and how avcc has login/auth .. can we offer "create account" for aerovista.us once complete, it shows up in avcc under identity. then and then update that account under avcc-identity?

## ASSISTANT
I’m tracing the cleanest identity flow across aerovista.us, AVCC, and the AVCC Identity service so we don’t accidentally create duplicate user records or split authentication from profile management.

## ASSISTANT
The key design choice is clear: **AVCC Identity should own the person record, while the authentication provider owns credentials.** Aerovista.us should create the account through that same identity boundary—not maintain a second user database.

## ASSISTANT
## Yes — that is the right architecture

A person should be able to select **Create Account** on `aerovista.us`, complete registration, and immediately appear inside **AVCC → Identity**. AVCC Identity would then become the administrative location for managing that person across AeroVista services.

The older NeXuS integration plan already points toward centralized authentication and a unified data model, although that document described it as planned rather than confirmed live. 

### Recommended flow

```text
aerovista.us
 └─ Create Account
 └─ AeroVista Identity API
 ├─ Creates authentication user
 ├─ Creates AVCC identity record
 ├─ Sends email verification
 └─ Records registration audit event

AVCC
 └─ Identity
 └─ New identity appears as:
 Registered / Pending Verification / Pending Approval
```

Afterward, the account can be managed under **AVCC Identity**:

- Update name, contact information, business details, and preferences.
- Connect the identity to a member, customer, booth owner, creator, vendor, or staff record.
- Assign division and workspace access.
- Approve, suspend, restore, or close the account.
- View login, verification, consent, and access history.
- Trigger password reset or email-change workflows.

## Keep authentication and identity separate

This distinction matters:

| System | Owns |
|---|---|
| **Authentication provider** | Passwords, MFA, email verification, login sessions, recovery |
| **AVCC Identity** | Person record, roles, relationships, memberships, workspace access, status |
| **aerovista.us** | Registration and account-management interface |
| **Individual workspaces** | Workspace-specific settings and data |

AVCC should **never store or display passwords**. It may provide controls such as “Send password reset,” but that action should be passed to the authentication provider.

The account should have two permanent identifiers:

```text
auth_subject = Authentication provider UID
identity_id = AeroVista-wide UUID
```

Do not use the email address as the permanent identity key. Emails can change.

## Suggested account lifecycle

```text
registered
 ↓
email_verified
 ↓
pending_review
 ↓
active
 ├─ suspended
 └─ closed
```

For ordinary member accounts, you could automatically activate basic public access after email verification. Anything involving internal AVCC access, staff tools, financial information, or division workspaces should require explicit approval.

A new public user must **not** be able to choose their own role or grant themselves workspace access.

## AVCC Identity record

A practical first schema would be:

```json
{
 "identity_id": "uuid",
 "auth_subject": "provider-uid",
 "primary_email": "member@example.com",
 "display_name": "Example Member",
 "status": "pending_review",
 "identity_types": ["member"],
 "registration_source": "aerovista.us",
 "email_verified_at": null,
 "created_at": "timestamp",
 "updated_at": "timestamp"
}
```

Keep these in separate related tables or collections:

- `identities`
- `identity_emails`
- `identity_roles`
- `workspace_memberships`
- `organization_relationships`
- `identity_consents`
- `identity_audit_events`

That allows one person to simultaneously be, for example, a customer, booth owner, creator, and contractor without creating four accounts.

## Recommended service boundary

```text
Public:
identity.aerovista.us
 └─ registration, login, recovery, account portal

Internal:
AVCC → Identity
 └─ administration, roles, relationships, approvals, auditing
```

This follows the documented preference for a canonical subdomain-per-service model. 

A Gen-2 Firebase Function could serve as the public registration bridge because the AeroVista site environment was already being prepared for Node 22 Gen-2 functions. However, the deployment troubleshooting report shows that functions deployment was still incomplete when that document was written, so it should not become a dependency until deployment is verified. 

The alternative is:

```text
aerovista.us
 → Cloudflare-protected public Identity API
 → AVCC Identity service on NXCore
```

## Most important implementation rule

Do **not** do this:

```text
Create Firebase user
Create separate AVCC user
Hope synchronization works
```

Do this instead:

```text
Register once
 → create authentication subject
 → idempotently upsert AVCC identity
 → emit identity.created event
```

Use an idempotency key and unique constraint on `auth_subject`. That prevents duplicate AVCC identities when someone double-clicks registration, retries after a timeout, or the event is delivered twice.

## First build sequence

1. Establish the canonical AVCC Identity schema and `identity_id`.
2. Connect the existing AVCC login UID to identity records.
3. Add `POST /identity/register` and `GET /identity/me`.
4. Add the public Create Account page to `aerovista.us`.
5. Add Pending Identities and identity editing to AVCC.
6. Add workspace memberships and role assignments.
7. Add a member-facing Account page for profile and security management.

This gives AeroVista one reusable identity layer for the main website, member workspaces, Art Localized, EchoVerse, Summit, customer portals, and future services—without making AVCC’s internal database directly accessible from the public website.

## USER
review the way we are currently doing the art localized new user flow.. to see if we want to tag into that

## ASSISTANT
I’m checking the actual Art Localized registration, claim, and creator onboarding paths so we can see whether AVCC Identity should attach to the existing flow or replace part of it.

## ASSISTANT
I’ve confirmed the public site describes Art Localized as having builder onboarding, but the live source is not surfacing cleanly through the indexed repo search. I’m narrowing this through the deployed routes and recent implementation history rather than guessing from the marketing copy.

## ASSISTANT
## Yes — we should tag into it, not build another account system

The review shows **two Art Localized user flows already exist beside each other**:

### 1. Public AeroVista/AVCC account flow

This is already very close to the account system we were just discussing:

```text
/art_localized/account/register
/art_localized/account/login
/art_localized/account/forgot-password
/art_localized/account
```

The flow is:

```text
Firebase Auth creates UID
→ POST /api/avcc/accounts/bootstrap
→ creates avcc_accounts/{uid}
→ creates the AVCC identity card
→ GET/PATCH /api/avcc/me manages the account
```

It already includes email verification, password reset, controlled preferences, idempotent bootstrap, and operator-controlled promotion to Client. Users cannot change their own role, tier, features, or email through `PATCH /me`, and Firestore is protected from direct client writes. 

### 2. Art Localized creator/booth flow

The creator path currently operates separately:

```text
Public application
→ NXCore registration
→ operator review
→ approve and assign booth
→ manually add email to Cloudflare Access
→ builder enters artists.aerovista.us
→ Setup Wizard
→ review
→ promote and deploy
```

That flow is live and proven through the Cindy external-builder release and Trust Pass v1. 

The Cloudflare rule is intentionally:

```text
Applying does not require Cloudflare Access.
Managing an approved booth does.
```



## The current weakness

The two flows are **adjacent but not truly joined**.

Today, the same person can potentially exist as:

```text
Firebase UID
Firestore avcc_accounts record
AVCC public identity card
Cloudflare authenticated email
artist-access.json entry
assignments.json booth grant
NXCore registration applicant
```

They are generally reconciled by email. That works for the pilot, but email should not remain the permanent relationship key.

The correct next move is to put one canonical `identity_id` behind all of them.

## Recommended joined architecture

```text
AeroVista Identity
 identity_id: av_id_...
 auth_subject: Firebase UID
 primary_email: creator@example.com

 relationships:
 - participation
 - art_localized_applicant
 - art_localized_builder
 - client

 service grants:
 - service: art_localized
 booth_slug: creator-slug
 permissions:
 - booth.edit
 - booth.submit
 - assets.manage
```

Then the different systems become adapters around the same identity:

```text
Firebase Auth
→ authenticates the public account

AVCC Identity
→ owns the person and their relationships

Art Localized
→ owns applications, booths, drafts, reviews, and publication

Cloudflare Access
→ protects the creator workspace

artist-access.json
→ temporary grant cache or deployment mirror
```

## Best user experience

I would **not require an account before somebody applies for a booth**. That adds friction too early and would undo a strong part of the existing flow.

Use this instead:

```text
1. Creator submits booth application without an account.
2. Application stores normalized applicant email.
3. If already logged in, also store identity_id.
4. Confirmation offers “Create or claim your AeroVista account.”
5. Operator approves and assigns a unique booth slug.
6. Approved creator must verify/create the account before entering Setup.
7. AVCC links the application, identity, booth grant, and Cloudflare email.
8. Creator enters artists.aerovista.us and completes Setup.
```

That preserves the low-friction public application while ensuring approved creators become real AeroVista identities.

## What should change

### Promote the Art Localized registration into the AeroVista-wide registration

Canonical new routes:

```text
/account/register
/account/login
/account/forgot-password
/account
```

Keep the existing paths as redirects:

```text
/art_localized/account/register
→ /account/register?source=art-localized
```

That lets Art Localized keep using the account system without making it appear that the account only belongs to Art Localized.

### Carry intent through registration

The current founding-offer material already links to:

```text
/art_localized/account/register?intent=founding-booth
```



Preserve that idea:

```text
/account/register
 ?intent=founding-booth
 &application_id=reg_...
 &source=art-localized
```

After registration and verification, bootstrap should link that application to the resulting `identity_id`.

### Add identity linkage to the Art Localized records

Registration:

```json
{
 "registration_id": "reg_uuid",
 "identity_id": null,
 "applicant_email": "creator@example.com",
 "status": "submitted"
}
```

After account claiming:

```json
{
 "registration_id": "reg_uuid",
 "identity_id": "av_id_uuid",
 "applicant_email": "creator@example.com",
 "status": "submitted"
}
```

After approval:

```json
{
 "identity_id": "av_id_uuid",
 "service": "art_localized",
 "role": "builder",
 "booth_slugs": ["creator-slug"]
}
```

### Return the AVCC identity from the builder `/me`

The existing Art Localized `/me` contract already controls booth grants and authority. 

Extend it:

```json
{
 "identityId": "av_id_uuid",
 "email": "creator@example.com",
 "boothSlugs": ["creator-slug"],
 "capabilities": {
 "canAssignBooths": false,
 "canEditAnyBooth": false
 }
}
```

This lets the Creator Setup Wizard and AVCC both know they are dealing with the same person.

## AVCC Identity should display

A creator’s identity page should show:

```text
Identity
 Name
 Verified email
 Firebase UID
 Status

Relationships
 Participation
 Art Localized Applicant
 Art Localized Builder
 Client

Art Localized
 Application ID
 Application status
 Assigned booth
 Setup status
 Review status
 Published URL
 Cloudflare access state

Audit
 Registered
 Verified
 Applied
 Approved
 Booth assigned
 Access granted
 Published
```

From AVCC, an operator could update the person’s profile, approve a relationship, suspend a service grant, resend onboarding, or open the Art Localized assignment—but not view or modify their password.

## What should remain separate

Do not merge these concepts:

```text
Account created ≠ booth approved
Booth approved ≠ booth assigned
Booth assigned ≠ Cloudflare access granted
Cloudflare access ≠ permission to edit every booth
Builder published ≠ public hosting deployed
```

The current Trust Pass and onboarding runbook correctly keep those authority stages separate. 

## Final recommendation

Use the existing Firebase/AVCC public account flow as the **AeroVista-wide identity front door**.

Then connect Art Localized through:

```text
application.identity_id
assignment.identity_id
grant.identity_id
Cloudflare email alias → identity_id
Firebase UID → identity_id
```

So the finished flow becomes:

```text
Apply publicly
→ claim/create AeroVista account
→ AVCC Identity appears
→ operator approves Art Localized relationship
→ booth assigned
→ Cloudflare creator door enabled
→ Setup
→ Review
→ Publish
```

That gives us exactly what you described—an account created publicly on AeroVista appears in AVCC Identity and can be managed there—while preserving the proven Art Localized approval, booth-grant, Trust Pass, and publication controls.

## USER
**Accuracy check (live probes + current docs/ledger, just now)**

### Accurate today
| Layer / claim | Evidence |
|---|---|
| **1. Public access** | `aerovista.us` market/booths/account register load with **no login** |
| **2. Cloudflare edge** | Public site and artist/API hosts return **Cloudflare** headers (`CF-RAY`) |
| **3. Tunnel → NXCore (art-api)** | Docs: tunnel `art-api` → `:8098`. Live: API answers; Tailscale **`:8098` reachable** on `100.115.9.61` |
| **4. Cloudflare Access** | `artists.aerovista.us` and `art-api …/builders/me` (and `/health`) → **CF Access login** |
| **Access bypasses** | Public **analytics** + **intake registrations** POSTs hit the app (**400**, not Access login) |
| **5. Tailscale** | This machine reaches NXCore **SSH :22** and **art-api :8098** |
| **8. Roles** | Live ledger: `founder` / `operator` / `artist` (+ **scoped** `orders@`) |
| **9. Resource grants** | Per-email `boothSlugs` (Cindy → `connect-with-cindy`, DigiMart artist → `digimart`, etc.) |
| **10. Action controls** | Documented + shipped: request review, artist publish blocked, operator approve/launch, audit events |
| **11. Audit** | NXCore `GET /audit` + review/revoke/publish events in hardening docs |

### Accurate with wording fixes
| Claim | Current reality |
|---|---|
| **Tunnel examples include `artists.aerovista.us`** | **No.** Artists SPA is **Firebase Hosting + CF Access**. Tunnel is for **NXCore services** (`art-api`, etc.). |
| **CF edge protects all public traffic** | Proxied hosts yes. Access only on protected apps — not the public market. |
| **6. Application session = signed AVCC session** | Builder lane today: **CF Access session → `Cf-Access-…-Email` → `/me`**. Separate AeroVista account login is the **public Participation/Client** path, not the Creator Console door. |
| **7. AVCC Identity = central person record** | **Partially.** Artist lane = email + badges/grants. Public AVCC accounts are a **separate** track. Not one fully unified identity product yet. |

### Not accurate / not healthy right now
| Claim | Status |
|---|---|
| **Private EchoVerse / `music.aerovista.us`** | Host resolves via CF but **`/` and `/api/catalog` → 404** (origin/tunnel path broken or empty) |
| **“Future AeroVista account login” as current builder auth** | Still future/partial for builders; **CF Access is the door now** |

### Short verdict
Your layer stack is a **good architecture map**. What is **proven live**: public site open, artists + art-api behind Access, art-api on Tunnel/NXCore, Tailscale private path up, roles + booth grants + action gates real.

What to **edit in the writeup**: don’t put `artists.aerovista.us` under Tunnel; describe builder auth as **CF Access → `/me` grants**, not a full signed AVCC account session; mark **music.aerovista.us** as currently down.

## ASSISTANT
You’re right. My previous writeup **overstated how unified the identity layer is today** and incorrectly grouped `artists.aerovista.us` under the NXCore tunnel.

Based on your live probes and current ledger, the accurate current model is:

```text
Public Participation / Client lane
aerovista.us
→ Firebase account login
→ AVCC public account record
→ separate public-facing identity track

Creator / Builder lane
artists.aerovista.us
→ Firebase Hosting
→ Cloudflare Access
→ Cf-Access-Authenticated-User-Email
→ art-api /builders/me
→ role + boothSlugs from Art Localized ledger
```

Those lanes coexist, but they are **not yet one identity system**.

## Revised recommendation

We should still connect Art Localized to AVCC Identity, but **not by replacing its current authentication flow**.

The safest move is to add an identity-association layer behind the existing Art Localized controls:

```text
Cloudflare Access remains the creator door
Art Localized remains the authorization authority
AVCC Identity becomes the linked person record
```

In other words:

```text
Authentication:
Cloudflare Access email

Authorization:
Art Localized role + boothSlugs + action gates

Person/account relationship:
AVCC identity_id, when available
```

## What we should keep unchanged

Do not disturb these proven components:

- `artists.aerovista.us` remains Firebase Hosting behind Cloudflare Access.
- `art-api` remains on the Cloudflare Tunnel to NXCore `:8098`.
- `/builders/me` continues resolving the Access email.
- Art Localized continues owning `founder`, `operator`, `artist`, and scoped service roles.
- Art Localized continues owning `boothSlugs`.
- Artist publishing remains blocked until operator review and launch.
- Audit events remain in the Art Localized API and ledger.
- Public registrations and analytics remain Access-bypassed endpoints.

That is the working security boundary. We should build around it, not through it.

## Where AVCC Identity should attach

Add an optional `identityId` to Art Localized records.

### Registration record

```json
{
 "registrationId": "reg_123",
 "email": "artist@example.com",
 "identityId": null,
 "status": "submitted"
}
```

### Artist access record

```json
{
 "email": "artist@example.com",
 "identityId": "avi_123",
 "role": "artist",
 "boothSlugs": ["digimart"],
 "status": "active"
}
```

### Builder `/me`

```json
{
 "email": "artist@example.com",
 "identityId": "avi_123",
 "role": "artist",
 "boothSlugs": ["digimart"],
 "capabilities": {
 "requestReview": true,
 "publish": false,
 "approve": false,
 "launch": false
 }
}
```

The important distinction is that `identityId` is descriptive linkage. It does **not replace** the role, booth grants, or action authorization.

## Linking logic

When someone creates or verifies an AeroVista public account:

```text
Firebase email verified
→ normalize email
→ search Art Localized registrations and grants
→ if one clear person-level match exists
→ attach AVCC identity_id
→ record identity.linked audit event
```

This can be automatic when all of these are true:

- The AeroVista account email is verified.
- The email exactly matches an Art Localized applicant or artist email.
- The record is clearly associated with a person.
- No conflicting AVCC identity is already linked.

Conflicts should go to operator review.

## Do not auto-link scoped service emails

Your `orders@` example is important.

Addresses such as:

```text
orders@
support@
billing@
admin@
```

may represent operational or scoped service identities rather than people.

Those should use something like:

```json
{
 "principalType": "service",
 "identityId": null,
 "servicePrincipalId": "svc_orders_123"
}
```

Otherwise AVCC may incorrectly represent a shared inbox as a human identity.

## Updated AVCC Identity role

Today, AVCC Identity should be described as:

> An emerging person and account directory that can link to service-specific identities and grants, but is not yet the sole authentication or authorization authority for Art Localized.

Initially, the AVCC identity page could display:

```text
Identity
- Name
- Verified public account email
- Firebase UID
- AVCC account state

Art Localized relationship
- Application ID
- Access email
- Current role
- Booth grants
- Review status
- Published booths
- Last Art Localized activity
```

AVCC should read these Art Localized details from the API or a synchronized projection. It should not silently maintain a second editable copy.

## Management from AVCC

Eventually, AVCC could provide operator controls such as:

- Grant or revoke Art Localized artist access.
- Assign or remove a booth.
- Resend creator onboarding.
- Suspend a creator relationship.
- Open the review record.
- View audit history.

But those actions should call the Art Localized API:

```text
AVCC action
→ authenticated internal request
→ Art Localized API
→ update authoritative ledger
→ create audit event
→ return updated state
```

AVCC should not directly modify a duplicate local role or booth list.

## Corrected target architecture

```text
 ┌──────────────────────┐
 │ AVCC Identity │
 │ person/account link │
 └──────────┬───────────┘
 │ optional identityId
 │
┌────────────────────┐ ┌────────▼─────────┐ ┌─────────────────────┐
│ Cloudflare Access │──▶│ Art Localized API│──▶│ Roles + boothSlugs │
│ authenticated email│ │ /builders/me │ │ action authorization│
└────────────────────┘ └────────┬─────────┘ └─────────────────────┘
 │
 ▼
 Art Localized audit
```

The public account lane remains separate but linkable:

```text
aerovista.us account
→ Firebase UID
→ AVCC account
→ AVCC identity_id
→ optionally linked to Art Localized email/grant
```

## Recommended rollout

### Phase 1 — Non-breaking linkage

- Add `identityId` and `principalType` to Art Localized registrations and access records.
- Add identity-link audit events.
- Return `identityId` from `/builders/me` when linked.
- Do not alter Cloudflare Access or authorization.

### Phase 2 — AVCC visibility

- Show Art Localized relationships in AVCC Identity.
- Read authoritative roles and booth grants from Art Localized.
- Mark records as linked, unlinked, conflicting, or service-principal.

### Phase 3 — Controlled AVCC operations

- Add AVCC operator actions that call Art Localized internal endpoints.
- Require reason and operator identity.
- Preserve Art Localized audit events.
- Never allow self-promotion or self-assignment.

### Phase 4 — Optional unified login later

Only after the linkage is stable should we consider replacing or supplementing the builder door with an AeroVista account session. That is a future architecture decision, not a description of current functionality.

## Corrected verdict

**Yes, tag into the Art Localized flow—but only as identity linkage.**

Do not replace:

```text
CF Access → email → /builders/me → role + boothSlugs
```

Add:

```text
email/grant → optional AVCC identity_id
```

That gives AVCC a real view of the creator without weakening the currently working Art Localized authentication, authorization, review, launch, and audit controls.

And `music.aerovista.us` should remain explicitly marked **unhealthy: Cloudflare resolves, but origin routes return 404** until its tunnel/origin routing is repaired.

## USER
Host	Role	Live check
echoverse.aerocoreos.com
Private EchoVerse catalog (NXCore)
Up — Cloudflare Access login

## ASSISTANT
Corrected.

| Host | Role | Current status |
|---|---|---|
| `echoverse.aerocoreos.com` | Private EchoVerse catalog on NXCore | **Up — protected by Cloudflare Access** |
| `music.aerovista.us` | Separate hostname previously discussed | **Do not treat as the canonical private EchoVerse endpoint; its status remains separate unless rechecked** |

The accurate private EchoVerse path is:

```text
echoverse.aerocoreos.com
→ Cloudflare edge
→ Cloudflare Access login
→ Cloudflare Tunnel
→ EchoVerse service on NXCore
```

So my previous statement that the private EchoVerse service was unhealthy was wrong. The corrected service map should state:

> **Private EchoVerse catalog:** `echoverse.aerocoreos.com` — operational and gated by Cloudflare Access.

This also reinforces the domain split:

```text
aerovista.us
→ public company, market, customer, and participation surfaces

aerocoreos.com
→ private/internal AeroVista services protected by Access or Tailscale
```

## USER
okay, next we want free account creation on aerovista.us. this should connect to identiy backend and allow for access badges to be created by admin/founder for profile that allows additional access

## ASSISTANT
I’m mapping this against the current AeroVista account and identity code so the new signup path plugs into what already exists instead of creating another parallel user system.

## ASSISTANT
## Yes — this should be the next identity milestone

The public flow should be:

```text
aerovista.us
→ Create Free Account
→ verify email
→ Identity Backend creates canonical identity
→ profile becomes available
→ identity appears in AVCC Identity
→ founder/admin may assign access badges
→ protected services enforce those badges server-side
```

The account is free by default. Additional access is granted intentionally through AVCC rather than letting users select privileged roles during registration.

## 1. Free account creation

Create canonical routes on `aerovista.us`:

```text
/account/register
/account/login
/account/verify
/account/recovery
/account/profile
```

Registration should collect only what is needed:

- Email
- Password or supported authentication method
- Display name
- Terms and privacy acceptance
- Optional public profile information

After authentication succeeds:

```text
Authentication provider UID
→ POST /identity/bootstrap
→ create or retrieve identity_id
→ create free profile
→ create audit event
```

Example result:

```json
{
 "identityId": "avi_01J...",
 "authSubject": "firebase_uid",
 "primaryEmail": "person@example.com",
 "displayName": "Example Person",
 "status": "active",
 "accountType": "free",
 "badges": []
}
```

The bootstrap must be idempotent. Repeated requests must return the same identity rather than creating duplicates.

## 2. AVCC Identity becomes the administrative view

Once registered, the account should appear in:

```text
AVCC
→ Identity
→ People
```

The identity record should show:

```text
Profile
- Identity ID
- Display name
- Verified email
- Account state
- Registration source
- Created date
- Last login

Access
- Active badges
- Resource grants
- Workspace memberships
- Service access

Relationships
- Participant
- Client
- Creator
- Contractor
- Staff
- Vendor

Audit
- Account created
- Email verified
- Profile updated
- Badge assigned
- Badge revoked
- Access used
```

## 3. Access badges

An access badge should be a managed authorization object, not merely a visual label stored in the browser.

A badge definition might look like:

```json
{
 "badgeId": "badge_art_localized_creator",
 "slug": "art-localized-creator",
 "name": "Art Localized Creator",
 "description": "Access to the Art Localized Creator Console",
 "service": "art-localized",
 "permissions": [
 "creator.console.open",
 "booth.edit",
 "booth.submit_review"
 ],
 "assignableBy": [
 "founder",
 "identity_admin"
 ],
 "status": "active"
}
```

A badge assignment should be a separate record:

```json
{
 "assignmentId": "ba_01J...",
 "identityId": "avi_01J...",
 "badgeId": "badge_art_localized_creator",
 "status": "active",
 "assignedBy": "avi_founder",
 "assignedAt": "2026-07-29T22:48:00-07:00",
 "reason": "Approved creator application",
 "expiresAt": null
}
```

This separation lets you update a badge policy without rewriting every user profile.

## 4. Founder and admin controls

Inside AVCC Identity, authorized administrators should be able to:

- Create badge definitions.
- Edit badge descriptions and permission mappings.
- Assign badges to identities.
- Revoke or suspend badges.
- Set expiration dates.
- Require a reason or ticket.
- Review badge assignment history.
- See what resources a badge unlocks.
- Preview effective access before saving.

Founder should have unrestricted badge administration.

Other admins should receive narrower permissions, such as:

```text
identity.badges.view
identity.badges.assign
identity.badges.revoke
identity.badges.define
identity.badges.delete
```

Creating or changing badge definitions should be more restricted than assigning an existing badge.

## 5. Badges versus resource grants

This distinction is important:

```text
Badge
= category of access

Resource grant
= the exact resource they may use
```

For example:

```text
Badge:
Art Localized Creator

Resource grant:
boothSlug = connect-with-cindy
```

The badge may permit someone to enter the Creator Console and use creator actions. It must not automatically allow them to edit every booth.

For Art Localized, the effective authorization remains:

```text
identity has art-localized-creator badge
AND
identity has grant for boothSlug
AND
requested action is allowed
```

Similarly:

```text
Profit Compass Pilot badge
AND
membership in business ABC

EchoVerse Catalog badge
AND
catalog access policy

Summit Facilitator badge
AND
assigned course or workspace
```

## 6. Initial badge set

Start small and controlled:

| Badge | Purpose |
|---|---|
| `aerovista-member` | Basic signed-in AeroVista profile |
| `art-localized-applicant` | Tracks a submitted creator application |
| `art-localized-creator` | Creator Console access |
| `profit-compass-pilot` | Profit Compass private pilot |
| `echoverse-private` | Private EchoVerse catalog access |
| `summit-facilitator` | Summit facilitator resources |
| `aerovista-client` | Client portal access |
| `aerovista-staff` | Staff workspace entry |
| `identity-admin` | Identity and badge administration |
| `founder` | Highest internal authority |

I would automatically assign only the basic `aerovista-member` badge after verified registration. All elevated badges should require founder/admin action or an explicitly approved workflow.

## 7. Badge enforcement

Every protected API should ask the Identity Backend for effective access or validate a signed session containing current claims.

Example request:

```text
GET /identity/me/access
```

Example response:

```json
{
 "identityId": "avi_01J...",
 "badges": [
 "aerovista-member",
 "art-localized-creator"
 ],
 "permissions": [
 "profile.read",
 "profile.update",
 "creator.console.open",
 "booth.edit",
 "booth.submit_review"
 ],
 "resourceGrants": [
 {
 "resourceType": "art-localized-booth",
 "resourceId": "connect-with-cindy"
 }
 ]
}
```

The backend must enforce this. Hiding a button in the interface is not security.

## 8. Cloudflare Access integration

Badges and Cloudflare Access are related, but they are not the same system.

For services currently protected by Cloudflare Access:

```text
AVCC assigns badge
→ provisioning adapter evaluates badge
→ email/group is added to the appropriate Access policy
→ service still verifies its own roles and resource grants
```

For the Art Localized creator lane:

```text
Cloudflare Access
→ confirms the authenticated email

Identity Backend
→ resolves email to identity_id

Art Localized
→ verifies creator badge and boothSlugs
```

The access badge should not remove the current Art Localized booth-level controls.

## 9. Public profile badge display

Some access badges may also appear visually on a profile, but that should be an explicit setting.

Example:

```json
{
 "badgeId": "badge_art_localized_creator",
 "profileVisibility": "public",
 "displayLabel": "Art Localized Creator",
 "icon": "palette"
}
```

Internal badges should remain hidden:

```text
identity-admin
founder
billing-reviewer
support-access
```

Do not expose internal permissions, security groups, or administrative authority through public profile markup.

## 10. Recommended data model

```text
identities
identity_emails
identity_auth_links
identity_profiles

badge_definitions
badge_assignments

resource_grants
workspace_memberships
service_relationships

identity_consents
identity_audit_events
```

Important uniqueness rules:

```text
auth_subject must be unique
verified primary email must not link to conflicting people
badge assignment must be unique per identity + badge + scope
resource grant must be unique per identity + resource
```

## 11. Build order

### Phase 1 — Free account foundation

- Create canonical `/account/*` pages.
- Connect authentication to the Identity Backend.
- Create canonical `identity_id`.
- Add email verification and recovery.
- Add `/identity/me`.
- Display new accounts in AVCC Identity.
- Automatically assign only `aerovista-member`.

### Phase 2 — Badge administration

- Add badge definitions and assignments.
- Build AVCC badge management.
- Add assign, revoke, expire, and reason controls.
- Add complete audit logging.
- Calculate effective permissions server-side.

### Phase 3 — Service adapters

- Connect Art Localized identities and booth grants.
- Connect Profit Compass pilot access.
- Connect private EchoVerse access.
- Connect workspace memberships.
- Add Cloudflare Access provisioning where required.

### Phase 4 — User profile

- Add profile editing.
- Display approved public badges.
- Show private access under “My Access.”
- Add account export, deletion, and security controls.

## Acceptance criteria for the first release

The first release is complete when:

1. Anyone can create a free account on `aerovista.us`.
2. Email verification is required before activation.
3. Exactly one canonical identity is created.
4. The identity immediately appears in AVCC Identity.
5. The user can manage their basic profile.
6. The user cannot assign their own roles or badges.
7. Founder/admin can assign and revoke an access badge.
8. Protected APIs enforce the badge server-side.
9. Resource-specific access remains separately scoped.
10. Every account and access change creates an audit event.

That gives AeroVista a clean public membership layer now, while establishing the same identity and badge framework for Art Localized, Profit Compass, EchoVerse, Summit, client access, and future workspaces.

## USER
review plan and make any recommendations you see fit

**Attachments:**
- IDENTITY_FREE_ACCOUNT_MILESTONE.md

## ASSISTANT
I’m checking the plan against the current account and AVCC identity implementation, then I’ll separate what is ready to build from what should be tightened before coding.

## ASSISTANT
## Overall verdict

The plan is strong and should move forward. It correctly preserves the working Firebase account flow, keeps Cloudflare Access as the protected-app door, makes AVCC the identity authority, separates badges from resource grants, and requires server-side enforcement. 

I would approve it **with several architectural amendments before coding**. The largest issue is that the plan currently uses “badge” for too many different concepts: business relationships, workflow states, administrative authority, authorization, and optional public profile labels.

## 1. Separate five different concepts

This is the most important change.

| Object | What it means | Examples |
|---|---|---|
| **Identity** | The person | Timbr, Cindy, a member |
| **Relationship** | How the person relates to AeroVista | client, staff, contractor, creator applicant |
| **System role** | Administrative authority | founder, operator, identity administrator |
| **Access badge** | What service capability they may use | EchoVerse private, Creator Console, Profit Compass pilot |
| **Resource grant** | Which exact resource they may affect | booth `digimart`, business `abc`, Summit course `123` |

The current proposed badge list mixes all five.

### Move these out of the access-badge catalog

- `art-localized-applicant` should be an application or relationship state.
- `aerovista-client` should be a relationship, potentially paired with a client-portal access badge.
- `aerovista-staff` should be a staff relationship, potentially paired with workspace access.
- `identity-admin` should be a protected system role.
- `founder` should be a protected system role, not an ordinary assignable badge.

### Keep these as actual access badges

- `aerovista-member`
- `artlocalized.creator-console`
- `profitcompass.pilot`
- `echoverse.private-catalog`
- `summit.facilitator`

That leads to a cleaner access decision:

```text
Relationship:
creator

Access badge:
artlocalized.creator-console

Resource grant:
art-localized-booth / connect-with-cindy
```

A creator relationship alone should not open the console. A console badge alone should not grant access to every booth.

## 2. Do not expose AVCC directly as the public registration API

AVCC should remain the **logical identity authority**, but the public website should call a narrow public identity gateway:

```text
aerovista.us
→ Public Identity Gateway
→ internal AVCC Identity API
→ AVCC database
```

The gateway can be a Firebase Gen-2 function or a narrowly exposed NXCore endpoint. It should:

- Validate the Firebase ID token.
- Verify issuer, audience, expiry, and `email_verified`.
- Apply rate limits and bot controls.
- Accept only allowlisted fields.
- Add a correlation ID.
- Forward the trusted subject to AVCC.
- Never accept `authSubject`, roles, badges, or verification state directly from browser JSON.

The browser should not be able to submit this:

```json
{
 "authSubject": "someone-else",
 "emailVerified": true,
 "badges": ["founder"]
}
```

Those values must always be derived server-side from the validated token.

## 3. Add an explicit identity state machine

The plan currently jumps to:

```json
{
 "status": "active",
 "emailVerified": true
}
```

Define the lifecycle before implementation:

```text
pending_verification
→ active
→ suspended
→ closed
```

Optional operational states:

```text
merge_review
email_change_pending
deletion_requested
```

My recommendation is:

1. Firebase creates the authentication user.
2. The user verifies their email.
3. `/identity/bootstrap` accepts only a freshly issued token with `email_verified=true`.
4. AVCC creates the canonical identity.
5. AVCC assigns `aerovista-member`.

This prevents abandoned and bot-created unverified accounts from filling AVCC People. Registration attempts can still be tracked separately without creating permanent identities.

## 4. Preserve existing badge codes before renaming them

The plan proposes aliases between existing codes such as `artlocalized.builder` and newer names such as `art-localized-creator`. 

Avoid immediately replacing working codes. Use:

```text
immutable internal code
display name
deprecated aliases
```

For example:

```json
{
 "code": "artlocalized.builder",
 "displayName": "Art Localized Creator",
 "aliases": ["art-localized-creator"],
 "deprecated": false
}
```

A safe migration pattern is:

```text
dual-read
single-write canonical code
backfill existing assignments
measure remaining alias usage
remove old alias later
```

I would also standardize internal codes on the existing namespaced pattern:

```text
aerovista.member
artlocalized.creator
echoverse.private_catalog
profitcompass.pilot
summit.facilitator
avcc.identity_admin
```

The UI can still show friendly labels with spaces.

## 5. Protect founder and administrative authority separately

`founder` should not appear in the normal “Assign Badge” selector.

Recommended controls:

- Founder identity is seeded out-of-band.
- Founder authority cannot be granted through the public API.
- Founder cannot be deleted through the normal UI.
- `identity_admin` cannot assign founder.
- An administrator cannot assign permissions exceeding their own delegation ceiling.
- Administrative-role changes require a reason and complete audit record.
- Emergency recovery uses a documented break-glass procedure.

A delegated badge administrator may assign something like EchoVerse private access, but should not automatically be able to create new permission definitions or grant themselves broader administrative power.

## 6. Add immediate revocation behavior

Cloudflare Access sessions can remain active after an AVCC badge is revoked. Therefore:

```text
Cloudflare Access = coarse door
Service API = final authorization decision
```

When a badge is revoked:

1. AVCC marks the assignment revoked immediately.
2. Effective access changes immediately.
3. Protected API mutations begin denying access immediately.
4. Cloudflare provisioning removes the email or group asynchronously.
5. Any remaining Cloudflare session is harmless because the service API denies the action.

Add an `accessVersion` to the identity:

```json
{
 "identityId": "avi_...",
 "accessVersion": 14
}
```

Increment it whenever badges, grants, roles, or status change. Services can cache access briefly, but sensitive mutations should validate the current version or resolve access directly.

Define a revocation target, such as:

```text
AVCC/API revocation: immediate
Service cache revocation: within 60 seconds
Cloudflare door removal: within 5 minutes
```

## 7. Treat Cloudflare provisioning as an asynchronous job

Do not make badge assignment depend on a fragile synchronous Cloudflare API call.

Use an outbox:

```text
badge assigned
→ database transaction commits
→ provisioning job created
→ Cloudflare adapter retries
→ provisioning state updated
```

Expose the distinction in AVCC:

```text
Authorized: Yes
Protected-app door: Provisioning / Ready / Failed / Revoking
```

Add reconciliation so AVCC can detect:

- Badge exists but Cloudflare access is missing.
- Cloudflare access exists but the badge was revoked.
- Email changed but Access still contains the old address.
- Shared/service mailbox was incorrectly linked to a person.

## 8. Add service principals now

Addresses such as `orders@`, `billing@`, or shared operator mailboxes should not become person identities.

Add:

```text
principal_type:
- person
- service
- shared_mailbox
```

Example:

```json
{
 "principalType": "service",
 "servicePrincipalId": "svc_orders",
 "email": "orders@example.com",
 "identityId": null
}
```

This prevents AVCC People from showing a shared inbox as a human and prevents accidental public profiles.

## 9. Separate access badges from public profile badges

The plan already says public badge display should be opt-in, which is good. 

I would go one step further: do not use the authorization record itself as the public display record.

```text
Access badge:
echoverse.private_catalog

Optional profile badge:
EchoVerse Contributor
```

An internal permission change should not unexpectedly alter a public profile. Public badges should be explicit projections approved for display.

Never expose:

- Founder
- Identity administrator
- Staff administration
- Billing access
- Support access
- Internal workspace access
- Security or operational groups

## 10. Change “accountType: free” to a clearer field

`accountType` may later be confused with person versus service account.

Use:

```json
{
 "principalType": "person",
 "membershipPlan": "free",
 "status": "active"
}
```

That leaves room for:

```text
membershipPlan:
free
client-sponsored
premium
internal
```

without changing what kind of identity it is.

Also preserve historical Participation records instead of overwriting them. Migration should add the new membership state and relationship while retaining original timestamps and source information.

## 11. Add email-change and identity-conflict workflows

Email must remain an identifier attached to a person, not the person’s permanent key.

For an email change:

```text
add new email
→ verify new email
→ check conflicts
→ set primary
→ update adapters
→ retain old email as historical alias or remove per policy
```

For an Art Localized creator whose Cloudflare email already exists:

```text
verified AeroVista identity
→ exact email match
→ no conflicting identity
→ link identityId
```

Any conflict should become an AVCC review case. Never merge identities automatically based only on name similarity.

## 12. Strengthen audit events

Every meaningful identity and access event should contain:

```json
{
 "eventType": "badge.assignment.revoked",
 "actorIdentityId": "avi_founder",
 "targetIdentityId": "avi_member",
 "reason": "Creator access ended",
 "before": {},
 "after": {},
 "correlationId": "req_...",
 "source": "avcc-console",
 "occurredAt": "timestamp"
}
```

The audit log should be append-only from ordinary application paths.

Add events for:

- Registration completed
- Identity created
- Profile changed
- Email changed
- Relationship created or ended
- Badge assigned, suspended, expired, or revoked
- Resource grant created or revoked
- Cloudflare provisioning succeeded or failed
- Access denied
- Identity suspended
- Account export or deletion requested

## 13. Add a pre-public security slice

Before marketing the account page publicly, include:

- Turnstile or equivalent bot protection.
- Signup and recovery rate limiting.
- Strict production CORS.
- Generic login/recovery errors to reduce account enumeration.
- Terms and privacy policy version stored with consent timestamp.
- Feature flag or registration kill switch.
- Session revocation support.
- Alerting for signup spikes and repeated bootstrap failures.
- Backup and restore test for identity tables.
- Negative authorization tests.

## Recommended rollout

### Phase 0 — Architecture decisions

Finalize:

- AVCC as logical authority.
- Thin public identity gateway.
- Firebase Auth for Phase 1.
- Canonical internal code naming.
- Identity state machine.
- Relationship versus access taxonomy.
- Founder protection.
- Revocation and provisioning rules.

### Phase 1A — Internal foundation

Build:

- `/account/*`
- Verified-token bootstrap
- Canonical identity
- `aerovista.member`
- AVCC People visibility
- Profile update allowlist
- Audit events
- Migration dry run

Test with founder and test identities only.

### Phase 1B — Limited account launch

Enable invite-only or low-visibility signup.

Measure:

- Signup completion
- Verification rate
- Bootstrap errors
- Duplicate conflicts
- Profile update errors
- Audit completeness

### Phase 2 — Minimum badge administration

Before public marketing, finish:

- Assign
- Revoke
- Suspend
- Expire
- Required reason
- Effective-access preview
- Server-side enforcement
- Protected founder/admin authority

### Phase 3 — Service adapters

Connect services one at a time:

1. Art Localized
2. Profit Compass
3. EchoVerse
4. Summit

Each adapter should have its own test and rollback path.

## My recommendations on the four open questions

### 1. AVCC as the authority

**Yes.** AVCC should own canonical identities, relationships, access definitions, assignments, grants, and audit.

However, use a separate narrow public gateway rather than exposing the main AVCC backend directly.

### 2. Firebase Auth for Phase 1

**Yes.** Keep Firebase for the initial release. Replacing authentication while also redesigning identity and authorization creates unnecessary risk.

Treat Firebase as replaceable authentication infrastructure:

```text
Firebase UID
→ identity_auth_link
→ canonical AVCC identity
```

That makes a later migration possible without changing identity IDs.

### 3. Art Localized approval workflow

Use **one operator approval action** that initiates several auditable operations:

```text
approve creator
→ create creator relationship
→ assign creator-console badge
→ create booth resource grant
→ enqueue Cloudflare provisioning
```

The Cloudflare step should be asynchronous and visible as pending/failed/ready. Do not require the operator to remember three unrelated manual steps.

### 4. Phase 1 versus Phase 1+2 before public marketing

Complete **Phase 1 plus the minimum Phase 2 administration controls** before publicly promoting account creation.

The route may be deployed earlier behind a feature flag for internal testing, but the advertised milestone includes founder/admin badge management. Launching publicly with only profile creation would technically work but would leave the central promise unfinished.

## Revised milestone exit criteria

I would expand the current ten criteria to include:

1. Public signup works.
2. Email verification is enforced server-side.
3. Exactly one canonical identity is created.
4. Unverified or conflicting identities are rejected safely.
5. Identity appears in AVCC People.
6. User can edit only allowlisted profile fields.
7. User cannot self-elevate.
8. Founder/admin can assign, suspend, expire, and revoke allowed access.
9. Founder authority cannot be assigned through normal badge administration.
10. Protected APIs enforce access badges server-side.
11. Resource grants remain separately scoped.
12. Revocation takes effect within the defined SLA.
13. Cloudflare provisioning is observable and reconciled.
14. Person and service principals remain separate.
15. Every identity and access mutation creates an audit event.
16. Rate limiting, consent capture, and registration kill switch are operational.
17. Migration can be rolled back without losing existing Participation, Client, or Art Localized grants.

## Final recommendation

Proceed, but revise the plan before implementation around these four principles:

```text
Identity is the person.
Relationships describe the business connection.
Access badges grant capabilities.
Resource grants define exact scope.
```

The submitted plan is already pointed in the right direction. These changes prevent badges from becoming another overloaded role system and make revocation, Cloudflare synchronization, founder safety, and future service expansion much more reliable. 

I could not independently inspect the current AVCC repository through the connected GitHub search, so implementation-state references above rely on the plan’s documented current-state inventory rather than a fresh code audit.

## USER
**Attachments:**
- IDENTITY_FREE_ACCOUNT_MILESTONE(1).md

## ASSISTANT
I’m reviewing the revised milestone against the recommendations we just made, focusing on whether any material gaps or contradictions remain before implementation.

## ASSISTANT
## Review verdict

This revision is **substantially stronger and ready for Phase 0 sign-off**. It correctly incorporates the major architectural corrections:

- Identity, relationships, system roles, badges, and resource grants are separated.
- AVCC remains the logical authority without exposing its main API publicly.
- Firebase stays as replaceable authentication infrastructure.
- Cloudflare Access remains a coarse protected-app door.
- Services make the final authorization decision.
- Badge revocation, Cloudflare synchronization, service principals, public badge projection, and append-only audit are covered.
- The code-audit section distinguishes what exists from what is only planned. 

I would make **six final decisions or edits** before declaring Phase 0 complete.

## 1. Resolve the “identity versus principal” wording

The document says:

> Identity is the person.

But the taxonomy also allows an identity to be a non-person principal.

Choose one consistent model. I recommend:

```text
Principal = anything that can authenticate or receive access
Person identity = a human principal
Service principal = an application or automated service
Shared mailbox principal = a shared operational address
```

Suggested root model:

```json
{
 "principalId": "avp_...",
 "principalType": "person",
 "identityId": "avi_..."
}
```

For the first release, you can keep the existing AVCC user table as the implementation, but the documentation should avoid calling `orders@` an identity.

A cleaner principle set would be:

```text
A principal is the access subject.
A person identity represents a human.
Relationships describe business connection.
Access badges grant capabilities.
Resource grants define exact scope.
```

## 2. Choose the Art Localized canonical badge code now

The plan currently gives both of these possible directions:

```text
artlocalized.creator
artlocalized.builder
```

Do not leave that ambiguous through implementation.

Because `artlocalized.builder` is already seeded and used, I recommend:

```json
{
 "code": "artlocalized.builder",
 "displayName": "Art Localized Creator Console",
 "kind": "access",
 "aliases": [
 "artlocalized.creator",
 "art-localized-creator"
 ]
}
```

For this milestone:

- Continue writing `artlocalized.builder`.
- Dual-read the aliases.
- Do not introduce a second active definition.
- Reconsider renaming only after all consumers have migrated.

The public-facing label can still say **Art Localized Creator**.

## 3. Pick the NXCore Identity Gateway

The document leaves one implementation choice unresolved. My recommendation is:

```text
identity-api.aerovista.us
→ Cloudflare edge
→ narrow public routes
→ Cloudflare Tunnel
→ NXCore Identity Gateway
→ internal AVCC Identity API
```

The gateway itself should **not** require Cloudflare Access because public users must be able to register and sign in. Only an exact allowlist of public identity endpoints should bypass Access:

```text
POST /v1/bootstrap
GET /v1/me
PATCH /v1/me
GET /v1/me/access
POST /v1/verification/resend
POST /v1/recovery/request
```

Administrative and internal routes remain unavailable through that public hostname.

This fits the current NXCore-centered backend model and avoids making Firebase Functions deployment another prerequisite.

## 4. Add an authorization precedence policy

The plan defines the pieces but not yet how conflicting signals are resolved.

Add a deny-first policy:

```text
1. Unknown principal → deny
2. Suspended or closed principal → deny
3. Revoked, suspended, or expired assignment → ignore
4. Missing required access badge → deny
5. Missing required resource grant → deny
6. Resource grant outside its scope → deny
7. Explicit service deny → deny
8. Otherwise permit the specifically requested action
```

Also define:

- Founder does not silently bypass service resource boundaries unless explicitly documented.
- An expired badge is treated as absent.
- An expired resource grant is treated as absent.
- Cloudflare access alone never authorizes an application action.
- Public profile badges have no authorization effect.

This will prevent each service adapter from inventing slightly different access behavior.

## 5. Add a source-of-truth matrix

The plan correctly says resource grants may remain service-owned initially. Make the authority explicit:

| Data | Authoritative system |
|---|---|
| Person identity | AVCC |
| Authentication subject link | AVCC |
| System role | AVCC |
| Access badge definition | AVCC |
| Badge assignment | AVCC |
| Art Localized booth grant | Art Localized API |
| Art Localized mirrored grant | AVCC, read-only projection |
| Cloudflare provisioning state | AVCC provisioning adapter |
| Cloudflare actual membership | Cloudflare |
| Public profile projection | AVCC Identity |
| Identity audit | AVCC |
| Service action audit | Owning service |

The key rule should be:

> A mirrored resource grant may support display and aggregated access resolution, but only the authoritative service may create or mutate it.

That avoids AVCC and Art Localized both believing they own `boothSlugs`.

## 6. Add transactional and idempotency requirements

The one-click Art Localized approval workflow spans several systems:

```text
relationship
badge
booth grant
Cloudflare provisioning
audit
```

It cannot be one distributed transaction. Define the reliable sequence:

```text
1. Create approval operation with idempotency key
2. Commit local authoritative changes
3. Write outbox events in the same transaction
4. Process service and Cloudflare jobs
5. Retry safely
6. Display partial provisioning state
7. Reconcile until complete
```

Suggested operation states:

```text
pending
applying
partially_applied
complete
failed
reversing
reversed
```

Every assignment and provisioning command should carry:

```json
{
 "operationId": "op_...",
 "idempotencyKey": "creator-approval:registration-id",
 "correlationId": "req_..."
}
```

This prevents double-clicks or retries from creating duplicate badges or booth grants.

## One additional acceptance test

Add a full vertical test before public launch:

```text
Create free account
→ verify email
→ bootstrap canonical identity
→ confirm aerovista.member only
→ attempt protected service access and receive denial
→ founder assigns service badge
→ access still denied without resource grant
→ founder/operator creates resource grant
→ access succeeds
→ revoke badge
→ API denies within revocation SLA
→ Cloudflare removal eventually reconciles
→ all events visible in audit
```

That single journey proves the architecture works rather than only proving each component individually.

## Final status

I would mark the document:

```text
Architecture: Approved
Phase 0: Nearly complete
Implementation: Blocked only on three explicit decisions
```

Those three decisions are:

1. Adopt `principal` as the umbrella access subject.
2. Keep `artlocalized.builder` as the current canonical code.
3. Select the NXCore narrow public Identity Gateway.

Once those are recorded, the plan is ready to break into work orders for Phase 1A.

## USER
GitHub vs local

There is no aerovista-us/aerovista-command-center GitHub repo.

Local AVCC remote is aerovista-us/ACOS.

Plan inventory should follow the local code audit, not GitHub folder names or doc-only claims.

What the code actually has

Identity Console, badge_definitions / user_badges, assign API, HMAC assign/revoke, founder guards, sessions, audit, seeded codes including artlocalized.builder.



Critical gaps the prior plan overstated

Claim	Reality

Full assign/revoke in console

UI has canRevokeBadges; browser revoke route missing (HMAC revoke only)

Badges = authorization

Console expands access_role; WO-NX-012 says badges are recognition only — split brain

Ready for public identity

No gateway, accessVersion, principalType, identity resource grants, or CF outbox

Best choice

AVCC = logical authority (extend existing tables; don’t invent a second identity DB).

Public Identity Gateway (prefer NXCore-narrow over new Firebase Functions unless you explicitly accept Gen-2).

Adopt your five-concept taxonomy before coding.

Keep Firebase for Phase 1; verified-only bootstrap.

Ship 1A → 1B → min Phase 2 before marketing signup.

Split recognition vs access badges so WO-NX-012 and console auth don’t conflict.

One Phase 0 decision still open: gateway host = NXCore vs Gen-2.

## ASSISTANT
That correction is the right one, and it materially tightens the plan.

## Authoritative implementation baseline

For this milestone, treat the following as source of truth:

```text
Local AVCC working tree
→ remote: aerovista-us/ACOS
→ current database schema and routes
→ current Identity Console behavior
```

Do not plan against a nonexistent `aerovista-us/aerovista-command-center` repository, and do not assume a feature exists merely because an architecture document describes it.

The verified foundation is:

- Identity Console exists.
- `badge_definitions` and `user_badges` exist.
- Browser badge assignment exists.
- Browser badge revocation is missing.
- HMAC assignment and revocation exist.
- Founder protection exists.
- Sessions and revocation helpers exist.
- Audit infrastructure exists.
- `artlocalized.builder` is already seeded.
- Badge semantics are currently inconsistent between recognition and authorization.

## Phase 0 decision: use the NXCore Identity Gateway

My recommendation is to formally choose:

> **NXCore-hosted narrow Public Identity Gateway**

Not Firebase Gen-2 for this milestone.

### Why NXCore is the better fit

It avoids introducing another deployment surface while the identity authority, audit, badge model, and internal APIs already live around AVCC/NXCore.

It also gives you one controlled boundary:

```text
aerovista.us
→ Cloudflare
→ identity-api.aerovista.us
→ Cloudflare Tunnel
→ NXCore Public Identity Gateway
→ internal AVCC Identity API
```

The public gateway should be a separate process or tightly separated router, not simply public exposure of the existing AVCC API.

## Public gateway scope

Only expose the small set required for member accounts:

```text
POST /v1/bootstrap
GET /v1/me
PATCH /v1/me
GET /v1/me/access
POST /v1/account/recovery
POST /v1/account/verification/resend
POST /v1/account/logout-all
```

Administrative endpoints remain internal:

```text
/users
/badges
/badges/assign
/badges/revoke
/roles
/audit
/diagnostics
/provisioning
```

The gateway must derive these from the verified Firebase token:

- Firebase UID
- Email
- Email verification state
- Token issuer
- Token audience

It must never accept those as trusted browser fields.

## Keep Firebase for Phase 1

The correct division is:

```text
Firebase Auth
= login credentials, email verification, recovery, token issuance

NXCore Identity Gateway
= public security boundary

AVCC
= canonical identity, relationships, roles, access badges, audit
```

This allows Firebase to be replaced later without replacing the AVCC identity ID.

```text
firebase_uid
→ identity_auth_link
→ AVCC user / external identity ID
```

## Fix the badge split before adding public accounts

This is the most important schema change before launch.

Add a clear badge classification such as:

```text
badge_definitions.kind

recognition
access
profile
```

Recommended meanings:

```text
recognition
→ achievements, acknowledgements, minted credentials
→ no authorization effect

access
→ capabilities enforced by APIs
→ assignment and revocation affect accessVersion

profile
→ optional public-facing labels
→ no authorization effect
```

Do not let an `access_role` field silently turn a recognition badge into system authority.

System roles remain separate:

```text
users.role
→ founder
→ operator
→ identity_admin
→ user
```

Access badges remain service capabilities:

```text
artlocalized.builder
echoverse.private_catalog
profitcompass.pilot
summit.facilitator
aerovista.member
```

## Keep `artlocalized.builder`

Do not rename the live badge during this milestone.

Use:

```json
{
 "code": "artlocalized.builder",
 "kind": "access",
 "displayName": "Art Localized Creator",
 "aliases": [
 "artlocalized.creator",
 "art-localized-creator"
 ]
}
```

Write the existing canonical code and read aliases only for compatibility.

## Required schema additions

Extend the existing AVCC model instead of creating a second identity database.

### Users or principals

Add:

```text
external_identity_id
principal_type
membership_plan
access_version
registration_source
email_verified_at
```

Suggested values:

```text
principal_type:
person
service
shared_mailbox

membership_plan:
free
client-sponsored
premium
internal
```

### Authentication links

Add a dedicated link table:

```text
identity_auth_links

id
user_id
provider
provider_subject
provider_email
verified_at
created_at
last_used_at
```

Unique constraint:

```text
provider + provider_subject
```

### Badge definitions

Add:

```text
kind
authorization_effect
public_visibility
aliases
deprecated_at
```

### Badge assignments

Ensure support for:

```text
status
assigned_by
assigned_at
suspended_at
expires_at
revoked_at
revoked_by
reason
scope
```

### Resource grants

Do not immediately move Art Localized booth authority into AVCC.

Use AVCC as an aggregate view:

```text
resource_grants

identity_id
service
resource_type
resource_id
authority
external_reference
status
last_synced_at
```

For Art Localized:

```text
authority = artlocalized-api
resource_type = booth
resource_id = digimart
```

Art Localized remains the write authority for `boothSlugs`.

## Immediate code gaps to fix

Before public account marketing, the minimum Phase 2 must include:

### Browser revoke parity

The console already understands `canRevokeBadges`, so add the missing browser API:

```text
POST /api/identity/users/:id/badges/:badgeId/revoke
```

Require:

- Authorized admin permission
- Founder target guards
- Reason
- Audit event
- `accessVersion++`
- Idempotent behavior

### `accessVersion`

Increment whenever any access-affecting property changes:

- Access badge assigned
- Access badge suspended
- Access badge expired
- Access badge revoked
- Resource grant changed
- System role changed
- User suspended or closed

Recognition and profile badges should not increment it.

### Effective access resolver

Create one canonical resolver used by:

- `/v1/me/access`
- HMAC identity resolve
- Art Localized adapter
- EchoVerse adapter
- Profit Compass adapter
- Summit adapter

Example result:

```json
{
 "identityId": "avi_...",
 "status": "active",
 "accessVersion": 12,
 "roles": [],
 "accessBadges": [
 "aerovista.member",
 "artlocalized.builder"
 ],
 "resourceGrants": [
 {
 "service": "artlocalized",
 "resourceType": "booth",
 "resourceId": "digimart",
 "authority": "artlocalized-api"
 }
 ]
}
```

## Revised rollout

### Phase 0

Lock these decisions:

- Local AVCC code is authoritative.
- `aerovista-us/ACOS` is the repository remote.
- NXCore hosts the Public Identity Gateway.
- Firebase remains Phase 1 authentication.
- Badge kinds are separated.
- `artlocalized.builder` remains canonical.
- Founder stays a system role.
- Art Localized retains booth-grant authority.

### Phase 1A

Internal-only:

- Add `/account/*`.
- Verify Firebase token server-side.
- Require verified email.
- Bootstrap canonical AVCC identity.
- Assign only `aerovista.member`.
- Add principal type and auth link.
- Show identity in AVCC People.
- Add profile allowlist.
- Add audit events.
- Add feature flag.

### Phase 1B

Invite-only:

- Exercise real signup.
- Check duplicate handling.
- Measure verification failures.
- Validate migration from Participation.
- Confirm sessions and logout-all.
- Test rollback.

### Minimum Phase 2

Before public marketing:

- Split badge kinds.
- Add browser revoke route.
- Add suspend and expiry handling.
- Add `accessVersion`.
- Add effective-access resolver.
- Protect founder/admin roles.
- Require reasons.
- Add negative authorization tests.

### Phase 3

Adapters, one at a time:

1. Art Localized
2. Profit Compass
3. EchoVerse
4. Summit

## Updated Phase 0 ADR

The final decision can now be recorded as:

```text
Decision:
Use an NXCore-hosted Public Identity Gateway.

Reason:
AVCC already contains the identity, badge, session, founder-guard,
HMAC, and audit foundations. A narrow NXCore gateway avoids exposing
the main AVCC API and avoids adding Firebase Gen-2 deployment as a
milestone dependency.

Authentication:
Firebase Auth for Phase 1.

Identity authority:
AVCC in the aerovista-us/ACOS codebase.

Authorization:
AVCC system roles + access badges, with service-owned resource grants.

Cloudflare:
Coarse protected-app door only; service APIs remain final authority.
```

With that decision, Phase 0 is no longer open conceptually. The remaining work is converting these decisions into schema migrations, route work orders, and test cases.

## USER
Locking Phase 0 into the milestone doc: NXCore gateway, badge kinds, schema, and the revised rollout.



Phase 0 is locked in docs/IDENTITY_FREE_ACCOUNT_MILESTONE.md.



Recorded decisions:



Gateway: NXCore identity-api.aerovista.us (not Gen-2)

Auth: Firebase Phase 1 → identity_auth_links → AVCC

Badge kinds: recognition | access | profile before public accounts

Canonical AL code: keep artlocalized.builder

Booth grants: art-api write authority; AVCC aggregate mirror

Also noted in NXCORE_BACKEND.md and AVCC_PUBLIC_ACCOUNTS.md. Next work is schema migrations, route WOs, and tests — starting Phase 1A when you want to code.

## ASSISTANT
Good. **Phase 0 is complete and the milestone is now implementation-ready.**

The architecture is locked around the right boundaries:

- NXCore hosts `identity-api.aerovista.us`.
- Firebase handles Phase 1 authentication only.
- AVCC remains the canonical identity authority.
- Badge kinds are separated before public rollout.
- `artlocalized.builder` remains the canonical live code.
- Art Localized retains booth-grant write authority.
- AVCC receives an aggregate, read-oriented access view.

The clean Phase 1A execution order is:

1. **Schema migration**
 - `identity_auth_links`
 - `principal_type`
 - `membership_plan`
 - `access_version`
 - badge `kind`
 - alias/deprecation fields

2. **Public Identity Gateway**
 - Firebase token validation
 - verified-email enforcement
 - strict request allowlists
 - correlation IDs, rate limits, feature flag

3. **Verified bootstrap**
 - Idempotent identity creation
 - assign only `aerovista.member`
 - create auth link
 - emit audit events
 - expose identity in AVCC People

4. **Canonical public account routes**
 - `/account/register`
 - `/account/login`
 - `/account/verify`
 - `/account/recovery`
 - `/account/profile`
 - redirects from legacy Art Localized account routes

5. **Tests**
 - unverified token denied
 - duplicate bootstrap returns same identity
 - conflicting auth subject/email denied safely
 - profile escalation fields ignored or rejected
 - member badge assigned exactly once
 - audit completeness
 - migration rollback

The first work order should be **Phase 1A Schema Foundation**, because every gateway and route decision depends on those canonical columns and constraints. After that, the gateway and bootstrap can be built without temporary compatibility hacks.

<details open>
<summary>Current branch: USER: Correct — the **Edit Team Member** modal has no Delete. That’s a UI gap, not a missing backend. **Ho</summary>

### USER
Correct — the **Edit Team Member** modal has no Delete. That’s a UI gap, not a missing backend.

**How to remove Jeanette from Team today**
1. Close that edit modal 
2. On her **Team card** in the Team grid, use the trash **Delete** button 
3. Confirm 

That hits `DELETE /api/team/:id` and removes the Team CRM record.

**What it does *not* do** 
Her email (`jlcorrickandco@gmail.com`) is also the DigiMart Art Localized creator. Deleting the Team card does **not** revoke booth access or CF Access. For that: Assign/Registry revoke + optional CF group remove.

So: Team delete = card trash button · Identity deactivate = managed login users only · Booth access = separate.

I can add a **Delete** action to the Edit Team Member modal if you want that next.

### ASSISTANT
Confirmed. The separation is correct:

- **Team record:** delete with the Team card trash button → `DELETE /api/team/:id`
- **Managed login identity:** deactivate through Identity
- **Art Localized creator access:** revoke the booth assignment/registry grant
- **Cloudflare Access:** remove separately when applicable

For Jeanette, deleting the Team card alone will not remove DigiMart access.

I recommend adding **Delete Team Member** to the edit modal, but labeling it very clearly:

> Deletes the Team CRM record only. Login, booth, and Cloudflare access are not affected.

That closes the UI gap without blurring the separate authority layers.

### USER
No files were changed or discarded.
AeroCoreOS.dev has a broken .gitignore: node_modules/release-builds/ is incorrectly one entry, so both folders appear untracked. It is also 6 commits ahead of origin.
aerovista-command-center contains substantial identity/BytePad work: 22 modified files plus new services, tests, and documentation.
aerovista-command-center-server contains deployment-safety changes: 10 modified files plus SAFE_DEPLOY_LANE.md.
All three repositories remain dirty.
The detailed classification/testing command was interrupted before returning results, so no commits were created.

### ASSISTANT
Understood. Current safe state:

- **No files changed or discarded**
- **No commits created**
- **All three repositories remain dirty**
- The detailed classification/test run was interrupted, so commit boundaries are not yet verified

### Repository status

**AeroCoreOS.dev**
- Broken `.gitignore`: `node_modules/release-builds/` is being interpreted as one path
- `node_modules/` and `release-builds/` both appear untracked
- Local branch is **6 commits ahead of origin**

**aerovista-command-center**
- **22 modified files**
- Additional new identity, BytePad, service, test, and documentation files
- Likely contains multiple logical changes that should not be committed as one bundle

**aerovista-command-center-server**
- **10 modified files**
- New `SAFE_DEPLOY_LANE.md`
- Changes appear deployment-safety related, but still need classification and testing

### Safest next sequence

1. Fix only the `.gitignore` entry in `AeroCoreOS.dev`:
 ```gitignore
 node_modules/
 release-builds/
 ```
2. Re-run repository status and confirm generated directories disappear from untracked output.
3. Re-run the interrupted classification command.
4. Group changes by purpose before staging:
 - Identity milestone
 - BytePad
 - Deployment safety
 - Documentation
 - Tests
 - Unrelated or generated files
5. Run tests for each logical group.
6. Commit each repository separately with narrow, descriptive commits.
7. Review the six unpushed `AeroCoreOS.dev` commits before pushing anything.

Do not use `git add .`, reset, clean, stash, or push until the classification pass completes.

</details>

<details>
<summary>Alternative branch: USER: Agreed. Phase 0 is done; implementation starts at schema. **First WO:** [`docs/WO-NX-016_IDENTITY_SC</summary>

### USER
Agreed. Phase 0 is done; implementation starts at schema.

**First WO:** [`docs/WO-NX-016_IDENTITY_SCHEMA_FOUNDATION.md`](docs/WO-NX-016_IDENTITY_SCHEMA_FOUNDATION.md)

Covers: `identity_auth_links`, principal/membership/`access_version`, badge `kind` + aliases, assignment fields, `resource_grants` stub, `aerovista.member` seed, keep `artlocalized.builder`, and stop recognition badges from elevating roles.

**Phase 1A order** is now in the milestone: Schema → Gateway/bootstrap → `/account/*` → tests.

Say when to implement WO-NX-016 in the AVCC codebase.

### ASSISTANT
Implement **WO-NX-016 now**.

Phase 0 decisions are locked, and the schema foundation is the correct first dependency. Complete it before touching the gateway, bootstrap, or `/account/*` routes.

Use this completion gate:

- Migration applies cleanly to the current AVCC database.
- Existing identities and badge assignments remain intact.
- `artlocalized.builder` remains valid.
- Recognition badges no longer elevate roles.
- `aerovista.member` seeds idempotently.
- Rollback is tested.
- Existing AVCC identity, session, HMAC, founder-guard, and audit tests still pass.
- New schema tests cover uniqueness, badge kinds, assignment states, `access_version`, and auth links.

Once those checks pass, move directly to the **NXCore Gateway + verified bootstrap work order**.

### USER
**WO-NX-016 is shipped.** All completion-gate checks passed (`52` backend tests green).

### Schema foundation (AVCC)
- `identitySchemaFoundation.js` on every `initDatabase()`
- Tables: `identity_auth_links`, `resource_grants`
- User columns: `external_identity_id`, `principal_type`, `membership_plan`, `access_version`, …
- Badge `kind` + aliases; `aerovista.member` / `artlocalized.builder` (`access`)
- Recognition badges no longer elevate roles (`identityPayload` + `identityRuntime`)
- Rollback-safe additive migration

### Moved on to WO-NX-017 ([Review](7fc63362-766f-4588-8f6e-c155c2b18468#changes))
- Internal `POST /api/internal/identity/bootstrap` + `identityBootstrap.js`
- Gateway skeleton at `services/identity-gateway/` (`/v1/bootstrap`, feature flag, rate limit, correlation ID)
- Bootstrap tests included in the 52 passing suite

**Still open for 017:** Firebase Admin prod verify, Cloudflare Tunnel for `identity-api.aerovista.us`, full `/v1/me*` surface (WO-018 can own account routes).

### ASSISTANT
Excellent. **WO-NX-016 is complete, and WO-NX-017 is on the right track.**

The key architectural win is already in place: the database now distinguishes identity linkage, principal type, badge purpose, access versioning, and resource-grant projection without breaking current AVCC behavior. The 52 green backend tests give you a solid migration baseline.

## Recommended ownership split

Keep **WO-NX-017 narrowly focused on the trusted identity boundary**:

- Firebase Admin token verification in production
- NXCore gateway hardening
- Internal bootstrap contract
- Public `/v1/bootstrap`
- Feature flag
- Rate limiting
- Correlation IDs
- Audit propagation
- Cloudflare Tunnel and DNS for `identity-api.aerovista.us`

Move these to **WO-NX-018**:

- `/v1/me`
- `/v1/me/access`
- `PATCH /v1/me`
- `/account/register`
- `/account/login`
- `/account/verify`
- `/account/recovery`
- `/account/profile`
- Legacy Art Localized route redirects

That keeps 017 from turning into the entire public-account launch.

## WO-NX-017 completion gate

Before calling 017 shipped, verify:

1. **Firebase Admin production validation**
 - issuer checked
 - audience checked
 - expiration checked
 - signature checked
 - `email_verified=true` required
 - UID and email derived only from token

2. **Bootstrap behavior**
 - same Firebase UID always returns same identity
 - repeated calls do not duplicate `aerovista.member`
 - conflicting verified email is rejected safely
 - unverified users never create AVCC identities
 - suspended or closed linked identities do not reactivate through bootstrap

3. **Gateway security**
 - feature flag defaults closed in production
 - strict production CORS
 - request-body allowlist
 - rate limiting by IP and auth subject
 - generic public errors
 - correlation ID returned and forwarded
 - no admin, badge, role, or resource-grant fields accepted

4. **Audit**
 - bootstrap requested
 - identity created
 - auth link created
 - member badge assigned
 - bootstrap reused
 - bootstrap denied
 - correlation ID preserved through gateway and AVCC

5. **Deployment**
 - `identity-api.aerovista.us` resolves through Cloudflare
 - only intended public routes bypass Access
 - administrative AVCC routes are unreachable through that hostname
 - direct NXCore service port is not publicly exposed
 - Tailscale/internal route remains available for operations

## One important implementation detail

Do not let the gateway pass a browser-supplied identity payload downstream.

The gateway should produce an internal trusted request similar to:

```json
{
 "provider": "firebase",
 "providerSubject": "verified-firebase-uid",
 "verifiedEmail": "person@example.com",
 "emailVerifiedAt": "2026-07-30T12:00:00Z",
 "displayName": "Example Person",
 "registrationSource": "aerovista.us",
 "correlationId": "req_..."
}
```

Everything except the display name and optional profile fields should come from the verified token or server context.

## Recommended next sequence

```text
Finish WO-NX-017
→ deploy gateway behind feature flag
→ run internal bootstrap probes
→ create WO-NX-018 for /v1/me* and /account/*
→ limited Phase 1B account testing
→ minimum badge-admin completion before marketing
```

I would **not** add Cloudflare badge provisioning to WO-NX-017. That belongs with the later service-adapter work because it depends on badge lifecycle, outbox processing, and reconciliation rather than account bootstrap.

</details>