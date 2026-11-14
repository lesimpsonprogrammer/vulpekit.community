"""Minimal read-only VulpeKit Community staging health API.

NO registration, user authentication, provisioning or public SQL endpoints.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os


def database_ready() -> bool:
    try:
        import psycopg
        with psycopg.connect(
            host=os.environ["PGHOST"],
            port=int(os.getenv("PGPORT", "5432")),
            dbname=os.environ["PGDATABASE"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            connect_timeout=3,
            options="-c default_transaction_read_only=on",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone() == (1,)
    except Exception:
        return False


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/api/health":
            self.send_error(404)
            return
        healthy = database_ready()
        body = json.dumps({"service": "vulpekit-community-staging", "database": "ready" if healthy else "unavailable"}).encode("utf-8")
        self.send_response(200 if healthy else 503)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
