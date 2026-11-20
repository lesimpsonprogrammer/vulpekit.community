"""Offline configuration diagnostics: never contact a database or print secrets."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from vulpekit import cli

class DoctorTests(unittest.TestCase):
    def test_missing_required_environment(self):
        with patch.dict("os.environ", {}, clear=True), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["doctor"]), 1)
        self.assertIn("PGHOST", output.getvalue())
        self.assertIn("PGUSER", output.getvalue())

    def test_secure_environment_passes_without_network(self):
        env = {"PGHOST": "db.example.org", "PGUSER": "developer", "PGSSLMODE": "verify-full"}
        with patch.dict("os.environ", env, clear=True), patch.object(cli, "check_connection", side_effect=AssertionError("must not connect")), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["doctor"]), 0)
        self.assertIn("connectivity not tested", output.getvalue())

    def test_tls_warning_never_leaks_secret(self):
        env = {"PGHOST": "localhost", "PGUSER": "tester", "PGPASSWORD": "super-secret", "PGSSLMODE": "disable"}
        with patch.dict("os.environ", env, clear=True), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["doctor"]), 1)
        self.assertIn("TLS", output.getvalue())
        self.assertNotIn("super-secret", output.getvalue())

if __name__ == "__main__":
    unittest.main()
