# VulpeKit Community tenant metadata foundation

This is a **review-only PostgreSQL migration** and CI test, not a live service.

- `community.tenants`: organization registry.
- `community.memberships`: future user-to-tenant association, with membership role vocabulary.
- `community.database_requests`: requests only; no databases are provisioned.
- Explicit RLS and FORCE RLS on each table, with no broad PUBLIC grants.
- Dedicated ephemeral PostgreSQL 18.7 CI tests for default-deny reads, cross-tenant visibility and insertion rejection.

## Security boundary limitations

The `vulpekit.tenant_id` custom session setting is **not independently secure**. Any untrusted user allowed to execute arbitrary SQL through the shared app role can change it. Do not expose that role or an SQL console to end users. A future backend must authenticate identities server-side, authorize membership for the requested tenant, scope the transaction with `SET LOCAL` and never expose raw connections/queries. Use separate per-tenant database roles or separate databases for customer SQL workloads.

The SQL schema contains **no users' passwords, no authentication implementation, no invitations, no signup endpoints, and no running provisioning worker**. Role values here are metadata, not working role-based access control.

For staging/production, plan a versioned migration and a separate non-owner, non-BYPASSRLS application role with minimum grants. Existing `deploy/compose.yaml` and `app/main.py` remain unchanged. No migrations will run automatically on the existing Oracle staging or local databases.

Before enabling public registration, add an audited authentication system, identity-to-membership enforcement, anti-abuse controls, tenant-aware APIs, backup/recovery, and integration tests through actual user sessions.
