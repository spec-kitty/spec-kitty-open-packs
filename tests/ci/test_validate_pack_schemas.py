"""The pack schema validator judges real pack files and fails closed when it cannot judge."""

from __future__ import annotations

import contextlib
import hashlib
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
            pack = self.write_pack(root, {"presets/p.yaml": "id: p\n", "pack.yaml": "pack_id: x\n", "pack-manifest.yaml": manifest})
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

    def test_content_hash_reads_crlf_and_lone_cr_as_lf(self) -> None:
        def sha(data: bytes) -> str:
            return hashlib.sha256(data).hexdigest()

        self.assertEqual(validator.content_hash(b"a\r\nb\rc\n"), sha(b"a\nb\nc\n"))
        self.assertEqual(validator.content_hash(b"a\r\r\nb"), sha(b"a\n\nb"))  # CRLF first, then the lone CR
        self.assertNotEqual(validator.content_hash(b"a\r\nb"), sha(b"a\r\nb"))
        self.assertNotEqual(validator.content_hash(b"a\n"), validator.content_hash(b"a"))

    def test_regenerate_and_verify_hash_crlf_lf_and_lone_cr_copies_alike(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml"], {"tactics/t.tactic.yaml": "id: t\r\nname: x\r\n"})
            self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack))[0], validator.EXIT_OK)
            entry = validator.load_yaml((pack / "pack-manifest.yaml").read_text(encoding="utf-8"))["constituents"][0]
            self.assertEqual(entry["content_hash"], hashlib.sha256(b"id: t\nname: x\n").hexdigest())
            for body in (b"id: t\r\nname: x\r\n", b"id: t\nname: x\n", b"id: t\rname: x\r"):
                (pack / "tactics" / "t.tactic.yaml").write_bytes(body)
                code, output = self.run_validator(root, str(pack))
                self.assertEqual(code, validator.EXIT_OK, output)

    def test_regenerate_alone_refuses_a_listed_file_that_is_missing_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml", "tactics/gone.tactic.yaml"])
            before = (pack / "pack-manifest.yaml").read_bytes()
            code, output = self.run_validator(root, "--regenerate-manifest", str(pack))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn("::error", output)
            self.assertIn("tactics/gone.tactic.yaml", output)
            self.assertIn("not regenerated:", output)
            self.assertFalse([line for line in output.splitlines() if line.startswith("regenerated:")])
            self.assertEqual((pack / "pack-manifest.yaml").read_bytes(), before)

    def test_regenerate_of_several_packs_keeps_a_miss_in_the_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            broken = self.manifest_pack(root, ["tactics/gone.tactic.yaml"], name="broken")
            clean = self.manifest_pack(root, ["tactics/t.tactic.yaml"], name="clean")
            code, output = self.run_validator(root, "--regenerate-manifest", str(broken), "--regenerate-manifest", str(clean), str(clean))
            self.assertEqual(code, validator.EXIT_INVALID, output)
            self.assertIn(f"regenerated: {clean / 'pack-manifest.yaml'}", output)
            self.assertIn(f"ok: {clean}", output)

    def test_validation_reports_a_listed_file_that_is_missing_with_a_remedy_that_fixes_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml", "tactics/u.tactic.yaml"], {"tactics/u.tactic.yaml": "id: u\n"})
            self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack), str(pack))[0], validator.EXIT_OK)
            (pack / "tactics" / "u.tactic.yaml").unlink()
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            missing_line = next(line for line in output.splitlines() if "stale manifest: missing: tactics/u.tactic.yaml" in line)
            self.assertIn("restore the file or remove its entry", missing_line)
            self.assertNotIn("--regenerate-manifest", missing_line)
            self.assertNotIn("u.tactic.yaml}.content_hash", output)

    def test_a_doctrine_file_the_manifest_does_not_list_fails_naming_the_file(self) -> None:
        """#182: a pack with a manifest lists every file-backed doctrine artifact it holds."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml"],
                                      {"tactics/t.tactic.yaml": "id: t\n", "tactics/u.tactic.yaml": "id: u\n"})
            self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack))[0], validator.EXIT_OK)
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            line = next(line for line in output.splitlines() if "incomplete manifest" in line)
            self.assertIn("tactics/u.tactic.yaml is not a constituent", line)
            self.assertNotIn("tactics/t.tactic.yaml", line)

            # Listing it (and restamping) clears the finding: the positive control.
            pack.joinpath("pack-manifest.yaml").unlink()
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml", "tactics/u.tactic.yaml"],
                                      {"tactics/t.tactic.yaml": "id: t\n", "tactics/u.tactic.yaml": "id: u\n"})
            self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack), str(pack))[0], validator.EXIT_OK)

    def test_a_listed_constituent_with_no_file_still_fails_as_stale_not_as_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.manifest_pack(root, ["tactics/t.tactic.yaml", "tactics/gone.tactic.yaml"], {"tactics/t.tactic.yaml": "id: t\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("stale manifest: missing: tactics/gone.tactic.yaml", output)
            self.assertNotIn("incomplete manifest", output)

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
        """A manifest-bearing pack with a tactic file, `files` and (optionally) a `tactic:ghost` entry; hashes regenerated."""
        paths = ["tactics/t.tactic.yaml"] + (["tactics/ghost.tactic.yaml"] if constituents else [])
        pack = self.manifest_pack(root, paths, {"tactics/t.tactic.yaml": "id: t\n", **files})
        self.assertEqual(self.run_validator(root, "--regenerate-manifest", str(pack))[0], validator.EXIT_OK)
        return pack

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
            for k in ("actions", "templates", "mission_types", "mission_step_contracts", "anti_patterns")
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

    def test_unlisted_nodes_is_exact_and_skips_exempt_kinds(self) -> None:
        manifest = {"constituents": [{"kind": "tactic", "id": "a"}, "junk"]}
        nodes = {("tactic", "a"), ("tactic", "b"), ("action", "x")}
        self.assertEqual(validator.unlisted_nodes(manifest, nodes), ["tactic:b"])
        self.assertEqual(validator.unlisted_nodes({"constituents": [{"kind": "tactic", "id": "b"}]}, nodes - {("tactic", "a")}), [])

    def test_only_file_backed_doctrine_kinds_are_constituents(self) -> None:
        self.assertIn("tactic", validator.MANIFEST_CONSTITUENT_SCHEMAS)
        for exempt in ("preset", "pack-manifest", "pack-descriptor", "mission-type", "mission-step-contract", "graph-shard"):
            self.assertNotIn(exempt, validator.MANIFEST_CONSTITUENT_SCHEMAS)
        self.assertEqual(validator.unlisted_constituents({"constituents": [{"path": "a"}]}, {"a", "b"}), ["b"])

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

    def test_a_file_no_rule_takes_is_unmodelled_as_the_charter_refuses_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # Not Markdown, or Markdown a files rule takes in another letter case (the fallback never sweeps those
            # up): the charter refuses each as `unmodelled` at registration, and built-in packs are never
            # registered, so this gate is the only one that sees them there.
            stray = ["tactics/x.tactic.yml", "tactics/y.tactic.YML", "tactics/x.tactc.yaml", "tactics/plain.yaml",
                     "presets/sub/x.yaml", "notes.txt", "data/table.json", "tactics/.gitkeep", "tactics/z.Tactic.yaml"]
            pack = self.write_pack(root, {name: "id: x\n" for name in stray})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            for name in stray:
                self.assertIn(f"pack/{name}: unmodelled: no file-kinds.yaml rule models this file", output)
            self.assertNotIn("unclassified", output)

    def test_markdown_only_the_ignored_rule_takes_is_not_held_and_fails_outside_the_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            # The charter leaves these out without refusing them and reports file_not_held; this repository
            # allows only README.md orientation notes (charter_service_check.py applies the same NOT_HELD_ALLOWANCES).
            # An orphan skill body is not held: only the body a skill's body_path names is its companion.
            stray = ["docs/notes.md", "x.promt.md", "tactics/GUIDE.MD", "tactics/t.guide.md", "skills/orphan.skill.md",
                     "directives/.draft.md"]
            allowed = ["README.md", "tactics/README.md", "docs/deep/README.md"]
            pack = self.write_pack(root, {name: "# t\n" for name in [*stray, *allowed]})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            for name in stray:
                self.assertIn(f"pack/{name}: not_held: the charter leaves this file out (**/*.md: Author aid, not pack content.)", output)
            for name in allowed:
                self.assertNotIn(f"pack/{name}:", output)

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
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/skills/notes.md: not_held", output)

    def test_expected_code_is_exempt_only_in_an_invalid_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract(root)
            pack = self.write_pack(root, {"expected-code": "composition: a\nregistration: b\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/expected-code: unmodelled", output)
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

    def test_cross_pack_checks_catch_a_missing_preset_id_a_dangling_bare_edge_and_an_id_shared_across_levels(self) -> None:
        def pack(root: Path, name: str, nodes: str, edges: str = "[]", preset: str = "", level: str = "org") -> Path:
            (root / name / "drg").mkdir(parents=True)
            (root / name / "pack.yaml").write_text(f"pack_id: {name}\nname: {name}\npack_level: {level}\n", encoding="utf-8")
            (root / name / "drg" / "fragment.yaml").write_text(f"nodes:\n{nodes}edges: {edges}\n", encoding="utf-8")
            if preset:
                (root / name / "presets").mkdir()
                (root / name / "presets" / "p.yaml").write_text(preset, encoding="utf-8")
            return root / name

        node = "  - {id: D_1, kind: directives}\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = pack(root, "a", node + "  - {id: D_2, kind: directives}\n",
                         "[{source: 'directive:D_1', target: 'directive:D_2', relation: requires}]",
                         "activated_directives:\n  - id: D_1\n")
            self.assertEqual(validator.cross_pack_violations([clean]), [])
            bad = pack(root, "b", "  - {id: D_2, kind: directives}\n", "[{source: 'directive:D_2', target: 'tactic:T_9'}]",
                       "activated_directives:\n  - id: DIRECTIVE_999\n")
            twin = pack(root, "c", node, level="built-in")
            found = "\n".join(validator.cross_pack_violations([clean, bad, twin]))
            for expected in ("'DIRECTIVE_999'", "'tactic:T_9'", "directive:D_1: declared by packs of different levels (a [org], c [built-in])"):
                self.assertIn(expected, found)
            # Artifact files declare ids too, by the kind their schema names (needs the contract).
            contract = validator.Contract(
                files=[validator.Rule(validator.glob_to_regex("**/*.step-contract.yaml"), "**/*.step-contract.yaml",
                                      schema="mission-step-contract")],
                exclusions=[], retired=[], payloads=[],
            )
            filed = pack(root, "e", node, preset="activated_mission_step_contracts:\n  - id: qa-plan\n")
            (filed / "steps").mkdir()
            (filed / "steps" / "qa-plan.step-contract.yaml").write_text("id: qa-plan\n", encoding="utf-8")
            self.assertEqual(validator.cross_pack_violations([filed], contract), [])  # a file-only id satisfies the preset
            self.assertTrue(validator.cross_pack_violations([filed]))  # ...but only when the contract classifies files
            # A file and a node for one id of one pack are a single declaration, not a collision.
            (filed / "steps" / "d1.step-contract.yaml").write_text("id: D_1\n", encoding="utf-8")
            (filed / "drg" / "fragment.yaml").write_text("nodes:\n  - {id: D_1, kind: mission_step_contracts}\nedges: []\n", encoding="utf-8")
            self.assertEqual(validator.cross_pack_violations([filed], contract), [])
            # The right id of the wrong kind does not satisfy a preset: D_1 is a directive in `a`, not a step contract.
            wrong = pack(root, "f", "", preset="activated_mission_step_contracts:\n  - id: D_1\n")
            (wrong / "drg" / "fragment.yaml").write_text("nodes: []\nedges: []\n", encoding="utf-8")
            found = "\n".join(validator.cross_pack_violations([clean, wrong], contract))
            self.assertIn("names 'D_1', which no pack declares as a mission_step_contract", found)
            # A file-only id shared by two packs is a collision.
            other = pack(root, "g", "  - {id: D_3, kind: directives}\n", level="built-in")
            (other / "steps").mkdir()
            (other / "steps" / "qa-plan.step-contract.yaml").write_text("id: qa-plan\n", encoding="utf-8")
            found = "\n".join(validator.cross_pack_violations([filed, other], contract))
            self.assertIn("mission_step_contract:qa-plan: declared by packs of different levels (e [org], g [built-in])", found)
            empty = pack(root, "d", "", "[]")
            (empty / "drg" / "fragment.yaml").write_text("nodes: []\n", encoding="utf-8")
            with self.assertRaises(validator.GateError):  # an empty id index must not pass
                validator.cross_pack_violations([empty])


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
                                   ("agent", "agent-profile"), ("step-contract", "mission-step-contract"),
                                   ("asset", "asset"), ("glossary-pack", "glossary-pack"), ("skill", "skill"),
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

    def test_a_must_have_id_resolves_within_the_presets_closure_and_another_id_anywhere(self) -> None:
        # The charter's requiredNotHeld: a governing preset's must-have item is held by the preset's pack or a
        # pack its depends_on reaches. A plain activation keeps the any-pack check.
        built_in = self.built_in()
        stranger = self.write("stranger", {"pack.yaml": self.descriptor(OTHER, "stranger"),
                                           "tactics/far.tactic.yaml": "id: far\n"})
        preset = ("schema_version: '1.0'\nid: p\nactivated_tactics:\n  - {id: held, must_have: true}\n"
                  "  - {id: own, must_have: true}\n  - {id: far}\n")
        inside = self.consumer(files={"presets/p.yaml": preset})
        self.assertNotIn("must_have", self.found(built_in, stranger, inside))
        outside = self.consumer(files={"presets/p.yaml": preset + "  - {id: far, must_have: true}\n"}, directory="outside")
        found = self.found(built_in, stranger, outside)
        self.assertIn("outside/presets/p.yaml: activated_tactics names 'far' as must_have, but no pack in its "
                      "depends_on closure (outside, built-in) holds it as a tactic", found)
        self.assertEqual(found.count("must_have"), 1)
        # A node of the closure's graph with no file is held by nobody (the charter's RequiredFloor reads held items).
        ghost = self.consumer(files={"presets/p.yaml": "schema_version: '1.0'\nid: p\nactivated_tactics:\n  - {id: ghost, must_have: true}\n",
                                     "drg/fragment.yaml": "nodes:\n  - {id: ghost, kind: tactics}\nedges: []\n"}, directory="ghost")
        self.assertIn("ghost/presets/p.yaml: activated_tactics names 'ghost' as must_have, but no pack in its depends_on closure "
                      "(ghost, built-in) holds it as a tactic", self.found(built_in, ghost))
        orphan = self.consumer(files={"presets/p.yaml": preset}, depends_on=(), directory="orphan")
        self.assertIn("orphan/presets/p.yaml: activated_tactics names 'held' as must_have", self.found(built_in, stranger, orphan))

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

    def test_an_anti_pattern_node_is_held_in_either_graph_document_shape(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "drg/fragment.yaml": "nodes:\n  - {id: in-fragment, kind: anti_patterns}\nedges: []\n",
            "anti_pattern.graph.yaml": "nodes:\n- {urn: 'anti_pattern:in-shard', kind: anti_pattern}\nedges: []\n",
        })
        held = validator.held_artifacts(built_in, self.CONTRACT)
        self.assertLessEqual({("anti_pattern", "in-fragment"), ("anti_pattern", "in-shard")}, held)

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


if __name__ == "__main__":
    unittest.main()
