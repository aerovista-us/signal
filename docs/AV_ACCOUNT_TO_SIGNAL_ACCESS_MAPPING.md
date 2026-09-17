# AV Account to Signal Registry access mapping

Status: Phase 2 contract; declarative and non-enforcing

Signal consumes identity, role, capability, entitlement, and agreement facts resolved by AV Account. Signal does not create a parallel identity, agreement, tax, or payment authority.

| Registry field | AV Account source | Match rule |
|---|---|---|
| `access.mode: public` | none | Anonymous and authenticated delivery remains public. |
| `access.mode: authenticated` | valid AV Account session | A resolved account is required; no role alone grants broader access. |
| `access.mode: entitled` | resolved AV Account access context | Every populated requirement group below must match. |
| `access.capabilities[]` | effective capabilities | The account must hold every named capability. |
| `access.accountRoles[]` | normalized effective role/relationship | At least one listed role must match. Roles describe relationship; they do not replace capabilities. |
| `access.entitlements[]` | effective entitlements | The account must hold every named entitlement. |
| `access.agreementRequirements[]` | accepted, versioned agreement records | Every named agreement version must be accepted and current. |

## Phase 2 safety boundary

- `access` remains optional.
- Existing public content stays public even if descriptive access metadata is added during Phase 2.
- Registry validation checks the metadata contract, but no delivery restriction is enabled by this phase.
- Missing or unresolved authority data must deny access only after a separately reviewed protected-delivery phase is implemented.
- UI filtering is never authorization; protected assets must eventually move behind server-side delivery enforcement.

## Example records

Public metadata:

```json
{"access":{"mode":"public"}}
```

Future Creator/Collaborator material:

```json
{
  "access": {
    "mode": "entitled",
    "capabilities": ["signal.read.creator"],
    "accountRoles": ["creator", "collaborator"],
    "entitlements": ["signal.creator.edition"],
    "agreementRequirements": ["creator-agreement@1"]
  }
}
```

This example is testable metadata only. It does not authorize publishing protected assets on a public static path.
