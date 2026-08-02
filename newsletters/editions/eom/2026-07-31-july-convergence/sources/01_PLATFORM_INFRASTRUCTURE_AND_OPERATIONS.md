# AeroVista Platform, Infrastructure, and Operations Report — July 2026

## Scope

This report covers NXCore, AeroCore OS, AeroVista Workspaces, AVCC platform stabilization, service routing, local infrastructure, operational resilience, and July’s major recovery work.

## Executive Summary

July materially strengthened AeroVista’s technical foundation. The largest gains came from clarifying system ownership, restoring broken internal services, improving same-origin routing, repairing authentication and CSRF handling, and recovering Art Localized backup operations.

AeroCore OS is now better defined as the shared technical platform rather than a monolithic application. AeroVista Workspaces are defined as purpose-built work environments, and AVCC is positioned as the commercial and operational record.

## NXCore and AeroCore OS

NXCore continued serving as AeroVista’s local-first infrastructure backbone, supporting:

- Dockerized services.
- Traefik routing.
- Tailscale private access.
- Cloudflare Tunnel exposure.
- Internal storage and shared files.
- API services.
- Workspaces.
- Backups and replication.
- Public and protected applications.

AeroCore OS was clarified as the shared layer for:

- Identity and permissions.
- Devices and services.
- Assets and versions.
- Tools and capability packages.
- Backend jobs and workers.
- Handoffs.
- Notifications.
- Technical audit and infrastructure support.

## AeroVista Workspaces

July formalized the Workspace model as a real operating system for work rather than a link collection.

Major outputs included:

- Master architecture blueprint.
- Division Registry model.
- Capability Registry model.
- Project Workbench.
- Tool Dock.
- Job Center.
- PWA direction.
- Tauri desktop bridge direction.
- Portable capability packages.
- AV-Skillset and Cursor rules.
- Mobile-first Workspaces landing page.
- Workspace infographic.
- README and build plan.

The intended relationship is:

```text
AeroCore OS
→ identity, permissions, devices, assets, services

AeroVista Workspaces
→ specialized work

AVCC
→ business and operational record
```

## AVCC Local Stack Stabilization

A major July 30 recovery session repaired or restored:

- AeroVista Workspaces.
- Drone Tour Builder.
- Daily Brief Builder.
- Catalog Console.
- Gear Store.
- Business Suite.
- AeroAI.
- Portable Library.
- Art Localized backups.

### Major repairs

- Workspaces restored at internal route.
- Drone Tour Builder restored.
- Daily Brief Builder route corrected.
- Catalog Console switched to same-origin `/store-console/`.
- Gear Store ops secret and authentication restored.
- Manifest `generatedAt` restored.
- Catalog on disk restored.
- Checkout bootstrap restored.
- Business Suite session credentials and CSRF handling repaired.
- AeroAI CSRF refresh and retry behavior added.
- Portable Library stale proxy replaced with an AVCC compatibility route.
- Art Localized backup and offsite operations recovered.
- Connect with Cindy typo corrected.

## Verified State

| System | Result |
|---|---|
| AVCC backend | Healthy |
| Workspaces | Operational |
| Drone Tour Builder | Operational |
| Daily Brief | Operational |
| Catalog Console | Operational |
| Business Suite route | Operational |
| Gear Store readiness | 4/4 |
| Gear catalog | 57 products |
| Gear checkout keys | 37 |
| Art Localized deep health | Green |
| Backup timers | Enabled and active |

## Durability Concerns

Several fixes were applied directly to runtime environments or served bundles.

Priority source-level follow-up includes:

- Business Suite session and CSRF logic.
- AeroAI token refresh behavior.
- Portable Library compatibility routing.
- Gear Store configuration.
- Art Localized backup scripts and service definitions.

A runtime fix is not considered durable until it exists in the authoritative source and survives a rebuild.

## Operational Resilience

Art Localized backup work restored:

- Primary backup.
- Replica copy.
- Critical export.
- Offsite service.
- systemd jobs and timers.
- Booth and registration data protection.

The next scheduled backup runs should be reviewed for:

- New files.
- Replication success.
- Offsite export success.
- Retention behavior.
- Failure visibility.

## Risks

- Source/runtime drift.
- Stale service references.
- Old ports and proxy paths.
- Files in noncanonical locations.
- Mixed production and experimental paths.
- Missing automated restore validation.
- Too many systems depending on one-off compatibility logic.

## August Handoff

1. Move runtime fixes into source.
2. Audit stale internal endpoints.
3. Confirm next backup and offsite cycles.
4. Create one service/port/hostname registry.
5. Continue Workspace vertical-slice implementation.
6. Reduce noncanonical files in home and shared directories.
