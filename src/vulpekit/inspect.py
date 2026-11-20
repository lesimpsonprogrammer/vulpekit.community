"""Permission-aware, read-only PostgreSQL schema and relation inventory."""
from __future__ import annotations

import os


def inspect_database(timeout: int = 5, limit: int = 100) -> dict:
    """Return visible user schemas and relations, without reading table rows."""
    if not 1 <= timeout <= 30:
        raise ValueError("timeout must be between 1 and 30 seconds")
    if not 1 <= limit <= 500:
        raise ValueError("limit must be between 1 and 500")
    if not os.getenv("PGHOST") or not os.getenv("PGUSER"):
        raise ValueError("PGHOST and PGUSER are required")

    import psycopg

    # Never store or log a connection string. libpq resolves credentials externally.
    with psycopg.connect(
        connect_timeout=timeout,
        sslmode=os.getenv("PGSSLMODE", "verify-full"),
        options="-c default_transaction_read_only=on -c statement_timeout=5000",
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT n.nspname,
                       c.relname,
                       CASE c.relkind
                           WHEN 'r' THEN 'table'
                           WHEN 'p' THEN 'partitioned_table'
                           WHEN 'v' THEN 'view'
                           WHEN 'm' THEN 'materialized_view'
                           WHEN 'f' THEN 'foreign_table'
                       END AS kind
                FROM pg_catalog.pg_class AS c
                JOIN pg_catalog.pg_namespace AS n ON n.oid = c.relnamespace
                WHERE c.relkind IN ('r', 'p', 'v', 'm', 'f')
                  AND n.nspname <> 'information_schema'
                  AND n.nspname NOT LIKE 'pg\\_%' ESCAPE '\\'
                  AND pg_catalog.has_schema_privilege(n.oid, 'USAGE')
                  AND pg_catalog.has_table_privilege(c.oid, 'SELECT')
                ORDER BY n.nspname, c.relname
                LIMIT %s
                """,
                (limit + 1,),
            )
            rows = cursor.fetchall()
    return {
        "relations": [
            {"schema": schema, "name": name, "kind": kind}
            for schema, name, kind in rows[:limit]
        ],
        "truncated": len(rows) > limit,
        "limit": limit,
        "note": "Inventory of SELECT-accessible relations only; no table rows retrieved.",
    }
