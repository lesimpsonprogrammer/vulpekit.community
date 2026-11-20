"""Unit tests for safe, read-only PostgreSQL relation inventory."""
import io
import json
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import MagicMock, patch
from vulpekit import cli
from vulpekit.inspect import inspect_database


class InspectTests(unittest.TestCase):
    def test_metadata_query_and_limit(self):
        connection = MagicMock()
        cursor = connection.__enter__.return_value.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = [("public", "accounts", "table"), ("reporting", "summary", "view")]
        with patch.dict("os.environ", {"PGHOST": "db.example", "PGUSER": "reader"}, clear=True):
            with patch("psycopg.connect", return_value=connection) as connect:
                result = inspect_database(timeout=5, limit=1)
        self.assertEqual(result["relations"], [{"schema": "public", "name": "accounts", "kind": "table"}])
        self.assertTrue(result["truncated"])
        self.assertEqual(cursor.execute.call_args.args[1], (2,))
        sql = cursor.execute.call_args.args[0]
        self.assertIn("has_table_privilege", sql)
        self.assertIn("has_schema_privilege", sql)
        self.assertIn("default_transaction_read_only=on", connect.call_args.kwargs["options"])

    def test_invalid_limits_refused_before_connection(self):
        for limit in (0, 501):
            with self.assertRaises(ValueError):
                inspect_database(limit=limit)

    def test_cli_sanitizes_errors(self):
        secret = "postgresql://user:secret@host/"
        with patch.object(cli, "inspect_database", side_effect=RuntimeError(secret)):
            with redirect_stderr(io.StringIO()) as output:
                result = cli.main(["inspect"])
        self.assertEqual(result, 1)
        self.assertNotIn(secret, output.getvalue())

    def test_cli_prints_json_without_network_in_mock(self):
        report = {"relations": [], "truncated": False, "limit": 100, "note": "Read only"}
        with patch.object(cli, "inspect_database", return_value=report), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["inspect"]), 0)
        self.assertEqual(json.loads(output.getvalue()), report)

    def test_cli_rejects_invalid_limit(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as exc:
                cli.main(["inspect", "--limit", "999"])
        self.assertEqual(exc.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
