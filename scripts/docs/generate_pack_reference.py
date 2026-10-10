#!/usr/bin/env python3
"""Generate the DocKitty pack reference pages from the Charter Packs in this repo.

Content-from-code (ADR 2026-07-18-2, rendered by DocKitty per ADR 2026-10-10-5):
every pack directory under ``--packs-root`` (default ``packs/``) becomes one
Markdown page under ``--out`` (default ``docs/packs/reference/``), plus an
``index.md`` catalog table and a machine-readable ``checksums.json``
(ADR 2026-07-18-3). Pages carry the DocKitty frontmatter contract
(title/description/doc_status/updated/type/kind) and a ``generated: {by, at}``
stamp, and must never be edited by hand.

Determinism. Output is a pure function of the pack files plus the committed
output: artifacts are sorted, YAML is parsed (never re-serialised), and no wall
clock leaks in. The only date on a page (``updated`` / ``generated.at``) is
*sticky*: when a page's rendered content is unchanged, the date already
committed on it is kept, so ``--check`` is stable across runs, machines, and
shallow CI clones. A page whose content changed gets a new date, taken from
``SOURCE_DATE_EPOCH`` when set (reproducible-builds convention) or today's UTC
date otherwise. (Git commit times were rejected: a pack change and its
regenerated page land in the same commit, so the commit time is unknowable at
generation time, and shallow CI checkouts report the wrong commit.)

Usage (from the repository root)::

    python3 scripts/docs/generate_pack_reference.py            # write docs/packs/reference/
    python3 scripts/docs/generate_pack_reference.py --check    # exit 1 on drift
    python3 scripts/docs/generate_pack_reference.py \\
        --packs-root tests/fixtures/valid --out tests/golden/pack-reference --check

Dependencies: Python 3.10+ standard library and PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

GENERATOR = "agent/generate_pack_reference.py"
CHECKSUM_RECIPE = "open-packs-sha256-v1"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKS_ROOT = "packs"
DEFAULT_OUT = "docs/packs/reference"
INDEX_SLUG = "packs/reference"
DESCRIPTION_MAX = 180  # DocKitty frontmatter contract
SUMMARY_MAX = 200


# --------------------------------------------------------------------------- #
# Artifact kinds (the Spec Kitty 4.x org Charter Pack layout)
# --------------------------------------------------------------------------- #


def _first(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = data.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def _count(value: Any) -> int:
    return len(value) if isinstance(value, (list, dict)) else 0


def _directive_detail(d: dict[str, Any]) -> str:
    return f"`{d['enforcement']}`" if d.get("enforcement") else ""


def _steps_detail(d: dict[str, Any]) -> str:
    n = _count(d.get("steps"))
    return f"{n} step{'s' if n != 1 else ''}" if n else ""


def _mission_detail(d: dict[str, Any]) -> str:
    n = _count(d.get("action_sequence"))
    return f"{n} action{'s' if n != 1 else ''}" if n else ""


def _preset_detail(d: dict[str, Any]) -> str:
    parts = []
    for key in sorted(k for k in d if k.startswith("activated_")):
        n = _count(d[key])
        if n:
            noun = key[len("activated_"):].replace("_", " ")
            parts.append(f"{n} {noun[:-1] if n == 1 and noun.endswith('s') else noun}")
    return ", ".join(parts)


def _glossary_detail(d: dict[str, Any]) -> str:
    n = _count(d.get("terms"))
    return f"{n} term{'s' if n != 1 else ''}" if n else ""


@dataclass(frozen=True)
class Kind:
    directory: str
    pattern: str
    singular: str
    plural: str
    detail: Callable[[dict[str, Any]], str] = lambda _d: ""
    detail_header: str = "Detail"


KINDS: tuple[Kind, ...] = (
    Kind("directives", "*.directive.yaml", "directive", "Directives", _directive_detail, "Enforcement"),
    Kind("tactics", "*.tactic.yaml", "tactic", "Tactics", _steps_detail, "Steps"),
    Kind("procedures", "*.procedure.yaml", "procedure", "Procedures", _steps_detail, "Steps"),
    Kind("styleguides", "*.styleguide.yaml", "styleguide", "Styleguides"),
    Kind("toolguides", "*.toolguide.yaml", "toolguide", "Toolguides"),
    Kind("paradigms", "*.paradigm.yaml", "paradigm", "Paradigms"),
    Kind("agent_profiles", "*.agent.yaml", "agent profile", "Agent profiles"),
    Kind("glossary_packs", "*.glossary-pack.yaml", "glossary pack", "Glossary packs", _glossary_detail, "Terms"),
    Kind("mission_types", "*.yaml", "mission type", "Mission types", _mission_detail, "Actions"),
    Kind("presets", "*.yaml", "preset", "Presets", _preset_detail, "Activates"),
    Kind("skills", "*.skill.yaml", "skill", "Skills"),
)


@dataclass
class Artifact:
    kind: Kind
    path: Path  # absolute
    ident: str
    title: str
    summary: str
    detail: str


@dataclass
class Pack:
    name: str
    root: Path
    artifacts: dict[str, list[Artifact]] = field(default_factory=dict)
    manifest: dict[str, Any] = field(default_factory=dict)  # optional pack.yaml (#21)
    org_charter: dict[str, Any] | None = None
    drg: dict[str, int] | None = None
    checksum: str = ""
    file_count: int = 0


class GeneratorError(Exception):
    pass


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GeneratorError(f"{path}: cannot parse YAML: {exc}") from exc


def _clean(value: Any, limit: int = SUMMARY_MAX) -> str:
    text = " ".join(str(value).split()) if value is not None else ""
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def _cell(value: str) -> str:
    """Escape a value for a Markdown table cell."""
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")


def pack_checksum(root: Path) -> tuple[str, int]:
    """Recipe ``open-packs-sha256-v1``.

    Equivalent to, from inside the pack directory::

        find . -type f ! -path '*/.*' | LC_ALL=C sort \\
          | while IFS= read -r f; do sha256sum "$f"; done | sha256sum

    i.e. the sha256 of the ``sha256sum``-format manifest (``<hex>  ./<path>``)
    of every non-hidden file, sorted bytewise by path.
    """
    files = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if not path.is_file() or any(part.startswith(".") for part in rel.parts):
            continue
        files.append("./" + rel.as_posix())
    files.sort(key=lambda s: s.encode("utf-8"))
    manifest = "".join(
        f"{hashlib.sha256((root / f[2:]).read_bytes()).hexdigest()}  {f}\n" for f in files
    )
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest(), len(files)


def load_pack(root: Path) -> Pack:
    pack = Pack(name=root.name, root=root)
    for kind in KINDS:
        directory = root / kind.directory
        if not directory.is_dir():
            continue
        items: list[Artifact] = []
        for path in sorted(directory.glob(kind.pattern), key=lambda p: p.name):
            data = _load_yaml(path)
            if not isinstance(data, dict):
                raise GeneratorError(f"{path}: expected a YAML mapping")
            ident = _clean(_first(data, "id", "profile_id", "name") or path.name.split(".")[0])
            title = _clean(_first(data, "title", "name", "display_name") or ident)
            summary = _clean(_first(data, "intent", "purpose", "description", "summary"))
            items.append(Artifact(kind, path, ident, title, summary, _clean(kind.detail(data))))
        if items:
            pack.artifacts[kind.directory] = items
    manifest = root / "pack.yaml"
    if manifest.is_file():
        data = _load_yaml(manifest)
        pack.manifest = data if isinstance(data, dict) else {}
    charter = root / "org-charter.yaml"
    if charter.is_file():
        data = _load_yaml(charter)
        pack.org_charter = data if isinstance(data, dict) else {}
    fragment = root / "drg" / "fragment.yaml"
    if fragment.is_file():
        data = _load_yaml(fragment) or {}
        pack.drg = {"nodes": _count(data.get("nodes")), "edges": _count(data.get("edges"))}
    pack.checksum, pack.file_count = pack_checksum(root)
    return pack


def discover(packs_root: Path) -> list[Pack]:
    if not packs_root.is_dir():
        raise GeneratorError(f"packs root not found: {packs_root}")
    dirs = sorted(
        (p for p in packs_root.iterdir() if p.is_dir() and not p.name.startswith(".")),
        key=lambda p: p.name,
    )
    return [load_pack(d) for d in dirs]


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #


def _q(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _frontmatter(*, title: str, description: str, kind: str, date: str, related: list[str]) -> str:
    if len(description) > DESCRIPTION_MAX:
        description = description[: DESCRIPTION_MAX - 1].rstrip() + "…"
    lines = [
        "---",
        f"title: {_q(title)}",
        f"description: {_q(description)}",
        "doc_status: active",
        f"updated: {_q(date)}",
        "type: API",
        f"kind: {kind}",
        "tags:",
        "- pack-reference",
        "- generated",
        "generated:",
        f"  by: {GENERATOR}",
        f"  at: {_q(date)}",
    ]
    if related:
        lines.append("related:")
        lines.extend(f"- {r}" for r in related)
    lines.append("---")
    return "\n".join(lines) + "\n"


def _banner(packs_root_rel: str) -> str:
    return (
        "> **Generated — do not edit.** This page is rendered from "
        f"`{packs_root_rel}/` by `scripts/docs/generate_pack_reference.py`; "
        "CI fails on drift. Change the pack, then re-run the generator.\n"
    )


def _counts(pack: Pack) -> list[str]:
    out = []
    for kind in KINDS:
        n = len(pack.artifacts.get(kind.directory, []))
        if n:
            out.append(f"{n} {kind.singular}{'' if n == 1 else 's'}")
    return out


def _depends(pack: Pack) -> list[str]:
    deps = pack.manifest.get("depends_on") or []
    return [str(d) for d in deps] if isinstance(deps, list) else [str(deps)]


class Renderer:
    def __init__(self, packs_root: Path, out_dir: Path):
        self.packs_root = packs_root
        self.out_dir = out_dir  # the *intended* location (links are relative to it)
        try:
            self.packs_root_rel = packs_root.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            self.packs_root_rel = packs_root.as_posix()

    def link(self, target: Path) -> str:
        return Path(os.path.relpath(target.resolve(), self.out_dir.resolve())).as_posix()

    def pack_page(self, pack: Pack, date: str) -> str:
        counts = _counts(pack)
        purpose = _clean(pack.manifest.get("purpose")) if pack.manifest else ""
        description = (
            f"Generated reference for the {pack.name} Charter Pack: "
            + (", ".join(counts) if counts else "no artifacts")
            + "."
        )
        out = [
            _frontmatter(
                title=f"Pack: {pack.name}",
                description=description,
                kind="Reference",
                date=date,
                related=[INDEX_SLUG],
            ),
            f"# Pack: {pack.name}\n",
            _banner(self.packs_root_rel),
            "## Summary\n",
            "| Field | Value |",
            "| --- | --- |",
            f"| Source | [`{self.packs_root_rel}/{pack.name}/`]({self.link(pack.root)}/) |",
            f"| Purpose | {_cell(purpose) if purpose else '— (no `pack.yaml`)'} |",
            f"| Depends on | {_cell(', '.join(f'`{d}`' for d in _depends(pack))) or '—'} |",
        ]
        maturity = pack.manifest.get("maturity") if pack.manifest else None
        if maturity:
            out.append(f"| Maturity | {_cell(_clean(maturity))} |")
        out.append(f"| Artifacts | {', '.join(counts) if counts else '—'} |")
        if pack.drg is not None:
            out.append(
                f"| DRG fragment | {pack.drg['nodes']} node(s), {pack.drg['edges']} edge(s) "
                f"([`drg/fragment.yaml`]({self.link(pack.root / 'drg' / 'fragment.yaml')})) |"
            )
        if pack.org_charter is not None:
            keys = ", ".join(f"`{k}`" for k in sorted(pack.org_charter))
            org = pack.org_charter.get("org_name")
            label = f"org `{_cell(str(org))}`; " if org else ""
            out.append(
                f"| Org charter | {label}keys: {keys or '—'} "
                f"([`org-charter.yaml`]({self.link(pack.root / 'org-charter.yaml')})) |"
            )
        out += [
            "",
            "## Provenance & integrity\n",
            f"- **Content checksum** (`{CHECKSUM_RECIPE}`, {pack.file_count} file(s)): `sha256:{pack.checksum}`",
            "- **Verify** a fetched copy from inside the pack directory:\n",
            "  ```sh",
            "  find . -type f ! -path '*/.*' | LC_ALL=C sort \\",
            '    | while IFS= read -r f; do sha256sum "$f"; done | sha256sum',
            "  ```\n",
            "  (`shasum -a 256` in place of `sha256sum` on macOS.) This is tamper-evidence for the published",
            "  content, not a signature: it tells you the copy matches this repository, not who to trust",
            "  (ADR 2026-07-18-3).",
            "",
        ]
        if not pack.artifacts:
            out.append("This pack ships no recognised artifact files.\n")
        for kind in KINDS:
            items = pack.artifacts.get(kind.directory)
            if not items:
                continue
            show_detail = any(a.detail for a in items)
            out.append(f"## {kind.plural}\n")
            header = "| ID | Title | Summary |" + (f" {kind.detail_header} |" if show_detail else "") + " Source |"
            out.append(header)
            out.append("| --- | --- | --- |" + (" --- |" if show_detail else "") + " --- |")
            for a in items:
                row = f"| `{_cell(a.ident)}` | {_cell(a.title)} | {_cell(a.summary) or '—'} |"
                if show_detail:
                    row += f" {_cell(a.detail) if a.detail else '—'} |"
                row += f" [`{kind.directory}/{a.path.name}`]({self.link(a.path)}) |"
                out.append(row)
            out.append("")
        return "\n".join(out).rstrip("\n") + "\n"

    def index_page(self, packs: list[Pack], date: str) -> str:
        out = [
            _frontmatter(
                title="Pack reference",
                description=(
                    "Generated reference for every Charter Pack in this repository: "
                    "artifacts per kind, dependencies, and content checksums."
                ),
                kind="Hub",
                date=date,
                related=["packs", "packs/catalog-proposal"],
            ),
            "# Pack reference\n",
            _banner(self.packs_root_rel),
        ]
        if not packs:
            out += [
                f"No packs are materialized under `{self.packs_root_rel}/` yet. The packs we intend to",
                f"ship are listed in the [catalog proposal]({self.link(REPO_ROOT / 'docs' / 'packs' / 'catalog-proposal.md')});",
                "each one gets a page here as soon as its directory lands.",
            ]
            return "\n".join(out).rstrip("\n") + "\n"
        out += [
            f"{len(packs)} pack(s) under `{self.packs_root_rel}/`. Checksums use recipe `{CHECKSUM_RECIPE}`;",
            "the machine-readable list is [`checksums.json`](checksums.json).\n",
            "| Pack | Purpose | Depends on | Artifacts | Checksum |",
            "| --- | --- | --- | --- | --- |",
        ]
        for p in packs:
            purpose = _clean(p.manifest.get("purpose")) if p.manifest else ""
            deps = ", ".join(f"`{d}`" for d in _depends(p))
            out.append(
                f"| [{_cell(p.name)}]({p.name}.md) | {_cell(purpose) or '—'} | {_cell(deps) or '—'} | "
                f"{', '.join(_counts(p)) or '—'} | `{p.checksum[:12]}…` |"
            )
        return "\n".join(out).rstrip("\n") + "\n"

    @staticmethod
    def checksums(packs: list[Pack]) -> str:
        data = {
            "recipe": CHECKSUM_RECIPE,
            "packs": {p.name: {"sha256": p.checksum, "files": p.file_count} for p in packs},
        }
        return json.dumps(data, indent=2, sort_keys=True) + "\n"


# --------------------------------------------------------------------------- #
# Sticky dates + write / check
# --------------------------------------------------------------------------- #

_UPDATED_RE = re.compile(r"^updated: '(\d{4}-\d{2}-\d{2})'$", re.M)


def new_date() -> str:
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        moment = _dt.datetime.fromtimestamp(int(epoch), tz=_dt.timezone.utc)
    else:
        moment = _dt.datetime.now(tz=_dt.timezone.utc)
    return moment.date().isoformat()


def sticky(render: Callable[[str], str], existing: str | None) -> str:
    """Keep the committed date when the content is otherwise unchanged."""
    if existing is not None:
        m = _UPDATED_RE.search(existing)
        if m:
            candidate = render(m.group(1))
            if candidate == existing:
                return candidate
    return render(new_date())


def build(packs_root: Path, out_dir: Path) -> dict[str, str]:
    """Return ``{filename: content}`` for the full generated output set."""
    packs = discover(packs_root)
    names = [p.name for p in packs]
    if "index" in names:
        raise GeneratorError("a pack may not be named 'index' (reserved for the catalog page)")
    renderer = Renderer(packs_root, out_dir)

    def existing(name: str) -> str | None:
        path = out_dir / name
        return path.read_text(encoding="utf-8") if path.is_file() else None

    files: dict[str, str] = {}
    for pack in packs:
        name = f"{pack.name}.md"
        files[name] = sticky(lambda d, p=pack: renderer.pack_page(p, d), existing(name))
    files["index.md"] = sticky(lambda d: renderer.index_page(packs, d), existing("index.md"))
    if packs:
        files["checksums.json"] = renderer.checksums(packs)
    return files


def _current(out_dir: Path) -> dict[str, str]:
    if not out_dir.is_dir():
        return {}
    return {
        p.name: p.read_text(encoding="utf-8")
        for p in sorted(out_dir.iterdir())
        if p.is_file() and p.suffix in {".md", ".json"}
    }


def write(files: dict[str, str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in set(_current(out_dir)) - set(files):
        (out_dir / stale).unlink()
    for name, content in files.items():
        path = out_dir / name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")


def check(files: dict[str, str], out_dir: Path) -> list[str]:
    """Diff the freshly rendered output set against ``out_dir``; return diff lines.

    Rendering already happened in memory (``build``), so nothing is written: a
    missing, changed, or stale (no longer generated) file is drift.
    """
    actual = _current(out_dir)
    diff: list[str] = []
    for name in sorted(set(files) | set(actual)):
        a = actual.get(name, "").splitlines(keepends=True)
        b = files.get(name, "").splitlines(keepends=True)
        if a != b or (name in files) != (name in actual):
            diff.extend(difflib.unified_diff(a, b, f"committed/{name}", f"generated/{name}"))
            if not a and not b:
                diff.append(f"{'missing' if name in files else 'stale'}: {name}\n")
    return diff


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--packs-root", default=DEFAULT_PACKS_ROOT, help="directory holding one subdirectory per pack (default: packs)")
    parser.add_argument("--out", default=DEFAULT_OUT, help="output directory (default: docs/packs/reference)")
    parser.add_argument("--check", action="store_true", help="do not write; exit 1 if the committed output drifts")
    args = parser.parse_args(argv)

    packs_root = Path(args.packs_root)
    out_dir = Path(args.out)
    if not packs_root.is_absolute():
        packs_root = REPO_ROOT / packs_root
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / out_dir
    try:
        files = build(packs_root, out_dir)
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        diff = check(files, out_dir)
        if diff:
            sys.stdout.writelines(diff)
            print(
                f"\n✖ {out_dir.relative_to(REPO_ROOT) if out_dir.is_relative_to(REPO_ROOT) else out_dir} "
                "is out of date — run scripts/docs/generate_pack_reference.py and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"✓ pack reference up to date ({len(files)} file(s)).")
        return 0

    write(files, out_dir)
    print(f"✓ wrote {len(files)} file(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
