#!/usr/bin/env python3
"""Validate Charter Pack files against the JSON Schemas of spec-kitty-charter.

The charter repository owns the pack shapes (``contracts/packs/schemas/*.schema.json``)
and says which file gets which schema (``contracts/packs/file-kinds.yaml``). This script
mirrors that mapping: it classifies every file of a pack by the ``files``, ``exclusions``,
``retired`` and ``payloads`` rules, validates YAML files against their schema, and reads
Markdown companions (``pack.md``, guides, mission-step prompts and guidelines) into the
charter's Markdown model ``{frontmatter?, title?, preamble, sections}`` before validating
that model against the rule's structure schema.

It fails closed. Exit status:

* 0  every pack is valid (its ``pack-manifest.yaml``, when it has one, carries the hashes of the
     files it lists: ``--regenerate-manifest PACK`` restamps them) and every ``--expect-invalid`` pack has schema violations;
* 1  a schema violation (or a retired-layout file) in a pack, or an ``--expect-invalid``
     pack that came out clean;
* 2  the gate cannot judge: unloadable contract or schema, a file of a known kind with no
     schema mapping, a pack with zero files checked, or an unreadable file.

Needs ``pyyaml`` and ``jsonschema`` (Draft 2020-12). The contract is fetched from the
pinned charter commit below unless ``--contract DIR`` (a directory holding
``file-kinds.yaml`` and ``schemas/``) or ``$CHARTER_CONTRACT_DIR`` is given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

CHARTER_REPOSITORY = "spec-kitty/spec-kitty-charter"
# Commit of spec-kitty-charter whose contracts/packs/ this repository validates against.
# It is the head of branch issue-194-mission-type-consolidation (open PR #275), the only
# place mission-type.schema.json and the mission-step prompt/guidelines schemas exist yet.
# TODO: move this to a commit on charter main once #275 has merged.
CHARTER_COMMIT = "ad949d165d41a344916be754fd70e1d9cfb69397"
CONTRACT_PATH = "contracts/packs"

#: File-name tokens (``<id>.<token>.yaml``) of kinds the contract must map to a schema.
KNOWN_KIND_TOKENS = frozenset(
    {
        "directive", "tactic", "styleguide", "toolguide", "paradigm", "procedure",
        "agent", "step-contract", "asset", "glossary-pack", "skill", "mission-type",
        "graph",
    }
)  # fmt: skip

EXIT_OK, EXIT_INVALID, EXIT_GATE = 0, 1, 2
REGENERATE_COMMAND = "python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest"


class GateError(Exception):
    """The validator cannot judge; the run must fail (exit 2)."""


# --------------------------------------------------------------------------- contract


@dataclass(frozen=True)
class Rule:
    regex: re.Pattern[str]
    match: str
    schema: str | None = None
    content_form: str = "yaml"
    reason: str = ""


@dataclass
class Contract:
    files: list[Rule]
    exclusions: list[Rule]
    retired: list[Rule]
    payloads: list[Rule]
    validators: dict[str, Draft202012Validator] = field(default_factory=dict)


def glob_to_regex(glob: str) -> re.Pattern[str]:
    """``*`` within one segment, ``**/`` zero or more whole segments, the rest literal."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def _rules(table: dict[str, Any], section: str) -> list[Rule]:
    rules = []
    for entry in table.get(section) or []:
        rules.append(
            Rule(
                regex=glob_to_regex(entry["match"]),
                match=entry["match"],
                schema=entry.get("schema"),
                content_form=entry.get("content_form", "yaml"),
                reason=str(entry.get("reason", "")).strip(),
            )
        )
    return rules


def load_contract(contract_dir: Path) -> Contract:
    """Read ``file-kinds.yaml`` and load every schema it names; fail closed on any gap."""
    table_path = contract_dir / "file-kinds.yaml"
    try:
        table = yaml.safe_load(table_path.read_text(encoding="utf-8"))
        contract = Contract(
            files=_rules(table, "files"),
            exclusions=_rules(table, "exclusions"),
            retired=_rules(table, "retired"),
            payloads=_rules(table, "payloads"),
        )
    except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError) as exc:
        raise GateError(f"cannot read {table_path}: {exc!r}") from exc
    if not contract.files:
        raise GateError(f"{table_path} has no `files` rules")
    for rule in contract.files:
        name = rule.schema
        if not name:
            raise GateError(f"files rule {rule.match!r} names no schema")
        if name in contract.validators:
            continue
        schema_path = contract_dir / "schemas" / f"{name}.schema.json"
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001 - any failure to load a schema is a gate failure
            raise GateError(f"cannot load schema {schema_path}: {exc!r}") from exc
        contract.validators[name] = Draft202012Validator(schema)
    return contract


def fetch_contract(dest: Path) -> Path:
    """Download file-kinds.yaml and the schemas it names from the pinned charter commit."""
    base = f"https://raw.githubusercontent.com/{CHARTER_REPOSITORY}/{CHARTER_COMMIT}/{CONTRACT_PATH}"
    headers = {}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    def get(relative: str) -> bytes:
        request = urllib.request.Request(f"{base}/{relative}", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 - fixed https URL
                return response.read()
        except OSError as exc:
            raise GateError(f"cannot fetch {base}/{relative}: {exc!r}") from exc

    (dest / "schemas").mkdir(parents=True, exist_ok=True)
    table_bytes = get("file-kinds.yaml")
    (dest / "file-kinds.yaml").write_bytes(table_bytes)
    try:
        names = {rule["schema"] for rule in yaml.safe_load(table_bytes)["files"]}
    except (yaml.YAMLError, KeyError, TypeError) as exc:
        raise GateError(f"fetched file-kinds.yaml is unreadable: {exc!r}") from exc
    for name in sorted(names):
        (dest / "schemas" / f"{name}.schema.json").write_bytes(get(f"schemas/{name}.schema.json"))
    return dest


_CONTRACT_CACHE: dict[str, Contract] = {}


def contract_for(contract_dir: Path | None) -> Contract:
    """The contract at ``contract_dir`` (or ``$CHARTER_CONTRACT_DIR``, else the pinned fetch)."""
    chosen = contract_dir or (Path(os.environ["CHARTER_CONTRACT_DIR"]) if os.environ.get("CHARTER_CONTRACT_DIR") else None)
    key = str(chosen or f"pinned:{CHARTER_COMMIT}")
    if key not in _CONTRACT_CACHE:
        if chosen is None:
            with tempfile.TemporaryDirectory(prefix="charter-contract-") as scratch:
                _CONTRACT_CACHE[key] = load_contract(fetch_contract(Path(scratch)))
        else:
            _CONTRACT_CACHE[key] = load_contract(chosen)
    return _CONTRACT_CACHE[key]


# --------------------------------------------------------------------------- YAML


class YamlRefused(yaml.YAMLError):
    """A document the charter's reader (ParsedYaml) refuses for a guard, not for a syntax error."""


class _Loader(yaml.SafeLoader):
    """Safe loader that keeps timestamps as strings, as JSON Schema sees them, and refuses duplicate keys.

    The charter loads with ``setAllowDuplicateKeys(false)`` (Yaml.java); PyYAML keeps the last value.
    """

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            try:
                duplicate = key in seen
                seen.add(key)
            except TypeError:  # unhashable key: the base class reports it
                break
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark, f"found duplicate key {key!r}", key_node.start_mark
                )
        return super().construct_mapping(node, deep=deep)


_Loader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

#: The guards of the charter's ParsedYaml: collections nested at most this deep, and a document that
#: expands (a shared, aliased node counted each time it is reached) to at most this many nodes.
MAX_DEPTH = 200
MAX_NODES = 100_000


def _nested_too_deeply(text: str) -> bool:
    """Whether the parser's events nest collections deeper than MAX_DEPTH; the event stream is not recursive."""
    depth = 0
    try:
        for event in yaml.parse(text, Loader=_Loader):
            if isinstance(event, yaml.CollectionStartEvent):
                depth += 1
                if depth > MAX_DEPTH:
                    return True
            elif isinstance(event, yaml.CollectionEndEvent):
                depth -= 1
    except yaml.YAMLError:
        return False  # the loader reports a syntax error in the parser's own words
    return False


def _problem(value: Any, depth: int, path: set[int], nodes: list[int]) -> str | None:
    """The first reason a loaded document cannot be validated (ParsedYaml.problem), or ``None``."""
    nodes[0] += 1
    if nodes[0] > MAX_NODES:
        return "the document is too large"
    if not isinstance(value, (dict, list)):
        plain = value is None or isinstance(value, (str, int, float, bool))
        return None if plain else "a value is not a string, a number, a boolean or null"
    if depth >= MAX_DEPTH:
        return "the document is nested too deeply"
    if id(value) in path:
        return "the document contains itself"
    path.add(id(value))
    try:
        if isinstance(value, dict):
            if not all(isinstance(key, str) for key in value):
                return "a mapping key is not a string"
            children: Any = value.values()
        else:
            children = value
        for child in children:
            if (problem := _problem(child, depth + 1, path, nodes)) is not None:
                return problem
        return None
    finally:
        path.discard(id(value))


def load_yaml(text: str) -> Any:
    """Load one YAML document through the charter's guards; raises ``yaml.YAMLError`` when it is refused."""
    if _nested_too_deeply(text):
        raise YamlRefused("the document is nested too deeply")
    document = yaml.load(text, Loader=_Loader)  # noqa: S506 - SafeLoader subclass
    if (problem := _problem(document, 0, set(), [0])) is not None:
        raise YamlRefused(problem)
    return document


# --------------------------------------------------------------------------- manifest

MANIFEST_NAME = "pack-manifest.yaml"
#: The ``pack-manifest.yaml`` entry lists that carry a ``content_hash``.
MANIFEST_LISTS = ("constituents", "presets")


def content_hash(data: bytes) -> str:
    """SHA-256 (lowercase hex) of a file's bytes after every CRLF, then every lone CR, becomes LF."""
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def manifest_hash(manifest: dict[str, Any]) -> str:
    """SHA-256 of the RFC 8785 canonical JSON of the manifest without ``manifest_hash``.

    Narrow like the charter's recipe (PackManifests.canonicalJson): every value is a string, a list
    or an object of the manifest's fixed keys, so no number output is needed, and the keys are
    ASCII, so sorting them by code point equals sorting them by UTF-16 code unit. ``presets`` is
    left out when the manifest lists none.
    """
    body: dict[str, Any] = {"schema_version": manifest["schema_version"]}
    for name in MANIFEST_LISTS:
        if name == "constituents" or manifest.get(name):
            body[name] = [
                {key: entry[key] for key in ("content_hash", "id", "kind", "path") if key in entry}
                for entry in manifest.get(name, [])
            ]
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _bytes_reader(pack_dir: Path) -> Callable[[str], bytes | None]:
    """The bytes of a pack-relative path; ``None`` for a missing file, a symlink or a path leaving the pack."""

    def read(relative: str) -> bytes | None:
        target = pack_dir / relative
        try:
            inside = target.resolve().is_relative_to(pack_dir.resolve())
            return target.read_bytes() if inside and not target.is_symlink() and target.is_file() else None
        except OSError:
            return None

    return read


def stale_manifest_fields(manifest: dict[str, Any], read: Callable[[str], bytes | None]) -> list[str]:
    """The derived fields of ``manifest`` that do not verify, as the charter names them (PackManifests.stale)."""
    stale, missing = [], []
    for name in MANIFEST_LISTS:
        for entry in manifest.get(name) or []:
            data = read(entry["path"])
            if data is None:
                missing.append(entry["path"])
            elif entry["content_hash"] != content_hash(data):
                stale.append(f"{name}{{{entry['path']}}}.content_hash")
    if manifest["manifest_hash"] != manifest_hash(manifest):
        stale.append("manifest_hash")
    return [*stale, *(f"missing: {path}" for path in missing)]


def regenerate_manifest(pack_dir: Path) -> list[str]:
    """Restamp every derived field of ``pack_dir``/pack-manifest.yaml from the files; membership is kept.

    Returns the listed paths that have no file (their entries keep the hash they had).
    """
    path = pack_dir / MANIFEST_NAME
    try:
        manifest = load_yaml(path.read_bytes().decode("utf-8"))
        read = _bytes_reader(pack_dir)
        missing = []
        for name in MANIFEST_LISTS:
            for entry in manifest.get(name) or []:
                data = read(entry["path"])
                if data is None:
                    missing.append(entry["path"])
                else:
                    entry["content_hash"] = content_hash(data)
        manifest["manifest_hash"] = manifest_hash(manifest)
        path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    except (OSError, UnicodeDecodeError, yaml.YAMLError, KeyError, TypeError, AttributeError) as exc:
        raise GateError(f"{path}: cannot regenerate the manifest: {exc!r}") from exc
    return missing


# --------------------------------------------------------------------------- Markdown model

_SETEXT = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_CLOSING = re.compile(r"^(?:#+|.*[ \t]#+)$")


class MarkdownRefused(Exception):
    def __init__(self, line: int, reason: str) -> None:
        super().__init__(f"line {line}: {reason}")


def _spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _run(text: str, char: str) -> int:
    return len(text) - len(text.lstrip(char)) if text.startswith(char) else 0


def _fence_opener(line: str) -> tuple[str, int] | None:
    rest = line[_spaces(line):]
    if not rest or rest[0] not in "`~":
        return None
    marker, length = rest[0], _run(rest, rest[0])
    if length < 3 or (marker == "`" and "`" in rest[length:]):
        return None
    return marker, length


def _heading(text: str, number: int) -> tuple[int, str] | None:
    indent = _spaces(text)
    if indent > 3:
        return None
    rest = text[indent:]
    level = _run(rest, "#")
    if level == 0 or level > 6:
        return None
    after = rest[level:]
    if after and after[0] not in " \t":
        return None
    if level > 2:
        return None
    name = "an H1" if level == 1 else "an H2"
    if indent:
        raise MarkdownRefused(number, f"{name} indented by {indent} spaces is ambiguous; start it at column 0")
    if not after.strip():
        raise MarkdownRefused(number, "an empty heading is ambiguous")
    if after[0] == "\t":
        raise MarkdownRefused(number, f"{name} separated from its text by a tab is ambiguous")
    title = after.strip()
    if _CLOSING.match(title):
        raise MarkdownRefused(number, f"{name} with a closing # sequence is ambiguous")
    return level, title


def _thematic_break(text: str) -> bool:
    indent = _spaces(text)
    if indent > 3 or indent == len(text) or text[indent] not in "-*_":
        return False
    marker, count = text[indent], 0
    for char in text[indent:]:
        if char == marker:
            count += 1
        elif char not in " \t":
            return False
    return count >= 3


def _deeper_heading(text: str) -> bool:
    if _spaces(text) > 3:
        return False
    rest = text[_spaces(text):]
    level = _run(rest, "#")
    return 2 < level <= 6 and (len(rest) == level or rest[level] in " \t")


def _trimmed(lines: list[str]) -> str:
    start, end = 0, len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return "\n".join(lines[start:end])


def parse_markdown(text: str) -> dict[str, Any]:
    """Read Markdown into the charter's model (MarkdownCodec): refuses what the codec refuses."""
    if not text:
        return {"preamble": "", "sections": []}
    if text[0] == "﻿":
        raise MarkdownRefused(1, "a byte order mark is not admitted")
    if "\r" in text:
        raise MarkdownRefused(text[: text.index("\r")].count("\n") + 1, "a carriage return is not admitted")
    lines = text.split("\n")
    if text.endswith("\n"):
        lines.pop()
    model: dict[str, Any] = {}
    start = 0
    if lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise MarkdownRefused(1, "unterminated frontmatter: no closing --- line") from None
        raw = "\n".join(lines[1:end])
        try:
            front = {} if not raw.strip() else load_yaml(raw + "\n")
        except yaml.YAMLError as exc:
            raise MarkdownRefused(1, f"frontmatter is not valid YAML: {exc}") from exc
        if not isinstance(front, dict) or not all(isinstance(key, str) for key in front):
            raise MarkdownRefused(1, "frontmatter must be a YAML mapping with string keys")
        model["frontmatter"] = front
        start = end + 1

    preamble: list[str] = []
    current = preamble
    titles: list[str] = []
    bodies: list[list[str]] = []
    title_line, any_block = 0, False
    fence: tuple[str, int, int] | None = None
    under_paragraph = False
    for offset, line in enumerate(lines[start:]):
        number = start + offset + 1
        if fence:
            stripped = line[_spaces(line):]
            if _run(stripped, fence[0]) >= fence[1] and not stripped[_run(stripped, fence[0]):].strip(" "):
                fence = None
            current.append(line)
            under_paragraph = False
            continue
        opened = _fence_opener(line)
        if opened:
            fence = (*opened, number)
            current.append(line)
            any_block = True
            under_paragraph = False
            continue
        if not line.strip():
            current.append(line)
            under_paragraph = False
            continue
        heading = _heading(line, number)
        if heading:
            level, title = heading
            under_paragraph = False
            if level == 1:
                if "title" in model:
                    raise MarkdownRefused(number, f"a second H1 (the first is at line {title_line})")
                if any_block:
                    raise MarkdownRefused(number, "an H1 that is not the first block")
                model["title"], title_line = title, number
            else:
                current = []
                titles.append(title)
                bodies.append(current)
            any_block = True
            continue
        if under_paragraph and _SETEXT.match(line):
            raise MarkdownRefused(number, "a setext heading underline is ambiguous; use an ATX heading or a blank line")
        current.append(line)
        any_block = True
        under_paragraph = not _thematic_break(line) and not _deeper_heading(line)
    if fence:
        raise MarkdownRefused(fence[2], f"unclosed fence opened at line {fence[2]}")
    model["preamble"] = _trimmed(preamble)
    model["sections"] = [{"title": t, "content": _trimmed(b)} for t, b in zip(titles, bodies, strict=True)]
    return model


# --------------------------------------------------------------------------- validation


@dataclass
class PackReport:
    pack: str
    checked: int = 0
    skipped: int = 0
    violations: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


def _short(message: str, limit: int = 300) -> str:
    return message if len(message) <= limit else message[: limit - 3] + "..."


def classify(contract: Contract, relative: str) -> tuple[str, Rule | None]:
    """The charter's classification of a path relative to the directory holding the packs."""
    for kind, rules in (("file", contract.files), ("excluded", contract.exclusions), ("retired", contract.retired)):
        for rule in rules:
            if rule.regex.match(relative):
                return kind, rule
    for rule in contract.payloads:
        if rule.regex.match(relative):
            return "payload", rule
    return "unclassified", None


#: Files the charter's ADR-0036 file table names as pack content without a schema (README.md,
#: PROVENANCE.md, a skill's ``*.skill.md`` body), which file-kinds.yaml does not list. Everything
#: else of .yaml/.yml/.md that no rule classifies is a violation. Globs match like the contract's.
UNCLASSIFIED_ALLOWANCES = tuple(glob_to_regex(glob) for glob in ("**/README.md", "*/PROVENANCE.md", "**/*.skill.md"))
CHECKED_SUFFIXES = frozenset({".yaml", ".yml", ".md"})


def validate_pack(pack_dir: Path, contract: Contract) -> PackReport:
    """Validate every file of one pack directory; violations are sorted and path-relative."""
    if not pack_dir.is_dir():
        raise GateError(f"{pack_dir} is not a directory")
    report = PackReport(pack=pack_dir.name)
    manifest: dict[str, Any] | None = None
    for path in sorted(p for p in pack_dir.rglob("*") if p.is_file() and not p.is_symlink()):
        inside = path.relative_to(pack_dir).as_posix()
        relative = f"{pack_dir.name}/{inside}"
        kind, rule = classify(contract, relative)
        if kind == "retired" and rule is not None:
            report.violations.append(f"{relative}: retired layout: {rule.reason}")
            continue
        if kind != "file" or rule is None:
            tokens = path.name.rsplit(".", 2)
            if kind == "unclassified" and path.suffix == ".yaml" and len(tokens) == 3 and tokens[1] in KNOWN_KIND_TOKENS:
                raise GateError(f"{relative}: a `{tokens[1]}` file has no schema mapping in file-kinds.yaml")
            if kind == "unclassified" and path.suffix in CHECKED_SUFFIXES and not any(
                allowed.match(relative) for allowed in UNCLASSIFIED_ALLOWANCES
            ):
                report.violations.append(f"{relative}: unclassified: no file-kinds.yaml rule covers this file")
                continue
            report.skipped += 1
            continue
        validator = contract.validators.get(rule.schema or "")
        if validator is None:
            raise GateError(f"{relative}: rule {rule.match!r} names schema {rule.schema!r}, which is not loaded")
        try:
            # Bytes, not read_text: universal newlines would turn a CR into LF before the Markdown
            # reader could refuse it, as the charter does.
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise GateError(f"{relative}: unreadable: {exc!r}") from exc
        report.checked += 1
        try:
            document = parse_markdown(text) if rule.content_form == "markdown" else load_yaml(text)
        except (yaml.YAMLError, MarkdownRefused) as exc:
            report.violations.append(f"{relative}: not readable as {rule.content_form}: {_short(str(exc))}")
            continue
        errors = sorted(validator.iter_errors(document), key=lambda e: (list(map(str, e.absolute_path)), e.message))
        for error in errors:
            where = "/" + "/".join(str(part) for part in error.absolute_path)
            report.violations.append(f"{relative}: {rule.schema} schema at {where}: {_short(error.message)}")
        if inside == MANIFEST_NAME and rule.schema == "pack-manifest" and not errors:
            manifest = document
    if manifest is not None:
        for stale in stale_manifest_fields(manifest, _bytes_reader(pack_dir)):
            report.violations.append(
                f"{pack_dir.name}/{MANIFEST_NAME}: stale manifest: {stale}; run `{REGENERATE_COMMAND} {pack_dir}`"
            )
    if report.checked == 0:
        raise GateError(f"{pack_dir}: no pack file was checked; the gate would prove nothing")
    return report


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("packs", nargs="*", type=Path, help="pack directories that must validate")
    parser.add_argument("--expect-invalid", action="append", default=[], type=Path, metavar="PACK",
                        help="a pack directory that must produce schema violations (non-vacuity)")
    parser.add_argument("--regenerate-manifest", action="append", default=[], type=Path, metavar="PACK",
                        help="restamp the content_hash and manifest_hash fields of PACK/pack-manifest.yaml "
                             "(membership is kept), then validate as usual")
    parser.add_argument("--contract", type=Path, help="directory holding file-kinds.yaml and schemas/")
    args = parser.parse_args(argv)
    if not args.packs and not args.expect_invalid and not args.regenerate_manifest:
        parser.error("give at least one pack directory")
    try:
        for pack in args.regenerate_manifest:
            for path in regenerate_manifest(pack):
                print(f"::warning file={pack}::{path} is listed in {MANIFEST_NAME} but has no file")
            print(f"regenerated: {pack / MANIFEST_NAME}")
        if not args.packs and not args.expect_invalid:
            return EXIT_OK
        contract = contract_for(args.contract)
        print(f"charter contract: {args.contract or os.environ.get('CHARTER_CONTRACT_DIR') or CHARTER_COMMIT}; "
              f"{len(contract.validators)} schemas loaded")
        status = EXIT_OK
        for pack in args.packs:
            report = validate_pack(pack, contract)
            for line in report.violations:
                print(f"::error file={pack}::{line}")
            print(f"{'ok' if report.ok else 'FAIL'}: {pack} ({report.checked} files checked, "
                  f"{report.skipped} excluded or payload, {len(report.violations)} violations)")
            status = status or (EXIT_OK if report.ok else EXIT_INVALID)
        for pack in args.expect_invalid:
            report = validate_pack(pack, contract)
            if report.ok:
                print(f"::error file={pack}::{pack} is an invalid fixture but passed schema validation; the gate is vacuous")
                status = EXIT_INVALID
            else:
                print(f"ok: {pack} fails validation as expected ({len(report.violations)} violations)")
    except GateError as exc:
        print(f"::error::cannot judge, failing closed: {exc}")
        return EXIT_GATE
    return status


if __name__ == "__main__":
    sys.exit(main())
