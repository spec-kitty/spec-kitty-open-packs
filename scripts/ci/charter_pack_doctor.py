#!/usr/bin/env python3
"""Gate every pack on the charter's whole-pack check, pack-doctor, at the charter pin (#252, #345; charter ADR-0075
decision 9, ADR-0083).

pack-doctor is the charter's own CLI over its pack validation. ``validate --round-trip --full`` checks each pack
(PACK), the closure of the set (CLOSURE), each pack's substep delegations, references and step enhancements' targets
against the packs it reaches over ``depends_on`` (REFERENCES, as registration does), and the production round trip by
meaning (ROUND_TRIP). What each check judges, the report and the exit codes are the charter's guide,
``docs/guides/check-packs.md`` in spec-kitty-charter. This script runs the jar of the pin
(``scripts/ci/charter_pack_doctor_jar.sh``) and judges what it says, fail-closed::

    python3 scripts/ci/charter_pack_doctor.py --jar path/to/pack-doctor-<version>.jar [--report-dir DIR]

1. **The set.** Every pack under ``packs/`` and ``tests/fixtures/valid/`` (each directory with a ``pack.yaml``) is
   checked together, ``--pack <dir>`` each, with ``--round-trip --full``. It passes only when pack-doctor exits 0 with
   a ``PackDoctorReport`` that ran all four checks (none skipped), names exactly those packs and holds no problem,
   holds no top-level key but ``tool``, ``inputs``, ``checks``, ``packs``, ``skipped``, ``problems`` and ``summary``,
   names ``pack-doctor`` as its tool, records ``--full`` and ``--round-trip`` among its options, states the exit code
   the run had, and printed no warning other than ``file_not_held``.
   - **Any other exit code fails.** pack-doctor exits 2 on a usage fault or a failure outside a pack read (the run
     directory, the report file), with nothing on standard output: nothing was judged.
   - **A warning other than ``file_not_held`` fails**, as it did in charter's driftTest, which this replaces.
     ``file_not_held`` is printed as a notice: a stray file warns, never fails (operator ruling R34, #331).
2. **Non-vacuity.** Every pack under ``tests/fixtures/invalid/`` is checked alone, from a copy without its own
   ``expected-code`` (pack-doctor models no such file, so it would be red for that file alone). Its ``expected-code``
   names, in a ``pack-doctor:`` line, a code that must appear in a problem or one of its violations, with exit 1. A
   fixture that passes, or is refused another way, fails the gate.

``--report`` writes each run's report to a file outside every pack checked: under ``--report-dir`` when given, kept with
the run's stderr; else in a temporary directory. The JSON on standard output stays the source this gate parses.

What pack-doctor does not check stays in this repository's schema pass (``validate_pack_schemas.py``): the house rules
only, each beside the charter ruling that leaves it to open-packs (#348).

Standard library only. Needs Java 25 (``JAVA_HOME`` is honoured, or ``--java``). Runs pack-doctor under
``LC_ALL=C.UTF-8`` (under the POSIX locale a non-ASCII file name is exit 2). Exit 0 when the gate passed, 1 when it
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
CHECKS = ("PACK", "CLOSURE", "REFERENCES", "ROUND_TRIP")
FILE_NOT_HELD = "file_not_held"
#: The top-level keys of a ``PackDoctorReport`` (charter ``contracts/charter/schemas/PackDoctorReport.yaml``). Any
#: other key is something this gate does not read, so cannot judge.
REPORT_KEYS = ("tool", "inputs", "checks", "packs", "skipped", "problems", "summary")
TOOL = "pack-doctor"
CODE = re.compile(r"[a-z][a-z0-9_]*")
WARNING = re.compile(r"warning: (?P<pack>[^:]+): (?P<code>\S+) (?P<rest>.*)")
#: The JVM prints these on stderr when JAVA_TOOL_OPTIONS or _JAVA_OPTIONS is set; they are not pack-doctor's.
JVM_NOISE = ("Picked up ",)
TIMEOUT_SECONDS = 600
TAIL_LINES = 20


class GateError(Exception):
    """The gate cannot run; nothing was judged."""


@dataclass
class Result:
    """One pack-doctor run: its exit code, its parsed report (None when stdout was not one) and its stderr."""

    exit_code: int
    report: dict[str, Any] | None
    stderr: str


# ------------------------------------------------------------------------------------------- reading a run

def unparsed_warnings(stderr: str) -> list[str]:
    """stderr lines that look like a warning but not like pack-doctor's format: a changed format must not pass silently."""
    return [line for line in stderr.splitlines()
            if line.strip().lower().startswith("warning") and not WARNING.fullmatch(line.strip())]


def warnings(stderr: str) -> list[tuple[str, str, str]]:
    """pack-doctor's ``warning: <pack>: <code> <file>: <detail>`` lines, as (pack, code, rest)."""
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

def _no_verdict(result: Result) -> list[str]:
    return ["pack-doctor exited 2 (a usage fault, a failure outside a pack read, or an internal error) and judged "
            "nothing; the gate fails closed",
            *(f"  {line}" for line in _tail(result.stderr))]


def report_faults(result: Result) -> list[str]:
    """What makes a report unreadable as this run's ``PackDoctorReport``: an unknown key, another tool, options
    other than ``--full --round-trip``, ``checks`` that is not an ordered list of known checks, or a summary whose exit
    code is not the run's. Each fails closed."""
    document = result.report or {}
    faults = [f"pack-doctor's report holds a key this gate cannot read, so cannot judge: '{key}' "
              f"(known: {', '.join(REPORT_KEYS)}); a changed format must not pass silently"
              for key in sorted(set(document) - set(REPORT_KEYS))]
    ran = document.get("checks")
    if not isinstance(ran, list) or not all(isinstance(check, str) for check in ran):
        faults.append(f"the report's checks is {ran!r}, not a list of check names")
    elif any(check not in CHECKS for check in ran) or ran != [check for check in CHECKS if check in ran]:
        faults.append(f"the report's checks {ran} are not a subset of {list(CHECKS)} in that order")
    tool = document.get("tool")
    name = tool.get("name") if isinstance(tool, dict) else None
    if name != TOOL:
        faults.append(f"the report's tool.name is {name!r}, not {TOOL!r}: it is not pack-doctor's report")
    inputs = document.get("inputs")
    options = inputs.get("options") if isinstance(inputs, dict) else None
    options = options if isinstance(options, dict) else {}
    for option, flag in (("full", "--full"), ("round_trip", "--round-trip")):
        if options.get(option) is not True:
            faults.append(f"the report's inputs.options.{option} is {options.get(option)!r}: the run did not record "
                          f"{flag}, so its verdict is not the gate's")
    summary = document.get("summary")
    stated = summary.get("exit_code") if isinstance(summary, dict) else None
    if type(stated) is not int or stated != result.exit_code:  # a boolean is not an exit code (False == 0)
        faults.append(f"the report's summary.exit_code is {stated!r}, but pack-doctor exited {result.exit_code}; "
                      "a report that disagrees with its run cannot be judged")
    return faults


def judge_set(result: Result, names: list[str]) -> list[str]:
    """The failures of the run over every pack and valid fixture; empty when it passed."""
    if result.exit_code == 2:
        return _no_verdict(result)
    failures = []
    if result.exit_code not in (0, 1):
        failures.append(f"pack-doctor exited {result.exit_code}, which it never does on a verdict; the gate fails closed")
        failures += [f"  {line}" for line in _tail(result.stderr)]
    document = result.report
    if document is None:
        return failures or ["pack-doctor wrote no report on standard output; the gate fails closed",
                            *(f"  {line}" for line in _tail(result.stderr))]
    # A skipped check's reason names the cause (a pack that cannot be read, e.g. a missing companion): it leads.
    for skipped in document.get("skipped") or []:
        failures.append(f"pack-doctor skipped {skipped.get('check') if isinstance(skipped, dict) else skipped}: "
                        f"{skipped.get('reason') if isinstance(skipped, dict) else ''}".rstrip(": "))
    failures += report_faults(result)
    if result.exit_code == 1 or document.get("problems"):
        failures.append(f"pack-doctor refused the packs (exit {result.exit_code}):")
        failures += [f"  {line}" for line in problem_lines(document)] or ["  (no problem in the report)"]
    ran = document.get("checks") if isinstance(document.get("checks"), list) else []
    for check in CHECKS:
        if check not in ran:
            failures.append(f"pack-doctor did not run {check}; a verdict without it proves nothing")
    reported = sorted(str(pack.get("name")) for pack in document.get("packs") or [] if isinstance(pack, dict))
    if reported != sorted(names):
        missing, extra = sorted(set(names) - set(reported)), sorted(set(reported) - set(names))
        twice = sorted({name for name in reported if reported.count(name) > 1})
        failures.append(f"pack-doctor judged other packs than it was given (missing: {missing or 'none'}; "
                        f"unexpected: {extra or 'none'}; reported twice: {twice or 'none'})")
    for pack, code, rest in warnings(result.stderr):
        if code != FILE_NOT_HELD:
            failures.append(f"pack-doctor warns {pack}: {code} {rest} (every warning but file_not_held fails, as in driftTest)")
    for line in unparsed_warnings(result.stderr):
        failures.append(f"pack-doctor printed a warning this gate cannot read, so cannot judge: {line.strip()}")
    return failures


def judge_invalid(result: Result, expected: str) -> list[str]:
    """The failures of an invalid fixture's run against its ``pack-doctor:`` expectation; empty when it was refused so."""
    if result.exit_code == 0:
        return [f"pack-doctor accepts it (exit 0), but must refuse it with {expected}"]
    if result.exit_code != 1 or result.report is None:
        return [f"pack-doctor gave no verdict (exit {result.exit_code}), but must refuse it with {expected}",
                *(f"  {line}" for line in _tail(result.stderr))]
    faults = report_faults(result)  # a refusal read from a report the gate cannot read proves nothing either
    if faults:
        return faults
    found = codes(result.report)
    if expected not in found:
        return [f"pack-doctor refused it with {sorted(found)}, not with {expected}",
                *(f"  {line}" for line in problem_lines(result.report))]
    return []


def expected_pack_doctor(fixture: Path) -> str:
    """The ``pack-doctor:`` line of a fixture's ``expected-code``: the code pack-doctor refuses it with."""
    path = fixture / "expected-code"
    if not path.is_file():
        raise GateError(f"{fixture}: no expected-code file")
    found = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = (part.strip() for part in raw.split("#", 1)[0].partition(":"))
        if separator and key == "pack-doctor":
            if found is not None:
                raise GateError(f"{path}: two 'pack-doctor:' lines")
            found = value
    if found is None:
        raise GateError(f"{path}: no 'pack-doctor:' line; name the code pack-doctor refuses this fixture with")
    if not CODE.fullmatch(found):
        raise GateError(f"{path}: 'pack-doctor: {found}' is not a code (lower-case words joined by underscores)")
    return found


# ---------------------------------------------------------------------------------------------- running

def command_for(java: str, jar: Path, packs: list[Path], report_file: Path) -> list[str]:
    """The argument vector of one ``pack-doctor validate --round-trip --full`` run, from checked values only.

    ``java`` and ``jar`` must be existing files, ``jar`` a ``.jar``; every pack is an existing directory, given by
    its resolved absolute path, so no value can be read as an option; ``report_file`` is a resolved absolute path
    outside every pack (pack-doctor refuses a report inside one). The vector is run without a shell."""
    if not Path(java).is_file() or not os.access(java, os.X_OK):
        raise GateError(f"{java} is not an executable file")
    if not jar.is_file() or jar.suffix != ".jar":
        raise GateError(f"{jar} is not a .jar file")
    resolved = [pack.resolve() for pack in packs]
    for pack in resolved:
        if not pack.is_dir() or not pack.is_absolute():
            raise GateError(f"{pack} is not a pack directory")
    report = report_file.resolve()
    if not report.is_absolute() or any(report == pack or pack in report.parents for pack in resolved):
        raise GateError(f"the report file {report} must lie outside every pack checked")
    return [str(Path(java).resolve()), "-jar", str(jar.resolve()), "validate",
            *(arg for pack in resolved for arg in ("--pack", str(pack))), "--round-trip", "--full",
            "--report", str(report)]


def run(java: str, jar: Path, packs: list[Path], report_file: Path | None) -> Result:
    """One pack-doctor run. ``report_file`` keeps its ``--report`` YAML and, beside it, its stderr; without one the
    report goes to a temporary directory and is dropped. The parsed source is the JSON on standard output."""
    with tempfile.TemporaryDirectory(prefix="pack-doctor-report-") as scratch:
        target = report_file if report_file is not None else Path(scratch) / "report.yaml"
        return _run(java, jar, packs, target, keep=report_file is not None)


def _run(java: str, jar: Path, packs: list[Path], report_file: Path, keep: bool) -> Result:
    command = command_for(java, jar, packs, report_file)  # refuses a report inside a pack before anything is made
    report_file.parent.mkdir(parents=True, exist_ok=True)
    environment = {**os.environ, "LC_ALL": "C.UTF-8"}  # a non-ASCII file name under the POSIX locale is exit 2
    try:
        # A justified suppression, not a removed taint flow: S8701/S8705 read the CLI as untrusted, and --java or
        # JAVA_HOME can still name any executable. The values come only from this repository's own workflow;
        # command_for checks each element (existing files, resolved absolute directories) and no shell runs it.
        done = subprocess.run(command, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False,  # NOSONAR
                              env=environment)
    except subprocess.TimeoutExpired as error:
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        return Result(exit_code=-1, report=None, stderr=f"{stderr}\npack-doctor ran past {TIMEOUT_SECONDS} s and was stopped")
    except OSError as error:
        raise GateError(f"cannot run {java}: {error}") from error
    if keep:
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
    parser.add_argument("--jar", required=True, type=Path, help="the pack-doctor jar of the pin")
    parser.add_argument("--root", type=Path, default=ROOT, help="the repository checkout (default: this one)")
    parser.add_argument("--report-dir", type=Path, help="where to keep each run's --report YAML and its stderr")
    parser.add_argument("--java", help="the java to run it with (default: $JAVA_HOME/bin/java, else java)")
    args = parser.parse_args(argv)
    failed = False
    try:
        if not args.jar.is_file():
            raise GateError(f"{args.jar} is not a file; obtain it with scripts/ci/charter_pack_doctor_jar.sh")
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
        expectations = {fixture: expected_pack_doctor(fixture) for fixture in fixtures}
        names = [pack.name for pack in packs]
        if len(set(names)) != len(names):
            raise GateError(f"two packs share a directory name: {sorted(n for n in names if names.count(n) > 1)}")

        report_dir = args.report_dir.resolve() if args.report_dir else None
        print(f"pack-doctor {args.jar.name} validate over {len(packs)} packs and valid fixtures, with --round-trip --full")
        result = run(java, args.jar, packs, report_dir / "packs.yaml" if report_dir else None)
        for pack, code, rest in warnings(result.stderr):
            if code == FILE_NOT_HELD:
                print(f"::notice::pack-doctor: {pack}: {code} {rest}")
        failures = judge_set(result, names)
        for line in failures:
            print(f"::error::pack-doctor: {line}" if not line.startswith("  ") else line)
        if failures:
            failed = True
        else:
            print(f"ok: pack-doctor passes every pack ({', '.join(CHECKS)}; {len(warnings(result.stderr))} file_not_held notices)")

        with tempfile.TemporaryDirectory(prefix="pack-doctor-invalid-") as scratch:
            for fixture, expected in expectations.items():
                copy = Path(scratch) / fixture.name
                shutil.copytree(fixture, copy, symlinks=True)
                (copy / "expected-code").unlink()  # the fixture's own file, at its root only
                report_file = report_dir / f"invalid-{fixture.name}.yaml" if report_dir else None
                found = judge_invalid(run(java, args.jar, [copy], report_file), expected)
                if found:
                    failed = True
                    print(f"::error::pack-doctor: invalid fixture {fixture.name}: {found[0]}")
                    for line in found[1:]:
                        print(line)
                else:
                    print(f"ok: pack-doctor refuses invalid fixture {fixture.name} as expected ({expected})")
    except GateError as error:
        print(f"::error::pack-doctor: cannot run, failing closed: {error}")
        return EXIT_CANNOT_RUN
    return EXIT_FAILED if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
