"""Validation of ADR-0066 prompt slots, fragment companions and composition."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "ci"))

import validate_pack_schemas as validator  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BUILT_IN_ID = "01ARWG13C000000000000000FG"
SPDD_ID = "01M6Y9ACNAAD96XPNQS0XWP2FF"


class PromptSlotValidation(unittest.TestCase):
    def test_empty_slot_is_well_formed_and_declared(self) -> None:
        prompt = "before\n<!-- spdd:reasons-block:start -->\n \t\n<!-- spdd:reasons-block:end -->\nafter\n"
        self.assertEqual(validator.prompt_slot_violations(prompt, require_empty=True), [])
        self.assertEqual(validator.declared_prompt_slots(prompt), {"spdd:reasons-block"})

    def test_nonempty_slot_is_refused_only_at_the_new_descriptor_version(self) -> None:
        prompt = "<!-- spdd:reasons-block:start -->\nguidance\n<!-- spdd:reasons-block:end -->\n"
        self.assertEqual(validator.prompt_slot_violations(prompt, require_empty=False), [])
        found = validator.prompt_slot_violations(prompt, require_empty=True)
        self.assertEqual(len(found), 1)
        self.assertIn("prompt_slot_not_empty", found[0])

    def test_repeat_nesting_bad_id_and_unpaired_markers_are_malformed(self) -> None:
        cases = {
            "repeat": "<!-- spdd:x:start --><!-- spdd:x:start --><!-- spdd:x:end --><!-- spdd:x:end -->",
            "nesting": "<!-- spdd:x:start --><!-- spdd:y:start --><!-- spdd:y:end --><!-- spdd:x:end -->",
            "bad id": "<!-- SPDD:x:start --><!-- SPDD:x:end -->",
            "unclosed": "<!-- spdd:x:start -->",
            "unopened": "<!-- spdd:x:end -->",
        }
        for label, prompt in cases.items():
            with self.subTest(label):
                found = validator.prompt_slot_violations(prompt, require_empty=True)
                self.assertTrue(found, label)
                self.assertTrue(any("prompt_slot_malformed" in problem for problem in found), found)

    def test_validator_cli_prints_legacy_slot_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contract = root / "contract"
            (contract / "schemas").mkdir(parents=True)
            (contract / "file-kinds.yaml").write_text(
                'files:\n- match: "*/missions/*/steps/*.prompt.md"\n'
                "  schema: mission-step-prompt\n  content_form: markdown\n",
                encoding="utf-8",
            )
            (contract / "schemas" / "mission-step-prompt.schema.json").write_text('{"type": "object"}\n', encoding="utf-8")
            pack = root / "base"
            prompt = pack / "missions" / "dev" / "steps" / "specify.prompt.md"
            prompt.parent.mkdir(parents=True)
            prompt.write_text("<!-- spdd:x:start -->\nlegacy guidance\n<!-- spdd:x:end -->\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = validator.main([str(pack), "--contract", str(contract)])
            self.assertEqual(code, validator.EXIT_OK)
            self.assertIn(f"::warning file={pack}::base/missions/dev/steps/specify.prompt.md: prompt_slot_not_empty", out.getvalue())
            self.assertIn("0 violations", out.getvalue())


class PromptFragmentValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = validator.contract_for(None)
        cls.schema_validator = cls.contract.validators["prompt-fragment"]

    def test_plain_nonblank_markdown_passes(self) -> None:
        text = "\n### REASONS Guidance\n\nKeep the canvas current.\n\n"
        model = validator.parse_markdown(text)
        self.assertEqual(list(self.schema_validator.iter_errors(model)), [])
        self.assertEqual(validator.prompt_fragment_violations(text), [])

    def test_blank_frontmatter_and_slot_markers_are_refused(self) -> None:
        blank = " \n\t\n"
        self.assertTrue(list(self.schema_validator.iter_errors(validator.parse_markdown(blank))))
        frontmatter = "---\ndescription: no\n---\nText.\n"
        self.assertTrue(list(self.schema_validator.iter_errors(validator.parse_markdown(frontmatter))))
        marker = "<!-- spdd:reasons-block:start -->\nText.\n"
        found = validator.prompt_fragment_violations(marker)
        self.assertTrue(any("cannot declare or fill a slot" in problem for problem in found))

    def test_enhancement_schema_rejects_repeat_slots_and_missing_companions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "spdd"
            enhancements = pack / "missions" / "software-dev" / "enhancements"
            enhancements.mkdir(parents=True)
            enhancement = enhancements / "spdd-specify.step-enhancement.yaml"
            enhancement.write_text(
                'schema_version: "1.0"\nid: spdd-specify\nprompt_fragments:\n'
                "  - {slot: 'spdd:reasons-block', path: spdd-specify.prompt-fragment.md}\n"
                "  - {slot: 'spdd:reasons-block', path: gone.prompt-fragment.md}\n",
                encoding="utf-8",
            )
            (enhancements / "spdd-specify.prompt-fragment.md").write_text("Guidance.\n", encoding="utf-8")
            report = validator.validate_pack(pack, self.contract)
            self.assertIn("enhancement names slot 'spdd:reasons-block' more than once", "\n".join(report.violations))
            self.assertIn("gone.prompt-fragment.md", "\n".join(report.violations))

    def test_descriptor_version_gates_the_empty_slot_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "base"
            prompt = pack / "missions" / "dev" / "steps" / "specify.prompt.md"
            prompt.parent.mkdir(parents=True)
            prompt.write_text("<!-- spdd:x:start -->\nlegacy guidance\n<!-- spdd:x:end -->\n", encoding="utf-8")
            open_validator = Draft202012Validator({"type": "object"})
            contract = validator.Contract(
                files=[validator.Rule(validator.glob_to_regex("*/missions/*/steps/*.prompt.md"), "prompt", schema="mission-step-prompt", content_form="markdown")],
                exclusions=[], retired=[], payloads=[], validators={"mission-step-prompt": open_validator},
            )
            legacy = validator.validate_pack(pack, contract)
            self.assertEqual(legacy.violations, [])
            self.assertIn("prompt_slot_not_empty", "\n".join(legacy.warnings))
            (pack / "pack.yaml").write_text('schema_version: "1.0"\n', encoding="utf-8")
            self.assertIn("prompt_slot_not_empty", "\n".join(validator.validate_pack(pack, contract).violations))


class PromptFragmentComposition(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.base = root / "built-in"
        self.spdd = root / "spdd"
        (self.base / "missions" / "software-dev" / "steps").mkdir(parents=True)
        (self.spdd / "missions" / "software-dev" / "enhancements").mkdir(parents=True)
        (self.spdd / "drg").mkdir(parents=True)
        (self.base / "pack.yaml").write_text(f"pack_id: {BUILT_IN_ID}\nname: built-in\n", encoding="utf-8")
        (self.spdd / "pack.yaml").write_text(
            f"pack_id: {SPDD_ID}\nname: spdd\ndepends_on:\n- {{pack_id: {BUILT_IN_ID}, range: '>=1.0,<2'}}\n",
            encoding="utf-8",
        )
        (self.base / "missions" / "software-dev" / "software-dev.mission-type.yaml").write_text(
            "id: software-dev\nsteps:\n- id: specify\n  prompt_path: steps/specify.prompt.md\n", encoding="utf-8")
        (self.base / "missions" / "software-dev" / "steps" / "specify.prompt.md").write_text(
            "<!-- spdd:reasons-block:start -->\n<!-- spdd:reasons-block:end -->\n", encoding="utf-8")
        self.enhancement = self.spdd / "missions" / "software-dev" / "enhancements" / "spdd-specify.step-enhancement.yaml"
        self.enhancement.write_text(
            'schema_version: "1.0"\nid: spdd-specify\nprompt_fragments:\n'
            "- {slot: 'spdd:reasons-block', path: spdd-specify.prompt-fragment.md}\n", encoding="utf-8")
        self.fragment = self.spdd / "drg" / "fragment.yaml"
        self.fragment.write_text(
            "nodes: []\nedges:\n- {source: 'step_enhancement:spdd-specify', "
            "target: 'built-in::action:software-dev/specify', relation: enhances}\n", encoding="utf-8")

    def found(self) -> str:
        return "\n".join(validator.prompt_fragment_composition_violations([self.base, self.spdd]))

    def test_valid_target_and_slot_resolve_regardless_of_activation(self) -> None:
        self.assertEqual(self.found(), "")

    def test_fragment_validation_uses_shared_graph_edge_discovery(self) -> None:
        with mock.patch.object(validator, "graph_edges", wraps=validator.graph_edges) as graph_edges:
            self.assertEqual(self.found(), "")
        self.assertEqual(graph_edges.call_args_list, [mock.call(self.base), mock.call(self.spdd)])

    def test_missing_slot_is_refused(self) -> None:
        self.enhancement.write_text(self.enhancement.read_text().replace("spdd:reasons-block", "spdd:other"), encoding="utf-8")
        self.assertIn("prompt_slot_missing", self.found())

    def test_non_step_and_missing_steps_are_refused(self) -> None:
        self.fragment.write_text(self.fragment.read_text().replace("built-in::action:software-dev/specify", "directive:DIRECTIVE_038"), encoding="utf-8")
        self.assertIn("is not an action:<type>/<step>", self.found())
        self.fragment.write_text(self.fragment.read_text().replace("directive:DIRECTIVE_038", "built-in::action:software-dev/gone"), encoding="utf-8")
        self.assertIn("pack_reference_artifact_missing", self.found())

    def test_fragments_require_exactly_one_enhances_edge(self) -> None:
        self.fragment.write_text("nodes: []\nedges: []\n", encoding="utf-8")
        self.assertIn("exactly one enhances edge", self.found())


if __name__ == "__main__":
    unittest.main()
