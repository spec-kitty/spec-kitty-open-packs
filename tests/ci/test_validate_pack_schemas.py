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
    "*/pack.md": "pack-doc",  # the one markdown rule
    "**/*.asset.yaml": "asset",
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
        schemas = {"preset": OPEN_SCHEMA, "pack-manifest": MANIFEST_SCHEMA, "tactic": OPEN_SCHEMA, "pack-doc": OPEN_SCHEMA, "pack-descriptor": OPEN_SCHEMA, "asset": OPEN_SCHEMA}
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
        held = {"assets/kept/held.txt": "x\n", "assets/t.tactic.yaml": "id: t2\n", "beside.txt": "x\n", "templates/held.md": "# t\n"}
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
            stray = ["tactics/x.tactic.yml", "tactics/y.tactic.YML", "tactics/x.tactc.yaml", "tactics/plain.yaml", "presets/sub/x.yaml", "x.promt.md"]
            allowed = ["README.md", "PROVENANCE.md", "skills/s.skill.md", "tactics/README.md"]
            pack = self.write_pack(root, {name: "id: x\n" for name in [*stray, *allowed]})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            for name in stray:
                self.assertIn(f"pack/{name}: unclassified", output)
            for name in allowed:
                self.assertNotIn(f"pack/{name}:", output)

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
            pack = self.write_pack(root, {"pack.md": "# Title\n", "presets/p.yaml": "id: q\n"})
            code, output = self.run_validator(root, str(pack))
            self.assertEqual(code, validator.EXIT_INVALID)
            self.assertIn("pack/pack.yaml: missing: a pack with a pack.md or a pack-manifest.yaml needs its descriptor", output)
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

    def test_cross_pack_checks_catch_a_missing_preset_id_a_dangling_edge_and_a_shared_id(self) -> None:
        def pack(root: Path, name: str, nodes: str, edges: str = "[]", preset: str = "") -> Path:
            (root / name / "drg").mkdir(parents=True)
            (root / name / "pack.yaml").write_text(f"pack_id: {name}\nname: {name}\n", encoding="utf-8")
            (root / name / "drg" / "fragment.yaml").write_text(f"nodes:\n{nodes}edges: {edges}\n", encoding="utf-8")
            if preset:
                (root / name / "presets").mkdir()
                (root / name / "presets" / "p.yaml").write_text(preset, encoding="utf-8")
            return root / name

        node = "  - {id: D_1, kind: directives}\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = pack(root, "a", node, "[{source: 'directive:D_1', target: 'directive:D_1', relation: requires}]",
                         "activated_directives:\n  - id: D_1\n")
            self.assertEqual(validator.cross_pack_violations([clean]), [])
            bad = pack(root, "b", "  - {id: D_2, kind: directives}\n", "[{source: 'directive:D_2', target: 'tactic:T_9'}]",
                       "activated_directives:\n  - id: DIRECTIVE_999\n")
            twin = pack(root, "c", node)
            found = "\n".join(validator.cross_pack_violations([clean, bad, twin]))
            for expected in ("'DIRECTIVE_999'", "'tactic:T_9'", "directive:D_1: declared by more than one pack (a, c)"):
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
            other = pack(root, "g", "  - {id: D_3, kind: directives}\n")
            (other / "steps").mkdir()
            (other / "steps" / "qa-plan.step-contract.yaml").write_text("id: qa-plan\n", encoding="utf-8")
            found = "\n".join(validator.cross_pack_violations([filed, other], contract))
            self.assertIn("mission_step_contract:qa-plan: declared by more than one pack (e, g)", found)
            empty = pack(root, "d", "", "[]")
            (empty / "drg" / "fragment.yaml").write_text("nodes: []\n", encoding="utf-8")
            with self.assertRaises(validator.GateError):  # an empty id index must not pass
                validator.cross_pack_violations([empty])


BUILT_IN = "01ARWG13C000000000000000FG"
OTHER = "01ARWG13C000000000000000XX"
CONSUMER = "01ARWG13C000000000000000YY"


class CompositionChecks(unittest.TestCase):
    """The strict composition rules the charter service enforces, caught here under ``--cross-pack``."""

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

    def descriptor(self, pack_id: str, name: str, depends_on: tuple[str, ...] = ()) -> str:
        entries = "".join(f"- {{pack_id: {dep}, range: '>=1.0,<2'}}\n" for dep in depends_on)
        return f"pack_id: {pack_id}\nname: {name}\n" + (f"depends_on:\n{entries}" if entries else "")

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

    def test_a_qualified_edge_resolves_in_the_named_pack_and_a_missing_target_is_named(self) -> None:
        built_in = self.built_in()
        self.assertEqual(self.found(built_in, self.consumer(self.edge("built-in::tactic:held"))), "")
        found = self.found(built_in, self.consumer(self.edge("built-in::tactic:gone")))
        self.assertIn("consumer/drg/fragment.yaml", found)
        self.assertIn("built-in::tactic:gone", found)

    def test_the_older_cross_pack_checks_still_fire_beside_a_correct_qualified_edge(self) -> None:
        built_in = self.built_in()
        correct = self.consumer(self.edge("built-in::tactic:held"))
        self.assertEqual(self.found(built_in, correct), "")
        twin = self.write("twin", {"pack.yaml": self.descriptor(OTHER, "twin"), "tactics/held.tactic.yaml": "id: held\n"})
        self.assertIn("tactic:held: declared by more than one pack (built-in, twin)", self.found(built_in, correct, twin))
        dangling = self.consumer("[{source: 'tactic:own', target: 'tactic:held'}, {source: 'tactic:own', target: 'tactic:nowhere'}]")
        self.assertIn("edge target 'tactic:nowhere' resolves to no node of any pack", self.found(built_in, dangling))

    def test_a_qualifier_names_the_descriptor_name_not_the_directory(self) -> None:
        renamed = self.built_in(directory="qa", name="quality-assurance")
        self.assertEqual(self.found(renamed, self.consumer(self.edge("quality-assurance::tactic:held"))), "")
        self.assertIn("qa::tactic:held", self.found(renamed, self.consumer(self.edge("qa::tactic:held"))))

    def test_a_bare_edge_end_held_only_by_another_pack_fails_and_its_own_and_action_targets_pass(self) -> None:
        built_in = self.built_in()
        passing = "[{source: 'tactic:own', target: 'tactic:own'}, {source: 'action:dev/plan', target: 'tactic:own'}]"
        self.assertEqual(self.found(built_in, self.consumer(passing)), "")
        for end in ("target: 'tactic:held', source: 'tactic:own'", "source: 'tactic:held', target: 'tactic:own'"):
            with self.subTest(end=end):
                found = self.found(built_in, self.consumer(f"[{{{end}}}]"))
                self.assertIn("consumer/drg/fragment.yaml: bare reference 'tactic:held' is held only by built-in", found)

    def test_an_edge_of_a_root_graph_document_is_read_like_a_fragment_edge(self) -> None:
        built_in = self.built_in()
        shard = "edges:\n- {source: 'tactic:own', target: '%s', relation: requires}\n"
        self.assertEqual(self.found(built_in, self.consumer(files={"tactic.graph.yaml": shard % "built-in::tactic:held"})), "")
        found = self.found(built_in, self.consumer(files={"tactic.graph.yaml": shard % "tactic:held"}))
        self.assertIn("consumer/tactic.graph.yaml: bare reference 'tactic:held'", found)

    def test_a_qualifier_outside_the_depends_on_closure_fails_and_a_transitive_one_passes(self) -> None:
        built_in = self.built_in()
        between = self.write("between", {"pack.yaml": self.descriptor(OTHER, "between", (BUILT_IN,)), "tactics/b.tactic.yaml": "id: b\n"})
        through = self.consumer(self.edge("built-in::tactic:held"), depends_on=(OTHER,))
        self.assertEqual(self.found(built_in, between, through), "")
        for label, depends_on, reference in (
            ("not declared", (), "built-in::tactic:held"),
            ("no such pack", (BUILT_IN,), "nowhere::tactic:held"),
        ):
            with self.subTest(label):
                found = self.found(built_in, between, self.consumer(self.edge(reference), depends_on=depends_on))
                self.assertIn(f"consumer/drg/fragment.yaml: reference '{reference}'", found)
                self.assertIn("outside this pack's depends_on closure", found)

    def test_a_qualified_target_must_be_held_by_the_named_pack_not_merely_by_some_pack(self) -> None:
        built_in = self.built_in()
        sibling = self.write("sibling", {"pack.yaml": self.descriptor(OTHER, "sibling"), "tactics/s.tactic.yaml": "id: s\n"})
        both = (BUILT_IN, OTHER)
        self.assertEqual(self.found(built_in, sibling, self.consumer(self.edge("sibling::tactic:s"), depends_on=both)), "")
        found = self.found(built_in, sibling, self.consumer(self.edge("built-in::tactic:s"), depends_on=both))
        self.assertIn("consumer/drg/fragment.yaml: reference 'built-in::tactic:s': built-in does not hold 'tactic:s'", found)
        kindless = self.found(built_in, sibling, self.consumer(self.edge("built-in::gone"), depends_on=both))
        self.assertIn("reference 'built-in::", kindless)  # the retired typed form, with no kind, resolves to nothing

    def test_a_qualified_action_needs_the_closure_but_no_held_artifact(self) -> None:
        built_in = self.built_in()
        self.assertEqual(self.found(built_in, self.consumer("[{source: 'built-in::action:dev/plan', target: 'tactic:own'}]")), "")
        found = self.found(built_in, self.consumer("[{source: 'built-in::action:dev/plan', target: 'tactic:own'}]", depends_on=()))
        self.assertIn("outside this pack's depends_on closure", found)

    def test_a_pack_directory_with_no_descriptor_fails(self) -> None:
        built_in = self.built_in()
        self.assertEqual(self.found(built_in), "")
        (built_in / "pack.yaml").unlink()
        self.assertIn("built-in/pack.yaml: missing", self.found(built_in))

    def test_two_packs_sharing_a_pack_id_or_a_name_fail(self) -> None:
        built_in = self.built_in()
        self.assertEqual(self.found(built_in, self.write("other", {"pack.yaml": self.descriptor(OTHER, "other")})), "")
        same_id = self.write("same-id", {"pack.yaml": self.descriptor(BUILT_IN, "same-id")})
        self.assertIn(f"built-in/pack.yaml, same-id/pack.yaml: pack_id '{BUILT_IN}' is declared by more than one pack", self.found(built_in, same_id))
        same_name = self.write("same-name", {"pack.yaml": self.descriptor(OTHER, "built-in")})
        self.assertIn("built-in/pack.yaml, same-name/pack.yaml: name 'built-in' is declared by more than one pack", self.found(built_in, same_name))

    def test_a_node_with_no_file_is_held_by_nobody(self) -> None:
        graph = "nodes:\n- {urn: 'procedure:shard-node', kind: procedure}\nedges: []\n"
        fragment = "nodes:\n  - {id: node-tactic, kind: tactics}\nedges: []\n"
        built_in = self.built_in()
        self.write("built-in", {"drg/fragment.yaml": fragment, "procedure.graph.yaml": graph})
        self.assertEqual(self.found(built_in, self.consumer(self.edge("built-in::tactic:held"))), "")  # same fixture, a file
        self.assertEqual(self.found(built_in, self.consumer(self.edge("tactic:node-tactic"))), "")
        self.assertEqual(self.found(built_in, self.consumer(self.edge("procedure:shard-node"))), "")
        for urn in ("tactic:node-tactic", "procedure:shard-node"):
            with self.subTest(urn):
                found = self.found(built_in, self.consumer(self.edge(f"built-in::{urn}")))
                self.assertIn(f"reference 'built-in::{urn}': built-in does not hold '{urn}'", found)

    def test_files_no_node_names_are_held_under_the_id_the_charter_reads(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "agent_profiles/p.agent.yaml": "profile-id: file-profile\n",
            "missions/doc/doc.mission-type.yaml": "id: doc\n",
            "templates/writing/top.md": "# t\n",
            "missions/doc/templates/in-mission.md": "# t\n",
        })
        for urn in ("agent_profile:file-profile", "mission_type:doc", "template:writing/top.md", "template:doc/in-mission.md"):
            with self.subTest(urn):
                self.assertEqual(self.found(built_in, self.consumer(self.edge(f"built-in::{urn}"))), "")
                self.assertIn(f"bare reference '{urn}' is held only by built-in", self.found(built_in, self.consumer(self.edge(urn))))

    def test_a_template_elsewhere_in_a_pack_is_not_held(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {"templates/held.md": "# t\n", "elsewhere/templates/stray.md": "# t\n"})
        self.assertEqual(self.found(built_in, self.consumer(self.edge("built-in::template:held.md"))), "")
        self.assertIn("built-in does not hold 'template:stray.md'", self.found(built_in, self.consumer(self.edge("built-in::template:stray.md"))))

    def test_an_anti_pattern_node_is_held_in_either_graph_document_shape(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {
            "drg/fragment.yaml": "nodes:\n  - {id: in-fragment, kind: anti_patterns}\nedges: []\n",
            "anti_pattern.graph.yaml": "nodes:\n- {urn: 'anti_pattern:in-shard', kind: anti_pattern}\nedges: []\n",
        })
        for urn in ("anti_pattern:in-fragment", "anti_pattern:in-shard"):
            with self.subTest(urn):
                self.assertEqual(self.found(built_in, self.consumer(self.edge(f"built-in::{urn}"))), "")
                self.assertIn(f"bare reference '{urn}'", self.found(built_in, self.consumer(self.edge(urn))))

    def test_a_template_directory_holds_only_what_the_contract_classifies_as_a_payload(self) -> None:
        built_in = self.built_in()
        self.write("built-in", {"templates/filed.tactic.yaml": "id: filed\n", "templates/held.md": "# t\n"})
        self.assertEqual(self.found(built_in, self.consumer(self.edge("built-in::tactic:filed"))), "")
        self.assertEqual(self.found(built_in, self.consumer(self.edge("built-in::template:held.md"))), "")
        found = self.found(built_in, self.consumer(self.edge("built-in::template:filed.tactic.yaml")))
        self.assertIn("built-in does not hold 'template:filed.tactic.yaml'", found)

    def test_a_pack_may_qualify_a_reference_with_its_own_name(self) -> None:
        built_in = self.built_in()
        files = {"tactics/second.tactic.yaml": "id: second\n"}
        self.assertEqual(self.found(built_in, self.consumer("[{source: 'tactic:second', target: 'consumer::tactic:own'}]", files=files)), "")
        found = self.found(built_in, self.consumer("[{source: 'tactic:second', target: 'consumer::tactic:gone'}]", files=files))
        self.assertIn("reference 'consumer::tactic:gone': consumer does not hold 'tactic:gone'", found)


if __name__ == "__main__":
    unittest.main()
