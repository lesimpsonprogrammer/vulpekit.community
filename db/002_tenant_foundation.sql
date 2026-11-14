-- Foundation only: NOT a public registration/provisioning endpoint.
-- Execute by the database owner during controlled migrations.
CREATE SCHEMA IF NOT EXISTS community;

CREATE TABLE IF NOT EXISTS community.tenants (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name text NOT NULL CHECK (length(trim(display_name)) BETWEEN 1 AND 160),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS community.memberships (
    tenant_id uuid NOT NULL REFERENCES community.tenants(id),
    user_id uuid NOT NULL,
    membership_role text NOT NULL CHECK (membership_role IN ('owner','admin','developer','viewer')),
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id,user_id)
);

CREATE TABLE IF NOT EXISTS community.database_requests (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES community.tenants(id),
    requested_name text NOT NULL CHECK (requested_name ~ '^[a-z][a-z0-9_]{2,62}$'),
    request_state text NOT NULL DEFAULT 'pending' CHECK (request_state IN ('pending','approved','rejected')),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(tenant_id,requested_name)
);

-- Default deny for roles that are not owners, superusers or BYPASSRLS.
ALTER TABLE community.tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE community.memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE community.database_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE community.tenants FORCE ROW LEVEL SECURITY;
ALTER TABLE community.memberships FORCE ROW LEVEL SECURITY;
ALTER TABLE community.database_requests FORCE ROW LEVEL SECURITY;

-- Trusted server-side tenant context. Never allow users to run arbitrary SQL
-- using the application's shared database role: PostgreSQL custom settings
-- can be changed by a SQL client and are NOT an authentication mechanism.
DROP POLICY IF EXISTS tenant_scope ON community.tenants;
CREATE POLICY tenant_scope ON community.tenants
    USING (id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid)
    WITH CHECK (id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid);
DROP POLICY IF EXISTS tenant_scope ON community.memberships;
CREATE POLICY tenant_scope ON community.memberships
    USING (tenant_id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid)
    WITH CHECK (tenant_id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid);
DROP POLICY IF EXISTS tenant_scope ON community.database_requests;
CREATE POLICY tenant_scope ON community.database_requests
    USING (tenant_id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid)
    WITH CHECK (tenant_id = NULLIF(current_setting('vulpekit.tenant_id', true), '')::uuid);

REVOKE ALL ON SCHEMA community FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA community FROM PUBLIC;
-- Application-specific grants must be reviewed separately. No user
-- registration, DB creation, or broad database privileges are granted here.
