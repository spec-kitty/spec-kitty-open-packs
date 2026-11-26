"""The pack schema validator judges real pack files and fails closed when it cannot judge."""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path

import yaml

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
    "*/pack.yaml": "pack-descriptor",
    "*/README.md": "pack-doc",  # the one markdown rule: the pack document
    "**/*.asset.yaml": "asset",
    "**/*.skill.yaml": "skill",
    "**/toolguides/*.guide.md": "pack-doc",  # a markdown rule beneath the root, for the folded guard
}


# The charter's last-resort rule (#451), as file-kinds.yaml writes it at the pin: Markdown nothing else takes is
# left out, in any letter case. Every contract write_contract builds carries it, as the real table does.
IGNORED = 'ignored:\n  - match: "**/*.md"\n    reason: Author aid, not pack content.\n'
RETIRED = ('retired:\n  - match: "*/PROVENANCE.md"\n    reason: folded into README.md\n'
           '  - match: "*/org-charter.yaml"\n    reason: org enforcement is a preset\n')


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
        (root / "contract" / "file-kinds.yaml").write_text(f"files:\n{rules}{extra}{IGNORED}", encoding="utf-8")
        schemas = {"preset": OPEN_SCHEMA, "pack-manifest": MANIFEST_SCHEMA, "tactic": OPEN_SCHEMA, "pack-doc": OPEN_SCHEMA, "pack-descriptor": OPEN_SCHEMA, "asset": OPEN_SCHEMA, "skill": OPEN_SCHEMA}
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

    def manifest_pack(self, root: Path, paths: list[str], files: dict[str, str] | None = None, name: str = "pack") -> Path:
        """A pack `root/name` whose zero-hash manifest lists the tactics at `paths`; `files` are written too."""
        zero = "'" + "0" * 64 + "'"
        manifest = (
            f"schema_version: '1.0'\nmanifest_hash: {zero}\nconstituents:\n"
            + "".join(f"- {{kind: tactic, id: {Path(p).name.split('.')[0]}, path: {p}, content_hash: {zero}}}\n" for p in paths)
        )
        pack = self.write_pack(root, {"pack.yaml": "pack_id: x\n", "pack-manifest.yaml": manifest, **(files or {})})
        if pack.name != name:
            pack = pack.rename(root / name)
        return pack

    def test_an_asset_sidecar_names_a_payload_the_pack_holds_under_assets(self) -> None:
        payloads = ('payloads:\n  - match: "*/assets/**/*"\n    kind: asset-payload\n    content_form: bytes\n'
                    '  - match: "*/templates/**/*"\n    kind: template\n    content_form: bytes\n')
        held = {"assets/kept/held.txt": "x\n", "assets/t.tactic.yaml": "id: t2\n", "templates/beside.txt": "x\n", "templates/held.md": "# t\n"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, payloads)
            good = self.write_pack(root, {**held, "assets/kept/held.txt.asset.yaml": "path: kept/held.txt\n"})
            code, output = self.run_validator(root, str(good))
            self.assertEqual(code, validator.EXIT_OK, output)
            for named in ("assets/kept/held.txt", "held.txt", "gone.txt", "kept", "../beside.txt", "t.tactic.yaml", "templates/held.md"):
                with self.subTest(named):
                    (good / "assets" / "kept" / "held.txt.asset.yaml").write_text(f"path: {named}\n", encoding="utf-8")
                    code, output = self.run_validator(root, str(good))
                    self.assertEqual(code, validator.EXIT_INVALID, output)
                    self.assertIn(f"pack/assets/kept/held.txt.asset.yaml: payload assets/{named} does not exist", output)

    def test_a_doctrine_file_the_manifest_does_not_list_is_left_to_pack_doctor(self) -> None:
        """Decision 01M8BMA8: an unlisted file is pack-doctor's manifest_membership alone (RealPackDoctor proves it on
        the jar with an anti-pattern file); the Python unlisted_constituents, a strict subset of it, is retired."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml"],
                                      {"tactics/t.tactic.yaml": "id: t\n", "tactics/u.tactic.yaml": "id: u\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("incomplete manifest", output)
        for name in ("unlisted_constituents", "MANIFEST_CONSTITUENT_SCHEMAS"):
            self.assertFalse(hasattr(validator, name), name)

    def test_manifest_hashes_and_a_listed_file_that_is_missing_are_left_to_pack_doctor(self) -> None:
        """#347, #348: pack-doctor judges a manifest's hashes and its listed files (manifest_stale, manifest_membership);
        the schema pass no longer verifies them, and the manifest modes are gone."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml", "tactics/gone.tactic.yaml"], {"tactics/t.tactic.yaml": "id: t\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("stale", output)
            for retired in ("--regenerate-manifest", "--derive-manifest", "--derived-manifests"):
                with self.subTest(retired), self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                    self.run_validator(root, retired, str(pack))
            for name in ("stale_manifest_fields", "regenerate_manifest", "derived_manifest", "derive_manifest",
                         "membership_mismatch", "REGENERATE_COMMAND", "DERIVE_COMMAND"):
                self.assertFalse(hasattr(validator, name), name)

    def test_a_pack_without_a_manifest_is_not_held_to_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"pack.yaml": "pack_id: x\n", "tactics/t.tactic.yaml": "id: t\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("incomplete manifest", output)

    GRAPH_RULES = '  - match: "*/drg/fragment.yaml"\n    schema: pack-descriptor\n  - match: "*/*.graph.yaml"\n    schema: pack-descriptor\n'

    def node_pack(self, root: Path, files: dict[str, str], constituents: bool = False) -> Path:
        """A manifest-bearing pack with a tactic file, `files` and (optionally) a `tactic:ghost` entry."""
        paths = ["tactics/t.tactic.yaml"] + (["tactics/ghost.tactic.yaml"] if constituents else [])
        return self.manifest_pack(root, paths, {"tactics/t.tactic.yaml": "id: t\n", **files})

    def test_a_graph_node_the_manifest_does_not_list_fails_naming_the_node(self) -> None:
        """#182 residual: a node of drg/fragment.yaml with no constituent is reported; listing it clears it."""
        fragment = "nodes:\n- {kind: tactics, id: ghost}\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, self.GRAPH_RULES)
            pack = self.node_pack(root, {"drg/fragment.yaml": fragment})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("incomplete manifest: graph node tactic:ghost is not a constituent", output)
            # The remedy is the charter's writer, not a Python derivation (#347).
            self.assertIn(f"run `pack-doctor remediate {pack}`", output)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, self.GRAPH_RULES)
            pack = self.node_pack(root, {"drg/fragment.yaml": fragment, "tactics/ghost.tactic.yaml": "id: ghost\n"}, constituents=True)
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)

    def test_a_root_graph_shard_node_the_manifest_does_not_list_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, self.GRAPH_RULES)
            pack = self.node_pack(root, {"tactic.graph.yaml": "nodes:\n- {urn: 'tactic:ghost'}\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("incomplete manifest: graph node tactic:ghost is not a constituent", output)

    def test_exempt_graph_node_kinds_need_no_constituent_but_an_unknown_kind_does(self) -> None:
        exempt = "nodes:\n" + "".join(
            f"- {{kind: {k}, id: x}}\n"
            for k in ("actions", "templates", "mission_types")
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, self.GRAPH_RULES)
            pack = self.node_pack(root, {"drg/fragment.yaml": exempt})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            (pack / "drg" / "fragment.yaml").write_text(exempt + "- {kind: widgets, id: x}\n", encoding="utf-8")
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("graph node widget:x is not a constituent", output)
            # The retired step-contract kind (charter slice F) is no longer exempt: it fails like any unknown kind.
            (pack / "drg" / "fragment.yaml").write_text(exempt + "- {kind: mission_step_contracts, id: x}\n", encoding="utf-8")
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("graph node mission_step_contract:x is not a constituent", output)
            # #348 (f): an anti-pattern is a file now, so its node is no longer exempt: unlisted, it is reported.
            (pack / "drg" / "fragment.yaml").write_text(exempt + "- {kind: anti_patterns, id: x}\n", encoding="utf-8")
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("graph node anti_pattern:x is not a constituent", output)
        self.assertNotIn("anti_pattern", validator.MANIFEST_EXEMPT_NODE_KINDS)

    def test_unlisted_nodes_is_exact_and_skips_exempt_kinds(self) -> None:
        manifest = {"constituents": [{"kind": "tactic", "id": "a"}, "junk"]}
        nodes = {("tactic", "a"), ("tactic", "b"), ("action", "x")}
        self.assertEqual(validator.unlisted_nodes(manifest, nodes), ["tactic:b"])
        self.assertEqual(validator.unlisted_nodes({"constituents": [{"kind": "tactic", "id": "b"}]}, nodes - {("tactic", "a")}), [])
        # A node a file of the pack declares is manifest_membership's (decision 01M8BMA8): only a fileless node is named.
        self.assertEqual(validator.unlisted_nodes(manifest, nodes, {("tactic", "b")}), [])

    def test_a_carriage_return_in_markdown_is_refused_not_read_as_a_newline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"README.md": "# Title\r\n\r\nText.\r\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("README.md: not readable as markdown: line 1: a carriage return is not admitted", output)

    def test_duplicate_keys_and_non_plain_values_are_refused_in_yaml_and_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {
                "tactics/dup.tactic.yaml": "id: a\nid: b\n",
                "tactics/bin.tactic.yaml": "id: !!binary aGk=\n",
                "README.md": "---\nname: a\nname: b\n---\n# Title\n",
            })
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/tactics/dup.tactic.yaml: not readable as yaml: ", output)
            self.assertIn("found duplicate key 'id'", output)
            self.assertIn("pack/tactics/bin.tactic.yaml: not readable as yaml: a value is not a string", output)
            self.assertIn("pack/README.md: not readable as markdown: line 1: frontmatter is not valid YAML: ", output)
            self.assertIn("found duplicate key 'name'", output)

    def test_a_file_no_rule_takes_is_a_file_not_held_warning_as_the_charter_answers_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # Not Markdown, or Markdown a files rule takes in another letter case (the fallback never sweeps those
            # up): from charter #554 (ruling Q1) the charter warns each as `file_not_held` and leaves it out (#309).
            stray = ["tactics/x.tactic.yml", "tactics/y.tactic.YML", "tactics/x.tactc.yaml", "tactics/plain.yaml",
                     "presets/sub/x.yaml", "notes.txt", "logs/run.log", "data/table.json", "tactics/.gitkeep",
                     "tactics/z.Tactic.yaml"]
            pack = self.write_pack(root, {name: "id: x\n" for name in stray})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            for name in stray:
                self.assertEqual(output.count(f"::warning file={pack}::pack/{name}: file_not_held: not held "
                                              "(no pack file kind models this file)"), 1, name)
            self.assertNotIn("unmodelled", output)
            self.assertNotIn("unclassified", output)

    def test_markdown_only_the_ignored_rule_takes_is_warned_not_held_outside_the_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # The charter leaves these out without refusing them and reports file_not_held. Operator ruling R34 (#331):
            # a stray file in a pack warns, it does not fail, so authors may keep notes. README.md orientation notes
            # stay silent (NOT_HELD_ALLOWANCES); any other is warned. An orphan skill body is not held: only the body a
            # skill's body_path names is its companion.
            stray = ["docs/notes.md", "x.promt.md", "tactics/GUIDE.MD", "tactics/t.guide.md", "skills/orphan.skill.md",
                     "directives/.draft.md"]
            # No root README.md: it is the pack document (held, not a note), and without a pack.yaml it would make the
            # validator ask for the descriptor.
            allowed = ["tactics/README.md", "docs/deep/README.md"]
            pack = self.write_pack(root, {name: "# t\n" for name in [*stray, *allowed]})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            for name in stray:
                self.assertIn(f"::warning file={pack}::pack/{name}: file_not_held: not held (**/*.md: Author aid, "
                              "not pack content.)", output)
            self.assertNotIn("::error", output)
            for name in allowed:
                self.assertNotIn(f"pack/{name}:", output)

    def test_r38_a_misspelled_companion_suffix_is_annotated_with_the_name_it_should_have(self) -> None:
        # Operator ruling R38: a lightweight, linter-style name check. A stray file whose suffix is close to a companion
        # suffix the contract models (.guide.md here; .skill.md for skill bodies) gets a PR annotation naming the
        # companion it was probably meant to be. It is never a failure (R34: a stray file warns).
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"toolguides/g.gudie.md": "# g\n", "toolguides/h.guide.MD": "# h\n",
                                          "skills/x.skil.md": "# x\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("::error", output)
            for stray, meant in (("toolguides/g.gudie.md", "toolguides/g.guide.md"),
                                 ("toolguides/h.guide.MD", "toolguides/h.guide.md"),
                                 ("skills/x.skil.md", "skills/x.skill.md")):
                with self.subTest(stray=stray):
                    self.assertIn(f"::warning file={pack}/{stray},title=Possible misspelled companion::", output)
                    line = next(l for l in output.splitlines() if l.startswith(f"::warning file={pack}/{stray},"))
                    self.assertIn(f"did you mean {meant}?", line)

    def test_r38_a_stray_file_beside_a_missing_companion_reference_is_annotated(self) -> None:
        # A skill whose body_path names a file that is not there, with a near-named stray file beside it: the
        # annotation names both, so the author can fix whichever is misspelled.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"skills/r.skill.yaml": "id: r\nbody_path: report-debreif.skill.md\n",
                                          "skills/report-debrief.skill.md": "# r\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            line = next(l for l in output.splitlines()
                        if l.startswith(f"::warning file={pack}/skills/report-debrief.skill.md,title=Possible misspelled companion::"))
            self.assertIn("did you mean skills/report-debreif.skill.md?", line)
            self.assertIn("skills/r.skill.yaml names it as body_path", line)

    def test_r38_ordinary_notes_and_logs_are_not_taken_for_misspelled_companions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # Dotted near-words are strays a broken lint would flag: still/spill/slide/guild are same-length
            # substitutions of a short token (the substitution guard), skit is two edits from skill (the
            # per-length allowance).
            pack = self.write_pack(root, {"notes.md": "n\n", "docs/plan.md": "p\n", "logs/run.log": "l\n",
                                          "notes.txt": "n\n", "toolguides/README.md": "# r\n", "my.notes.md": "n\n",
                                          "team.still.md": "n\n", "docs/oil.spill.md": "n\n",
                                          "toolguides/old.guild.md": "n\n", "talk.slide.md": "n\n",
                                          "docs/comedy.skit.md": "n\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("Possible misspelled companion", output)

    def test_r38_an_unresolvable_companion_reference_is_never_fatal(self) -> None:
        # Review of #332 (MAJOR): a 300-character body_path made target.exists() raise ENAMETOOLONG and crashed the
        # schema pass. A reference that cannot be resolved is not judged by the lint; the run goes on and exits 0.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"skills/long.skill.yaml": f"id: long\nbody_path: {'a' * 300}.skill.md\n",
                                          "skills/nul.skill.yaml": 'id: nul\nbody_path: "x\\0y.skill.md"\n'})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertNotIn("Traceback", output)

    def test_r38_a_missing_companion_reference_is_annotated_on_the_artifact(self) -> None:
        # Review of #332 (MINOR): a stem typo that still matches a files rule (implemnet.prompt.md) is held content,
        # so no stray-file signal fires. The artifact whose *_path names a missing file is annotated instead.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # toolguides/implement.guide.md is held content (the guide rule takes it), so it is no stray-file signal; the
            # artifact naming the misspelt stem is what gets annotated.
            pack = self.write_pack(root, {"skills/r.skill.yaml": "id: r\nbody_path: r.skill.md\n",
                                          "toolguides/g.skill.yaml": "id: g\nbody_path: implemnet.guide.md\n",
                                          "toolguides/implement.guide.md": "# g\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            for artifact, meant in (("skills/r.skill.yaml", "skills/r.skill.md"),
                                    ("toolguides/g.skill.yaml", "toolguides/implemnet.guide.md")):
                with self.subTest(artifact=artifact):
                    line = next(l for l in output.splitlines()
                                if l.startswith(f"::warning file={pack}/{artifact},title=Missing companion::"))
                    self.assertIn(f"names {meant} as body_path", line)
            self.assertNotIn("Possible misspelled companion", output)

    def test_r38_suffix_suggestion_names_close_companions_and_spares_ordinary_words(self) -> None:
        # Review of #332 (MINOR): two edits on a 5-6 letter token flagged English words. Short tokens take one edit at
        # most, a five-letter-or-shorter token no plain substitution (still is not skill), and only a long token
        # (guidelines, prompt-fragment) takes two edits.
        tokens = {"guide", "prompt", "guidelines", "prompt-fragment", "skill"}
        for name, meant in (("x.skil.md", "x.skill.md"), ("x.gudie.md", "x.guide.md"), ("x.promt.md", "x.prompt.md"),
                            ("x.skilll.md", "x.skill.md"), ("implement.promt.md", "implement.prompt.md"),
                            ("a.guidelnes.md", "a.guidelines.md"), ("a.guidlnes.md", "a.guidelines.md"),
                            ("f.prompt-fragmnet.md", "f.prompt-fragment.md"), ("s.SKILL.md", "s.skill.md")):
            with self.subTest(suggests=name):
                self.assertEqual(validator.suffix_suggestion(name, tokens), meant)
        for name in ("x.slide.md", "x.suite.md", "x.grid.md", "x.still.md", "x.drill.md", "x.skin.md", "x.promote.md",
                     "x.guilds.md", "x.spill.md", "implement.prompt.md", "notes.md", "my.notes.md", "a.txt",
                     "x.prompts.yaml", "README.md"):
            with self.subTest(never=name):
                self.assertIsNone(validator.suffix_suggestion(name, tokens))

    def test_a_skill_body_its_skill_names_is_held_as_a_companion_whatever_its_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # As the charter removes companions before it classifies (WholePackStore), the file a skill's
            # body_path names is held: Markdown or not, and whatever its name.
            pack = self.write_pack(root, {
                "skills/s.skill.yaml": "id: s\nbody_path: s.skill.md\n", "skills/s.skill.md": "# s\n",
                "skills/t.skill.yaml": "id: t\nbody_path: bodies/t.txt\n", "skills/bodies/t.txt": "t\n",
                "skills/u.skill.yaml": "id: u\nbody_path: notes.md\n", "skills/notes.md": "# u\n",
                "skills/v.skill.yaml": "id: v\nbody_path: ../../outside.md\n",
            })
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            (pack / "skills" / "u.skill.yaml").write_text("id: u\n", encoding="utf-8")  # no longer claimed
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)  # R34: no longer claimed, so warned, not failed
            self.assertIn("pack/skills/notes.md: file_not_held", output)

    def test_expected_code_is_exempt_only_in_an_invalid_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"expected-code": "composition: a\nregistration: b\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertIn("pack/expected-code: file_not_held", output)
            fixture = root / "fixtures" / "invalid" / "x"
            fixture.parent.mkdir(parents=True)
            pack.rename(fixture)
            code, output = self.run_validator(root, str(fixture))
            self.assertEqual(code, validator.EXIT_OK, output)

    def test_without_an_ignored_rule_stray_markdown_is_unmodelled(self) -> None:
        contract = validator.Contract(files=[], exclusions=[], retired=[], payloads=[])
        self.assertEqual(validator.classify(contract, "pack/docs/notes.md"), ("unmodelled", None))

    def test_a_root_case_variant_is_refused_under_the_rule_it_shadows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, RETIRED)
            variants = {"Readme.md": "README.md", "PROVENANCE.MD": "PROVENANCE.md", "Pack.yaml": "pack.yaml",
                        "ORG-CHARTER.yaml": "org-charter.yaml"}
            pack = self.write_pack(root, {name: "# t\n" for name in variants})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            for name, shadowed in variants.items():
                self.assertIn(f"pack/{name}: retired layout: differs only in letter case from '{shadowed}'", output)
            self.assertNotIn("not_held", output)
            # Only a root file: deeper, a case variant is ordinary Markdown the fallback takes.
            contract = validator.contract_for(root / "contract")
            self.assertEqual(validator.classify(contract, "pack/tactics/Readme.md")[0], "ignored")
            self.assertEqual(validator.classify(contract, "pack/README.md")[0], "file")
            # The repository's non-vacuity fixture for FR-022 holds the variant, and only the variant.
            fixture = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "invalid" / "case-variant-readme"
            names = {path.name for path in fixture.iterdir()}
            self.assertIn("Readme.md", names)
            self.assertNotIn("README.md", names)
            self.assertEqual(validator.classify(contract, "case-variant-readme/Readme.md")[1].reason,
                             "differs only in letter case from 'README.md'")

    def test_the_ignored_rule_comes_after_every_other_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, RETIRED + 'exclusions:\n  - match: "*/missions/README.md"\n    reason: notes\n'
                                'payloads:\n  - match: "*/templates/**/*"\n    kind: template\n    content_form: bytes\n')
            contract = validator.contract_for(root / "contract")
            for path, kind in (("p/README.md", "file"), ("p/missions/README.md", "excluded"), ("p/PROVENANCE.md", "retired"),
                               ("p/templates/a.md", "payload"), ("p/docs/a.md", "ignored"), ("p/docs/A.MD", "ignored"),
                               # folded onto an exclusion: still the fallback's
                               ("p/Missions/README.md", "ignored"),
                               # folded onto a files rule: refused, never swept up by the fallback
                               ("p/toolguides/x.guide.MD", "unmodelled"), ("p/Templates/a.md", "unmodelled"),
                               # a case variant is a root file only: `*/presets/*.yaml` anchors no root file
                               ("p/Presets/x.yaml", "unmodelled")):
                with self.subTest(path):
                    self.assertEqual(validator.classify(contract, path)[0], kind)

    def test_a_retired_rule_beats_a_files_rule_unless_an_exclusion_matches_too(self) -> None:
        """Charter slice F (ADR-0077): the folded step contracts' graph fragment is a `**/*.graph.yaml` its retired rule
        refuses by name (classifier-cases rule 1), so a leftover reports one `retired layout`, not graph-shard errors."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, '  - match: "*/*.graph.yaml"\n    schema: tactic\n'
                                'retired:\n  - match: "**/*.step-contract.yaml"\n    reason: folded into substeps\n'
                                '  - match: "**/mission_step_contract.graph.yaml"\n    reason: folded into substeps\n')
            pack = self.write_pack(root, {"steps/x.step-contract.yaml": "id: x\n",
                                          "mission_step_contract.graph.yaml": "nodes: [{urn: 'mission_step_contract:x'}]\n",
                                          "tactic.graph.yaml": "nodes: []\n"})
            contract = validator.contract_for(root / "contract")
            self.assertEqual(validator.classify(contract, "pack/mission_step_contract.graph.yaml")[0], "retired")
            self.assertEqual(validator.classify(contract, "pack/tactic.graph.yaml")[0], "file")
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertEqual(output.count("retired layout"), 2, output)
            self.assertNotIn("schema at", output)
            # When an exclusion matches too, the retired rule does not take precedence: table order decides again.
            excluded = validator.Contract(files=contract.files, exclusions=[validator.Rule(
                validator.glob_to_regex("*/mission_step_contract.graph.yaml"), "*/mission_step_contract.graph.yaml",
                reason="kept")], retired=contract.retired, payloads=[])
            self.assertEqual(validator.classify(excluded, "pack/mission_step_contract.graph.yaml")[0], "file")

    def test_a_shard_below_the_root_is_unmodelled_once_shards_are_root_only(self) -> None:
        """Charter #554: only `<name>.graph.yaml` at the pack root is a graph shard. A `drg/<kind>.graph.yaml` is
        unmodelled (a file_not_held warning, #309), not a lost mapping: the gate judges it instead of failing closed."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, '  - match: "*/*.graph.yaml"\n    schema: tactic\n')
            pack = self.write_pack(root, {"drg/tactic.graph.yaml": "nodes: []\n", "tactic.graph.yaml": "nodes: []\n"})
            contract = validator.contract_for(root / "contract")
            self.assertEqual(validator.classify(contract, "pack/drg/tactic.graph.yaml")[0], "unmodelled")
            self.assertTrue(validator.kind_mapped(contract, "graph"))
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertIn("pack/drg/tactic.graph.yaml: file_not_held", output)
            self.assertNotIn("cannot judge", output)

    def test_a_known_kind_the_contract_maps_nowhere_fails_closed(self) -> None:
        # No graph rule at all, or one renamed to a glob without the kind token: the mapping is lost.
        for extra in ("", '  - match: "*/graphs/*.yaml"\n    schema: tactic\n'):
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_contract(root, extra)
                pack = self.write_pack(root, {"drg/tactic.graph.yaml": "nodes: []\n"})
                self.assertFalse(validator.kind_mapped(validator.contract_for(root / "contract"), "graph"))
                code, output = self.run_validator(root, str(pack))
                self.assertEqual(code, validator.EXIT_GATE, output)
                self.assertIn("a `graph` file has no schema mapping", output)

    def test_a_path_scoped_kind_placed_elsewhere_is_unmodelled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root, '  - match: "*/missions/*/enhancements/*.step-enhancement.yaml"\n    schema: tactic\n')
            pack = self.write_pack(root, {"foo.step-enhancement.yaml": "id: x\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_OK, output)
            self.assertIn("pack/foo.step-enhancement.yaml: file_not_held", output)

    def test_a_symlinked_file_or_directory_in_a_pack_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"tactics/real.tactic.yaml": "id: r\n"})
            try:
                (pack / "tactics" / "link.tactic.yaml").symlink_to("real.tactic.yaml")
                (pack / "linked-dir").symlink_to("tactics", target_is_directory=True)
            except OSError as exc:  # pragma: no cover - a platform without symlinks
                self.skipTest(f"cannot create symlinks: {exc!r}")
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/tactics/link.tactic.yaml: symlink", output)
            self.assertIn("pack/linked-dir: symlink", output)

    def test_pack_level_structure_needs_a_descriptor_and_a_preset_id_equal_to_its_stem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"README.md": "# Title\n", "presets/p.yaml": "id: q\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/pack.yaml: missing: a pack with a README.md or a pack-manifest.yaml needs its descriptor", output)
            self.assertIn("pack/presets/p.yaml: preset id 'q' is not its file stem 'p'", output)

    def test_markdown_blankness_and_line_separators_follow_the_java_codec(self) -> None:
        # Java isBlank/strip do not count NBSP as whitespace and `.` stops at U+2028, so the charter
        # reads these as a heading titled NBSP, a heading without a closing sequence, and a kept line.
        model = validator.parse_markdown("# T\n\n## \u00a0\n\n## a\u2028 #\n\n\u00a0\n")
        self.assertEqual(
            model["sections"],
            [{"title": "\u00a0", "content": ""}, {"title": "a\u2028 #", "content": "\u00a0"}],
        )
        with self.assertRaises(validator.MarkdownRefused):  # a plain space-only title is still empty
            validator.parse_markdown("## \u2003\n")

    def test_a_specializes_from_cycle_among_agent_profiles_is_named_in_order(self) -> None:
        """#286 (charter ADR-0078 decision 2): the specialization edges are acyclic; a profile may have several parents."""
        def pack(root: Path, name: str, edges: str) -> Path:
            (root / name / "drg").mkdir(parents=True)
            (root / name / "pack.yaml").write_text(f"pack_id: {name}\nname: {name}\npack_level: org\n", encoding="utf-8")
            (root / name / "drg" / "fragment.yaml").write_text(f"nodes: []\nedges: {edges}\n", encoding="utf-8")
            return root / name

        spec = "{{source: 'agent_profile:{}', target: '{}agent_profile:{}', relation: specializes_from}}"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Several parents and a shared ancestor: acyclic, so nothing to report.
            base = pack(root, "base", f"[{spec.format('ivan', '', 'generic')}]")
            langs = pack(root, "langs", "[" + ", ".join((spec.format("gwen", "base::", "ivan"), spec.format("gwen", "base::", "generic"),
                                                          spec.format("jenny", "base::", "ivan"))) + "]")
            self.assertEqual(validator.specialization_cycle_violations([base, langs]), [])
            # The positive control: two profiles that specialize each other, across packs and qualified.
            loop = pack(root, "loop", f"[{spec.format('zed', 'base::', 'ivan')}, {spec.format('generic', 'loop::', 'zed')}]")
            self.assertEqual(validator.specialization_cycle_violations([base, langs, loop]),
                             ["specializes_from cycle among agent profiles: generic -> zed -> ivan -> generic"])
            mutual = pack(root, "mutual", f"[{spec.format('bob', '', 'amy')}, {spec.format('amy', '', 'bob')}]")
            self.assertEqual(validator.specialization_cycle_violations([mutual]),
                             ["specializes_from cycle among agent profiles: amy -> bob -> amy"])
            # Edges of another relation, or between other kinds, are not specialization edges.
            other = pack(root, "other", "[{source: 'agent_profile:x', target: 'agent_profile:y', relation: requires}, "
                                        "{source: 'agent_profile:y', target: 'agent_profile:x', relation: requires}]")
            self.assertEqual(validator.specialization_cycle_violations([other]), [])

    def test_a_long_specialization_chain_does_not_exhaust_the_recursion_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "deep"
            (root / "drg").mkdir(parents=True)
            (root / "pack.yaml").write_text("pack_id: deep\nname: deep\npack_level: org\n", encoding="utf-8")
            edges = "".join(f"  - {{source: 'agent_profile:p{i}', target: 'agent_profile:p{i + 1}', relation: specializes_from}}\n"
                            for i in range(5000))
            (root / "drg" / "fragment.yaml").write_text(f"nodes: []\nedges:\n{edges}", encoding="utf-8")
            self.assertEqual(validator.specialization_cycle_violations([root]), [])

    def test_a_bare_vocabulary_edge_to_a_held_term_resolves(self) -> None:
        """A term is never declared: a vocabulary edge reaches it as term:<context-id>/<term-id> (charter ADR-0049)."""
        contract = validator.Contract(
            files=[validator.Rule(validator.glob_to_regex("**/*.glossary.yaml"), "**/*.glossary.yaml", schema="glossary")],
            exclusions=[], retired=[], payloads=[],
        )
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "g"
            (pack / "drg").mkdir(parents=True)
            (pack / "glossaries").mkdir()
            (pack / "pack.yaml").write_text("pack_id: g\nname: g\npack_level: org\n", encoding="utf-8")
            (pack / "glossaries" / "core.glossary.yaml").write_text("id: core\nterms:\n  - {id: foo, name: foo}\n", encoding="utf-8")
            (pack / "drg" / "fragment.yaml").write_text(
                "nodes:\n  - {id: D_1, kind: directives}\nedges:\n"
                "  - {source: 'directive:D_1', target: 'term:core/foo', relation: vocabulary}\n"
                "  - {source: 'directive:D_1', target: 'term:core/bar', relation: vocabulary}\n", encoding="utf-8")
            found = validator.cross_pack_violations([pack], contract)
            self.assertEqual(found, ["g/drg/fragment.yaml: edge target 'term:core/bar' resolves to no node of any pack"])

    def test_cross_pack_rules_catch_a_dangling_bare_edge_and_an_id_shared_across_levels(self) -> None:
        def pack(root: Path, name: str, nodes: str, edges: str = "[]", level: str = "org") -> Path:
            (root / name / "drg").mkdir(parents=True)
            (root / name / "pack.yaml").write_text(f"pack_id: {name}\nname: {name}\npack_level: {level}\n", encoding="utf-8")
            (root / name / "drg" / "fragment.yaml").write_text(f"nodes:\n{nodes}edges: {edges}\n", encoding="utf-8")
            return root / name

        node = "  - {id: D_1, kind: directives}\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = pack(root, "a", node + "  - {id: D_2, kind: directives}\n",
                         "[{source: 'directive:D_1', target: 'directive:D_2', relation: requires}]")
            self.assertEqual(validator.cross_pack_violations([clean]), [])
            bad = pack(root, "b", "  - {id: D_2, kind: directives}\n", "[{source: 'directive:D_2', target: 'tactic:T_9'}]")
            twin = pack(root, "c", node, level="built-in")
            found = "\n".join(validator.cross_pack_violations([clean, bad, twin]))
            for expected in ("b/drg/fragment.yaml: edge target 'tactic:T_9' resolves to no node of any pack",
                             "directive:D_1: declared by packs of different levels (a [org], c [built-in])"):
                self.assertIn(expected, found)
            # Artifact files declare ids too, by the kind their schema names (needs the contract).
            # A glossary file declares the node glossary_context:<id>, which the fragment plural glossaries names too
            # (file-kinds.yaml, charter ADR-0053 decision 13).
            contract = validator.Contract(
                files=[validator.Rule(validator.glob_to_regex("**/*.glossary.yaml"), "**/*.glossary.yaml", schema="glossary")],
                exclusions=[], retired=[], payloads=[],
            )
            to_terms = "[{source: 'directive:D_1', target: 'glossary_context:qa-terms', relation: vocabulary}]"
            filed = pack(root, "e", node, to_terms)
            (filed / "glossaries").mkdir()
            (filed / "glossaries" / "qa-terms.glossary.yaml").write_text("id: qa-terms\n", encoding="utf-8")
            self.assertEqual(validator.cross_pack_violations([filed], contract), [])  # a file-only id resolves the end
            self.assertTrue(validator.cross_pack_violations([filed]))  # ...but only when the contract classifies files
            # A file and a node for one id of one pack are a single declaration, not a collision.
            (filed / "glossaries" / "d1.glossary.yaml").write_text("id: D_1\n", encoding="utf-8")
            (filed / "drg" / "fragment.yaml").write_text("nodes:\n  - {id: D_1, kind: glossaries}\nedges: []\n", encoding="utf-8")
            self.assertEqual(validator.cross_pack_violations([filed], contract), [])
            # The right id of the wrong kind does not resolve an end: D_1 is a directive in `a`, not a glossary.
            wrong = pack(root, "f", "  - {id: D_4, kind: directives}\n",
                         "[{source: 'directive:D_4', target: 'glossary_context:D_1', relation: vocabulary}]")
            found = "\n".join(validator.cross_pack_violations([clean, wrong], contract))
            self.assertIn("edge target 'glossary_context:D_1' resolves to no node of any pack", found)
            # A file-only id shared by two packs is a collision.
            other = pack(root, "g", "  - {id: D_3, kind: directives}\n", level="built-in")
            (other / "glossaries").mkdir()
            (other / "glossaries" / "qa-terms.glossary.yaml").write_text("id: qa-terms\n", encoding="utf-8")
            found = "\n".join(validator.cross_pack_violations([filed, other], contract))
            self.assertIn("glossary_context:qa-terms: declared by packs of different levels (e [org], g [built-in])", found)
            empty = pack(root, "d", "", "[]")
            (empty / "drg" / "fragment.yaml").write_text("nodes: []\n", encoding="utf-8")
            with self.assertRaises(validator.GateError):  # an empty id index must not pass
                validator.cross_pack_violations([empty])

    def test_preset_items_are_left_to_pack_doctor(self) -> None:
        """#346, #348: pack-doctor judges every preset item against its pack's own closure (preset_item_undeclared,
        preset_item_not_held, RealPackDoctor proves both against the jar), so the cross-pack rules no longer do."""
        with tempfile.TemporaryDirectory() as tmp:
            pack = Path(tmp) / "a"
            (pack / "drg").mkdir(parents=True)
            (pack / "presets").mkdir()
            (pack / "pack.yaml").write_text("pack_id: a\nname: a\npack_level: org\n", encoding="utf-8")
            (pack / "drg" / "fragment.yaml").write_text("nodes:\n  - {id: NODE_ONLY, kind: directives}\nedges: []\n",
                                                       encoding="utf-8")
            (pack / "presets" / "p.yaml").write_text(
                "schema_version: '1.0'\nid: p\nactivated_directives:\n  - {id: NOWHERE}\n  - {id: NODE_ONLY, must_have: true}\n",
                encoding="utf-8")
            self.assertEqual(validator.cross_pack_violations([pack]), [])

BUILT_IN = "01ARWG13C000000000000000FG"
OTHER = "01ARWG13C000000000000000XX"
CONSUMER = "01ARWG13C000000000000000YY"


class CompositionChecks(unittest.TestCase):
    """What ``--cross-pack`` still judges because the charter service does not: agent-profile references,
    an id re-declared at another level, and the held-artifact rules those references resolve against. The
    composition rules the service makes (descriptors, ``depends_on``, edge ends) are its job, in
    ``scripts/ci/charter_service_check.py``, and are no longer judged here."""

    CONTRACT = validator.Contract(
        files=[
            validator.Rule(validator.glob_to_regex(f"**/*.{suffix}.yaml"), f"**/*.{suffix}.yaml", schema=schema)
            for suffix, schema in (("directive", "directive"), ("tactic", "tactic"), ("paradigm", "paradigm"),
                                   ("procedure", "procedure"), ("mission-type", "mission-type"),
                                   ("agent", "agent-profile"),
                                   ("asset", "asset"), ("glossary", "glossary"), ("skill", "skill"),
                                   ("styleguide", "styleguide"), ("toolguide", "toolguide"))
        ],
        exclusions=[], retired=[],
        payloads=[validator.Rule(validator.glob_to_regex(glob), glob) for glob in ("*/templates/**/*", "*/missions/*/templates/**/*")],
    )

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def write(self, directory: str, files: dict[str, str]) -> Path:
        for name, body in files.items():
            target = self.root / directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        return self.root / directory

    def descriptor(self, pack_id: str, name: str, depends_on: tuple[str, ...] = (), level: str | None = None) -> str:
        entries = "".join(f"- {{pack_id: {dep}, range: '>=1.0,<2'}}\n" for dep in depends_on)
        return (f"pack_id: {pack_id}\nname: {name}\n" + (f"pack_level: {level}\n" if level else "")
                + (f"depends_on:\n{entries}" if entries else ""))

    def built_in(self, directory: str = "built-in", name: str = "built-in", pack_id: str = BUILT_IN) -> Path:
        """A pack holding tactic `held` as a file, and an action as a node."""
        return self.write(directory, {
            "pack.yaml": self.descriptor(pack_id, name),
            "tactics/held.tactic.yaml": "id: held\n",
            "drg/fragment.yaml": "nodes:\n  - {id: dev/plan, kind: actions}\nedges: []\n",
        })

    def consumer(self, edges: str = "[]", files: dict[str, str] | None = None, depends_on: tuple[str, ...] = (BUILT_IN,),
                 directory: str = "consumer") -> Path:
        """A pack depending on `depends_on`, holding tactic `own`; `edges` is its fragment's edge list."""
        return self.write(directory, {
            "pack.yaml": self.descriptor(CONSUMER, directory, depends_on),
            "tactics/own.tactic.yaml": "id: own\n",
            "drg/fragment.yaml": f"nodes: []\nedges: {edges}\n",
            **(files or {}),
        })

    def edge(self, target: str) -> str:
        return f"[{{source: 'tactic:own', target: '{target}', relation: requires}}]"

    def found(self, *packs: Path) -> str:
        return "\n".join(validator.cross_pack_violations(list(packs), self.CONTRACT))

    def test_an_id_declared_at_another_level_fails_and_one_declared_twice_at_one_level_is_the_services(self) -> None:
        built_in = self.write("built-in", {"pack.yaml": self.descriptor(BUILT_IN, "built-in", level="built-in"),
                                           "tactics/held.tactic.yaml": "id: held\n"})
        org = self.write("org", {"pack.yaml": self.descriptor(OTHER, "org", (BUILT_IN,), level="org"),
                                 "tactics/held.tactic.yaml": "id: held\n"})
        found = self.found(built_in, org)
        self.assertIn("tactic:held: declared by packs of different levels (built-in [built-in], org [org])", found)
        sibling = self.write("sibling", {"pack.yaml": self.descriptor(CONSUMER, "sibling", (BUILT_IN,), level="org"),
                                         "tactics/held.tactic.yaml": "id: held\n"})
        # two org packs holding one id are a sibling conflict, which the service refuses (pack_sibling_conflict)
        self.assertEqual(self.found(built_in, sibling).count("different levels"), 1)
        self.assertNotIn("different levels", self.found(org, sibling))

    def test_a_bare_dangling_edge_end_fails_and_composition_defects_are_left_to_the_service(self) -> None:
        built_in = self.built_in()
        self.assertIn("edge target 'tactic:nowhere' resolves to no node of any pack",
                      self.found(built_in, self.consumer("[{source: 'tactic:own', target: 'tactic:nowhere'}]")))
        # Judged by the service (scripts/ci/charter_service_check.py), so silent here: a qualifier outside the
        # closure, a qualified end the named pack does not hold, an edge to itself, a missing descriptor,
        # a shared pack_id or name, an unknown dependency and a depends_on cycle.
        for label, packs in (
            ("outside the closure", (built_in, self.consumer(self.edge("built-in::tactic:held"), depends_on=()))),
            ("not held", (built_in, self.consumer(self.edge("built-in::tactic:gone")))),
            ("to itself", (built_in, self.consumer("[{source: 'tactic:own', target: 'tactic:own', relation: requires}]"))),
            ("unknown dependency", (built_in, self.consumer(depends_on=("01ARWG13C000000000000000ZZ",), directory="lost"))),
            ("shared pack_id", (built_in, self.write("same-id", {"pack.yaml": self.descriptor(BUILT_IN, "same-id")}))),
            ("shared name", (built_in, self.write("same-name", {"pack.yaml": self.descriptor(OTHER, "built-in")}))),
            ("cycle", (built_in, self.consumer(depends_on=(CONSUMER,), directory="loop"))),
        ):
            with self.subTest(label):
                found = self.found(*packs)
                for fragment in ("outside this pack's depends_on closure", "does not hold", "joins", "missing", "declared by more than one",
                                 "resolves to no pack", "depends_on cycle"):
                    self.assertNotIn(fragment, found)

    def test_cross_pack_runs_every_house_rule(self) -> None:
        """--cross-pack (cross_pack_violations) runs each house rule of #348, one pack set with one fault of each."""
        built_in = self.write("built-in", {
            "pack.yaml": self.descriptor(BUILT_IN, "built-in", level="built-in"),
            "tactics/held.tactic.yaml": "id: held\n",
            "missions/dev/dev.mission-type.yaml": "id: dev\nsteps:\n- id: plan\n  prompt_path: steps/plan.prompt.md\n",
            "missions/dev/steps/plan.prompt.md": "<!-- x:block:start -->\n<!-- x:block:end -->\n",
            "drg/fragment.yaml": "nodes: []\nedges: []\n",
        })
        consumer = self.consumer(
            "[{source: 'tactic:own', target: 'tactic:nowhere', relation: requires}, "
            "{source: 'agent_profile:a', target: 'agent_profile:b', relation: specializes_from}, "
            "{source: 'agent_profile:b', target: 'agent_profile:a', relation: specializes_from}, "
            "{source: 'step_enhancement:enh', target: 'built-in::action:dev/plan', relation: enhances}]",
            files={
                "pack.yaml": self.descriptor(CONSUMER, "consumer", (BUILT_IN,), level="org"),
                "tactics/again.tactic.yaml": "id: held\n",
                "agent_profiles/p.agent.yaml": self.profile_file(tactic_id="nowhere-held"),
                "missions/dev/enhancements/enh.step-enhancement.yaml": "id: enh\nprompt_fragments:\n- {slot: 'x:other', path: f.md}\n",
            })
        found = self.found(built_in, consumer)
        for expected in (
            "tactic:held: declared by packs of different levels",  # ADR-0053 decision 6
            "consumer/drg/fragment.yaml: edge target 'tactic:nowhere' resolves to no node of any pack",  # DIV-007
            "prompt_slot_missing at /prompt_fragments/0/slot",  # C38
            "specializes_from cycle among agent profiles: a -> b -> a",  # ruling R-s remainder
            "bare tactic reference 'nowhere-held' resolves to no artifact of any pack",  # rule-coverage.md row 6
        ):
            with self.subTest(expected):
                self.assertIn(expected, found)

    def test_a_node_with_no_file_is_held_by_nobody(self) -> None:
        graph = "nodes:\n- {urn: 'procedure:shard-node', kind: procedure}\nedges: []\n"
        fragment = "nodes:\n  - {id: node-tactic, kind: tactics}\nedges: []\n"
        built_in = self.built_in()
        self.write("built-in", {"drg/fragment.yaml": fragment, "procedure.graph.yaml": graph})
        held = validator.held_artifacts(built_in, self.CONTRACT)
        self.assertIn(("tactic", "held"), held)  # a file
        self.assertNotIn(("tactic", "node-tactic"), held)
        self.assertNotIn(("procedure", "shard-node"), held)

    def test_files_no_node_names_are_held_under_the_id_the_charter_reads(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "agent_profiles/p.agent.yaml": "profile-id: file-profile\n",
            "missions/doc/doc.mission-type.yaml": "id: doc\n",
            "templates/writing/top.md": "# t\n",
            "missions/doc/templates/in-mission.md": "# t\n",
        })
        held = validator.held_artifacts(built_in, self.CONTRACT)
        for key in (("agent_profile", "file-profile"), ("mission_type", "doc"),
                    ("template", "writing/top.md"), ("template", "doc/in-mission.md")):
            with self.subTest(key):
                self.assertIn(key, held)

    def test_a_template_elsewhere_in_a_pack_is_not_held(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {"templates/held.md": "# t\n", "elsewhere/templates/stray.md": "# t\n"})
        held = validator.held_artifacts(built_in, self.CONTRACT)
        self.assertIn(("template", "held.md"), held)
        self.assertNotIn(("template", "stray.md"), held)

    def test_an_anti_pattern_is_held_by_its_file_only(self) -> None:
        """#348 (f): an anti-pattern is held by anti_patterns/<id>.anti-pattern.yaml, never by its graph node alone
        (charter check-packs.md: "An anti-pattern is held only by its file")."""
        contract = validator.Contract(
            files=[*self.CONTRACT.files, validator.Rule(validator.glob_to_regex("**/*.anti-pattern.yaml"),
                                                        "**/*.anti-pattern.yaml", schema="anti-pattern")],
            exclusions=[], retired=[], payloads=[],
        )
        built_in = self.built_in()
        self.write("built-in", {
            "anti_patterns/filed.anti-pattern.yaml": "id: filed\n",
            "drg/fragment.yaml": "nodes:\n  - {id: filed, kind: anti_patterns}\n  - {id: in-fragment, kind: anti_patterns}\nedges: []\n",
            "anti_pattern.graph.yaml": "nodes:\n- {urn: 'anti_pattern:in-shard', kind: anti_pattern}\nedges: []\n",
        })
        held = validator.held_artifacts(built_in, contract)
        self.assertIn(("anti_pattern", "filed"), held)
        self.assertNotIn(("anti_pattern", "in-fragment"), held)
        self.assertNotIn(("anti_pattern", "in-shard"), held)
        self.assertIn(("anti_pattern", "filed"), validator.declared_nodes(built_in, contract))  # the file declares it

    def test_a_template_directory_holds_only_what_the_contract_classifies_as_a_payload(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {"templates/filed.tactic.yaml": "id: filed\n", "templates/held.md": "# t\n"})
        held = validator.held_artifacts(built_in, self.CONTRACT)
        self.assertIn(("tactic", "filed"), held)
        self.assertIn(("template", "held.md"), held)
        self.assertNotIn(("template", "filed.tactic.yaml"), held)

    def profile_file(self, tactic_id: str = "own", styleguide_id: str | None = None,
                     toolguide_id: str | None = None, directive_code: str | None = None,
                     procedure: str | None = None) -> str:
        """An agent profile naming the given reference ids (a directive by its ``code``);
        ``None`` leaves a field out. The default tactic id is the consumer pack's own
        tactic, which stays bare."""
        parts = [f"tactic-references:\n  - id: {tactic_id}\n    rationale: r\n"]
        if styleguide_id is not None:
            parts.append(f"styleguide-references:\n  - id: {styleguide_id}\n    rationale: r\n")
        if toolguide_id is not None:
            parts.append(f"toolguide-references:\n  - id: {toolguide_id}\n    rationale: r\n")
        if directive_code is not None:
            parts.append(f"directive-references:\n  - code: {directive_code}\n    name: n\n    rationale: r\n")
        if procedure is not None:
            parts.append(f"collaboration:\n  operating-procedures:\n    - {procedure}\n")
        return "".join(parts)

    def test_a_bare_agent_profile_reference_held_only_by_a_dependency_fails_and_qualifying_fixes_it(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "styleguides/held.styleguide.yaml": "id: held-style\n",
            "toolguides/held.toolguide.yaml": "id: held-tool\n",
            "procedures/held.procedure.yaml": "id: held-procedure\n",
        })
        bare = self.consumer(files={"agent_profiles/p.agent.yaml": self.profile_file(
            tactic_id="held", styleguide_id="held-style", toolguide_id="held-tool", procedure="held-procedure")})
        found = self.found(built_in, bare)
        for kind, ref in (
            ("tactic", "held"), ("styleguide", "held-style"),
            ("toolguide", "held-tool"), ("procedure", "held-procedure"),
        ):
            with self.subTest(kind=kind):
                self.assertIn(
                    f"consumer/agent_profiles/p.agent.yaml: bare {kind} reference {ref!r} is held only by built-in; "
                    "qualify it with that pack's name",
                    found,
                )
        qualified = self.consumer(files={"agent_profiles/p.agent.yaml": self.profile_file(
            tactic_id="built-in::held", styleguide_id="built-in::held-style",
            toolguide_id="built-in::held-tool", procedure="built-in::held-procedure")})
        self.assertEqual(self.found(built_in, qualified), "")

    def test_a_bare_directive_code_held_only_by_a_dependency_fails_and_qualifying_fixes_it(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {"directives/held.directive.yaml": "id: DIR_HELD\n"})
        bare = self.consumer(files={"agent_profiles/p.agent.yaml": self.profile_file(directive_code="DIR_HELD")})
        self.assertIn(
            "consumer/agent_profiles/p.agent.yaml: bare directive reference 'DIR_HELD' is held only by built-in; "
            "qualify it with that pack's name",
            self.found(built_in, bare),
        )
        qualified = self.consumer(files={"agent_profiles/p.agent.yaml": self.profile_file(directive_code="built-in::DIR_HELD")})
        self.assertEqual(self.found(built_in, qualified), "")

    def test_a_directive_code_also_names_an_id_numbered_under_directive(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "directives/numbered.directive.yaml": "id: DIRECTIVE_010\n",
            "agent_profiles/own.agent.yaml": self.profile_file(tactic_id="held", directive_code="010"),
        })
        self.assertEqual(self.found(built_in), "")

    def test_an_agent_profiles_own_references_stay_bare_and_one_no_pack_holds_is_refused(self) -> None:
        built_in = self.built_in()
        files = {
            "styleguides/own.styleguide.yaml": "id: own-style\n",
            "toolguides/own.toolguide.yaml": "id: own-tool\n",
            "procedures/own.procedure.yaml": "id: own-procedure\n",
            "agent_profiles/p.agent.yaml": self.profile_file(
                tactic_id="own", styleguide_id="own-style", toolguide_id="own-tool", procedure="own-procedure"),
        }
        self.assertEqual(self.found(built_in, self.consumer(files=files)), "")
        nowhere = self.consumer(files={"agent_profiles/p.agent.yaml": self.profile_file(tactic_id="nowhere")})
        self.assertIn(
            "consumer/agent_profiles/p.agent.yaml: bare tactic reference 'nowhere' resolves to no artifact of any pack",
            self.found(built_in, nowhere),
        )

    def test_a_profile_reference_qualified_with_the_profiles_own_pack_is_refused(self) -> None:
        built_in = self.built_in()
        # the referrer looks like the real qa pack: directory `qa`, descriptor name `quality-assurance`
        referrer = self.write("qa", {
            "pack.yaml": self.descriptor(CONSUMER, "quality-assurance", (BUILT_IN,)),
            "tactics/own.tactic.yaml": "id: own\n",
            "drg/fragment.yaml": "nodes: []\nedges: []\n",
        })
        for qualifier in ("qa", "quality-assurance"):  # the directory name and the descriptor name
            with self.subTest(qualifier=qualifier):
                self.write("qa", {"agent_profiles/p.agent.yaml": self.profile_file(tactic_id=f"{qualifier}::own")})
                found = self.found(built_in, referrer)
                self.assertIn(
                    f"qa/agent_profiles/p.agent.yaml: reference '{qualifier}::own' names this profile's own pack; "
                    "references inside one pack stay bare",
                    found,
                )
                self.assertNotIn("outside this pack's depends_on closure", found)
        self.write("qa", {"agent_profiles/p.agent.yaml": self.profile_file(tactic_id="built-in::held")})
        self.assertEqual(self.found(built_in, referrer), "")  # a dependency's qualifier keeps passing

    def test_a_qualified_agent_profile_reference_outside_the_closure_or_unheld_fails(self) -> None:
        built_in = self.built_in()
        for label, depends_on, reference, expected in (
            ("outside the closure", (), "built-in::held", "outside this pack's depends_on closure"),
            ("no such pack", (BUILT_IN,), "nowhere::held", "outside this pack's depends_on closure"),
            ("unheld by the named pack", (BUILT_IN,), "built-in::gone", "built-in does not hold tactic 'gone'"),
        ):
            with self.subTest(label):
                profile = self.profile_file(tactic_id=reference)
                found = self.found(built_in, self.consumer(files={"agent_profiles/p.agent.yaml": profile}, depends_on=depends_on))
                self.assertIn(f"consumer/agent_profiles/p.agent.yaml: reference '{reference}'", found)
                self.assertIn(expected, found)


class AntiPatternFilesOnThePinnedContract(unittest.TestCase):
    """#348 (f), FR-017: an anti-pattern is a file, ``anti_patterns/<id>.anti-pattern.yaml``, classified through the
    pinned ``file-kinds.yaml`` (data, not code), validated against the pinned ``anti-pattern.schema.json`` and listed
    in the manifest as a constituent (its membership judged by pack-doctor), so this job and pack-doctor agree on it."""

    ANTI_PATTERN = (
        "schema_version: '1.0'\nid: secret-in-repo\ntitle: A secret in the repository\n"
        "description: Credentials committed beside the code.\nseverity: breaking\n"
        "bad_example: An API key in config.yaml.\n"
    )
    ENTRY = ("- kind: anti_pattern\n  id: secret-in-repo\n  path: anti_patterns/secret-in-repo.anti-pattern.yaml\n"
             "  content_hash: '" + "0" * 64 + "'\n")

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = validator.contract_for(None)

    def pack(self, tmp: str, *, listed: bool = True, text: str | None = None) -> Path:
        """The valid example pack with one anti-pattern file and its node; the manifest lists it when ``listed``."""
        pack = Path(tmp) / "example-pack"
        shutil.copytree(Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "valid" / "example-pack", pack)
        (pack / "anti_patterns").mkdir()
        (pack / "anti_patterns" / "secret-in-repo.anti-pattern.yaml").write_text(text or self.ANTI_PATTERN, encoding="utf-8")
        fragment = pack / "drg" / "fragment.yaml"
        fragment.write_text(fragment.read_text(encoding="utf-8").replace(
            "edges:\n", "- id: secret-in-repo\n  kind: anti_patterns\n  title: A secret in the repository\nedges:\n", 1),
            encoding="utf-8")
        if listed:
            manifest = pack / "pack-manifest.yaml"
            manifest.write_text(manifest.read_text(encoding="utf-8").replace("presets:\n", self.ENTRY + "presets:\n", 1),
                                encoding="utf-8")
        return pack

    def test_the_file_is_classified_by_the_pinned_contract_and_validates(self) -> None:
        kind, rule = validator.classify(self.contract, "example-pack/anti_patterns/secret-in-repo.anti-pattern.yaml")
        self.assertEqual((kind, rule.schema if rule else None), ("file", "anti-pattern"))
        with tempfile.TemporaryDirectory() as tmp:
            report = validator.validate_pack(self.pack(tmp), self.contract)
        self.assertEqual(report.violations, [])
        self.assertEqual(report.warnings, [])

    def test_a_missing_severity_fails_against_the_pinned_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text = self.ANTI_PATTERN.replace("severity: breaking\n", "")
            found = "\n".join(validator.validate_pack(self.pack(tmp, text=text), self.contract).violations)
        self.assertIn("anti_patterns/secret-in-repo.anti-pattern.yaml: anti-pattern schema at /: 'severity' is a required property",
                      found)

    def test_an_unlisted_file_and_its_node_are_left_to_pack_doctor(self) -> None:
        # The file's membership, and so its node's, is pack-doctor's manifest_membership (decision 01M8BMA8;
        # RealPackDoctor proves the jar refuses this pack): the schema pass names only a node no file declares.
        with tempfile.TemporaryDirectory() as tmp:
            found = validator.validate_pack(self.pack(tmp, listed=False), self.contract).violations
        self.assertEqual(found, [])


class ClassifierConformance(unittest.TestCase):
    """The charter's own classification cases at the pin (contracts/packs/conformance/classifier-cases.yaml): every
    path is classified as the charter states, by the same rule (precedence of retired over files included)."""

    EXPECT = {"file": "mapped", "payload": "mapped", "excluded": "excluded", "ignored": "excluded",
              "retired": "retired", "unmodelled": "unmodelled"}

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = validator.contract_for(None)
        relative = "conformance/classifier-cases.yaml"
        if local := os.environ.get("CHARTER_CONTRACT_DIR"):
            text = (Path(local) / relative).read_text(encoding="utf-8")
        else:
            url = (f"https://raw.githubusercontent.com/{validator.CHARTER_REPOSITORY}/{validator.charter_commit()}/"
                   f"{validator.CONTRACT_PATH}/{relative}")
            with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310 - fixed https URL
                text = response.read().decode("utf-8")
        cls.cases = yaml.safe_load(text)["cases"]

    def test_every_case_is_classified_as_the_charter_states(self) -> None:
        self.assertGreater(len(self.cases), 50)
        for case in self.cases:
            with self.subTest(case["path"]):
                kind, rule = validator.classify(self.contract, case["path"])
                self.assertEqual(self.EXPECT[kind], case["expect"])
                if "rule" in case:
                    self.assertEqual(rule.match if rule else None, case["rule"])


class CompanionLintOnTheShippedPacks(unittest.TestCase):
    """R38's lint raises nothing over this repository's own packs at the pin: no false positive, no missing companion."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = validator.contract_for(None)

    def test_no_shipped_pack_or_valid_fixture_has_a_lint_finding(self) -> None:
        root = Path(__file__).resolve().parents[2]
        packs = sorted(p for base in (root / "packs", root / "tests" / "fixtures" / "valid") for p in base.iterdir()
                       if p.is_dir() and (p / "pack.yaml").is_file())
        self.assertTrue(packs)
        for pack in packs:
            with self.subTest(pack=pack.name):
                self.assertEqual(validator.validate_pack(pack, self.contract).suspects, [])
