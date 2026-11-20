"""Minimal, read-only PostgreSQL connectivity and offline configuration diagnostics."""

import argparse
import json
import os
import sys

from vulpekit.inspect import inspect_database


def inspect_config(environ=None) -> list[str]:
    """Return generic configuration warnings without exposing environment values."""
    env = os.environ if environ is None else environ
    warnings = []
    if not env.get("PGHOST"):
        warnings.append("PGHOST is not configured.")
    if not env.get("PGUSER"):
        warnings.append("PGUSER is not configured.")
    if env.get("PGSSLMODE", "verify-full") != "verify-full":
        warnings.append("TLS hostname verification is not enabled (PGSSLMODE should be verify-full for remote use).")
    return warnings


def check_connection(timeout: int = 5) -> bool:
    """Validate a configured PostgreSQL connection without modifying data."""
    if not os.environ.get("PGHOST") or not os.environ.get("PGUSER"):
        raise ValueError("Set PGHOST and PGUSER before running the connection check.")

    # Imported only when a real connection is requested; avoids exposing DSNs in logs.
    import psycopg

    # Defaults to verifying both server certificate and host name.
    # PGSSLMODE may be set explicitly when connecting to a local development server.
    sslmode = os.environ.get("PGSSLMODE", "verify-full")
    with psycopg.connect(
        connect_timeout=timeout,
        sslmode=sslmode,
        autocommit=True,
        options="-c default_transaction_read_only=on",
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="vulpekit", description="VulpeKit PostgreSQL tools")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Check configured PostgreSQL connectivity")
    check.add_argument("--timeout", type=int, default=5)
    commands.add_parser("doctor", help="Validate connection environment without opening a connection")
    inspect_cmd = commands.add_parser("inspect", help="List SELECT-accessible schemas and relations as JSON")
    inspect_cmd.add_argument("--timeout", type=int, default=5)
    inspect_cmd.add_argument("--limit", type=int, default=100)
    args = parser.parse_args(argv)

    if args.command == "doctor":
        warnings = inspect_config()
        if warnings:
            for warning in warnings:
                print(f"WARNING: {warning}")
            return 1
        print("PostgreSQL connection environment looks ready (connectivity not tested).")
        return 0

    if args.command == "inspect":
        if not 1 <= args.timeout <= 30:
            parser.error("--timeout must be between 1 and 30 seconds")
        if not 1 <= args.limit <= 500:
            parser.error("--limit must be between 1 and 500")
        try:
            report = inspect_database(timeout=args.timeout, limit=args.limit)
        except Exception:
            print("PostgreSQL inspection failed. Verify access and TLS.", file=sys.stderr)
            return 1
        print(json.dumps(report, indent=2))
        return 0

    if args.command == "check":
        if not 1 <= args.timeout <= 30:
            parser.error("--timeout must be between 1 and 30 seconds")
        try:
            healthy = check_connection(timeout=args.timeout)
        except Exception:
            # Never echo connection strings, server error details, or passwords.
            print("PostgreSQL connectivity check failed. Verify settings and TLS.", file=sys.stderr)
            return 1
        if healthy:
            print("PostgreSQL connection healthy.")
            return 0
        print("PostgreSQL health query returned an unexpected response.", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
