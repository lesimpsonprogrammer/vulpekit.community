# VulpeKit Community — Oracle Cloud staging deployment

This project includes a **staging example**, NOT a production-ready public database service. It uses one Oracle VM for a static site, a read-only /api/health API and an isolated PostgreSQL 18.7 service. **No public account registration, tenant provisioning, database client access or SQL console is implemented.**

## Oracle readiness (read-only check before deployment)

1. Confirm the VM is eligible for your Oracle Cloud free-tier allocation and sufficient capacity remains.
2. Verify VM CPU architecture supports the chosen container images, available disk storage, and OS security updates.
3. Check the VM isn't currently hosting Cloud Performance Deploy + Host or other critical workloads; prefer a dedicated isolated instance.
4. Verify VCN ingress/security rules. Only 80/443 should be public for this staging site; restrict SSH to trusted management IPs. Never expose 5432, 8080 or Docker daemon ports.
5. Select the public hostname and configure DNS to the dedicated VM's verified public IP. Caddy needs a reachable hostname to provision an HTTPS certificate.

## Deploy only after explicit infrastructure approval

On the verified, isolated Oracle VM with Docker Compose installed:

```bash
git clone https://github.com/lesimpsonprogrammer/vulpekit.community.git
cd vulpekit.community
cp deploy/.env.example deploy/.env
# Edit deploy/.env locally; set COMMUNITY_DOMAIN to your approved DNS name
# and VULPEKIT_DB_PASSWORD to a fresh, strong, development-only secret.
docker compose --env-file deploy/.env -f deploy/compose.yaml config
docker compose --env-file deploy/.env -f deploy/compose.yaml up -d --build
docker compose --env-file deploy/.env -f deploy/compose.yaml ps
```

The web service automatically serves files under `site/`, the API serves only `/api/health`, and PostgreSQL is only accessible on the internal Compose network. `/api/health` intentionally exposes a limited readiness status, not connection details.

## Important protections before launching public database access

- Implement authenticated registration, email verification and anti-abuse controls.
- Build tenant-isolated provisioning with separate database roles and resource quotas.
- Add rate limits, auditing, secrets storage, backups and restore tests.
- Add operational monitoring, patching and incident response.
- Prove isolation with automated authorization and tenant-boundary tests.
- Keep VulpesDB Master enterprise customer databases completely separate.

**Never use this staging compose file as-is for commercial public database hosting.**
