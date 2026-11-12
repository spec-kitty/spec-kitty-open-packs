#!/usr/bin/env python3
"""Generate per-pack reference pages for the open-packs docsite.

This is the *content-from-code* generator described in
``docs/architecture/docsite-design.md``. For every doctrine pack it emits a
``docs/packs/<pack>.md`` page carrying only facts derivable from the source:

* doc-kitty-valid frontmatter (so the Astro site keeps building);
* a "generated — do not edit" banner plus a deterministic content checksum
  (sha256 over each file's ``relative-path + NUL + bytes + LF``, sorted by path);
* the version, ``pack_level`` and ``depends_on`` declared in ``pack.yaml``, *if
  present*, each dependency named by the pack of this repository that holds its
  ``pack_id`` (a bare ``pack_id`` otherwise);
* the pack's authored description — the preamble of its root ``README.md``,
  the pack document (charter #260, #451) — under "Purpose";
* an artifact inventory with per-kind counts.

It records no validation verdict: the CI gates (``scripts/ci/validate-packs.sh``
and ``scripts/ci/charter_service_check.py``) are the verdict, and a page that
recorded one could be committed failing and still pass ``--check`` (#249).

The output is **deterministic**: re-running on an unchanged tree yields a
byte-identical file. WP05 adds a CI drift gate that re-runs this generator and
fails on any diff, so nothing here may depend on wall-clock time, dict
iteration order, or filesystem ordering.

Run it from the repository root::

    python3 scripts/docs/gen_pack_reference.py            # write pages
    python3 scripts/docs/gen_pack_reference.py --check    # fail on any drift

``pack.yaml`` is read with ``pyyaml``; nothing else is needed, and nothing is
fetched.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_PACKS_DIR = REPO_ROOT / "docs" / "packs"
GENERATOR_REL = "scripts/docs/gen_pack_reference.py"

#: Exact opening of the do-not-edit banner every generated page carries. Used
#: both to render the banner and to recognise generated pages on disk (orphan
#: detection), so the two can never drift apart.
GENERATED_BANNER_PREFIX = "> **Generated page — do not edit by hand.**"

#: Hand-authored pages that live beside the generated ones in docs/packs/. A
#: pack slugged like one of these would overwrite it, so it is rejected.
RESERVED_SLUGS = frozenset({"index", "catalog-proposal"})

#: Fixed generation-baseline date stamped into every generated page's `updated`
#: and `generated.at`. Deliberately NOT git-derived: a git date is ref-dependent
#: (it changes when main moves under the branch and differs on a PR merge ref),
#: which makes a drift-gated generated page fail spuriously. The on-page content
#: checksum is the real per-change freshness signal. Bump only on a deliberate
#: generator change.
GENERATED_PAGE_DATE = "2026-11-12"

#: Artifact-kind subdirectories understood by the doctrine model, in the order
#: the design document lists them. Any *other* subdirectory a pack contains is
#: still reported (appended, sorted) so the inventory never silently hides
#: content — it is just ordered after the canonical kinds.
CANONICAL_KINDS: tuple[str, ...] = (
    "directives",
    "tactics",
    "styleguides",
    "toolguides",
    "paradigms",
    "procedures",
    "agent_profiles",
    "assets",
    "glossary_packs",
    "drg",
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PackDescriptor:
    """The authored ``pack.yaml`` fields the reference page surfaces."""

    name: str | None = None
    pack_version: str | None = None
    pack_id: str | None = None
    pack_level: str | None = None
    #: ``(pack_id, range)`` per entry, in the order written; ``range`` is ``None`` when absent.
    depends_on: tuple[tuple[str, str | None], ...] = ()


@dataclass(frozen=True)
class PackDocument:
    """The authored root ``README.md`` — the charter's description of the pack.

    The charter contract maps ``*/README.md`` to the ``pack-document`` schema and
    calls it "A pack's description" (charter #260, #451, ADR-0042 decision 8 as
    amended 2026-11-11). Only
    the preamble — the "what it is and why" prose between the optional H1 title
    and the first H2 section — is published: it is the author-facing purpose
    the closed ``pack.yaml`` descriptor schema (identity and lineage only) can
    never carry.
    """

    preamble: str = ""


@dataclass
class PackReference:
    """Everything needed to render one pack's reference page."""

    slug: str
    directory: Path
    rel_directory: str
    checksum: str
    descriptor: PackDescriptor
    pack_document: PackDocument | None = None
    counts: list[tuple[str, int]] = field(default_factory=list)
    inventory: list[tuple[str, list[str]]] = field(default_factory=list)
    file_count: int = 0
    #: ``pack_id`` -> slug of every pack of the repository, to name dependencies.
    pack_names: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Pack discovery
# ---------------------------------------------------------------------------


def discover_packs(repo_root: Path) -> list[tuple[str, Path]]:
    """Return ``(slug, directory)`` for built-in plus every ``packs/*`` dir.

    built-in (``packs/built-in``) is always first; the rest follow sorted by
    slug so the catalog order is stable.
    """

    packs: list[tuple[str, Path]] = []
    packs_root = repo_root / "packs"
    built_in = packs_root / "built-in"
    if built_in.is_dir():
        packs.append(("built-in", built_in))

    if packs_root.is_dir():
        for child in sorted(packs_root.iterdir(), key=lambda p: p.name):
            if child.is_dir() and child != built_in:
                packs.append((child.name, child))
    return packs


# ---------------------------------------------------------------------------
# pack.yaml reader
# ---------------------------------------------------------------------------


def read_pack_descriptor(directory: Path) -> PackDescriptor:
    """Read ``pack.yaml`` if present; otherwise return empties.

    Packs without a ``pack.yaml`` degrade gracefully: the page omits what the
    descriptor would have said. A ``depends_on`` entry names the pack by
    ``pack_id`` with a version ``range``.
    """

    path = directory / "pack.yaml"
    if not path.is_file():
        return PackDescriptor()
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return PackDescriptor()

    def _text(key: str) -> str | None:
        value = document.get(key)
        return None if value is None else str(value)

    entries = document.get("depends_on")
    return PackDescriptor(
        name=_text("name"),
        pack_version=_text("pack_version"),
        pack_id=_text("pack_id"),
        pack_level=_text("pack_level"),
        depends_on=tuple(
            (str(entry["pack_id"]), None if entry.get("range") is None else str(entry["range"]))
            for entry in (entries if isinstance(entries, list) else [])
            if isinstance(entry, dict) and entry.get("pack_id") is not None
        ),
    )


def pack_names(repo_root: Path) -> dict[str, str]:
    """``pack_id`` -> slug for every pack ``discover_packs`` finds."""

    names: dict[str, str] = {}
    for slug, directory in discover_packs(repo_root):
        pack_id = read_pack_descriptor(directory).pack_id
        if pack_id is not None:
            names.setdefault(pack_id, slug)
    return names


# ---------------------------------------------------------------------------
# Pack document (README.md) reader
# ---------------------------------------------------------------------------


def _markdown_fence(line: str) -> tuple[str, int, str] | None:
    """Return a CommonMark fence's character, length and info string."""

    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3 or not stripped or stripped[0] not in "`~":
        return None
    character = stripped[0]
    length = len(stripped) - len(stripped.lstrip(character))
    if length < 3:
        return None
    return character, length, stripped[length:]


def read_pack_document(directory: Path) -> PackDocument | None:
    """Read the pack's root ``README.md`` (the charter's pack document), if present.

    Follows the ``pack-document`` model the charter validates the file against:
    optional frontmatter, an optional H1 title, a preamble, then H2 sections in
    order. Only the preamble is kept — the authored description prose rendered
    under "Purpose". A missing file returns ``None`` so the page falls back to
    its authored-context note.
    """

    path = directory / "README.md"
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()

    # Optional frontmatter fence.
    if lines and lines[0].strip() == "---":
        close = next(
            (i for i in range(1, len(lines)) if lines[i].strip() == "---"), None
        )
        if close is None:
            # Unterminated fence: the file is malformed; treat it as no preamble
            # rather than rendering frontmatter data as prose.
            return PackDocument(preamble="")
        lines = lines[close + 1 :]

    # Skip blank lines, then the optional H1 title.
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    # The preamble runs to the first H2 section outside a code fence.
    preamble: list[str] = []
    fence: tuple[str, int] | None = None
    for line in lines:
        marker = _markdown_fence(line)
        if fence:
            preamble.append(line)
            if (
                marker
                and marker[0] == fence[0]
                and marker[1] >= fence[1]
                and not marker[2].strip()
            ):
                fence = None
            continue
        if line.startswith("## "):
            break
        preamble.append(line)
        if marker:
            fence = marker[:2]
    return PackDocument(preamble="\n".join(preamble).strip())


# ---------------------------------------------------------------------------
# Inventory, checksum, dates
# ---------------------------------------------------------------------------


def _pack_files(directory: Path) -> list[Path]:
    """All regular files under ``directory``, sorted by POSIX relative path."""

    files = [p for p in directory.rglob("*") if p.is_file()]
    return sorted(files, key=lambda p: p.relative_to(directory).as_posix())


def compute_checksum(directory: Path) -> str:
    """sha256 over ``relative-path + NUL + bytes + LF`` for every pack file, sorted by path.

    The relative path is folded into the hash so that moving a file changes
    the checksum even when its bytes are unchanged. A newline follows every
    file's bytes, including bytes that already end in a newline. Published
    verbatim in the page so a consumer can re-hash a downloaded pack and compare.
    """

    digest = hashlib.sha256()
    for file_path in _pack_files(directory):
        rel = file_path.relative_to(directory).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_path.read_bytes())
        digest.update(b"\n")
    return digest.hexdigest()


def build_inventory(
    directory: Path,
) -> tuple[list[tuple[str, int]], list[tuple[str, list[str]]], int]:
    """Return per-kind counts, per-kind file listings, and total file count.

    Kinds are the immediate subdirectories of the pack; canonical kinds come
    first in doctrine order, any extra subdirectories follow sorted. Counts are
    recursive so nested artifact assets are included.
    """

    subdirs = {
        child.name: child for child in directory.iterdir() if child.is_dir()
    }
    ordered = [k for k in CANONICAL_KINDS if k in subdirs]
    ordered += sorted(name for name in subdirs if name not in CANONICAL_KINDS)

    counts: list[tuple[str, int]] = []
    inventory: list[tuple[str, list[str]]] = []
    for kind in ordered:
        kind_dir = subdirs[kind]
        members = sorted(
            p.relative_to(kind_dir).as_posix()
            for p in kind_dir.rglob("*")
            if p.is_file()
        )
        counts.append((kind, len(members)))
        inventory.append((kind, members))

    total = sum(1 for p in directory.rglob("*") if p.is_file())
    return counts, inventory, total


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def build_reference(
    repo_root: Path, slug: str, directory: Path, names: dict[str, str] | None = None
) -> PackReference:
    counts, inventory, file_count = build_inventory(directory)
    try:
        rel_directory = directory.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        rel_directory = directory.name
    return PackReference(
        slug=slug,
        directory=directory,
        rel_directory=rel_directory,
        checksum=compute_checksum(directory),
        descriptor=read_pack_descriptor(directory),
        pack_document=read_pack_document(directory),
        counts=counts,
        inventory=inventory,
        file_count=file_count,
        pack_names=pack_names(repo_root) if names is None else names,
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _yaml_quote(value: str) -> str:
    """Quote a frontmatter scalar when needed (colon, leading symbol)."""

    needs_quote = any(ch in value for ch in ":#") or value.strip() != value
    if needs_quote:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def render_frontmatter(ref: PackReference) -> list[str]:
    title = f"{ref.slug} pack reference"
    description = (
        f"Generated reference for the {ref.slug} Charter Pack: artifact "
        f"inventory, per-kind counts, and content checksum."
    )
    lines = [
        "---",
        f"title: {_yaml_quote(title)}",
        f"description: {_yaml_quote(description)}",
        "doc_status: active",
        f"updated: '{GENERATED_PAGE_DATE}'",
        "kind: Reference",
        "related:",
        "- packs",
        "- architecture/docsite-design",
        "- packs/catalog-proposal",
        "generated:",
        f"  by: {GENERATOR_REL}",
        f"  at: '{GENERATED_PAGE_DATE}'",
        "---",
    ]
    # NOTE: `updated`/`generated.at` use a fixed generation-baseline constant,
    # not a git-derived date. A git date is ref-dependent (changes when main
    # moves under the branch, differs on a PR merge ref), which would make this
    # drift-gated page fail spuriously. The on-page content checksum is the real
    # per-change freshness signal.
    return lines


def render_dependency(pack_id: str, version_range: str | None, names: dict[str, str]) -> str:
    """A dependency by name, linked to its page, when this repository holds it; else by ``pack_id``."""

    slug = names.get(pack_id)
    named = f"[`{slug}`]({slug}.md)" if slug else f"`{pack_id}`"
    return f"{named} `{version_range}`" if version_range else named


def render_inventory(ref: PackReference) -> list[str]:
    lines = ["## Artifact inventory", ""]
    if not ref.counts:
        lines.append("This pack contains no artifact-kind subdirectories.")
        lines.append("")
        return lines

    lines.append("| Kind | Count |")
    lines.append("| --- | --- |")
    for kind, count in ref.counts:
        lines.append(f"| `{kind}` | {count} |")
    lines.append(f"| **Total files** | **{ref.file_count}** |")
    lines.append("")

    lines.append("### Full listing")
    lines.append("")
    for kind, members in ref.inventory:
        lines.append(f"<details>")
        lines.append(f"<summary><code>{kind}</code> ({len(members)})</summary>")
        lines.append("")
        if members:
            lines.extend(f"- `{member}`" for member in members)
        else:
            lines.append("- _(empty)_")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    return lines


def render_page(ref: PackReference) -> str:
    lines: list[str] = []
    lines.extend(render_frontmatter(ref))
    lines.append("")
    lines.append(f"# {ref.slug} pack reference")
    lines.append("")
    lines.append(
        f"{GENERATED_BANNER_PREFIX} This file is produced by "
        f"`{GENERATOR_REL}` from the pack source. Hand edits are overwritten on "
        "regeneration, and the CI drift gate fails on any difference."
    )
    lines.append("")

    # Provenance & integrity.
    lines.append("## Provenance & integrity")
    lines.append("")
    lines.append(f"- **Pack directory:** `{ref.rel_directory}`")
    if ref.descriptor.pack_level:
        lines.append(f"- **Pack level:** `{ref.descriptor.pack_level}`")
    if ref.descriptor.pack_version:
        lines.append(f"- **Declared version:** `{ref.descriptor.pack_version}`")
    lines.append(f"- **Content checksum (sha256):** `{ref.checksum}`")
    lines.append(
        "- **Checksum recipe:** sha256 over the sorted "
        "`(relative-path + NUL + bytes + LF)` of every file in the pack directory. "
        "Re-hash a downloaded pack with the same recipe to verify integrity."
    )
    lines.append("")

    # The authored README.md is the charter's description of the pack (charter
    # #260, #451, ADR-0042 decision 8); its preamble is the purpose prose the closed
    # pack.yaml descriptor schema — identity and lineage only — cannot carry.
    # A pack without one falls back to pointing at authored context.
    lines.append("## Purpose")
    lines.append("")
    preamble = ref.pack_document.preamble if ref.pack_document else ""
    if preamble:
        lines.append(preamble)
    elif ref.pack_document is not None:
        lines.append(
            "_This pack's `README.md` has no preamble. See the pack's `README.md` "
            "sections and the [Packs hub](index.md) for authored context._"
        )
    else:
        lines.append(
            "_No `purpose` is declared for this pack: it authors no `README.md` "
            "description. See the [Packs hub](index.md) for authored context._"
        )
    lines.append("")

    if ref.descriptor.depends_on:
        deps = ", ".join(
            render_dependency(pack_id, version_range, ref.pack_names)
            for pack_id, version_range in ref.descriptor.depends_on
        )
        lines.append(f"**Depends on:** {deps}")
        lines.append("")

    lines.extend(render_inventory(ref))

    return "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def generate(
    repo_root: Path,
    docs_packs_dir: Path,
    *,
    check: bool,
) -> int:
    packs = discover_packs(repo_root)
    if not packs:
        print("No packs discovered — nothing to generate.", file=sys.stderr)
        return 1

    clashes = sorted(slug for slug, _ in packs if slug in RESERVED_SLUGS)
    if clashes:
        raise ValueError(
            "Pack slug(s) collide with hand-authored docs/packs pages: "
            + ", ".join(clashes)
        )

    docs_packs_dir.mkdir(parents=True, exist_ok=True)
    drifted: list[str] = []
    written: list[str] = []

    names = pack_names(repo_root)
    for slug, directory in packs:
        ref = build_reference(repo_root, slug, directory, names)
        content = render_page(ref)
        target = docs_packs_dir / f"{slug}.md"

        existing = target.read_text(encoding="utf-8") if target.is_file() else None
        if check:
            if existing != content:
                drifted.append(slug)
            continue

        if existing != content:
            target.write_text(content, encoding="utf-8")
            written.append(slug)

    if check:
        known = {slug for slug, _ in packs}
        orphaned = sorted(
            page.name
            for page in docs_packs_dir.glob("*.md")
            if page.stem not in known
            and page.stem not in RESERVED_SLUGS
            and GENERATED_BANNER_PREFIX in page.read_text(encoding="utf-8")
        )
        if drifted or orphaned:
            if drifted:
                print(
                    "Drift detected in generated pack pages: "
                    + ", ".join(sorted(drifted)),
                    file=sys.stderr,
                )
            if orphaned:
                print(
                    "Orphaned generated pack pages (pack no longer exists): "
                    + ", ".join(f"docs/packs/{name}" for name in orphaned),
                    file=sys.stderr,
                )
            return 1
        print(f"No drift: {len(packs)} pack page(s) up to date.")
        return 0

    for slug in written:
        print(f"wrote docs/packs/{slug}.md")
    unchanged = len(packs) - len(written)
    print(
        f"Generated {len(packs)} pack page(s) "
        f"({len(written)} written, {unchanged} unchanged)."
    )
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated pages are up to date; exit 1 on any drift.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (defaults to the generator's own repo).",
    )
    parser.add_argument(
        "--docs-packs-dir",
        type=Path,
        default=None,
        help="Output directory for generated pages (defaults to docs/packs).",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    docs_packs_dir = (
        args.docs_packs_dir.resolve()
        if args.docs_packs_dir is not None
        else repo_root / "docs" / "packs"
    )
    return generate(repo_root, docs_packs_dir, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
