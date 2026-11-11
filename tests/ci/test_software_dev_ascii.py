"""Keep every non-ASCII character out of the software-dev mission authoring content."""

from __future__ import annotations

import unittest
from pathlib import Path

SOFTWARE_DEV = (
    Path(__file__).resolve().parents[2]
    / "packs"
    / "foundation"  # the software-dev mission type moved to foundation in #73
    / "missions"
    / "software-dev"
)


class SoftwareDevAsciiTest(unittest.TestCase):
    def test_no_non_ascii_characters(self) -> None:
        failures: list[str] = []
        examined = 0
        for path in sorted(SOFTWARE_DEV.rglob("*")):
            if not path.is_file():
                continue
            examined += 1
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                for column, character in enumerate(line, 1):
                    if ord(character) >= 128:
                        failures.append(
                            f"{path.relative_to(SOFTWARE_DEV)}:{line_number}:{column}: "
                            f"U+{ord(character):04X}"
                        )
        self.assertGreater(examined, 10, f"{SOFTWARE_DEV} holds no mission files: the check would prove nothing")
        self.assertEqual([], failures, "non-ASCII characters found:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
