"""Guards for the release assets core pins by digest (spec-kitty-open-packs#53).

Builds archives from a throwaway git repository through the real entry points.
Stdlib ``unittest`` only. Run it with::

    python3 -m unittest discover -s tests/release
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "release" / "release_assets.py"
_spec = importlib.util.spec_from_file_location("release_assets", _SCRIPT)
release = importlib.util.module_from_spec(_spec)
sys.modules["release_assets"] = release
_spec.loader.exec_module(release)


def _git(repo: Path, *args: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull}
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


class ReleaseAssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        files = {
            "packs/qa/pack.yaml": "name: qa\n",
            "packs/qa/directives/b.yaml": "id: b\n",
            "packs/qa/directives/a.yaml": "id: a\n",
            "packs/qa/assets/gate.sh": "#!/bin/sh\n",
            "packs/built-in/pack.yaml": "name: built-in\n",
            "packs/README.md": "not a pack\n",
        }
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        (self.repo / "packs/qa/assets/gate.sh").chmod(0o755)
        _git(self.repo, "init", "-q")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-qm", "seed")
        _git(self.repo, "tag", "v1.2.3")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_every_pack_directory_is_released(self) -> None:
        self.assertEqual(release.list_packs(self.repo, "v1.2.3"), ["built-in", "qa"])
        self._add_gitlink("packs/vendored")  # a pack that is not a directory must fail, not vanish
        with self.assertRaisesRegex(release.ReleaseError, "packs/vendored is a commit"):
            release.list_packs(self.repo, "HEAD")

    def _add_gitlink(self, path: str) -> None:
        head = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        _git(self.repo, "update-index", "--add", "--cacheinfo", f"160000,{head},{path}")
        _git(self.repo, "commit", "-qm", f"gitlink {path}")

    def test_archive_is_reproducible(self) -> None:
        first = release.build_archive(self.repo, "v1.2.3", "qa")
        os.utime(self.repo / "packs/qa/pack.yaml", (0, 0))  # working-tree state must not matter
        self.assertEqual(first, release.build_archive(self.repo, "v1.2.3", "qa"))

    def test_archive_equals_the_tagged_subtree(self) -> None:
        (self.repo / "packs/qa/untracked.yaml").write_text("stray\n")
        (self.repo / "packs/qa/pack.yaml").write_text("modified after the tag\n")
        with tarfile.open(fileobj=io.BytesIO(release.build_archive(self.repo, "v1.2.3", "qa"))) as tar:
            members = tar.getmembers()
            self.assertEqual(
                [m.name for m in members],
                ["qa/assets/gate.sh", "qa/directives/a.yaml", "qa/directives/b.yaml", "qa/pack.yaml"],
            )
            self.assertTrue(all(m.isfile() and m.uid == 0 and m.uname == "" for m in members))
            self.assertEqual(members[0].mode, 0o755)
            self.assertEqual(tar.extractfile("qa/pack.yaml").read(), b"name: qa\n")

    def test_symlink_or_submodule_in_a_pack_fails(self) -> None:
        os.symlink("pack.yaml", self.repo / "packs/qa/link.yaml")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-qm", "link")
        with self.assertRaisesRegex(release.ReleaseError, "packs/qa/link.yaml"):
            release.build_archive(self.repo, "HEAD", "qa")
        self._add_gitlink("packs/built-in/vendor")
        with self.assertRaisesRegex(release.ReleaseError, "packs/built-in/vendor is a commit"):
            release.build_archive(self.repo, "HEAD", "built-in")

    def test_sha256_file_matches_its_archive(self) -> None:
        out = self.repo / "dist"
        release.write_assets(self.repo, "v1.2.3", "v1.2.3", out)
        digest, name = (out / "qa-v1.2.3.tar.gz.sha256").read_text().split()
        self.assertEqual(name, "qa-v1.2.3.tar.gz")
        self.assertEqual(digest, hashlib.sha256((out / name).read_bytes()).hexdigest())

    def test_changelog_section_is_extracted(self) -> None:
        changelog = ("# Changelog\n\n## [Unreleased]\n\n## [1.2.3] - 2026-10-20\n\n- Shipped, see [ADR].\n\n"
                     "[ADR]: docs/adr.md\n\n## [1.2.2]\n\n- Old.\n\n[1.2.3]: https://example.test/v1.2.3\n")
        self.assertEqual(release.changelog_section(changelog, "1.2.3"), "- Shipped, see [ADR].\n\n[ADR]: docs/adr.md\n")
        self.assertEqual(release.changelog_section(changelog, "1.2.2"), "- Old.\n")

    def test_missing_changelog_section_fails(self) -> None:
        with self.assertRaisesRegex(release.ReleaseError, r"no '## \[1.2.3\]'"):
            release.changelog_section("# Changelog\n\n## [Unreleased]\n\n- Pending.\n", "1.2.3")
        with self.assertRaisesRegex(release.ReleaseError, "is empty"):
            release.changelog_section("## [1.2.3] - 2026-10-20\n\n## [1.2.2]\n\n- Old.\n", "1.2.3")

    def test_tag_must_be_semver(self) -> None:
        for tag in ("1.2.3", "v1.2", "v01.2.3", "v1.2.3-rc1"):
            with self.assertRaises(release.ReleaseError, msg=tag):
                release.version_of(tag)


if __name__ == "__main__":
    unittest.main()
