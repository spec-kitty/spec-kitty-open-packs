"""Regression guard for the pack-reference generator's determinism + checksum.

Runs through the real generator entry points (``build_reference`` /
``render_page`` / ``compute_checksum``) against a realistic on-disk fixture
pack, with no third-party dependency (stdlib ``unittest`` — the repo has no
pytest harness). Run it with::

    python3 -m unittest discover -s tests/docs

The single thing worth guarding here is the property the CI drift gate (WP05)
relies on: re-generating an unchanged pack yields byte-identical output, and the
content checksum is sensitive to both file bytes and file paths.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

_GENERATOR_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "docs" / "gen_pack_reference.py"
)
_spec = importlib.util.spec_from_file_location("gen_pack_reference", _GENERATOR_PATH)
assert _spec and _spec.loader
gen = importlib.util.module_from_spec(_spec)
# Register before executing so dataclass processing can resolve the module's
# namespace (dataclasses looks the module up in sys.modules at class creation).
sys.modules[_spec.name] = gen
_spec.loader.exec_module(gen)


def _make_pack(root: Path) -> Path:
    """Create a small but realistic pack (two kinds, a pack.yaml) on disk."""

    pack = root / "built-in"
    (pack / "directives").mkdir(parents=True)
    (pack / "tactics").mkdir(parents=True)
    (pack / "directives" / "d-001.directive.yaml").write_text(
        "id: D_001\ntitle: First\n", encoding="utf-8"
    )
    (pack / "tactics" / "t-001.tactic.yaml").write_text(
        "id: T_001\ntitle: Tac\n", encoding="utf-8"
    )
    (pack / "pack.yaml").write_text(
        "name: built-in\npack_version: 1.0.0\n", encoding="utf-8"
    )
    return pack


class GeneratorDeterminismTest(unittest.TestCase):
    def test_regeneration_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_pack(root)
            first = gen.render_page(gen.build_reference(root, "built-in", root / "built-in"))
            second = gen.render_page(gen.build_reference(root, "built-in", root / "built-in"))
            self.assertEqual(first, second)
            # The checksum must actually appear in the rendered page.
            checksum = gen.compute_checksum(root / "built-in")
            self.assertIn(checksum, first)

    def test_checksum_changes_with_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            baseline = gen.compute_checksum(pack)
            (pack / "directives" / "d-001.directive.yaml").write_text(
                "id: D_001\ntitle: Changed\n", encoding="utf-8"
            )
            self.assertNotEqual(baseline, gen.compute_checksum(pack))

    def test_checksum_is_path_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            baseline = gen.compute_checksum(pack)
            # Same bytes, different path -> different checksum.
            src = pack / "directives" / "d-001.directive.yaml"
            src.rename(pack / "directives" / "d-002.directive.yaml")
            self.assertNotEqual(baseline, gen.compute_checksum(pack))

    def test_pack_without_pack_yaml_omits_purpose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            (pack / "pack.yaml").unlink()
            page = gen.render_page(gen.build_reference(root, "built-in", pack))
            self.assertIn("No `purpose` is declared", page)


if __name__ == "__main__":
    unittest.main()
