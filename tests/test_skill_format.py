import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from skill_format import validate_skill


class FormatTests(unittest.TestCase):
    def validate(self, front):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "example"
            folder.mkdir()
            path = folder / "SKILL.md"
            path.write_text("---\n" + front + "\n---\nPerform the requested task.\n", encoding="utf-8")
            return validate_skill(path)

    def test_valid_metadata_and_multiline_description(self):
        self.assertEqual(self.validate("name: example\ndescription: >\n  Use for a relevant task.\n  This language need not match a literal routing phrase.\nmetadata:\n  version: '1.2.0'"), [])

    def test_top_level_version_is_rejected(self):
        self.assertTrue(any("Unsupported" in e for e in self.validate("name: example\ndescription: Task\nversion: 1.2.0")))

    def test_duplicate_key_is_rejected(self):
        self.assertTrue(any("Duplicate" in e for e in self.validate("name: example\nname: different\ndescription: Task")))

    def test_types_and_limits(self):
        self.assertTrue(self.validate("name: example\ndescription: 12\nmetadata:\n  revision: 2"))
        self.assertTrue(self.validate("name: example\ndescription: " + "x" * 1025))

    def test_mixed_unknown_keys_are_errors_not_crashes(self):
        self.assertTrue(self.validate("name: example\ndescription: Task\n1: extra\nother: extra"))


if __name__ == "__main__":
    unittest.main()
