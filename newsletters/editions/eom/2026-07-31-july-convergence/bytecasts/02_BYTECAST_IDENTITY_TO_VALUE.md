This is ByteCast.

The July identity, business systems, and commerce review.

Every operating company eventually has to answer the same questions.

Who is this person?

What are they allowed to do?

What business do they belong to?

What work was promised?

What work was performed?

What did it cost?

What can be billed?

And did the company create value?

July brought AeroVista closer to answering those questions through one connected architecture.

The public identity path is now live.

A user enters through the canonical AeroVista account routes.

Firebase handles credentials, email verification, recovery, and token issuance.

The request then moves through the public identity gateway on NXCore.

Cloudflare Tunnel protects the connection.

AVCC remains the canonical authority for the person, profile, provider links, account state, roles, badges, and preferences.

Individual services then decide exact resource access.

That separation prevents one login system from becoming an excuse for unlimited authority.

A verified free signup may receive the AeroVista member capability.

It does not automatically receive Art Localized builder access.

It does not automatically gain Profit Compass pilot access.

It does not become an operator, founder, administrator, or creator simply because the account exists.

Identity proves who the person is.

Capability defines broad access.

Resource membership defines the exact scope.

Action permission defines what may be done.

Audit records what actually happened.

That is the model.

July also clarified AVCC’s role.

AVCC is not every division’s production editor.

It is the commercial and operational core.

AeroCore OS manages the platform.

Division Workspaces perform specialized work.

AVCC records the business relationship and accountable outcome.

That means AVCC should own contacts, customers, opportunities, quotes, engagements, projects, work orders, tasks, costs, invoices, payments, profitability, approvals, and executive visibility.

It should answer:

Who is the client?

What did they request?

What did AeroVista agree to deliver?

Which division owns the work?

Who performed it?

What did it cost?

What is billable?

What has been approved?

What belongs on the invoice?

Has the invoice been paid?

Was the project profitable?

To support that model, July established a three-ledger architecture.

The Activity Ledger records what occurred.

A flight completed.

A render finished.

A file was uploaded.

A track was approved.

A course was published.

A client requested a revision.

The Work Ledger converts meaningful activity into accountable work.

Two hours of design.

One field-capture session.

Three renders.

A revision cycle.

An external expense.

A storage charge.

A deployment.

The Billing Ledger contains only approved commercial value.

A fixed-fee package.

A completed milestone.

An approved overage.

A recurring support charge.

A reimbursable expense.

This progression matters.

Activity is not automatically billing.

Application-open time is not automatically labor.

Worker usage is not automatically a customer charge.

Internal cost and client price are not the same field.

The company needs evidence without creating surveillance.

It needs cost visibility without inventing invoices.

It needs controlled billing without losing the details that explain margin.

Profit Compass applies a similar philosophy to member businesses.

The system is intentionally separate from AeroVista corporate accounting.

It is designed for members operating their own independent businesses.

The product now supports income, direct costs, operating expenses, products, events, CSV imports, correction history, report snapshots, YTD cash-basis profit and loss, exports, audit records, invitations, policy acknowledgement, support access, and controlled data requests.

The Cash Commitment Map adds another layer.

A profit-and-loss statement asks whether the business earned money during a period.

The Cash Commitment Map asks what is actually safe to spend after known obligations.

Cash on hand.

Bills.

Payroll.

Taxes.

Subscriptions.

Expected customer payments.

Overdue items.

Thirty-, sixty-, and ninety-day commitments.

That difference makes Profit Compass more useful than a simple calculator.

The current product has forty-three out of forty-three tests passing.

The API is healthy.

PostgreSQL is persistent.

The frontend and database restart automatically.

A live session-signing secret was removed from source and rotated into protected system configuration.

Bigcapital remains disabled, clean, and untouched.

The product is no longer blocked by missing features.

It is blocked by three control decisions.

First, the whole-store read-modify-write pattern must be serialized so two requests cannot overwrite each other.

Second, the business-role permission matrix must be approved and enforced.

Owner.

Bookkeeper.

Contributor.

Viewer.

Those roles cannot remain labels without real restrictions.

Third, export and deletion requests must be fulfilled through an authorized support path rather than allowing an ordinary member to approve their own sensitive request.

After those controls, the premium roadmap becomes clear.

Drill every total down to the source transactions.

Turn reports into polished management packs and a deterministic Financial Story.

Build a Decision Lab where members can test price, volume, cost, and event assumptions without changing real records.

Then expand the Cash Commitment Map into a fuller Cash Compass.

Commerce advanced in parallel.

Gear remained the protected live storefront.

The multi-store backend now supports store-aware catalogs, cart quotes, sandbox checkout, signed webhooks, persistent rate limits, PostgreSQL, isolation, and rollback rehearsal.

Fifty-eight backend tests passed.

The dependency audit was clean.

Production catalog data remained protected.

But production slash V-one is still intentionally offline.

The public ingress path continues to encounter a same-URL redirect loop.

That is a release gate, not a sandbox failure.

The storefront strategy also improved.

AeroVista does not need one identical frontend for every store.

It needs one dependable commerce foundation underneath multiple appropriate experiences.

Gear can remain direct and retail-focused.

Horizon can lead with artwork, story, scale, canvas, and room presentation.

The engine can be shared without forcing the brands to look or behave the same.

That is the larger July achievement.

Identity now has a real public path.

AVCC has a defined business role.

Profit Compass has become a credible pilot product.

Commerce has a tested foundation.

The next step is not more architectural imagination.

It is enforcing the controls, releasing carefully, and connecting identity to accountable value.

This has been ByteCast.

From identity to access.

From activity to work.

From work to value.
