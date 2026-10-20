#!/usr/bin/env python3
"""Build the release assets for a ``vX.Y.Z`` tag (spec-kitty-open-packs#53).

For every pack directory under ``packs/`` this writes ``<pack>-vX.Y.Z.tar.gz`` and
``<pack>-vX.Y.Z.tar.gz.sha256``, and it writes the release notes taken from the
matching ``CHANGELOG.md`` section. Core pins a release by these archive digests,
so the archives must be reproducible:

- the content is read from the git tree of the tagged commit, never from the
  working tree, so untracked or modified files cannot leak in;
- entries are sorted, owner/group are blank with uid/gid 0, the mode is 0644 or
  0755, every mtime is the tagged commit's committer time, and there are no
  directory entries;
- the gzip header has no filename and mtime 0.

A symlink or submodule inside a pack fails the build: the archive must equal the
``packs/<pack>`` subtree, and neither has a portable byte form.

Stdlib only. Usage (from the repository root)::

    scripts/release/release_assets.py build vX.Y.Z --out dist
    scripts/release/release_assets.py notes vX.Y.Z > notes.md
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import re
import subprocess
import sys
import tarfile
from pathlib import Path

TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PACKS_DIR = "packs"


class ReleaseError(Exception):
    pass


def version_of(tag: str) -> str:
    if not TAG_RE.match(tag):
        raise ReleaseError(f"{tag!r} is not a vX.Y.Z release tag")
    return tag[1:]


def _git(repo: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout


def list_packs(repo: Path, rev: str) -> list[str]:
    """Every directory directly under ``packs/`` at ``rev``."""
    out = _git(repo, "ls-tree", "-z", f"{rev}:{PACKS_DIR}")
    packs = []
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, name = entry.split(b"\t", 1)
        kind = meta.split()[1]
        if kind == b"tree":
            packs.append(name.decode())
        elif kind != b"blob":
            raise ReleaseError(f"{PACKS_DIR}/{name.decode()} is a {kind.decode()}; a pack must be a directory")
    return sorted(packs)


def _pack_blobs(repo: Path, rev: str, pack: str) -> list[tuple[str, int, str]]:
    """``(path inside the pack, mode, blob sha)`` for every file, sorted by path."""
    prefix = f"{PACKS_DIR}/{pack}/"
    # List the pack's tree object, so the paths come back relative to the pack.
    out = _git(repo, "ls-tree", "-r", "-z", "--full-tree", f"{rev}:{PACKS_DIR}/{pack}")
    blobs = []
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, path = entry.decode().split("\t", 1)
        mode, kind, sha = meta.split()
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ReleaseError(f"{prefix}{path} is a {kind} with mode {mode}; a pack may hold only regular files")
        blobs.append((path, 0o755 if mode == "100755" else 0o644, sha))
    if not blobs:
        raise ReleaseError(f"{prefix} has no files at {rev}")
    return sorted(blobs)


def _read_blobs(repo: Path, shas: list[str]) -> dict[str, bytes]:
    proc = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input="".join(f"{sha}\n" for sha in shas).encode(),
        check=True,
        capture_output=True,
    )
    data, pos, blobs = proc.stdout, 0, {}
    for sha in shas:
        header_end = data.index(b"\n", pos)
        header = data[pos:header_end].split()
        if len(header) != 3 or header[0].decode() != sha or header[1] != b"blob":
            raise ReleaseError(f"git cat-file returned {data[pos:header_end]!r} for blob {sha}")
        size = header[2]
        start = header_end + 1
        blobs[sha] = data[start:start + int(size)]
        pos = start + int(size) + 1
    return blobs


def build_archive(repo: Path, rev: str, pack: str) -> bytes:
    """The deterministic ``.tar.gz`` of ``packs/<pack>`` at ``rev``, rooted at ``<pack>/``."""
    mtime = int(_git(repo, "log", "-1", "--format=%ct", rev).strip())
    files = _pack_blobs(repo, rev, pack)
    contents = _read_blobs(repo, [sha for _, _, sha in files])

    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.GNU_FORMAT) as tar:
        for path, mode, sha in files:
            info = tarfile.TarInfo(f"{pack}/{path}")
            info.size, info.mode, info.mtime = len(contents[sha]), mode, mtime
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            tar.addfile(info, io.BytesIO(contents[sha]))

    packed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=packed, compresslevel=9, mtime=0) as gz:
        gz.write(raw.getvalue())
    return packed.getvalue()


def changelog_section(changelog: str, version: str) -> str:
    """The body of the ``## [version]`` section; a missing or empty section is an error."""
    heading = re.compile(rf"^## \[{re.escape(version)}\][^\n]*$", re.MULTILINE)
    match = heading.search(changelog)
    if not match:
        raise ReleaseError(f"CHANGELOG.md has no '## [{version}]' section")
    # The section ends at the next version heading or at the link-reference footer, which
    # Keep a Changelog keys by version ("[1.2.3]: https://..."), not at any "[x]:" line.
    following = re.compile(r"^## \[|^\[(?:Unreleased|\d+\.\d+\.\d+)\]: ", re.MULTILINE).search(changelog, match.end())
    body = changelog[match.end():following.start() if following else len(changelog)].strip()
    if not body:
        raise ReleaseError(f"CHANGELOG.md section '## [{version}]' is empty")
    return body + "\n"


def write_assets(repo: Path, rev: str, tag: str, out: Path) -> list[Path]:
    version_of(tag)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for pack in list_packs(repo, rev):
        archive = out / f"{pack}-{tag}.tar.gz"
        archive.write_bytes(build_archive(repo, rev, pack))
        digest = out / f"{archive.name}.sha256"
        digest.write_text(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
        written += [archive, digest]
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="write every pack's archive and .sha256")
    build.add_argument("tag")
    build.add_argument("--rev", help="commit to archive (default: the tag)")
    build.add_argument("--out", type=Path, default=Path("dist"))
    notes = sub.add_parser("notes", help="print the CHANGELOG.md section for the tag")
    notes.add_argument("tag")
    args = parser.parse_args(argv)

    repo = Path.cwd()
    try:
        if args.command == "build":
            for path in write_assets(repo, args.rev or args.tag, args.tag, args.out):
                print(path)
        else:
            sys.stdout.write(changelog_section((repo / "CHANGELOG.md").read_text(), version_of(args.tag)))
    except ReleaseError as err:
        print(f"::error::{err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
