"""The pack digest recipe, discovery, fail-closed check and text-preserving update (#194)."""

from __future__ import annotations

import contextlib
import hashlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts" / "ci"
sys.path.insert(0, str(SCRIPTS))

import pack_digest as pd  # noqa: E402

sys.path.insert(0, str(SCRIPTS.parent / "release"))

BUILT_IN_DIGEST = "ad841252089ca5cdc5da33d7a027fb34386a80fe64249c1e368e61162dea38ca"
FIXTURE = {"a.txt": b"x", "sub/b.txt": b"yz", "pack-manifest.yaml": b"m"}


def write_tree(root: Path, files: dict[str, bytes]) -> None:
    for rel, data in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def reference_digest(files: dict[str, bytes]) -> str:
    """The recipe written out independently: sorted POSIX paths, length-prefixed, manifest skipped."""
    digest = hashlib.sha256()
    for rel in sorted(files):
        if rel == "pack-manifest.yaml":
            continue
        name = rel.encode()
        digest.update(len(name).to_bytes(8, "big") + name)
        digest.update(len(files[rel]).to_bytes(8, "big") + files[rel])
    return digest.hexdigest()


def git_track(root: Path) -> None:
    """Make ``root`` a git work tree with everything in it tracked (the index is enough)."""
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "add", "-A", "-f"], check=True, capture_output=True)


def run(func, *args) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = func(*args)
    return code, out.getvalue()


class RecipeTests(unittest.TestCase):
    def test_vector_matches_independent_recipe_and_pinned_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(Path(tmp), FIXTURE)
            git_track(Path(tmp))
            actual = pd.snapshot_sha256(Path(tmp))
        self.assertEqual(actual, reference_digest(FIXTURE))
        self.assertEqual(actual, "825dfc8804c11988e9ad4c33e6565fa284d1e280d5d5db5830f59e0d8d4a43c9")

    def test_only_the_root_manifest_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(root, FIXTURE)
            git_track(root)
            base = pd.snapshot_sha256(root)
            (root / "pack-manifest.yaml").write_bytes(b"changed")
            self.assertEqual(pd.snapshot_sha256(root), base)
            write_tree(root, {"sub/pack-manifest.yaml": b"nested"})
            git_track(root)
            self.assertNotEqual(pd.snapshot_sha256(root), base)

    def test_symlink_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(root, FIXTURE)
            try:
                (root / "link").symlink_to(root / "a.txt")
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unsupported")
            git_track(root)
            with self.assertRaises(OSError):
                pd.snapshot_sha256(root)

    def test_real_tree_parity_with_core_pin(self) -> None:
        recorded = pd.recorded_digest(pd.PACKS / "built-in.source.yaml")
        self.assertEqual(pd.snapshot_sha256(pd.PACKS / "built-in"), recorded)
        self.assertEqual(recorded, BUILT_IN_DIGEST)


class TrackedOnlyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        write_tree(self.root, {"pack.yaml": b"id: p\n", "a.md": b"a"})
        git_track(self.root)
        self.base = pd.snapshot_sha256(self.root)

    def test_untracked_and_ignored_files_do_not_change_the_digest(self) -> None:
        write_tree(self.root, {"__pycache__/x.pyc": b"junk", "new.md": b"untracked", ".gitignore": b"*.log\n", "x.log": b"i"})
        self.assertEqual(pd.snapshot_sha256(self.root), self.base)

    def test_modified_tracked_file_is_hashed_from_disk(self) -> None:
        (self.root / "a.md").write_bytes(b"changed")
        self.assertNotEqual(pd.snapshot_sha256(self.root), self.base)

    def test_staged_new_file_counts(self) -> None:
        write_tree(self.root, {"new.md": b"n"})
        subprocess.run(["git", "-C", str(self.root), "add", "new.md"], check=True)
        self.assertNotEqual(pd.snapshot_sha256(self.root), self.base)

    def test_outside_a_git_work_tree_refuses_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            write_tree(Path(tmp), {"a": b"x"})
            with self.assertRaisesRegex(OSError, "not inside a git work tree"):
                pd.snapshot_sha256(Path(tmp))

    def test_lister_is_injectable(self) -> None:
        self.assertEqual(pd.snapshot_sha256(self.root, lambda _root: ["a.md", "pack.yaml"]), self.base)


class ReleaseAgreesTests(unittest.TestCase):
    def test_release_and_gate_both_ignore_a_directory_without_pack_yaml(self) -> None:
        import release_assets as release

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(root, {"packs/p1/pack.yaml": b"a", "packs/scratch/notes.md": b"n"})
            git_track(root)
            env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                   "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "seed"], check=True, capture_output=True, env=env)
            self.assertEqual(release.list_packs(root, "HEAD"), ["p1"])
            self.assertEqual([d.name for d in pd.discover_packs(root / "packs")], ["p1"])

    def test_the_sidecar_suffix_is_shared(self) -> None:
        import release_assets as release

        self.assertEqual(pd.SIDECAR_SUFFIX, release.SIDECAR_SUFFIX)


class DiscoveryTests(unittest.TestCase):
    def test_discovery_and_orphans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            packs = Path(tmp) / "packs"
            write_tree(packs, {"p1/pack.yaml": b"a", "p2/x.md": b"b", "README.md": b"r",
                               "p1.source.yaml": b"", "ghost.source.yaml": b""})
            self.assertEqual([d.name for d in pd.discover_packs(packs)], ["p1"])
            self.assertEqual([p.name for p in pd.orphan_sidecars(packs)], ["ghost.source.yaml"])

    def test_real_tree_discovery_is_complete(self) -> None:
        expected = sorted(p.parent.name for p in pd.PACKS.glob("*/pack.yaml"))
        found = [d.name for d in pd.discover_packs(pd.PACKS)]
        self.assertEqual(found, expected)
        self.assertGreater(len(found), 1)
        for pack in pd.discover_packs(pd.PACKS):
            self.assertRegex(pd.snapshot_sha256(pack), r"^[0-9a-f]{64}$")


class PackFixture(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.packs = Path(self._tmp.name) / "packs"
        write_tree(self.packs, {"p1/pack.yaml": b"id: p1\n", "p1/doc.md": b"doc\n"})
        git_track(Path(self._tmp.name))
        self.pack = self.packs / "p1"
        self.sidecar = self.packs / "p1.source.yaml"

    def stamp(self, value: str | None = None, extra: str = "") -> str:
        value = value or pd.snapshot_sha256(self.pack)
        self.sidecar.write_text(
            f"# comment\n{extra}tree_digest:\n  algorithm: {pd.ALGORITHM}\n  value: {value}\n", encoding="utf-8")
        return value


class CheckTests(PackFixture):
    def test_fresh_then_stale(self) -> None:
        value = self.stamp()
        code, out = run(pd.check, self.packs, None)
        self.assertEqual((code, out), (0, f"ok: packs/p1/ digest matches {value}\n"))
        (self.pack / "doc.md").write_bytes(b"doc!\n")
        code, out = run(pd.check, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/p1.source.yaml::packs/p1/ digest", out)
        self.assertIn("run `python3 scripts/ci/pack_digest.py --update p1`", out)

    def test_missing_sidecar(self) -> None:
        code, out = run(pd.check, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("packs/p1/ has no recorded digest", out)
        self.stamp()
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)

    def test_malformed_sidecars_report_without_traceback(self) -> None:
        good = pd.snapshot_sha256(self.pack)
        bad = {
            "algorithm": f"tree_digest:\n  algorithm: md5\n  value: {good}\n".encode(),
            "non-hex": f"tree_digest:\n  algorithm: {pd.ALGORITHM}\n  value: ZZ\n".encode(),
            "not-a-mapping": b"- a\n- b\n",
            "invalid-yaml": b"tree_digest: [unclosed\n",
            "non-utf8": b"\xff\xfe\x00bad",
        }
        for label, content in bad.items():
            with self.subTest(label):
                self.sidecar.write_bytes(content)
                code, out = run(pd.check, self.packs, None)
                self.assertEqual(code, 1)
                self.assertIn("::error file=packs/p1.source.yaml::", out)
        self.stamp()
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)

    def test_orphan_fails_all_pack_check_only(self) -> None:
        self.stamp()
        (self.packs / "ghost.source.yaml").write_text("x: 1\n", encoding="utf-8")
        code, out = run(pd.check, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("no pack directory packs/ghost/ for this sidecar; delete it", out)
        self.assertEqual(run(pd.check, self.packs, ["p1"])[0], 0)

    def test_every_failing_pack_is_reported(self) -> None:
        write_tree(self.packs, {"p2/pack.yaml": b"id: p2\n"})
        git_track(Path(self._tmp.name))
        code, out = run(pd.check, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("packs/p1.source.yaml", out)
        self.assertIn("packs/p2.source.yaml", out)

    def test_no_pack_is_not_vacuous(self) -> None:
        empty = Path(self._tmp.name) / "empty" / "packs"
        empty.mkdir(parents=True)
        (empty / "p").mkdir()
        for func in (pd.check, pd.update):
            code, out = run(func, empty, None)
            self.assertEqual(code, 1)
            self.assertIn("no pack found", out)

    def test_unknown_pack_is_a_usage_error(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run(pd.check, self.packs, ["nope"])[0], 2)


class UpdateTests(PackFixture):
    def test_stale_rewrites_only_the_value_line(self) -> None:
        self.stamp("a" * 64, extra="seeded_from:\n  commit: abc\n  value: keep\n")
        before = self.sidecar.read_text(encoding="utf-8").split("\n")
        code, out = run(pd.update, self.packs, None)
        self.assertEqual((code, out), (0, "updated: packs/p1.source.yaml\n"))
        after = self.sidecar.read_text(encoding="utf-8").split("\n")
        changed = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
        self.assertEqual(len(before), len(after))
        self.assertEqual(len(changed), 1)
        self.assertEqual(after[changed[0]], f"  value: {pd.snapshot_sha256(self.pack)}")
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)

    def test_missing_is_created_from_template_and_second_run_is_a_noop(self) -> None:
        code, out = run(pd.update, self.packs, None)
        self.assertEqual((code, out), (0, "created: packs/p1.source.yaml\n"))
        text = self.sidecar.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Recorded tree digest of packs/p1/"))
        self.assertTrue(text.endswith("\n"))
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)
        os.utime(self.sidecar, (1, 1))
        self.assertEqual(run(pd.update, self.packs, None), (0, ""))
        self.assertEqual(self.sidecar.read_text(encoding="utf-8"), text)
        self.assertEqual(self.sidecar.stat().st_mtime, 1)
        write_tree(self.packs, {"p2/pack.yaml": b"id: p2\n"})  # never git-added: no tracked files
        code, out = run(pd.update, self.packs, ["p2"])
        self.assertEqual(code, 1)
        self.assertIn("no git-tracked files; `git add` the pack first", out)
        self.assertFalse((self.packs / "p2.source.yaml").exists())

    def test_malformed_is_untouched_and_refused(self) -> None:
        self.sidecar.write_bytes(b"tree_digest: [unclosed\n")
        code, out = run(pd.update, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/p1.source.yaml::", out)
        self.assertEqual(self.sidecar.read_bytes(), b"tree_digest: [unclosed\n")

    def test_quoted_stale_value_is_refused_untouched(self) -> None:
        text = f"tree_digest:\n  algorithm: {pd.ALGORITHM}\n  value: '{'a' * 64}'\n"
        self.sidecar.write_text(text, encoding="utf-8")
        code, out = run(pd.update, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/p1.source.yaml::", out)
        self.assertEqual(self.sidecar.read_text(encoding="utf-8"), text)

    def test_other_value_keys_are_not_touched(self) -> None:
        text = (f"seeded_from:\n  value: {'1' * 64}\ntree_digest:\n  algorithm: {pd.ALGORITHM}\n"
                f"  value: {'a' * 64}\nlater:\n  value: {'2' * 64}\n")
        self.sidecar.write_text(text, encoding="utf-8")
        self.assertEqual(run(pd.update, self.packs, None)[0], 0)
        out = self.sidecar.read_text(encoding="utf-8")
        self.assertIn(f"seeded_from:\n  value: {'1' * 64}\n", out)
        self.assertIn(f"later:\n  value: {'2' * 64}\n", out)
        self.assertIn(pd.snapshot_sha256(self.pack), out)

    def test_orphan_is_warned_not_deleted(self) -> None:
        ghost = self.packs / "ghost.source.yaml"
        ghost.write_text("x: 1\n", encoding="utf-8")
        code, out = run(pd.update, self.packs, None)
        self.assertEqual(code, 0)
        self.assertIn("::warning file=packs/ghost.source.yaml::", out)
        self.assertTrue(ghost.is_file())


class ShimTests(unittest.TestCase):
    def run_shim(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPTS / "built_in_digest.py"), *args],
                              capture_output=True, text=True, check=False)

    def test_no_args_prints_only_the_digest(self) -> None:
        result = self.run_shim()
        self.assertEqual((result.returncode, result.stdout), (0, BUILT_IN_DIGEST + "\n"))

    def test_check_passes_on_the_real_tree(self) -> None:
        result = self.run_shim("--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ok: packs/built-in/", result.stdout)


    def test_help_and_unknown_flags_behave_like_main(self) -> None:
        helped = self.run_shim("--help")
        self.assertEqual(helped.returncode, 0)
        self.assertIn("--check", helped.stdout)
        self.assertNotIn(BUILT_IN_DIGEST, helped.stdout)
        bad = self.run_shim("--bogus")
        self.assertEqual((bad.returncode, bad.stdout), (2, ""))
        self.assertIn("unrecognized arguments: --bogus", bad.stderr)


class SymlinkAndNewlineTests(PackFixture):
    def link(self) -> None:
        try:
            os.symlink("doc.md", self.pack / "link.md")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unsupported")
        git_track(Path(self._tmp.name))

    def test_symlink_in_pack_is_an_error_line_not_a_traceback(self) -> None:
        self.stamp()
        self.link()
        code, out = run(pd.check, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/p1::packs/p1/ cannot be hashed", out)
        self.assertIn("unsupported symlink: link.md", out)
        code, out = run(pd.update, self.packs, None)
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/p1::", out)
        (self.pack / "link.md").unlink()
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)

    def test_crlf_sidecar_keeps_its_line_endings(self) -> None:
        self.stamp("a" * 64)
        crlf = self.sidecar.read_bytes().replace(b"\n", b"\r\n")
        self.sidecar.write_bytes(crlf)
        self.assertEqual(run(pd.update, self.packs, None)[0], 0)
        after = self.sidecar.read_bytes()
        self.assertEqual(after, crlf.replace(b"a" * 64, pd.snapshot_sha256(self.pack).encode()))
        self.assertNotIn(b"\n", after.replace(b"\r\n", b""))
        self.assertEqual(run(pd.check, self.packs, None)[0], 0)


class CliTests(unittest.TestCase):
    def test_print_mode_lists_digest_and_pack(self) -> None:
        out = subprocess.run([sys.executable, str(SCRIPTS / "pack_digest.py"), "built-in"],
                             capture_output=True, text=True, check=False)
        self.assertEqual((out.returncode, out.stdout), (0, f"{BUILT_IN_DIGEST}  packs/built-in\n"))

    def test_unknown_pack_exits_2(self) -> None:
        out = subprocess.run([sys.executable, str(SCRIPTS / "pack_digest.py"), "nope"],
                             capture_output=True, text=True, check=False)
        self.assertEqual(out.returncode, 2)


if __name__ == "__main__":
    unittest.main()
