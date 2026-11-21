#!/usr/bin/env python3
"""Gate every pack on the charter's whole-pack check, pack-check, at the charter pin (#252; charter ADR-0075 decision 9).

pack-check is the charter's own CLI over its pack validation: per pack (PACK), the closure of the set (CLOSURE) and,
with ``--round-trip``, the production round trip by meaning (ROUND_TRIP). This script runs the jar of the pin
(``scripts/ci/charter_pack_check_jar.sh``) and judges what it says, fail-closed::

    python3 scripts/ci/charter_pack_check.py --jar path/to/pack-check-<version>.jar [--report-dir DIR]

1. **The set.** Every pack under ``packs/`` and ``tests/fixtures/valid/`` (each directory with a ``pack.yaml``) is
   checked together, ``--pack <dir>`` each, with ``--round-trip``. It passes only when pack-check exits 0 with a
   report that ran all three checks (none skipped), names exactly those packs and holds no problem, holds no
   top-level key but ``checks``, ``packs``, ``problems`` and ``skipped``, and printed no warning other than
   ``file_not_held``.
   - **Any other exit code fails.** pack-check exits 2 on a usage or I/O failure, and rc.3 also exits 2, with a stack
     trace and no report, on a malformed ``pack_version`` (spec-kitty-charter#624). Until #624 lands, exit 2 is a
     failure of the gate, never an infrastructure skip (operator ruling R32).
   - **A warning other than ``file_not_held`` fails**, as it did in charter's driftTest, which this replaces.
     ``file_not_held`` is printed as a notice: pack-check only warns on a stray file, and the schema pass owns the
     stray-file rule (``validate_pack_schemas.NOT_HELD_ALLOWANCES``, #249), which is stricter.
2. **Non-vacuity.** Every pack under ``tests/fixtures/invalid/`` is checked alone, from a copy without its own
   ``expected-code`` (pack-check models no such file, so it would be red for that file alone). Its ``expected-code``
   names what pack-check must say in a ``pack-check:`` line: a code that must appear in a problem or one of its
   violations, with exit 1; or ``failed``, which expects exactly the charter#624 crash: exit 2, no report, and an
   ``internal error`` on stderr naming ``pack_version``. A usage or I/O failure, or another crash, does not match it.
   A fixture that passes, or is refused another way, fails the gate.

What pack-check does NOT check, and so stays in this repository's schema pass (``validate_pack_schemas.py``), as
measured against rc.3 with ``--round-trip``: an ignored file other than a ``README.md`` note (only a ``file_not_held``
warning), a preset ``must_have`` item no pack of the preset pack's closure holds (``requiredNotHeld``), and a preset id
no pack declares. All three pass pack-check with exit 0. (A stale manifest hash is refused under ``--round-trip``, as
``round_trip_red``; the schema pass keeps its own check as the fast pre-check that names the fix.)

Standard library only. Needs Java 25 (``JAVA_HOME`` is honoured, or ``--java``). Exit 0 when the gate passed, 1 when it
failed, 2 when it could not run (no jar, no java, no pack, no invalid fixture).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXIT_OK, EXIT_FAILED, EXIT_CANNOT_RUN = 0, 1, 2
ROOT = Path(__file__).resolve().parents[2]
CHECKS = ("PACK", "CLOSURE", "ROUND_TRIP")
FILE_NOT_HELD = "file_not_held"
#: The top-level keys of rc.3's report. Any other key is something this gate does not read (a warnings array, say).
REPORT_KEYS = ("checks", "packs", "problems", "skipped")
#: pack-check exit 2 on a malformed pack_version, with no report: https://github.com/spec-kitty/spec-kitty-charter/issues/624
CRASH_ISSUE = "spec-kitty-charter#624"
#: The ``pack-check:`` value that expects the charter#624 crash. No charter refusal code is named ``failed``.
FAILED = "failed"
#: What the charter#624 crash prints: ``pack-check: internal error: ... pack_version '...' is not a PEP 440 version``.
CRASH_SIGN = re.compile(r"internal error:.*pack_version '[^'\n]*' is not a PEP 440 version", re.S)
CODE = re.compile(r"[a-z][a-z0-9_]*")
WARNING = re.compile(r"warning: (?P<pack>[^:]+): (?P<code>\S+) (?P<rest>.*)")
#: The JVM prints these on stderr when JAVA_TOOL_OPTIONS or _JAVA_OPTIONS is set; they are not pack-check's.
JVM_NOISE = ("Picked up ",)
TIMEOUT_SECONDS = 600
TAIL_LINES = 20


class GateError(Exception):
    """The gate cannot run; nothing was judged."""


@dataclass
class Result:
    """One pack-check run: its exit code, its parsed report (None when stdout was not one) and its stderr."""

    exit_code: int
    report: dict[str, Any] | None
    stderr: str


# ------------------------------------------------------------------------------------------- reading a run

def unparsed_warnings(stderr: str) -> list[str]:
    """stderr lines that look like a warning but not like pack-check's format: a changed format must not pass silently."""
    return [line for line in stderr.splitlines()
            if line.strip().lower().startswith("warning") and not WARNING.fullmatch(line.strip())]


def warnings(stderr: str) -> list[tuple[str, str, str]]:
    """pack-check's ``warning: <pack>: <code> <file>: <detail>`` lines, as (pack, code, rest)."""
    found = []
    for line in stderr.splitlines():
        match = WARNING.fullmatch(line.strip())
        if match:
            found.append((match["pack"], match["code"], match["rest"]))
    return found


def _tail(stderr: str) -> list[str]:
    lines = [line for line in stderr.splitlines()
             if line.strip() and not line.startswith(JVM_NOISE) and not line.lstrip().startswith("at ")]
    return lines[-TAIL_LINES:]


def problem_lines(document: dict[str, Any] | None) -> list[str]:
    """One line per problem and per violation of a report."""
    lines = []
    for problem in (document or {}).get("problems") or []:
        if not isinstance(problem, dict):
            lines.append(f"problem: {problem!r}")
            continue
        where = problem.get("instance", "")
        lines.append(f"problem {problem.get('code')}: {problem.get('detail')} {where}".rstrip())
        for violation in problem.get("violations") or []:
            if isinstance(violation, dict):
                lines.append(f"  {violation.get('code')} at {violation.get('pointer')}: {violation.get('detail')}")
    return lines


def codes(document: dict[str, Any] | None) -> set[str]:
    """Every code a report's problems and their violations carry."""
    found: set[str] = set()
    for problem in (document or {}).get("problems") or []:
        if isinstance(problem, dict):
            found.add(str(problem.get("code")))
            found.update(str(v.get("code")) for v in problem.get("violations") or [] if isinstance(v, dict))
    return found


# ---------------------------------------------------------------------------------------------- judging

def _crash(result: Result) -> list[str]:
    return [f"pack-check exited 2 (a usage or I/O failure, or a crash) and gave no verdict; the gate fails closed. "
            f"rc.3 crashes this way on a malformed pack_version ({CRASH_ISSUE}): look for one first",
            *(f"  {line}" for line in _tail(result.stderr))]


def judge_set(result: Result, names: list[str]) -> list[str]:
    """The failures of the run over every pack and valid fixture; empty when it passed."""
    if result.exit_code == 2:
        return _crash(result)
    failures = []
    if result.exit_code not in (0, 1):
        failures.append(f"pack-check exited {result.exit_code}, which it never does on a verdict; the gate fails closed")
        failures += [f"  {line}" for line in _tail(result.stderr)]
    document = result.report
    if document is None:
        return failures or ["pack-check wrote no report on standard output; the gate fails closed",
                            *(f"  {line}" for line in _tail(result.stderr))]
    for key in sorted(set(document) - set(REPORT_KEYS)):
        failures.append(f"pack-check's report holds a key this gate cannot read, so cannot judge: '{key}' "
                        f"(known: {', '.join(REPORT_KEYS)}); a changed format must not pass silently")
    if result.exit_code == 1 or document.get("problems"):
        failures.append(f"pack-check refused the packs (exit {result.exit_code}):")
        failures += [f"  {line}" for line in problem_lines(document)] or ["  (no problem in the report)"]
    ran = document.get("checks") or []
    for check in CHECKS:
        if check not in ran:
            failures.append(f"pack-check did not run {check}; a verdict without it proves nothing")
    for skipped in document.get("skipped") or []:
        failures.append(f"pack-check skipped {skipped.get('check') if isinstance(skipped, dict) else skipped}: "
                        f"{skipped.get('reason') if isinstance(skipped, dict) else ''}".rstrip(": "))
    reported = sorted(str(pack.get("name")) for pack in document.get("packs") or [] if isinstance(pack, dict))
    if reported != sorted(names):
        missing, extra = sorted(set(names) - set(reported)), sorted(set(reported) - set(names))
        failures.append(f"pack-check judged other packs than it was given (missing: {missing or 'none'}; "
                        f"unexpected: {extra or 'none'})")
    for pack, code, rest in warnings(result.stderr):
        if code != FILE_NOT_HELD:
            failures.append(f"pack-check warns {pack}: {code} {rest} (every warning but file_not_held fails, as in driftTest)")
    for line in unparsed_warnings(result.stderr):
        failures.append(f"pack-check printed a warning this gate cannot read, so cannot judge: {line.strip()}")
    return failures


def judge_invalid(result: Result, expected: str) -> list[str]:
    """The failures of an invalid fixture's run against its ``pack-check:`` expectation; empty when it was refused so."""
    if expected == FAILED:
        crashed = result.exit_code == 2 and result.report is None and CRASH_SIGN.search(result.stderr)
        if crashed:
            return []
        return [f"expected the {CRASH_ISSUE} crash (exit 2, no report, an internal error naming pack_version), got "
                f"exit {result.exit_code}{' with a report' if result.report is not None else ''}. If pack-check now "
                "reports this fault, name the code it gives in the fixture's 'pack-check:' line",
                *(f"  {line}" for line in problem_lines(result.report)),
                *(f"  {line}" for line in _tail(result.stderr))]
    if result.exit_code == 0:
        return [f"pack-check accepts it (exit 0), but must refuse it with {expected}"]
    if result.exit_code != 1 or result.report is None:
        return [f"pack-check gave no verdict (exit {result.exit_code}), but must refuse it with {expected}",
                *(f"  {line}" for line in _tail(result.stderr))]
    found = codes(result.report)
    if expected not in found:
        return [f"pack-check refused it with {sorted(found)}, not with {expected}",
                *(f"  {line}" for line in problem_lines(result.report))]
    return []


def expected_pack_check(fixture: Path) -> str:
    """The ``pack-check:`` line of a fixture's ``expected-code``: a code, or ``failed``."""
    path = fixture / "expected-code"
    if not path.is_file():
        raise GateError(f"{fixture}: no expected-code file")
    found = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = (part.strip() for part in raw.split("#", 1)[0].partition(":"))
        if separator and key == "pack-check":
            if found is not None:
                raise GateError(f"{path}: two 'pack-check:' lines")
            found = value
    if found is None:
        raise GateError(f"{path}: no 'pack-check:' line; name the code pack-check refuses this fixture with (or '{FAILED}')")
    if not CODE.fullmatch(found):
        raise GateError(f"{path}: 'pack-check: {found}' is not a code (lower-case words joined by underscores) or '{FAILED}'")
    return found


# ---------------------------------------------------------------------------------------------- running

def command_for(java: str, jar: Path, packs: list[Path]) -> list[str]:
    """The argument vector of one pack-check run, from checked values only.

    ``java`` and ``jar`` must be existing files, ``jar`` a ``.jar``; every pack is an existing directory, given by
    its resolved absolute path, so no value can be read as an option. The vector is run without a shell."""
    if not Path(java).is_file() or not os.access(java, os.X_OK):
        raise GateError(f"{java} is not an executable file")
    if not jar.is_file() or jar.suffix != ".jar":
        raise GateError(f"{jar} is not a .jar file")
    resolved = [pack.resolve() for pack in packs]
    for pack in resolved:
        if not pack.is_dir() or not pack.is_absolute():
            raise GateError(f"{pack} is not a pack directory")
    return [str(Path(java).resolve()), "-jar", str(jar.resolve()),
            *(arg for pack in resolved for arg in ("--pack", str(pack))), "--round-trip"]


def run(java: str, jar: Path, packs: list[Path], report_file: Path | None) -> Result:
    command = command_for(java, jar, packs)
    try:
        # A justified suppression, not a removed taint flow: S8701/S8705 read the CLI as untrusted, and --java or
        # JAVA_HOME can still name any executable. The values come only from this repository's own workflow;
        # command_for checks each element (existing files, resolved absolute directories) and no shell runs it.
        done = subprocess.run(command, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False)  # NOSONAR
    except subprocess.TimeoutExpired as error:
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return Result(exit_code=-1, report=None, stderr=f"{stderr}\npack-check ran past {TIMEOUT_SECONDS} s and was stopped")
    except OSError as error:
        raise GateError(f"cannot run {java}: {error}") from error
    if report_file is not None:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(done.stdout, encoding="utf-8")
        report_file.with_suffix(".stderr.txt").write_text(done.stderr, encoding="utf-8")
    try:
        document = json.loads(done.stdout) if done.stdout.strip() else None
    except json.JSONDecodeError:
        document = None
    if document is not None and not isinstance(document, dict):
        document = None
    return Result(exit_code=done.returncode, report=document, stderr=done.stderr)


def pack_dirs(parent: Path) -> list[Path]:
    if not parent.is_dir():
        return []
    return sorted(path for path in parent.iterdir() if path.is_dir() and (path / "pack.yaml").is_file())


def java_command(given: str | None) -> str:
    """The java to run: ``--java``, else ``$JAVA_HOME/bin/java``, else ``java`` on the PATH; an existing file."""
    if given:
        return given
    home = os.environ.get("JAVA_HOME")
    if home:
        return str(Path(home) / "bin" / "java")
    found = shutil.which("java")
    if found is None:
        raise GateError("no java: set JAVA_HOME, put java on the PATH, or pass --java")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--jar", required=True, type=Path, help="the pack-check jar of the pin")
    parser.add_argument("--root", type=Path, default=ROOT, help="the repository checkout (default: this one)")
    parser.add_argument("--report-dir", type=Path, help="where to keep each run's report and stderr")
    parser.add_argument("--java", help="the java to run it with (default: $JAVA_HOME/bin/java, else java)")
    args = parser.parse_args(argv)
    failed = False
    try:
        if not args.jar.is_file():
            raise GateError(f"{args.jar} is not a file; obtain it with scripts/ci/charter_pack_check_jar.sh")
        java = java_command(args.java)
        root = args.root.resolve()
        packs = pack_dirs(root / "packs") + pack_dirs(root / "tests" / "fixtures" / "valid")
        # Every directory there is a pack: one without a pack.yaml would otherwise be left out of the check unseen.
        for parent in (root / "packs", root / "tests" / "fixtures" / "valid"):
            stray = sorted(d.name for d in parent.iterdir() if d.is_dir() and not (d / "pack.yaml").is_file()) \
                if parent.is_dir() else []
            if stray:
                raise GateError(f"{parent.relative_to(root)}/ holds directories without a pack.yaml: {stray}")
        fixtures = sorted(p for p in (root / "tests" / "fixtures" / "invalid").glob("*") if p.is_dir())
        if not packs or not fixtures:
            raise GateError("no pack under packs/ or tests/fixtures/valid/, or no invalid fixture: the check would prove nothing")
        expectations = {fixture: expected_pack_check(fixture) for fixture in fixtures}
        names = [pack.name for pack in packs]
        if len(set(names)) != len(names):
            raise GateError(f"two packs share a directory name: {sorted(n for n in names if names.count(n) > 1)}")

        print(f"pack-check {args.jar.name} over {len(packs)} packs and valid fixtures, with --round-trip")
        result = run(java, args.jar, packs, args.report_dir / "packs.json" if args.report_dir else None)
        for pack, code, rest in warnings(result.stderr):
            if code == FILE_NOT_HELD:
                print(f"::notice::pack-check: {pack}: {code} {rest}")
        failures = judge_set(result, names)
        for line in failures:
            print(f"::error::pack-check: {line}" if not line.startswith("  ") else line)
        if failures:
            failed = True
        else:
            print(f"ok: pack-check passes every pack ({', '.join(CHECKS)}; {len(warnings(result.stderr))} file_not_held notices)")

        with tempfile.TemporaryDirectory(prefix="pack-check-invalid-") as scratch:
            for fixture, expected in expectations.items():
                copy = Path(scratch) / fixture.name
                shutil.copytree(fixture, copy, symlinks=True)
                (copy / "expected-code").unlink()  # the fixture's own file, at its root only
                report_file = args.report_dir / f"invalid-{fixture.name}.json" if args.report_dir else None
                found = judge_invalid(run(java, args.jar, [copy], report_file), expected)
                if found:
                    failed = True
                    print(f"::error::pack-check: invalid fixture {fixture.name}: {found[0]}")
                    for line in found[1:]:
                        print(line)
                else:
                    how = f"exit 2, no report ({CRASH_ISSUE})" if expected == FAILED else expected
                    print(f"ok: pack-check refuses invalid fixture {fixture.name} as expected ({how})")
    except GateError as error:
        print(f"::error::pack-check: cannot run, failing closed: {error}")
        return EXIT_CANNOT_RUN
    return EXIT_FAILED if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
