# VulpeKit Community 🦊

**Community PostgreSQL developer tools from Momentum Data Solutions**

> **Status:** Early development. This repository is currently named `vulpesdb.pb` on GitHub; the approved new name is `vulpekit.community` (rename pending).

## Purpose

VulpeKit Community is the **public, developer-focused edition** of VulpeKit. It will offer approachable tools, examples, and documentation for connecting to and administering PostgreSQL, with reviewed community contributions. The toolkit is complementary to, but distinct from, the proprietary VulpesDB database hosting platform.

### Three-repository organization

| Repository | Visibility | Purpose |
| --- | --- | --- |
| **`vulpekit.community`** | Public | Approved community code, developer tooling and documentation |
| **`vulpekit.master`** | Private; creation pending | Internal development, testing and governance of the toolkit and community |
| **`vulpesdb.master`** | Private | Commercial PostgreSQL services and MDS database infrastructure |

The planned release flow is **VulpeKit Master → review and security checks → VulpeKit Community**. Nothing is automatically mirrored between private and public repositories.

## First development milestone

This first code change provides:

- A Python 3.11+ package with the `vulpekit` command.
- A **read-only PostgreSQL connectivity check** using Psycopg 3.
- A conservative remote TLS default (`verify-full`).
- Automated unit tests that do not need a live database.
- GitHub Actions continuous integration.

The toolkit targets upstream **PostgreSQL 18.7** for development, but the current CLI uses standard PostgreSQL connectivity and is not an official packaged PostgreSQL server.

## Local installation and use

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Configure PostgreSQL using normal libpq environment variables, for example `PGHOST`, `PGUSER`, `PGDATABASE`, `PGPORT`, and secure authentication through your credential provider. **Never commit passwords or connection strings.**

```bash
vulpekit check --timeout 5
python -m unittest discover -s tests -v
```

The default SSL mode is `verify-full`; supply a trusted server certificate and matching host name when connecting remotely. Local developers may explicitly choose another TLS mode only in their isolated development environment.

## Planned next capabilities

1. Local PostgreSQL 18.7 test environment and health diagnostics.
2. Read-only database metadata inspection and permission-aware commands.
3. Improved developer documentation and configuration validation.
4. A reviewed release and contribution pipeline.

These are **goals**, not existing production services.

## Funding and distributions

A GitHub funding button is planned, pending a verified sponsorship URL or account. No active funding destination is configured.

**Public GitHub source can be downloaded without approval.** Approval can be required for separately distributed official software packages, but not for downloads from a public source repository.

## Security and licensing

Do not submit secrets, production configuration, private customer information, or proprietary code. Sensitive vulnerability reports should be handled privately.

PostgreSQL uses the PostgreSQL License. A license for **original VulpeKit code** has not yet been selected; public visibility does not automatically grant reuse rights. Contributions will need an explicit license and contribution policy before broader public acceptance.

© Momentum Data Solutions. VulpeKit is independent of the PostgreSQL Global Development Group.
