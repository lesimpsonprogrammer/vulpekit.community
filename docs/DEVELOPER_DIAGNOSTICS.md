# VulpeKit Community — Developer diagnostics

VulpeKit is an early-development PostgreSQL toolkit, not a hosted database service.

## Offline configuration check

```bash
vulpekit doctor
```

Checks whether `PGHOST` and `PGUSER` are present and whether `PGSSLMODE` enables `verify-full` TLS verification. It opens **no database connection**, prints **no environment values or passwords**, and exits with status 1 when warnings are present. A passing result **does not** confirm that any database is reachable or secure.

## Read-only connectivity check

```bash
vulpekit check --timeout 5
```

Requires a configured PostgreSQL server and checks `SELECT 1` with a read-only transaction default. It does not provision databases, run migrations, or validate tenancy isolation.

## Development milestones

- Configuration validation and tests (this change).
- Read-only inspection with documented permission requirements.
- Local PostgreSQL integration-test fixture.
- Public contribution policy and an explicitly selected license for original code.
- Independent tenant-isolation review before any multi-tenant release.

Do not commit credentials, customer information, or any private VulpeKit Master implementation to this public repository.
