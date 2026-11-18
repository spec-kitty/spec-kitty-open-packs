#!/usr/bin/env python3
"""Resolve a charter target and move ``charter.lock.yaml`` to it, with everything the pin derives (#253).

The PR gate, the scheduled release run and the on-demand run share this tool and the gate's own jobs
(``.github/workflows/validate-packs.yml``); only the target differs::

    python3 scripts/ci/charter_pin.py newest-release        # the newest service-v* release or pre-release
    python3 scripts/ci/charter_pin.py resolve-release TAG   # its commit and the jar digest its .sha256 asset states
    python3 scripts/ci/charter_pin.py resolve-ref REF       # a branch, tag, pull/N/head or commit of the charter
    python3 scripts/ci/charter_pin.py apply --commit C [--release-tag T --jar-sha256 S]
    python3 scripts/ci/charter_pin.py changelog --release-tag T --commit C --previous P --date YYYY-MM-DD
    python3 scripts/ci/charter_pin.py commit-payload --branch B --head-oid OID --headline TEXT

``newest-release``, ``resolve-release`` and ``resolve-ref`` print ``key=value`` lines (append them to
``$GITHUB_OUTPUT``). ``newest-release`` lists the releases and never asks for "latest": GitHub's latest skips
pre-releases, which count here. It prints ``newer=true`` only when the newest tag is later, by semantic
version precedence, than the lock's ``release_tag``; a lock without one (a charter ``main`` pin, taken on
demand) is left alone, ``newer=false``, so the scheduled run never replaces a deliberate main pin.

``apply`` writes the three pin values into the lock (comments kept), then re-derives what the pin decides
here: every pack's ``pack-manifest.yaml`` (the derived membership and hashes, against the target's contract),
every ``packs/<name>.source.yaml`` digest and the generated pack pages. The checks then judge the tree a bump
pull request would carry. ``commit-payload`` prints the ``createCommitOnBranch`` input for the working tree's
changes, so the bump commit is made, and signed, by GitHub.

Network: the GitHub API (``GH_TOKEN`` or ``GITHUB_TOKEN`` is sent when set), github.com release downloads and
``git ls-remote``. Exit 0 on success, 2 when nothing can be judged (a malformed answer, a missing asset).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charter_lock  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = "spec-kitty/spec-kitty-charter"
GIT_URL = f"https://github.com/{REPOSITORY}.git"
API = f"https://api.github.com/repos/{REPOSITORY}"
VERSION = re.compile(r"service-v(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.]+))?")
#: A ref the on-demand run accepts: a branch or tag name, ``pull/<n>/head``, or a full commit.
REF = re.compile(r"[0-9A-Za-z][0-9A-Za-z._/-]{0,199}")
PULL_REF = re.compile(r"pull/\d+/head")
PACK_ROOTS = ("packs", "tests/fixtures/valid")
EMPTY = '""'  # how the lock spells an unset value


class PinError(Exception):
    """The target cannot be resolved or applied; nothing may be judged against it."""


# --------------------------------------------------------------------------------------------- versions

def precedence(tag: str) -> tuple:
    """The semantic version precedence of ``service-v<version>`` (SemVer 2.0.0, section 11), as a sort key.

    A release sorts after its pre-releases; pre-release identifiers compare numerically when numeric, a numeric one
    before an alphanumeric one, and a shorter list first when one is a prefix of the other."""
    match = VERSION.fullmatch(tag)
    if not match:
        raise PinError(f"{tag!r} is not a service-v<major>.<minor>.<patch>[-<pre>] tag")
    core = tuple(int(part) for part in match.group(1, 2, 3))
    pre = match.group(4)
    if pre is None:
        return (core, 1, ())
    identifiers = tuple((0, int(part), "") if part.isdigit() else (1, 0, part) for part in pre.split("."))
    return (core, 0, identifiers)


def newest(tags: list[str]) -> str | None:
    candidates = [tag for tag in tags if VERSION.fullmatch(tag)]
    return max(candidates, key=precedence) if candidates else None


# ---------------------------------------------------------------------------------------------- network

def _request(url: str, *, api: bool) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "spec-kitty-open-packs-ci"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if api:
        request.add_header("Accept", "application/vnd.github+json")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 (https only, fixed hosts)
            return response.read()
    except OSError as error:
        raise PinError(f"cannot fetch {url}: {error}") from error


def release_tags() -> list[str]:
    """Every published (non-draft) release's tag, pre-releases included, over every page."""
    tags: list[str] = []
    for page in range(1, 51):
        batch = json.loads(_request(f"{API}/releases?per_page=100&page={page}", api=True))
        if not isinstance(batch, list):
            raise PinError(f"the releases listing is not a list: {str(batch)[:200]}")
        tags += [release["tag_name"] for release in batch if not release.get("draft") and release.get("tag_name")]
        if len(batch) < 100:
            return tags
    raise PinError("more than 5000 releases; refusing to judge a partial listing")


def ls_remote(*patterns: str) -> dict[str, str]:
    done = subprocess.run(["git", "ls-remote", GIT_URL, *patterns], capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise PinError(f"git ls-remote {GIT_URL} failed: {done.stderr.strip()}")
    refs: dict[str, str] = {}
    for line in done.stdout.splitlines():
        sha, _, name = line.partition("\t")
        refs[name] = sha
    return refs


def tag_commit(tag: str) -> str:
    refs = ls_remote(f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}")
    commit = refs.get(f"refs/tags/{tag}^{{}}") or refs.get(f"refs/tags/{tag}")  # an annotated tag peels to its commit
    if not commit:
        raise PinError(f"{REPOSITORY} has no tag {tag}")
    return commit


def jar_digest(tag: str) -> str:
    version = tag.removeprefix("service-v")
    asset = f"spec-kitty-charter-service-{version}.jar.sha256"
    text = _request(f"https://github.com/{REPOSITORY}/releases/download/{tag}/{asset}", api=False).decode("utf-8")
    fields = text.split()
    if not fields or not charter_lock.SHA256.fullmatch(fields[0]):
        raise PinError(f"{asset} of {tag} does not start with a 64-hex SHA-256: {text[:200]!r}")
    if len(fields) > 1 and fields[1].lstrip("*") != asset.removesuffix(".sha256"):
        raise PinError(f"{asset} of {tag} names {fields[1]!r}, not the jar")
    return fields[0]


def resolve_ref(ref: str) -> str:
    """The commit a charter ref names now. Branches win over tags, as git resolves a bare name."""
    if charter_lock.COMMIT.fullmatch(ref):
        return ref
    if not REF.fullmatch(ref) or ".." in ref or ref.endswith((".lock", "/")):
        raise PinError(f"{ref!r} is not a branch, a tag, pull/<n>/head or a 40-hex commit")
    if PULL_REF.fullmatch(ref):
        candidates = [f"refs/{ref}"]
    else:
        name = ref.removeprefix("refs/heads/").removeprefix("refs/tags/")
        candidates = [f"refs/heads/{name}", f"refs/tags/{name}^{{}}", f"refs/tags/{name}"]
    refs = ls_remote(*candidates)
    for candidate in candidates:
        if candidate in refs:
            return refs[candidate]
    raise PinError(f"{REPOSITORY} has no ref {ref!r}")


# ------------------------------------------------------------------------------------------------ apply

def write_lock(commit: str, release_tag: str, jar_sha256: str, path: Path | None = None) -> None:
    path = path or charter_lock.LOCK_FILE
    if not charter_lock.COMMIT.fullmatch(commit):
        raise PinError(f"commit must be 40 lowercase hex characters, got {commit!r}")
    if release_tag and not charter_lock.RELEASE_TAG.fullmatch(release_tag):
        raise PinError(f"release_tag must be empty or service-vX.Y.Z[-pre], got {release_tag!r}")
    if jar_sha256 and not charter_lock.SHA256.fullmatch(jar_sha256):
        raise PinError(f"jar_sha256 must be empty or 64 lowercase hex characters, got {jar_sha256!r}")
    values = {"commit": commit, "release_tag": release_tag, "jar_sha256": jar_sha256}
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    seen: set[str] = set()
    for index, line in enumerate(lines):
        match = re.match(r"(commit|release_tag|jar_sha256):", line)
        if match:
            key = match.group(1)
            seen.add(key)
            lines[index] = f"{key}: {values[key] or EMPTY}\n"
    if seen != set(values):
        raise PinError(f"{path} lacks {', '.join(sorted(set(values) - seen))}; cannot move the pin")
    # Written beside the lock and read back with the lock's own rules first, so a refused pin leaves the lock alone.
    candidate = path.with_name(path.name + ".candidate")
    candidate.write_text("".join(lines), encoding="utf-8")
    try:
        if charter_lock.read(candidate) != values:
            raise PinError(f"{path} would not read back as the pin asked for")
    except charter_lock.LockError as error:
        candidate.unlink()
        raise PinError(f"{path}: {error}") from error
    except PinError:
        candidate.unlink()
        raise
    os.replace(candidate, path)


def _run(*command: str) -> None:
    print("+ " + " ".join(command), file=sys.stderr, flush=True)
    done = subprocess.run(command, cwd=ROOT, check=False)
    if done.returncode != 0:
        raise PinError(f"{' '.join(command)} exited {done.returncode}")


def rederive() -> None:
    """Re-derive every pin-derived file: the pack manifests, the pack digests, then the pack pages."""
    packs = sorted(str(path.relative_to(ROOT)) for base in PACK_ROOTS for path in (ROOT / base).iterdir()
                   if path.is_dir() and (path / "pack.yaml").is_file())
    if not packs:
        raise PinError("no pack found under packs/ or tests/fixtures/valid/")
    derive = [arg for pack in packs for arg in ("--derive-manifest", pack)]
    _run(sys.executable, "scripts/ci/validate_pack_schemas.py", *derive)
    _run(sys.executable, "scripts/ci/pack_digest.py", "--update")
    _run(sys.executable, "scripts/docs/gen_pack_reference.py")


# --------------------------------------------------------------------------------------------- changelog

CHANGELOG = ROOT / "docs" / "changelog" / "CHANGELOG.md"
CHANGED = "### 🔄 Changed"


def changelog_entry(release_tag: str, commit: str, previous: str, date: str, path: Path | None = None) -> None:
    """Record the bump first under ``## [Unreleased]`` / ``### 🔄 Changed`` (made when missing), and date the page."""
    path = path or CHANGELOG
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise PinError(f"date must be YYYY-MM-DD, got {date!r}")
    lines = path.read_text(encoding="utf-8").split("\n")
    try:
        start = lines.index("## [Unreleased]")
    except ValueError as error:
        raise PinError(f"{path} has no '## [Unreleased]' section") from error
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    entry = [
        f"- **The packs are pinned to charter release `{release_tag}`** (#253, opened by `charter-track.yml`).",
        f"  `charter.lock.yaml` moves from `{previous or 'a main pin'}` to `{release_tag}`, its commit",
        f"  `{commit}` and the jar digest its `.sha256` asset states. Every pack manifest, digest and pack",
        "  page is re-derived at the new pin; the scheduled run proved the whole gate green on that tree.",
    ]
    heading = next((i for i in range(start + 1, end) if lines[i] == CHANGED), None)
    if heading is None:
        lines[end:end] = [CHANGED, "", *entry, ""]
    elif heading + 1 < len(lines) and lines[heading + 1] == "":
        lines[heading + 2:heading + 2] = [*entry, ""]  # first under the heading, one blank line before it
    else:
        lines[heading + 1:heading + 1] = ["", *entry, ""]
    text = "\n".join(lines)
    text, count = re.subn(r"^updated: '\d{4}-\d{2}-\d{2}'$", f"updated: '{date}'", text, count=1, flags=re.M)
    if count != 1:
        raise PinError(f"{path} has no frontmatter 'updated' date")
    path.write_text(text, encoding="utf-8")


# ------------------------------------------------------------------------------------------ the commit

def commit_payload(branch: str, head_oid: str, headline: str, body: str) -> dict:
    """The ``createCommitOnBranch`` input for the working tree's changes against HEAD (tracked files only)."""
    if not charter_lock.COMMIT.fullmatch(head_oid):
        raise PinError(f"head oid must be 40 lowercase hex characters, got {head_oid!r}")
    done = subprocess.run(["git", "diff", "--name-status", "--no-renames", "-z", "HEAD"], cwd=ROOT,
                          capture_output=True, check=True)
    fields = done.stdout.decode("utf-8").split("\0")
    additions, deletions = [], []
    for status, path in zip(fields[0::2], fields[1::2]):
        if status == "D":
            deletions.append({"path": path})
        else:
            contents = base64.b64encode((ROOT / path).read_bytes()).decode("ascii")
            additions.append({"path": path, "contents": contents})
    if not additions and not deletions:
        raise PinError("the working tree has no change to commit")
    return {
        "branch": {"repositoryNameWithOwner": os.environ.get("GITHUB_REPOSITORY", ""), "branchName": branch},
        "expectedHeadOid": head_oid,
        "message": {"headline": headline, "body": body},
        "fileChanges": {"additions": additions, "deletions": deletions},
    }


# ------------------------------------------------------------------------------------------------- main

def _emit(**values: str) -> None:
    for key, value in values.items():
        print(f"{key}={value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("newest-release", help="the newest service-v* release or pre-release, and whether it is newer")
    sub.add_parser("resolve-release", help="a release's commit and jar digest").add_argument("tag")
    sub.add_parser("resolve-ref", help="the commit a charter ref names now").add_argument("ref")
    apply = sub.add_parser("apply", help="move the lock and re-derive the manifests, digests and pack pages")
    apply.add_argument("--commit", required=True)
    apply.add_argument("--release-tag", default="")
    apply.add_argument("--jar-sha256", default="")
    log = sub.add_parser("changelog", help="record the bump in the changelog's Unreleased section")
    log.add_argument("--release-tag", required=True)
    log.add_argument("--commit", required=True)
    log.add_argument("--previous", default="")
    log.add_argument("--date", required=True)
    payload = sub.add_parser("commit-payload", help="the createCommitOnBranch input for the working tree")
    payload.add_argument("--branch", required=True)
    payload.add_argument("--head-oid", required=True)
    payload.add_argument("--headline", required=True)
    payload.add_argument("--body", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "newest-release":
            current = charter_lock.read()["release_tag"]
            tag = newest(release_tags())
            if tag is None:
                raise PinError(f"{REPOSITORY} has no service-v* release")
            newer = bool(current) and precedence(tag) > precedence(current)
            _emit(tag=tag, current=current, newer=str(newer).lower())
        elif args.command == "resolve-release":
            if not VERSION.fullmatch(args.tag):
                raise PinError(f"{args.tag!r} is not a service-v* tag")
            _emit(commit=tag_commit(args.tag), release_tag=args.tag, jar_sha256=jar_digest(args.tag))
        elif args.command == "resolve-ref":
            _emit(commit=resolve_ref(args.ref), release_tag="", jar_sha256="")
        elif args.command == "apply":
            write_lock(args.commit, args.release_tag, args.jar_sha256)
            rederive()
        elif args.command == "changelog":
            changelog_entry(args.release_tag, args.commit, args.previous, args.date)
        else:
            print(json.dumps(commit_payload(args.branch, args.head_oid, args.headline, args.body)))
    except (PinError, charter_lock.LockError) as error:
        print(f"::error::charter_pin.py {args.command}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
