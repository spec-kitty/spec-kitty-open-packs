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


class ValidatorExitCodes(unittest.TestCase):
    def run_validator(self, root: Path, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = validator.main([*args, "--contract", str(root / "contract")])
        return code, out.getvalue()

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


if __name__ == "__main__":
    unittest.main()
