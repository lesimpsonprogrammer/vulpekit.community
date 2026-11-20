# VulpeKit Community — PostgreSQL inspection

## Read-only relation inventory

```bash
vulpekit doctor
vulpekit check --timeout 5
vulpekit inspect --timeout 5 --limit 100
```

The `inspect` command emits JSON for relations accessible to the configured PostgreSQL role. It lists schema, relation name and type (table, partitioned table, view, materialized view or foreign table), with a `truncated` marker when a limit is reached. It does **not** fetch table rows, read data samples, run migrations, grant permissions, or modify database objects. The result is permission-filtered and **is not a complete database audit**.

Connection configuration uses libpq environment variables (for example `PGHOST`, `PGUSER`, `PGDATABASE`, and `PGPORT`) and a secure credential provider. Remote TLS defaults to `verify-full`; configure trusted certificates and a matching hostname. Never place secrets in a repository, issue, or CI output.

The command uses a read-only session default, a 5-second statement timeout, fixed SQL, bound limit parameter, and 1–500 item limit. Metadata names may themselves be sensitive; do not share reports without authorization. No live database is required for unit tests.

**Current scope:** developer CLI proof of concept. No verified hosted service, tenant isolation, or production readiness is implied.
