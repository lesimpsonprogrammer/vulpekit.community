import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

API_PATH = Path(__file__).resolve().parents[1] / "app" / "main.py"
spec = importlib.util.spec_from_file_location("vulpekit_staging_api", API_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DatabaseReadinessTests(unittest.TestCase):
    def test_unconfigured_connection_fails_closed(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertFalse(module.database_ready())

    def test_server_has_health_handler(self):
        self.assertTrue(hasattr(module.Handler, "do_GET"))

    def test_staging_exposes_no_provisioning_api(self):
        source = API_PATH.read_text(encoding="utf-8")
        self.assertNotIn("/api/provision", source)
        self.assertNotIn("/api/signup", source)


if __name__ == "__main__":
    unittest.main()
