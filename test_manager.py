import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import manager


class PasswordFileTests(unittest.TestCase):
    def setUp(self):
        self.original_password_file = manager.PASSWORDS_FILE
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.password_file = Path(directory) / "passwords.json"
        self.enterContext(patch.object(manager, "PASSWORDS_FILE", self.password_file))
        self.output = self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.subprocess_run = self.enterContext(patch.object(manager.subprocess, "run"))
        self.entry = {
            "Website": "example.test",
            "Username": "test-user",
            "Password": "test-password",
        }

    def test_paths_are_relative_to_script(self):
        self.assertEqual(
            self.original_password_file,
            Path(manager.__file__).resolve().with_name("passwords.json"),
        )
        self.assertEqual(
            manager.MAIN_MANAGER_FILE,
            Path(manager.__file__).resolve().with_name("main_manager.py"),
        )

    def test_load_missing_file_reports_empty_store(self):
        manager.load_passwords()
        self.assertIn("No saved passwords found", self.output.getvalue())
        self.assertFalse(self.password_file.exists())
        self.subprocess_run.assert_called_once_with(
            [manager.sys.executable, str(manager.MAIN_MANAGER_FILE)]
        )

    def test_save_creates_missing_file(self):
        with patch("builtins.input", side_effect=[
            "test-password", "test-password", "example.test", "test-user"
        ]):
            manager.save_password()
        self.assertEqual(json.loads(self.password_file.read_text()), [self.entry])

    def test_save_preserves_existing_entries(self):
        self.password_file.write_text(json.dumps([self.entry]))
        with patch("builtins.input", side_effect=[
            "another-password", "another-password", "other.test", "other-user"
        ]):
            manager.save_password()
        entries = json.loads(self.password_file.read_text())
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], self.entry)
        self.assertEqual(entries[1]["Website"], "other.test")

    def test_load_uses_store_outside_working_directory(self):
        self.password_file.write_text(json.dumps([self.entry]))
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                Path("passwords.json").write_text("[]")
                manager.load_passwords()
            finally:
                os.chdir(original_cwd)
        self.assertIn("example.test", self.output.getvalue())
        self.assertEqual(json.loads(self.password_file.read_text()), [self.entry])

    def test_search_missing_file_reports_empty_store(self):
        with patch("builtins.input", side_effect=["example.test", "n"]):
            manager.search_data()
        self.assertIn("No saved passwords found", self.output.getvalue())
        self.assertFalse(self.password_file.exists())

    def test_delete_missing_file_reports_empty_store(self):
        with patch("builtins.input", return_value="example.test"):
            manager.delete_password()
        self.assertIn("no saved entries to delete", self.output.getvalue())
        self.assertFalse(self.password_file.exists())

    def test_invalid_json_is_not_treated_as_missing(self):
        self.password_file.write_text("{invalid json")
        with self.assertRaises(json.JSONDecodeError):
            manager.load_passwords()
        self.assertEqual(self.password_file.read_text(), "{invalid json")
        self.subprocess_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
