"""Disposable PostgreSQL catalog inventory integration fixture.

Runs ONLY against a dedicated GitHub Actions PostgreSQL service. Does not
touch production databases, and rolls back all fixture objects.
"""
import os

EXPECTED = {
    "GITHUB_ACTIONS": "true",
    "VULPEKIT_TEST_MODE": "catalog-ci-only",
    "PGHOST": "127.0.0.1",
    "PGPORT": "5432",
    "PGDATABASE": "vulpekit_catalog_ci",
    "PGUSER": "vulpekit_catalog_ci",
}
if any(os.getenv(k) != v for k, v in EXPECTED.items()):
    raise SystemExit("Refusing to run outside dedicated ephemeral catalog CI")

import psycopg
from psycopg import sql
from vulpekit.inspect import INSPECTION_SQL

with psycopg.connect(sslmode="disable") as conn:
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE ROLE catalog_reader NOLOGIN NOSUPERUSER NOBYPASSRLS")
            cur.execute("GRANT catalog_reader TO vulpekit_catalog_ci")
            cur.execute('CREATE SCHEMA "catalog fixture"')
            cur.execute('CREATE SCHEMA "catalog hidden"')
            cur.execute('CREATE TABLE "catalog fixture"."Order \"Details\" 🦊" (id integer)')
            cur.execute('CREATE VIEW "catalog fixture"."Sales report" AS SELECT 1 AS id')
            cur.execute('CREATE TABLE "catalog fixture"."not granted" (id integer)')
            cur.execute('CREATE TABLE "catalog hidden"."private" (id integer)')
            cur.execute('GRANT USAGE ON SCHEMA "catalog fixture" TO catalog_reader')
            cur.execute('GRANT SELECT ON "catalog fixture"."Order \"Details\" 🦊" TO catalog_reader')
            cur.execute('GRANT SELECT ON "catalog fixture"."Sales report" TO catalog_reader')
            cur.execute('GRANT SELECT ON "catalog hidden"."private" TO catalog_reader')
            cur.execute("SET ROLE catalog_reader")
            cur.execute(INSPECTION_SQL, (100,))
            rows = cur.fetchall()
            expected = {
                ("catalog fixture", 'Order "Details" 🦊', "table"),
                ("catalog fixture", "Sales report", "view"),
            }
            actual = set(rows)
            assert actual == expected, f"Unexpected catalog rows: {actual!r}"
            cur.execute(INSPECTION_SQL, (2,))
            assert len(cur.fetchall()) == 2
            cur.execute("RESET ROLE")
            print("Catalog privileges, special identifiers, and read-only metadata: PASS")
    finally:
        conn.rollback()
