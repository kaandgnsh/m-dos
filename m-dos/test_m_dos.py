import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("m-dos.py")
SPEC = importlib.util.spec_from_file_location("m_dos_local_lab", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class TargetValidationTests(unittest.TestCase):
    def test_accepts_localhost(self):
        self.assertEqual(
            MODULE.validate_target("http://localhost:8000/"),
            "http://localhost:8000/",
        )

    def test_accepts_loopback_ipv4(self):
        self.assertEqual(
            MODULE.validate_target("http://127.0.0.1:8000/"),
            "http://127.0.0.1:8000/",
        )

    def test_accepts_loopback_ipv6(self):
        self.assertEqual(
            MODULE.validate_target("http://[::1]:8000/"),
            "http://[::1]:8000/",
        )

    def test_rejects_remote_host(self):
        with self.assertRaises(ValueError):
            MODULE.validate_target("https://example.com/")

    def test_rejects_unsupported_scheme(self):
        with self.assertRaises(ValueError):
            MODULE.validate_target("ftp://localhost/file")

    def test_rejects_embedded_credentials(self):
        with self.assertRaises(ValueError):
            MODULE.validate_target("http://user:pass@localhost/")

    def test_duration_bounds(self):
        self.assertEqual(MODULE.validate_duration(1), 1)
        self.assertEqual(MODULE.validate_duration(30), 30)
        for duration in (0, -1, 31):
            with self.subTest(duration=duration):
                with self.assertRaises(ValueError):
                    MODULE.validate_duration(duration)


if __name__ == "__main__":
    unittest.main()
