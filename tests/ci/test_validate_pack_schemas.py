"""The pack schema validator judges real pack files and fails closed when it cannot judge."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "ci"))

import validate_pack_schemas as validator  # noqa: E402

# A one-rule contract in the charter's own shape: `presets/<id>.yaml` is a closed preset.
PRESET_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["schema_version", "id"],
    "additionalProperties": False,
    "properties": {
        "schema_version": {"const": "1.0"},
        "id": {"type": "string"},
        "activated_directives": {
            "type": "array",
            "items": {"type": "object", "required": ["id"], "additionalProperties": False,
                      "properties": {"id": {"type": "string"}}},
        },
    },
}

# The pack-level rules a small pack needs, with permissive schemas except for the manifest, whose
# shape the verification relies on (the charter's own schema is closed the same way).
MANIFEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["schema_version", "manifest_hash", "constituents"],
}
OPEN_SCHEMA = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
RULES = {  # file-kinds `files` rules, glob -> schema name
    "*/presets/*.yaml": "preset",
    "*/pack-manifest.yaml": "pack-manifest",
    "**/*.tactic.yaml": "tactic",
    "*/pack.md": "pack-doc",  # the one markdown rule
}


class ValidatorExitCodes(unittest.TestCase):
    def run_validator(self, root: Path, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = validator.main([*args, "--contract", str(root / "contract")])
        return code, out.getvalue()

    def write_contract(self, root: Path, extra: str = "") -> None:
        """A contract holding RULES (and `extra`, appended verbatim) with the schemas above."""
        (root / "contract" / "schemas").mkdir(parents=True)
        rules = "".join(
            f'  - match: "{glob}"\n    schema: {name}\n' + ("    content_form: markdown\n" if name == "pack-doc" else "")
            for glob, name in RULES.items()
        )
        (root / "contract" / "file-kinds.yaml").write_text(f"files:\n{rules}{extra}", encoding="utf-8")
        schemas = {"preset": OPEN_SCHEMA, "pack-manifest": MANIFEST_SCHEMA, "tactic": OPEN_SCHEMA, "pack-doc": OPEN_SCHEMA}
        for name, schema in schemas.items():
            (root / "contract" / "schemas" / f"{name}.schema.json").write_text(json.dumps(schema), encoding="utf-8")

    def write_pack(self, root: Path, files: dict[str, str]) -> Path:
        """A pack `root/pack` holding a tactic and `files` (relative path -> text, written verbatim)."""
        pack = root / "pack"
        for name, body in {"tactics/t.tactic.yaml": "id: t\n", **files}.items():
            target = pack / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body.encode("utf-8"))
        return pack

    def test_valid_pack_passes_old_shape_fails_and_unmapped_known_kind_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "contract" / "schemas").mkdir(parents=True)
            (root / "contract" / "file-kinds.yaml").write_text(
                'files:\n  - match: "*/presets/*.yaml"\n    schema: preset\n', encoding="utf-8")
            (root / "contract" / "schemas" / "preset.schema.json").write_text(json.dumps(PRESET_SCHEMA), encoding="utf-8")

            good, bad, unmapped = root / "good", root / "bad", root / "unmapped"
            for pack, preset in (
                (good, 'schema_version: "1.0"\nid: p\nactivated_directives:\n  - id: D_1\n'),
                (bad, "name: p\nactivated_directives: [D_1]\n"),
            ):
                (pack / "presets").mkdir(parents=True)
                (pack / "presets" / "p.yaml").write_text(preset, encoding="utf-8")
            (unmapped / "presets").mkdir(parents=True)
            (unmapped / "presets" / "p.yaml").write_text('schema_version: "1.0"\nid: p\n', encoding="utf-8")
            (unmapped / "directives").mkdir()
            (unmapped / "directives" / "d.directive.yaml").write_text("id: D_1\n", encoding="utf-8")

            self.assertEqual(self.run_validator(root, str(good))[0], validator.EXIT_OK)
            code, output = self.run_validator(root, str(bad))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("bad/presets/p.yaml: preset schema", output)
            self.assertEqual(self.run_validator(root, "--expect-invalid", str(good))[0], validator.EXIT_INVALID)
            self.assertEqual(self.run_validator(root, str(unmapped))[0], validator.EXIT_GATE)

    def test_manifest_hashes_are_verified_and_the_regenerate_mode_restores_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # Membership is authored; the hashes are what the regenerate mode derives.
            zero = "0" * 64
            manifest = (
                "schema_version: '1.0'\n"
                f"manifest_hash: {zero}\n"
                "constituents:\n"
                f"- {{kind: tactic, id: t, path: tactics/t.tactic.yaml, content_hash: {zero}}}\n"
                "presets:\n"
                f"- {{id: p, path: presets/p.yaml, content_hash: {zero}}}\n"
            )
            pack = self.write_pack(root, {"presets/p.yaml": "id: p\n", "pack-manifest.yaml": manifest})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("constituents{tactics/t.tactic.yaml}.content_hash", output)
            self.assertIn("manifest_hash", output)

            self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack), str(pack))[0], validator.EXIT_OK)
            self.assertEqual(self.run_validator(root, str(pack))[0], validator.EXIT_OK)

            (pack / "presets" / "p.yaml").write_text("id: p\nextra: 1\n", encoding="utf-8")  # edited, manifest not
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("presets{presets/p.yaml}.content_hash", output)

    def test_a_carriage_return_in_markdown_is_refused_not_read_as_a_newline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"pack.md": "# Title\r\n\r\nText.\r\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack.md: not readable as markdown: line 1: a carriage return is not admitted", output)

    def test_duplicate_keys_and_non_plain_values_are_refused_in_yaml_and_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {
                "tactics/dup.tactic.yaml": "id: a\nid: b\n",
                "tactics/bin.tactic.yaml": "id: !!binary aGk=\n",
                "pack.md": "---\nname: a\nname: b\n---\n# Title\n",
            })
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/tactics/dup.tactic.yaml: not readable as yaml: ", output)
            self.assertIn("found duplicate key 'id'", output)
            self.assertIn("pack/tactics/bin.tactic.yaml: not readable as yaml: a value is not a string", output)
            self.assertIn("pack/pack.md: not readable as markdown: line 1: frontmatter is not valid YAML: ", output)
            self.assertIn("found duplicate key 'name'", output)

    def test_a_yaml_or_markdown_file_no_rule_covers_fails_unless_documented(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            stray = ["tactics/x.tactic.yml", "tactics/x.tactc.yaml", "tactics/plain.yaml", "presets/sub/x.yaml", "x.promt.md"]
            allowed = ["README.md", "PROVENANCE.md", "skills/s.skill.md", "tactics/README.md"]
            pack = self.write_pack(root, {name: "id: x\n" for name in [*stray, *allowed]})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            for name in stray:
                self.assertIn(f"pack/{name}: unclassified", output)
            for name in allowed:
                self.assertNotIn(f"pack/{name}:", output)


if __name__ == "__main__":
    unittest.main()
