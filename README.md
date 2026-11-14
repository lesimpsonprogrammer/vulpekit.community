# VulpesDB PB — Public Edition 🦊

**Open PostgreSQL tooling from Momentum Data Solutions**

**Purpose:** VulpesDB PB (`vulpesdb.pb`) is the community-facing edition of VulpesDB. It aims to make PostgreSQL administration, connectivity, and developer tooling accessible, inspectable, and reusable by individuals and teams.

- **Visibility:** Public (subject to change by repository owner)
- **Engine baseline:** Upstream PostgreSQL 18.7
- **Website (planned):** https://vulpesdb.momentumdatasolutions.com/
- **Tagline:** *Intelligent by Nature. Dependable by Design.*

## Intended capabilities

- Local PostgreSQL development and documented setup
- Database and connection management interfaces
- Health checks and basic operational observability
- Community documentation, examples, and issue reporting
- Secure-by-default workflows and standard PostgreSQL compatibility

These are roadmap goals, **not claims of implemented or production-ready features**.

## How PB differs from Master

| | **VulpesDB PB** (this repository) | **VulpesDB Master** |
|---|---|---|
| GitHub | `vulpesdb.pb` | `vulpesdb.master` |
| Visibility | Public | Private |
| Purpose | Community/developer foundation | Proprietary managed database platform |
| Audience | Developers and contributors | MDS operations and approved business customers |
| Focus | Open tools and documentation | Enterprise provisioning, tenant isolation, managed services, billing, recovery and integrations |

Both editions are based on official PostgreSQL releases. **No proprietary code, production secrets, customer data, or private configurations may be copied from Master into PB without explicit authorization and review.**

## Download and access policy

**Important:** Public GitHub repositories can be cloned or downloaded without approval. If we require approval *before obtaining source code*, this repository must be private, or distributable source must be stored in an access-controlled service rather than GitHub. We may separately require approval for **official packaged installers** distributed through an MDS-controlled portal, while the repository stays public.

## Support development

VulpesDB PB welcomes community support. A GitHub Sponsor button will be activated when an approved, working funding destination is configured. No payment URL is currently asserted to be active.

## Security

Do not commit API keys, credentials, production connection strings, customer information, or internal infrastructure configuration. Use least privilege and encrypted connections. Report security issues privately rather than disclosing exploitable details in public issues.

## Licensing and contributions

PostgreSQL itself is distributed under the **PostgreSQL License**. The license for original VulpesDB PB source must be selected and added explicitly before promoting this as an independently licensed open-source distribution. Public visibility alone does not grant rights to reuse original source. Contributions should be submitted through reviewable pull requests.

© Momentum Data Solutions. VulpesDB is independent of the PostgreSQL Global Development Group.
