"""Fast CLI checks that require no running PostgreSQL service."""

import io
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

from vulpekit import cli


class CliTests(unittest.TestCase):
    def test_healthy_connection(self):
        with patch.object(cli, "check_connection", return_value=True), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["check"]), 0)
        self.assertIn("healthy", output.getvalue())

    def test_failure_does_not_leak_exception(self):
        secret = "postgres://user:secret@db.example"
        with patch.object(cli, "check_connection", side_effect=RuntimeError(secret)), redirect_stderr(io.StringIO()) as output:
            self.assertEqual(cli.main(["check"]), 1)
        self.assertNotIn(secret, output.getvalue())

    def test_missing_configuration(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                cli.check_connection()

    def test_negative_timeout_rejected(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as failure:
                cli.main(["check", "--timeout", "-1"])
        self.assertEqual(failure.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
