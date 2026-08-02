# RydeSync Versions Comparison

Source: https://chatgpt.com/c/6a6e2758-b66c-83e8-82d0-15a231b80ebb

## USER
https://aerovista-rydesync.web.app/ vs rydesync.aerovista.us

## ASSISTANT
I’m checking both addresses for redirects, live content, SSL, and whether they’re serving the same build or drifting apart.

## ASSISTANT
## They are **two different RydeSync versions**, not two addresses for the same build.

### `aerovista-rydesync.web.app`

This is the **older Firebase version**:

- Basic room joining
- Peer-to-peer voice through PeerJS/WebRTC
- Local device music player
- Music does **not** sync or broadcast to other riders
- No account required
- Presented as **RydeSync v1.1.0**
- Recommends approximately five users per room 

### `rydesync.aerovista.us`

This is the **newer and significantly more capable version**:

- Create and host rooms
- Shareable room links and room codes
- Host and co-host roles
- Optional room passwords
- Ryde, classroom, practice, listening-party, and campaign modes
- Push-to-talk
- Synced EchoVerse catalog playback
- Music queue and host playback controls
- Designed for roughly 2–12 participants
- Node/Express, WebSocket, PeerJS, and EchoVerse integration 

## My recommendation

**`rydesync.aerovista.us` should be the official production address.**

It has the stronger AeroVista branding, looks like a real product URL, and represents the current hosted-room direction. The Firebase URL currently exposes an older product concept and could confuse users because its capabilities and room behavior are different.

I would:

1. Keep `rydesync.aerovista.us` as the canonical public address.
2. Redirect `aerovista-rydesync.web.app` to it.
3. Remove the old version number and legacy product description from anything still indexed.
4. Keep the old build only under an internal name such as **RydeSync Classic** if you still need it for testing.

The practical verdict is:

> **Firebase URL = legacy prototype.** 
> **Custom AeroVista URL = current RydeSync platform.**

## USER
ok. let put on todo list ..

## ASSISTANT
Added to the RydeSync todo list:

**Canonical URL cleanup**
- Make `rydesync.aerovista.us` the official production address
- Redirect `aerovista-rydesync.web.app` to it
- Remove old version/product copy from indexed references
- Keep the legacy build only as **RydeSync Classic** for internal testing, if still needed

## USER
anything else "rydesync" that can go on this list too?

## ASSISTANT
I’m doing a broader RydeSync pass now—product gaps, launch polish, reliability, and how it fits into EchoVerse and AeroVista accounts.

## ASSISTANT
Yes—there were several worthwhile RydeSync items hiding in earlier work. I added them to the master todo list.

## Highest priority

- **Fix and verify shared join links**, especially the earlier `/rydesync/join?room=...` redirect-to-home problem.
- **Confirm one master router** remains in place, with no nested `BrowserRouter` regressions.
- **Run real two-rider field tests** using Bluetooth helmets/headsets, locked screens, weak cellular coverage, disconnects, and reconnects.
- Add clear **connection, microphone, WebSocket, reconnect, and permission status** indicators.
- Run the complete RydeSync smoke suite covering room creation, roles, playback permissions, WebSocket presence, listener restrictions, and speaker queues.

## Security and reliability

- Expiring room invites and access tokens
- Room-password and role-enforcement testing
- Rate limiting and automatic abandoned-room cleanup
- Confirm no internal EchoVerse catalog configuration leaks
- Add latency, playback-drift, disconnect, and WebSocket-health monitoring
- Preserve the privacy position that voice is not recorded or stored

The legacy page still publicly presents RydeSync as version **1.1.0**, lists roughly five riders as the recommended limit, and describes push-to-talk, password protection, music broadcasting, larger-room infrastructure, and Android packaging as future enhancements. That makes cleaning up or redirecting it particularly important. 

## Architecture cleanup

- Keep **one canonical RydeSync backend**
- Fold the separate two-rider/Echo experience into a simplified `group_ride` mode
- Retire the old `frontier-signal` stack only after equivalent pairing and music-sync behavior exists
- Complete the migration from the legacy EchoVerse catalog service to the Library API
- Standardize AeroVista identity claims, roles, signed audio URLs, and catalog-proxy behavior
- Verify production WebSocket routing, health endpoints, service timeouts, and minimum-instance behavior

## Product polish

- Make the primary promise clearer: **ride communication first, synchronized music second**
- Add QR-code joining, shareable links, recent rooms, rider names, and obvious host/co-host controls
- Add a **pre-ride audio test** for microphone, output device, push-to-talk, and music balance
- Create a safer riding interface with large controls and minimal interaction while moving
- Keep room templates—group ride, two-rider, listening party, classroom, practice, and campaign—but avoid exposing every option at once
- Add onboarding, privacy details, troubleshooting, release notes, and a repeatable field-test checklist
- Track activation, session completion, disconnects, skips, session length, and feature usage without collecting voice
- Reassess whether a native Android/Capacitor app is necessary after PWA field testing

The main AeroVista site already positions RydeSync as a connected-system live demo using WebRTC and NxCore signaling, so the next step should be turning it from a capable demo into a clearly supported AeroVista product. 

My strongest recommendation: **do the redirect, join-link repair, and two-rider Bluetooth field test first.** Those three will reveal whether RydeSync is genuinely ready for people to use on a real ride.

## USER
good. create work order that discribes each item with basic direction / approch that should be used

## ASSISTANT
I’m turning the backlog into a single implementation work order with priorities, scope, approach, acceptance checks, dependencies, and a suggested execution sequence.

## ASSISTANT
Below is the implementation-ready work order, organized so it can be assigned as one project or broken into individual tickets.

 
# WORK ORDER — RydeSync Production Consolidation and Launch Readiness

**Work Order ID:** WO-RS-001 
**Product:** RydeSync 
**Company:** AeroVista LLC 
**Related Division:** EchoVerse Audio / Nexus TechWorks 
**Priority:** High 
**Status:** Ready for Planning 
**Primary Production URL:** `https://rydesync.aerovista.us`

---

## 1. Objective

Consolidate RydeSync into one reliable, clearly branded AeroVista product suitable for real-world group rides.

The work should:

- Eliminate confusion between legacy and current versions.
- Establish one canonical frontend and backend.
- Repair and verify room joining.
- Improve connection reliability and user feedback.
- Validate operation with real riders, mobile devices, Bluetooth headsets, and changing cellular conditions.
- Strengthen room security and operational monitoring.
- Simplify the user experience around RydeSync’s primary purpose: live rider communication.
- Retain synchronized EchoVerse playback as a supporting feature.

---

## 2. Product Direction

RydeSync should be presented primarily as:

> A live communication and shared-audio system for riders traveling together.

Communication reliability must take priority over music, campaigns, classroom modes, or advanced room configuration.

Advanced capabilities may remain available, but they should not make the basic create-room and join-room experience feel complicated.

---

# PHASE 1 — PUBLIC URL AND LEGACY CLEANUP

## RS-001 — Establish the Canonical Production URL

### Requirement

Make `rydesync.aerovista.us` the official and canonical RydeSync production address.

### Direction

- Confirm the custom domain serves the latest approved production build.
- Add a canonical URL tag to public pages.
- Update navigation, documentation, social links, QR codes, and AeroVista product listings.
- Ensure room-sharing links use the custom domain.
- Remove internal use of the Firebase URL where it is presented as the main product URL.

### Acceptance Criteria

- All newly generated RydeSync links use `rydesync.aerovista.us`.
- Search engines and social previews identify the custom domain as canonical.
- No current public AeroVista page intentionally directs users to the Firebase URL.

---

## RS-002 — Redirect the Legacy Firebase Site

### Requirement

Redirect `aerovista-rydesync.web.app` to the canonical RydeSync domain.

### Direction

- Use a permanent redirect where Firebase Hosting permits it.
- Preserve useful route and query information when possible.
- A legacy room link should redirect to the equivalent current route rather than only the homepage.
- Do not delete the old deployment until redirects have been tested.

### Acceptance Criteria

- Opening the Firebase homepage redirects to the production homepage.
- Legacy join links preserve their room code or invitation information.
- No redirect loop occurs.
- Mobile and desktop browsers follow the redirect correctly.

---

## RS-003 — Archive RydeSync Classic

### Requirement

Remove public confusion caused by the older RydeSync v1.1.0 experience.

### Direction

- Rename the retained old build to **RydeSync Classic**.
- Restrict it to internal testing or archival access.
- Remove outdated public capability descriptions.
- Do not present Classic as an actively supported production version.
- Keep the source and deployment rollback information until the new system has passed field testing.

### Acceptance Criteria

- Public users encounter only the current product.
- The legacy build remains recoverable for internal reference.
- Legacy version numbers and roadmap copy are no longer indexed as current product information.

---

# PHASE 2 — ROUTING AND ROOM ACCESS

## RS-004 — Repair and Verify Shared Join Links

### Requirement

Ensure every shared room link opens the correct room-joining experience.

### Direction

Test and correct routes such as:

`/join?room=ROOM_CODE`

`/rydesync/join?room=ROOM_CODE`

Invitation links containing room tokens or passwords.

The join route should:

1. Read the room identifier.
2. Validate the room or invitation.
3. Ask for any required display name, password, or permissions.
4. Connect the rider to the intended room.
5. Show a clear error when the room has expired or does not exist.

Do not silently send failed links to the homepage.

### Acceptance Criteria

- Valid links open the correct room.
- Invalid links display a useful explanation.
- Password-protected rooms request the password.
- Expired invitations are identified as expired.
- Join links work when the app is initially closed.
- Join links work from text messages, QR codes, email, and social apps.

---

## RS-005 — Protect the Master Router Architecture

### Requirement

Prevent nested-router and route-reset regressions.

### Direction

- Keep `Root.tsx`, or its approved replacement, as the single master application router.
- Remove nested `BrowserRouter` instances.
- Keep room, join, settings, and player routes inside the same route hierarchy.
- Add automated route tests for direct URL loading and browser refreshes.

### Acceptance Criteria

- Directly loading a join URL does not return the user to the homepage.
- Refreshing inside a room does not break the application.
- Browser back and forward navigation behave predictably.
- The codebase contains only the intentionally approved top-level router.

---

## RS-006 — Simplify Room Creation and Joining

### Requirement

Make starting or joining a basic ride possible without understanding every RydeSync mode.

### Direction

The default entry screen should emphasize:

- **Start a Ride**
- **Join a Ride**

Advanced room types should appear under an additional-options control.

Room creation should produce:

- A clear room name or code.
- A shareable link.
- A copy-link button.
- A QR code.
- An optional room password.
- A simple host summary before entering the room.

### Acceptance Criteria

- A first-time user can create a basic room without instructions.
- A second rider can join using either a link, code, or QR code.
- Advanced room settings do not block the default flow.
- The host can clearly see which room was created.

---

# PHASE 3 — CONNECTION RELIABILITY

## RS-007 — Add Connection Health Indicators

### Requirement

Users must be able to understand whether they are connected and whether voice communication is functioning.

### Direction

Show separate states for:

- Application online/offline status.
- RydeSync server connection.
- Room connection.
- Peer voice connection.
- Microphone permission.
- Microphone muted or active.
- Push-to-talk state.
- Reconnecting.
- Connection failed.

Use understandable language rather than exposing raw WebRTC or WebSocket terminology to normal users.

### Acceptance Criteria

- A user can distinguish between microphone failure, server failure, and peer failure.
- Reconnecting is visibly different from being fully disconnected.
- Error messages include a useful next action.
- The interface does not report “connected” until the required room services are operational.

---

## RS-008 — Implement Controlled Reconnection

### Requirement

RydeSync should recover from common short-term network disruptions.

### Direction

- Add WebSocket reconnection with limited exponential backoff.
- Rejoin the existing room when the user’s session remains valid.
- Restore the user’s role, mute state, and permitted queue state.
- Avoid creating duplicate participants during reconnect.
- Show the rider that reconnection is underway.
- Require a deliberate rejoin when the room or invitation is no longer valid.

### Acceptance Criteria

- Brief network loss does not permanently remove the rider.
- Duplicate rider records are not created.
- Host and co-host permissions are restored correctly.
- Reconnection failure produces a visible manual-retry option.

---

## RS-009 — Handle Permission Failures Clearly

### Requirement

Microphone, autoplay, Bluetooth, and browser permission failures must not appear as unexplained connection failures.

### Direction

- Detect denied, dismissed, unavailable, and interrupted microphone permissions.
- Provide browser-specific recovery instructions where practical.
- Identify when audio playback requires a user interaction.
- Detect when no input device is available.
- Recheck permissions when the app returns from the background.

### Acceptance Criteria

- Permission denial displays a specific explanation.
- The user can retry after changing browser settings.
- The room can remain open while audio permissions are repaired.
- Permission errors are captured in operational logs without recording audio.

---

# PHASE 4 — REAL-WORLD FIELD VALIDATION

## RS-010 — Two-Rider Field Test

### Requirement

Validate RydeSync with two actual riders under realistic operating conditions.

### Direction

Test with:

- Two separate mobile devices.
- Bluetooth helmets or headsets.
- Cellular data rather than only Wi-Fi.
- Devices placed in pockets or mounted on bikes.
- Screen locked and unlocked.
- App moved to the background.
- Riders separating and reconnecting.
- Weak or changing signal conditions.
- Incoming phone calls or audio interruptions.
- Microphone permissions removed and restored.
- One rider temporarily losing connectivity.

Record:

- Join success rate.
- Time to establish voice.
- Disconnect frequency.
- Reconnect time.
- Perceived voice delay.
- Audio routing problems.
- Battery usage.
- Device heat.
- Required user interactions while moving.

### Acceptance Criteria

- A documented field-test report is produced.
- Critical failures are converted into follow-up tickets.
- Two riders can complete a representative ride without repeatedly rebuilding the room.
- Any unsupported background or lock-screen behavior is clearly documented.

---

## RS-011 — Bluetooth and Audio Routing Test Matrix

### Requirement

Confirm behavior across common mobile audio configurations.

### Direction

Test:

- Phone speaker and microphone.
- Wired headset where supported.
- Standard Bluetooth earbuds.
- Helmet intercom systems.
- Bluetooth device connected before opening RydeSync.
- Bluetooth device connected after entering a room.
- Bluetooth device disconnected during a room.
- Music and communication using the same output device.
- Android audio-focus interruptions.

Prioritize Android because RydeSync is expected to be used heavily on Android devices.

### Acceptance Criteria

- Supported device combinations are documented.
- Audio-route changes do not silently disable communication.
- Known device-specific limitations are added to the support page.
- The pre-ride audio test accurately reflects the selected input and output.

---

## RS-012 — Background and Screen-Lock Validation

### Requirement

Determine exactly what RydeSync can reliably support when the device is locked or the application is in the background.

### Direction

- Test the current PWA behavior before committing to native packaging.
- Evaluate browser throttling, microphone suspension, audio-focus loss, and WebSocket suspension.
- Clearly separate behavior that can be repaired in the PWA from behavior imposed by the mobile operating system.
- Avoid claiming reliable background communication until it is verified.

### Acceptance Criteria

- Supported and unsupported states are documented.
- The application detects and explains suspension where possible.
- Product copy accurately represents background capabilities.
- A native-app decision can be made using test evidence.

---

# PHASE 5 — SECURITY AND PRIVACY

## RS-013 — Harden Room Invitations

### Requirement

Room invitations must not grant indefinite access.

### Direction

- Use signed invitation tokens.
- Include expiration times.
- Bind tokens to the intended room.
- Allow the host to invalidate active invitations.
- Avoid exposing internal room identifiers or infrastructure details unnecessarily.
- Generate new invitations when room security settings change.

### Acceptance Criteria

- Expired tokens cannot be used.
- Tokens cannot be transferred to another room.
- Revoked invitations fail immediately or within an approved cache interval.
- Invitation errors do not disclose private room details.

---

## RS-014 — Verify Password and Role Enforcement

### Requirement

Host, co-host, speaker, listener, and campaign permissions must be enforced by the server.

### Direction

- Treat frontend controls as convenience only.
- Validate every privileged action on the backend.
- Verify room password handling.
- Verify host transfer and co-host assignment.
- Prevent listeners from issuing playback or room-management commands.
- Prevent unauthorized participants from changing another participant’s role.

### Acceptance Criteria

- Unauthorized API and WebSocket actions return a denial.
- Hidden frontend controls cannot be bypassed with direct requests.
- Role changes are reflected for all connected participants.
- Host departure follows a defined transfer or room-closing policy.

---

## RS-015 — Add Rate Limiting and Abuse Controls

### Requirement

Protect room creation, joining, authentication, signaling, and messaging endpoints from automated abuse.

### Direction

- Apply rate limits based on endpoint sensitivity.
- Use stricter controls for failed passwords and invalid tokens.
- Limit repeated room creation.
- Limit signaling floods and repeated reconnection attempts.
- Add temporary blocking rather than permanent denial for ordinary failures.
- Keep thresholds configurable.

### Acceptance Criteria

- Normal riders are not blocked during expected reconnect behavior.
- Automated rapid requests are limited.
- Rate-limit events appear in operational logs.
- The service does not expose sensitive details in rate-limit responses.

---

## RS-016 — Automatic Room Cleanup

### Requirement

Abandoned and expired rooms should not remain active indefinitely.

### Direction

Define policies for:

- Rooms that were created but never joined.
- Empty rooms.
- Rooms whose host disconnected.
- Scheduled or campaign rooms.
- Practice-room history.
- Temporary playback and presence records.

Use a grace period to allow reconnection before cleanup.

### Acceptance Criteria

- Empty temporary rooms expire automatically.
- Active rooms are not removed during brief connection loss.
- Room cleanup also removes unnecessary tokens and temporary state.
- Cleanup activity is logged.

---

## RS-017 — Confirm Voice Privacy

### Requirement

Maintain a clear position that RydeSync does not record or retain voice unless a future recording feature is deliberately introduced.

### Direction

- Do not store voice streams.
- Do not add voice transcription to production telemetry.
- Document what signaling and connection metadata is retained.
- Explain peer-to-peer and server-relayed behavior accurately.
- Include a concise privacy explanation before microphone activation.

### Acceptance Criteria

- No voice recordings are found in application storage, logs, or analytics.
- Privacy documentation matches the implemented architecture.
- Users understand that operational metadata may still be recorded.
- Any future recording capability requires separate approval and visible consent.

---

# PHASE 6 — TESTING AND OPERATIONAL VISIBILITY

## RS-018 — Maintain the Production Smoke Suite

### Requirement

Preserve automated validation of critical RydeSync behavior.

### Direction

The smoke suite should cover at minimum:

- Health endpoint.
- Current version endpoint.
- Room creation.
- Room joining.
- Invalid and expired invitation tokens.
- Password-protected room behavior.
- Token-gated peers.
- Token-gated playback controls.
- Host and co-host actions.
- Listener permission restrictions.
- WebSocket presence.
- Reconnection.
- Campaign-room behavior.
- Practice-room append-only speaker queues.
- Room cleanup.

Run the suite against staging before production deployment.

### Acceptance Criteria

- Every production release has a recorded smoke result.
- Critical smoke failures block deployment.
- Tests use isolated temporary rooms.
- Test cleanup removes generated data.

---

## RS-019 — Add Operational Telemetry

### Requirement

Provide enough visibility to diagnose failures without recording rider conversations.

### Direction

Track:

- Room creation attempts and success.
- Join attempts and success.
- Time required to establish a connection.
- WebSocket disconnects.
- Peer connection failures.
- Reconnect attempts and success.
- Playback command failures.
- Playback synchronization drift.
- API response times.
- Active room and participant counts.
- Permission failures.
- Client and server versions.

Use anonymous or pseudonymous identifiers where possible.

### Acceptance Criteria

- Operators can determine whether a failure is widespread or isolated.
- Logs can be correlated across room, client, and backend events.
- Voice contents are never collected.
- Retention limits are documented.

---

## RS-020 — Create Health and Latency Monitoring

### Requirement

Detect service degradation before users report it.

### Direction

Monitor:

- Backend health endpoint.
- WebSocket availability.
- Room-creation latency.
- Join latency.
- EchoVerse catalog response time.
- Signed-audio URL generation.
- Active connections.
- Error rate.
- Container or instance restarts.
- CPU, memory, and network pressure.

Create alert thresholds that identify meaningful failures without generating constant noise.

### Acceptance Criteria

- A service outage produces an actionable alert.
- A major latency increase is visible on a dashboard.
- Health checks do not report success when critical dependencies are unavailable.
- Operators can identify which dependency is causing degradation.

---

# PHASE 7 — BACKEND AND SERVICE CONSOLIDATION

## RS-021 — Establish One Canonical RydeSync Backend

### Requirement

RydeSync should not depend on multiple competing production backends for overlapping functionality.

### Direction

- Identify the current authoritative service.
- Inventory functionality in each legacy or experimental backend.
- Move required capabilities into the canonical service.
- Route all production clients through the canonical backend.
- Keep rollback access during migration.
- Remove old services only after traffic and feature-equivalence verification.

### Acceptance Criteria

- Production clients use one approved backend.
- Duplicate room state cannot exist across separate production services.
- Deployment and rollback procedures identify the canonical service.
- Legacy services receive no production traffic before retirement.

---

## RS-022 — Consolidate Two-Rider and Echo Behavior

### Requirement

Avoid maintaining a separate product stack for simplified two-rider operation.

### Direction

Add a simplified `group_ride` experience that can support:

- Two riders.
- Multiple riders.
- Push-to-talk or approved communication mode.
- Optional synchronized EchoVerse playback.
- Minimal setup.

Keep specialized behavior configurable inside the canonical room system rather than running a separate backend.

### Acceptance Criteria

- Two riders can achieve the intended simplified experience through the main RydeSync system.
- Music synchronization does not require a separate public domain or separate room database.
- The simplified flow hides unnecessary advanced controls.

---

## RS-023 — Retire the Frontier Signal Stack Safely

### Requirement

Remove the old `frontier-signal` stack only after its necessary capabilities have been replaced.

### Direction

Before retirement, compare:

- Pairing behavior.
- Room creation.
- Peer signaling.
- Reconnection.
- Music synchronization.
- Bluetooth/mobile behavior.
- Deployment dependencies.
- Logs and troubleshooting tools.

Create a rollback snapshot before shutdown.

### Acceptance Criteria

- Required features have an approved equivalent in the canonical backend.
- Production traffic has been moved.
- A rollback package exists.
- The old service is disabled before it is deleted.
- Related DNS, tunnels, containers, and secrets are cleaned up after the soak period.

---

## RS-024 — Complete EchoVerse Library API Migration

### Requirement

Move RydeSync from the legacy EchoVerse catalog service to the current Library API.

### Direction

Migrate from the legacy catalog endpoint to the approved Library API through staged validation:

1. Confirm API contract and authentication.
2. Add an adapter if the response structures differ.
3. Run both sources in parallel.
4. Compare catalog and playback results.
5. Move a limited portion of traffic.
6. Complete production cutover.
7. Maintain rollback during a defined soak period.

### Acceptance Criteria

- Catalog browsing and playback work through the Library API.
- Track, artist, artwork, and playback metadata remain compatible.
- Signed or protected audio access remains enforced.
- Legacy catalog calls stop after the soak period.
- Rollback has been tested.

---

## RS-025 — Standardize AeroVista Identity and Session Claims

### Requirement

RydeSync should use the shared AeroVista account and session model where authentication is required.

### Direction

Standardize:

- User identity.
- Member identity.
- Display name.
- Session issuer and audience.
- Expiration.
- Session revocation.
- Room role claims.
- Host and co-host authorization.
- Signed audio access.

Guest room participation may remain available if intentionally supported, but guest access must be explicit and limited.

### Acceptance Criteria

- Production rejects unsigned or invalid sessions.
- Expired and revoked sessions cannot perform protected actions.
- Room authorization is not based only on frontend state.
- Guest permissions are documented and restricted.

---

## RS-026 — Verify Production Routing and WebSocket Infrastructure

### Requirement

Confirm that production hosting correctly supports both normal web requests and long-lived RydeSync connections.

### Direction

Review:

- DNS.
- TLS certificates.
- Firebase or Cloud Run routing.
- Reverse-proxy rules.
- WebSocket upgrades.
- Timeouts.
- Sticky-session requirements.
- Minimum instances or cold-start behavior.
- Health checks.
- CORS.
- Cache headers.
- Deployment rollback.

### Acceptance Criteria

- WebSocket connections remain stable for representative ride durations.
- Production routing does not downgrade or block connection upgrades.
- Cold starts remain within the approved user-experience threshold.
- Health checks identify dependency failures.
- Deployment documentation matches the actual infrastructure.

---

# PHASE 8 — PRODUCT AND RIDING EXPERIENCE

## RS-027 — Clarify the Primary Product Promise

### Requirement

Make the purpose of RydeSync immediately understandable.

### Direction

Lead with rider communication and group coordination.

Supporting features may include:

- Synchronized EchoVerse music.
- Listening parties.
- Practice rooms.
- Classroom sessions.
- Campaign rooms.

Do not present every capability with equal importance on the first screen.

### Acceptance Criteria

- A new visitor can explain RydeSync’s primary purpose after viewing the landing page.
- Create and join actions are more prominent than advanced feature explanations.
- Product copy does not promise capabilities that have not passed field testing.

---

## RS-028 — Add Rider Display Names and Participant Clarity

### Requirement

Participants must be able to recognize who is connected and who is speaking.

### Direction

- Ask for or retrieve a display name before joining.
- Show role, connection state, mute state, and speaking state.
- Avoid exposing email addresses or internal user identifiers.
- Clearly identify the host and co-host.
- Handle duplicate display names without merging participants.

### Acceptance Criteria

- Every participant has a visible rider identity.
- Active speaker indicators are understandable.
- Private account information is not shown to other riders.
- Reconnecting riders do not appear as duplicate active participants.

---

## RS-029 — Add a Pre-Ride Audio Check

### Requirement

Allow users to confirm audio behavior before they begin moving.

### Direction

The check should verify:

- Microphone permission.
- Detected input device.
- Selected output device where browser support permits.
- Microphone level.
- Push-to-talk operation.
- Local playback.
- Music volume.
- Communication-to-music balance.
- Bluetooth connection.
- Basic server connectivity.

Do not record or upload the test audio unless required for an approved diagnostic process.

### Acceptance Criteria

- The user can confirm that speech is reaching the application.
- The user can hear a test sound.
- Permission or device failures are explained.
- The user can enter the room after passing or intentionally skipping the check.

---

## RS-030 — Create a Safer Riding Interface

### Requirement

Reduce the need for detailed visual interaction while a rider is moving.

### Direction

- Use large touch targets.
- Keep the active-ride screen simple.
- Avoid small menus and text-heavy actions.
- Make push-to-talk visually and physically obvious.
- Use optional audio confirmations for major state changes.
- Move setup and advanced controls to pre-ride or stopped states.
- Do not encourage riders to type, browse music, or configure settings while moving.

### Acceptance Criteria

- Core ride actions are usable with minimal visual attention.
- Advanced configuration is not placed on the active-ride surface.
- Safety messaging clearly advises riders to configure the app before moving.
- Motion-based restrictions may be evaluated but should not create dangerous unexpected behavior.

---

## RS-031 — Organize Room Templates

### Requirement

Retain different use cases without overwhelming users.

### Direction

Support templates such as:

- Group Ride.
- Two-Rider Ride.
- Listening Party.
- Classroom.
- Practice Room.
- Campaign Room.

Each template should define default permissions, controls, and layouts.

The main interface should show the most common templates first and place specialized templates under additional options.

### Acceptance Criteria

- Templates use the same canonical backend.
- Each template has documented default roles.
- Switching templates does not create inconsistent authorization behavior.
- The default Group Ride experience remains the simplest option.

---

# PHASE 9 — DOCUMENTATION AND SUPPORT

## RS-032 — Create First-Run Onboarding

### Requirement

Explain RydeSync without requiring users to read a full manual.

### Direction

The onboarding should cover:

- What RydeSync does.
- Start versus join.
- Microphone permission.
- Headset recommendation.
- Push-to-talk behavior.
- Connection status.
- Basic privacy.
- Configure before riding.
- What to do after disconnecting.

Allow returning users to skip onboarding.

### Acceptance Criteria

- First-time users receive concise guidance.
- Onboarding does not block experienced users repeatedly.
- Instructions match the current interface.
- Safety and privacy information is visible before first use.

---

## RS-033 — Publish Privacy and Data Handling Information

### Requirement

Provide a plain-language explanation of RydeSync data handling.

### Direction

Describe:

- Account information used.
- Guest information used.
- Room and connection metadata.
- Operational logs.
- Analytics.
- Voice handling.
- EchoVerse playback requests.
- Retention periods.
- User controls and support contact.

### Acceptance Criteria

- Privacy copy matches actual behavior.
- Voice is clearly distinguished from connection metadata.
- The policy is accessible from the app and landing page.
- Privacy changes are included in release review.

---

## RS-034 — Create Troubleshooting and Support Pages

### Requirement

Give users practical answers for common problems.

### Direction

Include guidance for:

- Microphone denied.
- No sound.
- Bluetooth using the wrong device.
- Join link not opening.
- Room expired.
- Connection repeatedly dropping.
- Music not starting.
- App suspended in the background.
- Browser compatibility.
- Reporting a problem.

### Acceptance Criteria

- Error messages can link directly to relevant troubleshooting sections.
- Instructions prioritize Android and common mobile browsers.
- Unsupported behavior is stated honestly.
- Support documentation includes the displayed application version.

---

## RS-035 — Add Release Notes and Version Visibility

### Requirement

Make it possible to identify which frontend and backend versions are in use.

### Direction

- Display the frontend version in Settings or About.
- Expose an approved backend version endpoint.
- Maintain concise release notes.
- Include deployment date, major changes, known issues, and rollback reference.
- Avoid showing sensitive infrastructure information.

### Acceptance Criteria

- Support can identify the client version from a screenshot.
- Telemetry records compatible frontend and backend versions.
- Every production deployment has corresponding release notes.

---

## RS-036 — Create the Field-Test Checklist

### Requirement

Standardize future ride testing.

### Direction

Create a reusable checklist covering:

- Devices.
- Operating systems.
- Browser or installed PWA.
- Headsets.
- Network type.
- Room creation.
- Room joining.
- Permissions.
- Voice.
- Music.
- Reconnection.
- Screen lock.
- Background use.
- Battery.
- Heat.
- Observed delay.
- Failure notes.
- Final pass or fail decision.

### Acceptance Criteria

- Each field test produces comparable results.
- Failures include reproduction steps.
- Device and software versions are recorded.
- Results can be attached to release approval.

---

# PHASE 10 — ANALYTICS AND PLATFORM DECISION

## RS-037 — Add Privacy-Respecting Product Analytics

### Requirement

Measure whether users can successfully use RydeSync without collecting conversation contents.

### Direction

Track events such as:

- Landing page opened.
- Room creation started.
- Room successfully created.
- Join started.
- Join completed.
- Audio check completed.
- Communication connection established.
- Reconnect occurred.
- Room completed normally.
- Music started.
- Track skipped.
- Session duration.
- Feature or template used.

Avoid recording voice, message contents, passwords, full invitation tokens, or unnecessary personal information.

### Acceptance Criteria

- Activation and completion rates can be calculated.
- Failed joins and disconnect patterns are measurable.
- Sensitive values are excluded.
- Analytics retention and access are documented.

---

## RS-038 — Decide Whether to Build a Native Android Package

### Requirement

Make the native-app decision after PWA field evidence is available.

### Direction

Compare the current PWA with a Capacitor or native Android package for:

- Background microphone reliability.
- Screen-lock behavior.
- Bluetooth routing.
- Audio focus.
- Notification and foreground-service support.
- Android Auto potential.
- Installation experience.
- Update process.
- Development and maintenance cost.

Do not create a native package merely to hide unresolved backend or WebRTC problems.

### Decision Criteria

Proceed with native packaging when it provides material improvement in:

- Background reliability.
- Bluetooth audio control.
- Foreground ride operation.
- Lock-screen control.
- Rider safety.
- Installation consistency.

### Acceptance Criteria

- The decision references field-test evidence.
- Benefits and maintenance costs are documented.
- The selected direction is approved before major implementation begins.

---

# 3. Recommended Execution Order

## Release Blockers

Complete first:

1. RS-001 — Canonical URL.
2. RS-002 — Firebase redirect.
3. RS-004 — Shared join links.
4. RS-005 — Router protection.
5. RS-007 — Connection indicators.
6. RS-008 — Reconnection.
7. RS-009 — Permission handling.
8. RS-010 — Two-rider field test.
9. RS-013 through RS-017 — Security and privacy.
10. RS-018 — Production smoke suite.

## Production Stabilization

Complete next:

1. RS-019 — Operational telemetry.
2. RS-020 — Health monitoring.
3. RS-021 — Canonical backend.
4. RS-024 — EchoVerse Library API migration.
5. RS-025 — Shared identity.
6. RS-026 — Infrastructure validation.

## Product Polish

Complete after the core is stable:

1. RS-006 — Simplified room flow.
2. RS-027 — Product positioning.
3. RS-028 — Rider identities.
4. RS-029 — Pre-ride audio check.
5. RS-030 — Safer ride interface.
6. RS-031 — Room templates.
7. RS-032 through RS-036 — Documentation and support.
8. RS-037 — Product analytics.
9. RS-038 — Native Android decision.

---

# 4. Non-Goals for This Work Order

Unless separately approved, this work order does not include:

- Recording rider conversations.
- Automatic voice transcription.
- Public social-network features.
- A full messaging platform.
- Building a native iOS application.
- Replacing EchoVerse itself.
- Supporting very large public audio rooms.
- Adding complex subscription or payment systems.
- Deleting legacy infrastructure before migration verification.

---

# 5. Completion Standard

This work order is complete when:

- `rydesync.aerovista.us` is the single public production destination.
- Legacy links safely redirect.
- Shared room links reliably open the intended room.
- Two riders can join, communicate, disconnect, and reconnect during a real-world field test.
- Connection and permission failures are understandable to users.
- Room access and privileged actions are enforced by the backend.
- Voice is not recorded.
- Critical behavior is covered by automated smoke tests.
- Operators can detect outages and diagnose connection failures.
- RydeSync uses one canonical backend.
- EchoVerse playback uses the approved Library API.
- Product positioning, onboarding, privacy, and support information match actual capabilities.
- The native Android decision is based on documented PWA field-test results.
:::

This is structured so each `RS-###` section can be copied directly into AVCC as its own task while the full document remains the controlling work order.

## USER
please add to this avcc export, so i can simpliy import and overwrite:
also while here. clean up by removing test items. weather tasks, projects, people, etc. update dates so we have realistisc targets, add calender items. search for any other pending items that i have and add it all, scheduled and prioritized correctly

**Attachments:**
- aerovista-data-export(2).json

## ASSISTANT
I’ll audit the export structure first, remove obvious demo/test/weather records, reconcile stale and completed work, then add the RydeSync work order, realistic dates, priorities, dependencies, and AVCC calendar entries. I’ll preserve the import schema so the result can replace the current export directly.

## ASSISTANT
The export has 34 projects, 38 tasks, 9 clients, 3 team records, and 13 calendar events. I found clear demo debris—Playwright/Smoke Test/Test clients, placeholder messages, test events, duplicate Valentine events, and a demo-review task—plus many legitimate tasks with dates that expired months ago.

## ASSISTANT
I’m consolidating the stale EchoVerse phase projects into current actionable tasks rather than carrying five overdue “Planning” projects forward. I’m also adding missing active lanes—RydeSync, Profit Compass, AeroVista Identity/Accounts, and the CDA Library Reading Reward App—while keeping real client records and paid invoice history intact.

## ASSISTANT
Done. I rebuilt the AVCC export as a direct overwrite file while preserving the original schema—projects, tasks, clients, team, invoices, messages, and events. The source export already used the expected project structure and import-oriented metadata. L2-L8

[Download the cleaned AVCC overwrite export](sandbox:/mnt/data/aerovista-data-export-cleaned-overwrite-2026-08-01.json)

### What changed

- **31 projects**, reduced from 34
- **111 prioritized tasks**, expanded from 38
- **4 real client records**, reduced from 9
- **3 team records:** Timbr, Byte, and Billy
- **30 calendar events**, rebuilt from 13
- Preserved both invoice records
- Removed all placeholder messages

### Cleanup performed

Removed:

- Playwright Client
- Smoke Test Lead
- Test Client
- Generic Partner and internal EchoVerse client placeholders
- Jeanette and the suspended Sam Alem Team records
- Research Project
- Five obsolete EchoVerse UI phase-project shells
- Demo-review and save-test tasks
- Test calendar entries
- Duplicate Valentine events
- St. Patrick’s Day test project event
- Old generic Team Standup and sales-training entries
- Completed TWR setup tasks that no longer belong in the active task view
- Weather-related records; none remain

The old EchoVerse phase projects were consolidated into the current **EchoVerse Platform Stabilization & Release** project instead of leaving several overdue “Planning” records.

### Major projects added

- **RydeSync Production Consolidation & Launch Readiness**
 - All 38 `RS-001` through `RS-038` work-order items
 - Dependencies, implementation direction, target dates, estimates, priorities, and acceptance criteria

- **Profit Compass Management Intelligence**
 - Drill-down to source transactions
 - Management report packs
 - Financial Story Report
 - Decision Lab
 - Cash Compass
 - Controlled pilot review

- **AeroVista Public Accounts & Identity Integration**
 - Identity schema migration
 - Public account routes
 - NXCore identity gateway
 - AVCC identity synchronization
 - Security and rollback tests

### Additional pending work added or corrected

This includes current known work across:

- AVCC release and cleanup
- Art Localized creator pilot, CTA repair, ad review, and public-market polish
- EchoVerse Android/Android Auto polish, Inspect Track, play history, Edit playback, catalog metadata, and release packaging
- NXCore AVShare repair, startup hardening, repository cleanup, and service documentation
- AeroCore OS shared contracts and workspace pilot
- Horizon curated gallery and 360 presentation
- CDA Library paper-first reading reward pilot
- Summit flagship course
- AeroVista website CTA validation
- Commerce proof purchase
- Creative release board
- Publishing cadence
- 4Runner upgrade planning
- RV vehicle-class decision
- Client follow-ups for Blake and Cindy

### Scheduling

Targets now run from **August 3 through November 6, 2026**, with dependencies sequenced rather than assigning everything the same deadline.

The AVCC calendar now includes:

- Import and validation checkpoint
- Weekly AeroVista operating reviews
- Monthly portfolio reviews
- AVCC release review
- Art Localized creator-pilot checkpoint
- EchoVerse/RydeSync stabilization review
- RydeSync two-rider field test
- RydeSync release-blocker checkpoint
- Horizon and library pilot review
- Profit Compass controlled-pilot review
- AeroCore/Lumina workspace review
- Final RydeSync production-readiness and Android decision

I also checked connected Google Calendar for existing AeroVista, AVCC, and EchoVerse events between August and December; none were returned, so the export calendar did not need deduplication against those searches. Gmail access was declined, so email-only commitments could not be included.