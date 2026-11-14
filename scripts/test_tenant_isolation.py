"""PostgreSQL tenant foundation test; writes ONLY to dedicated ephemeral CI DB."""
import os
from pathlib import Path
from uuid import uuid4

def main():
    expected = {
        "GITHUB_ACTIONS": "true",
        "VULPEKIT_TEST_MODE": "ephemeral-ci-only",
        "PGHOST": "127.0.0.1",
        "PGPORT": "5432",
        "PGDATABASE": "vulpekit_tenant_ci",
        "PGUSER": "vulpekit_ci",
    }
    if any(os.getenv(key) != value for key, value in expected.items()):
        raise RuntimeError("Refusing to modify anything other than dedicated CI database")

    import psycopg
    from psycopg import errors

    sql = (Path(__file__).resolve().parents[1] / "db/002_tenant_foundation.sql").read_text()
    tenant_a, tenant_b = uuid4(), uuid4()
    with psycopg.connect(connect_timeout=5) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cur.execute(sql)  # repeatable bootstrap
            cur.execute("INSERT INTO community.tenants(id,display_name) VALUES (%s,'Tenant A'),(%s,'Tenant B')", (tenant_a,tenant_b))
            cur.execute("INSERT INTO community.database_requests(tenant_id,requested_name) VALUES (%s,'db_alpha'),(%s,'db_bravo')", (tenant_a,tenant_b))
            cur.execute("CREATE ROLE vulpekit_test_app NOLOGIN NOSUPERUSER NOBYPASSRLS")
            cur.execute("GRANT vulpekit_test_app TO vulpekit_ci")
            cur.execute("GRANT USAGE ON SCHEMA community TO vulpekit_test_app")
            cur.execute("GRANT SELECT, INSERT ON community.tenants, community.memberships, community.database_requests TO vulpekit_test_app")
            cur.execute("SET ROLE vulpekit_test_app")

            for table in ("tenants", "memberships", "database_requests"):
                cur.execute(f"SELECT count(*) FROM community.{table}")
                assert cur.fetchone()[0] == 0, f"Unscoped access to {table}"

            cur.execute("SELECT set_config('vulpekit.tenant_id', %s, true)", (str(tenant_a),))
            cur.execute("SELECT requested_name FROM community.database_requests")
            assert cur.fetchall() == [("db_alpha",)]
            cur.execute("SELECT display_name FROM community.tenants")
            assert cur.fetchall() == [("Tenant A",)]

            # RLS WITH CHECK blocks inserting another tenant's data.
            cur.execute("SAVEPOINT isolation_violation")
            try:
                cur.execute("INSERT INTO community.database_requests(tenant_id,requested_name) VALUES (%s,'db_cross')", (tenant_b,))
            except errors.InsufficientPrivilege:
                cur.execute("ROLLBACK TO SAVEPOINT isolation_violation")
            else:
                raise AssertionError("Cross-tenant insertion was unexpectedly permitted")

            cur.execute("SELECT set_config('vulpekit.tenant_id', %s, true)", (str(tenant_b),))
            cur.execute("SELECT requested_name FROM community.database_requests")
            assert cur.fetchall() == [("db_bravo",)]
            cur.execute("RESET ROLE")

    print("Isolated tenant metadata row-level policies passed on ephemeral PostgreSQL.")

if __name__ == "__main__":
    main()
