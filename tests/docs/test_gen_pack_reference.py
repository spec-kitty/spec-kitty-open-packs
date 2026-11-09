"""Regression guard for the pack-reference generator's determinism + checksum.

Runs through the real generator entry points (``build_reference`` /
``render_page`` / ``compute_checksum``) against a realistic on-disk fixture
pack, on stdlib ``unittest`` (the repo has no pytest harness) plus the
generator's own ``pyyaml``. Run it with::

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

    pack = root / "packs" / "built-in"
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
    (pack / "pack.md").write_text(
        "# built-in\n"
        "\n"
        "The baseline pack every project starts with.\n"
        "\n"
        "## Details\n"
        "\n"
        "Section prose that must not render as the description.\n",
        encoding="utf-8",
    )
    return pack


class GeneratorDeterminismTest(unittest.TestCase):
    def test_regeneration_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_pack(root)
            first = gen.render_page(gen.build_reference(root, "built-in", root / "packs" / "built-in"))
            second = gen.render_page(gen.build_reference(root, "built-in", root / "packs" / "built-in"))
            self.assertEqual(first, second)
            # The checksum must actually appear in the rendered page.
            checksum = gen.compute_checksum(root / "packs" / "built-in")
            self.assertIn(checksum, first)

    def test_check_gate_fails_closed_on_orphaned_generated_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            docs = root / "docs" / "packs"
            self.assertEqual(gen.generate(root, docs, check=False), 0)
            self.assertEqual(gen.generate(root, docs, check=True), 0)
            # Hand-authored pages that lack the generated banner must never be
            # flagged as orphans: not the reserved hub page, and not a
            # non-reserved page that merely mentions the word "generated". The
            # latter pins banner-EXACTNESS — a loose "generated"-substring match
            # would wrongly flag it and turn this red.
            (docs / "index.md").write_text("# Packs hub\n", encoding="utf-8")
            (docs / "my-notes.md").write_text(
                "# My notes\n\nHand-authored notes about the generated reference pages.\n",
                encoding="utf-8",
            )
            self.assertEqual(gen.generate(root, docs, check=True), 0)
            # A banner-bearing page whose pack no longer exists is drift.
            orphan = gen.render_page(gen.build_reference(root, "removed-pack", pack))
            (docs / "removed-pack.md").write_text(orphan, encoding="utf-8")
            self.assertNotEqual(gen.generate(root, docs, check=True), 0)

    def test_reserved_slug_collision_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _make_pack(root)
            # A discovered pack whose slug collides with a hand-authored
            # docs/packs page (index, catalog-proposal) must be rejected, not
            # silently overwrite the page.
            clash = root / "packs" / "index"
            (clash / "directives").mkdir(parents=True)
            (clash / "directives" / "d.directive.yaml").write_text(
                "id: D_009\ntitle: X\n", encoding="utf-8"
            )
            docs = root / "docs" / "packs"
            with self.assertRaises(ValueError):
                gen.generate(root, docs, check=False)

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

    def test_pack_without_pack_md_falls_back_to_the_authored_context_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            (pack / "pack.md").unlink()
            page = gen.render_page(gen.build_reference(root, "built-in", pack))
            self.assertIn("No `purpose` is declared", page)
            self.assertIn("the [Packs hub](index.md)", page)

    def test_pack_md_preamble_is_rendered_under_purpose(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            page = gen.render_page(gen.build_reference(root, "built-in", pack))
            # The authored pack.md preamble is the page's Purpose prose...
            self.assertIn(
                "## Purpose\n\nThe baseline pack every project starts with.\n",
                page,
            )
            # ...while its frontmatter-free H1, H2 section and section prose are
            # not published as the description.
            self.assertNotIn("# built-in\n", page)
            self.assertNotIn("## Details", page)
            self.assertNotIn("Section prose that must not render", page)
            self.assertNotIn("No `purpose` is declared", page)

    def test_pack_md_preamble_ignores_frontmatter_and_skips_blank_lead(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            (pack / "pack.md").write_text(
                "---\ntitle: ignored frontmatter\n---\n"
                "\n"
                "# built-in\n"
                "\n"
                "Description after frontmatter.\n",
                encoding="utf-8",
            )
            page = gen.render_page(gen.build_reference(root, "built-in", pack))
            self.assertIn("## Purpose\n\nDescription after frontmatter.\n", page)
            self.assertNotIn("ignored frontmatter", page)

    def test_depends_on_is_published_with_every_entry_as_the_schema_shapes_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pack = _make_pack(root)
            (pack / "pack.yaml").write_text(
                "pack_id: 01ARWG13C000000000000000FG\n"
                "name: built-in\n"
                "pack_version: 1.0.0\n"
                "pack_level: org\n"
                "depends_on:\n"
                "- pack_id: 01ARWG13C000000000000000AA\n"
                "  range: '>=1.0,<2'\n"
                "- {pack_id: 01ARWG13C000000000000000BB, range: '>=2.1,<3'}\n",
                encoding="utf-8",
            )
            page = gen.render_page(gen.build_reference(root, "built-in", pack))
            self.assertIn(
                "**Depends on:** `01ARWG13C000000000000000AA >=1.0,<2`, `01ARWG13C000000000000000BB >=2.1,<3`",
                page,
            )
            self.assertIn("- **Declared version:** `1.0.0`", page)

    def test_the_page_does_not_invite_a_purpose_field_the_closed_schema_forbids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = gen.render_page(gen.build_reference(root, "built-in", _make_pack(root)))
            # The description comes from pack.md, never from a pack.yaml prose
            # field the closed descriptor schema forbids.
            self.assertNotIn("in this pack's `pack.yaml`", page)
            self.assertNotIn("schema has no such field", page)


if __name__ == "__main__":
    unittest.main()
