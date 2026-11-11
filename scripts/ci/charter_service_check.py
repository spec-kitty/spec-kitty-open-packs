#!/usr/bin/env python3
"""Prove every pack of this repository valid through the charter service (charter ADR-0070).

The charter no longer tests this repository's content; this repository proves its own packs against
the charter service at the commit pinned in ``charter.lock.yaml``. The service is the authority on
composition and on whole-pack registration. This script starts a built service jar and asks it, so
the same check runs in CI (``Charter service validation`` in ``.github/workflows/validate-packs.yml``)
and on a developer machine::

    python3 scripts/ci/charter_service_check.py --jar path/to/spec-kitty-charter-service.jar

Three phases, every one of which runs even when an earlier one failed:

1. **Composition.** Every pack under ``packs/`` and ``tests/fixtures/valid/`` is placed in a
   configuration root, ``<root>/packs/<directory name>/``, and the service is started over it. A pack
   declares its own level in ``pack.yaml`` (``pack_level``), so the root needs no other
   configuration (charter ADR-0038). ``GET /api/v1/offering`` must answer 200, name every pack at its
   declared level and resolve every ``depends_on`` entry. A refusal (``pack_unreadable``, a
   composition code) fails the run, printing the problem document.
2. **Registration.** Built-in is read-only to registration (charter ADR-0065 D3), so a scratch root
   holds the built-in pack only; every org and project pack is then sent whole, dependencies first,
   with ``PUT /api/v1/packs/{packId}`` and its registration polled until it ends. A ``refused``
   registration fails the run, printing its problem and violations. The composed offering of the
   resulting root must also answer 200.
3. **Non-vacuity.** Every pack under ``tests/fixtures/invalid/`` names, in its ``expected-code`` file,
   the code the service must refuse it with, once composed and once registered. A fixture the service
   accepts, or refuses with another code, fails the run: a service that passes everything is not a gate.

``expected-code`` holds ``key: value`` lines (``#`` starts a comment)::

    composition: pack_unreadable     # the code of the refusal of GET /offering
    registration: validation_failed  # the code of the refused registration's problem
    precheck: accepted               # optional; ``accepted`` = the per-pack schema pass cannot see it

Standard library only. Needs Java 25 for the jar (``JAVA_HOME`` is honoured). Exit 0 when every phase
passed, 1 when any check failed, 2 when the check could not run (no jar, the service would not start).
"""

from __future__ import annotations

import argparse
import fnmatch
import io
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

EXIT_OK, EXIT_FAILED, EXIT_CANNOT_RUN = 0, 1, 2
API = "/api/v1"
BUILT_IN = "built-in"
START_TIMEOUT_SECONDS = 90
REGISTRATION_TIMEOUT_SECONDS = 120  # the service's own deadline for one registration is 90 s
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024  # the service refuses a larger upload (413)
EXPECTED_CODE_KEYS = {"composition", "registration", "precheck"}
CODE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
#: Files a pack carries that a registration refuses as ``unmodelled`` ("a registration holds only
#: modelled files", ADR-0065): documentation, the active charter the CLI reads, and the mission template
#: notes. They are left out of the uploaded archive, and only these: any other file the service does not
#: model (a misspelt artifact file name, a new kind of file) is refused and fails the run. They stay
#: covered by the per-pack schema pass (``validate_pack_schemas.py``) and by composition, which reads the
#: pack directory itself. Matched with ``fnmatch`` against the path relative to the pack root.
NOT_REGISTERED = (
    "README.md",
    "PROVENANCE.md",
    "org-charter.yaml",
    "missions/*/templates/README.md",
    "missions/*/templates/plan-field-declaration.yaml",
)


class CannotRun(Exception):
    """The check could not be performed (as opposed to a pack being refused)."""


# --------------------------------------------------------------------------- pack metadata


def read_descriptor(pack: Path) -> dict[str, Any]:
    """The ``key: value`` and ``depends_on`` fields of ``pack.yaml`` this script needs.

    A small reader, not a YAML parser: the script is standard-library only so the CI job installs
    nothing. It reads the flat scalars and the ``pack_id`` of each ``depends_on`` entry; the service
    judges the file itself, so a descriptor this reader cannot understand is the service's to refuse.
    """
    descriptor: dict[str, Any] = {"depends_on": []}
    path = pack / "pack.yaml"
    if not path.is_file():
        return descriptor
    in_depends = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] not in " -":
            in_depends = raw.startswith("depends_on:")
            match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*(?:#.*)?$", raw)
            if match and match.group(2) not in ("", "null", "~"):
                descriptor[match.group(1)] = match.group(2).strip("'\"")
        elif in_depends:
            match = re.match(r"^\s*-?\s*pack_id:\s*([0-9A-Za-z]+)", raw)
            if match:
                descriptor["depends_on"].append(match.group(1))
    return descriptor


def pack_dirs(*parents: Path) -> list[Path]:
    found = sorted(child for parent in parents if parent.is_dir() for child in parent.iterdir() if child.is_dir())
    names = [pack.name for pack in found]
    duplicated = sorted({name for name in names if names.count(name) > 1})
    if duplicated:
        raise CannotRun(f"two pack directories are both named {duplicated}; a configuration root holds one directory per name")
    return found


def parse_expected_code(fixture: Path) -> dict[str, str]:
    """The ``expected-code`` file of an invalid fixture, validated: a fixture without one is an error."""
    path = fixture / "expected-code"
    if not path.is_file():
        raise CannotRun(f"{fixture}: no expected-code file; an invalid fixture must name the code it is refused with")
    expected: dict[str, str] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        key, separator, value = (part.strip() for part in line.partition(":"))
        if not separator or key not in EXPECTED_CODE_KEYS or not value:
            raise CannotRun(f"{path}:{number}: expected 'composition|registration|precheck: <value>', got {raw!r}")
        if key == "precheck":
            if value not in ("refused", "accepted"):
                raise CannotRun(f"{path}:{number}: precheck is 'refused' or 'accepted', not {value!r}")
        elif not CODE_PATTERN.match(value):
            raise CannotRun(f"{path}:{number}: {value!r} is not a refusal code (lower-case words joined by underscores)")
        expected[key] = value
    for key in ("composition", "registration"):
        if key not in expected:
            raise CannotRun(f"{path}: no '{key}:' line; both refusal paths must be proven")
    return expected


# --------------------------------------------------------------------------- the service


class Response:
    def __init__(self, status: int, headers: dict[str, str], body: bytes) -> None:
        self.status, self.headers, self.body = status, headers, body

    def json(self) -> Any:
        try:
            return json.loads(self.body)
        except ValueError:
            return {"unparsable": self.body[:500].decode("utf-8", "replace")}


class Service:
    """A running charter service over one configuration root."""

    def __init__(self, base: str, token: str) -> None:
        self.base, self.token = base, token

    def request(self, method: str, path: str, body: bytes | None = None, content_type: str | None = None) -> Response:
        request = urllib.request.Request(self.base + path, data=body, method=method)
        request.add_header("Authorization", f"Bearer {self.token}")
        if content_type:
            request.add_header("Content-Type", content_type)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))  # straight to loopback
        try:
            with opener.open(request, timeout=60) as answer:
                return Response(answer.status, dict(answer.headers), answer.read())
        except urllib.error.HTTPError as error:
            return Response(error.code, dict(error.headers), error.read())

    def get(self, path: str) -> Response:
        return self.request("GET", path)


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@contextmanager
def running_service(jar: Path, root: Path, *, registration: bool, log_dir: Path) -> Iterator[Service]:
    """Start the jar over ``root``, wait until it answers, stop it afterwards."""
    java = Path(os.environ["JAVA_HOME"]) / "bin" / "java" if os.environ.get("JAVA_HOME") else "java"
    port, token = free_port(), secrets.token_hex(20)
    command = [str(java), "-jar", str(jar), f"--server.port={port}", "--configRootLocation", str(root)]
    if registration:
        command.append("--charter.registration.enabled=true")
    log_path = log_dir / f"service-{port}.log"
    env = {**os.environ, "CHARTER_WORKTREE_TOKEN": token}
    with log_path.open("wb") as log:
        try:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, env=env)  # noqa: S603
        except OSError as error:
            raise CannotRun(f"cannot start {command[0]}: {error}") from error
        service = Service(f"http://127.0.0.1:{port}{API}", token)
        try:
            deadline = time.monotonic() + START_TIMEOUT_SECONDS
            while True:
                if process.poll() is not None:
                    raise CannotRun(f"the service exited ({process.returncode}) before it answered:\n{tail(log_path)}")
                try:
                    if service.get("/info").status == 200:
                        break
                except OSError:
                    pass
                if time.monotonic() > deadline:
                    raise CannotRun(f"the service did not answer within {START_TIMEOUT_SECONDS} s:\n{tail(log_path)}")
                time.sleep(0.2)
            yield service
        finally:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def tail(path: Path, lines: int = 40) -> str:
    return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:])


# --------------------------------------------------------------------------- the checks


class Report:
    """Collects the failures; every check runs, so one run reports all of the red."""

    def __init__(self) -> None:
        self.failures: list[str] = []

    def ok(self, message: str) -> None:
        print(f"ok: {message}")

    def fail(self, message: str, problem: Any = None) -> None:
        self.failures.append(message)
        print(f"::error::{message}")
        if problem is not None:
            print(json.dumps(problem, indent=2, sort_keys=True))


def stage(root: Path, packs: list[Path]) -> None:
    """Copy ``packs`` into ``<root>/packs/<directory name>/``: the layout of charter ADR-0038."""
    for pack in packs:
        shutil.copytree(pack, root / "packs" / pack.name, ignore=shutil.ignore_patterns(".git", "expected-code"))


def archive(pack: Path, left_out: list[str] | None = None) -> bytes:
    """The pack as a gzip tar with ``pack.yaml`` at its root, the form ``PUT /packs/{packId}`` takes.

    Leaves out ``expected-code`` (a fixture's own file) and ``NOT_REGISTERED``; ``left_out`` collects the
    latter so the run can name them."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for path in sorted(pack.rglob("*")):
            relative = path.relative_to(pack)
            name = relative.as_posix()
            if name == "expected-code" or ".git" in relative.parts:
                continue
            if any(fnmatch.fnmatchcase(name, pattern) for pattern in NOT_REGISTERED):
                if left_out is not None and path.is_file():
                    left_out.append(name)
                continue
            tar.add(path, arcname=name, recursive=False)
    return buffer.getvalue()


def register(service: Service, pack: Path, left_out: list[str] | None = None) -> dict[str, Any]:
    """Send ``pack`` whole and poll its registration to an end; returns the final status document."""
    body = archive(pack, left_out)
    if len(body) > MAX_ARCHIVE_BYTES:
        raise CannotRun(f"{pack.name}: the archive is {len(body)} bytes; the service accepts at most {MAX_ARCHIVE_BYTES}")
    accepted = service.request("PUT", f"/packs/{pack.name}", body, "application/gzip")
    if accepted.status != 202:
        return {"state": "refused", "problem": {**accepted.json(), "status": accepted.status}, "synchronous": True}
    location = accepted.headers.get("Location") or accepted.json().get("_links", {}).get("self", {}).get("href")
    if not location or "/pack-registrations/" not in location:
        raise CannotRun(f"{pack.name}: the 202 names no registration status: {accepted.headers!r}")
    path = location[location.index("/pack-registrations/") :]
    deadline = time.monotonic() + REGISTRATION_TIMEOUT_SECONDS
    while True:
        status = service.get(path)
        document = status.json()
        if status.status != 200:
            raise CannotRun(f"{pack.name}: GET {path} answered {status.status}: {document}")
        if document.get("state") in ("succeeded", "refused"):
            return document
        if time.monotonic() > deadline:
            raise CannotRun(f"{pack.name}: the registration did not end within {REGISTRATION_TIMEOUT_SECONDS} s: {document}")
        time.sleep(0.2)


def registration_order(packs: list[Path]) -> list[Path]:
    """Dependencies first among ``packs`` (a registration is judged over the closure it joins)."""
    by_id = {read_descriptor(pack).get("pack_id"): pack for pack in packs}
    ordered: list[Path] = []
    seen: set[Path] = set()

    def visit(pack: Path, trail: tuple[Path, ...]) -> None:
        if pack in seen or pack in trail:  # a cycle is the service's to refuse
            return
        for dependency in read_descriptor(pack)["depends_on"]:
            if dependency in by_id:
                visit(by_id[dependency], (*trail, pack))
        seen.add(pack)
        ordered.append(pack)

    for pack in packs:
        visit(pack, ())
    return ordered


def check_composition(jar: Path, packs: list[Path], scratch: Path, report: Report) -> None:
    root = scratch / "composition"
    stage(root, packs)
    with running_service(jar, root, registration=False, log_dir=scratch) as service:
        answer = service.get("/offering")
        if answer.status != 200:
            report.fail(f"composition: GET /offering answered {answer.status}", answer.json())
            return
        offered = {entry["packId"]: entry for entry in answer.json().get("packs", [])}
        report.ok(f"composition: GET /offering composes {len(offered)} packs")
        by_id = {read_descriptor(pack).get("pack_id"): pack.name for pack in packs}
        for pack in packs:
            descriptor, entry = read_descriptor(pack), offered.get(pack.name)
            if entry is None:
                report.fail(f"composition: {pack.name} is configured but the offering does not name it")
                continue
            if entry.get("level") != descriptor.get("pack_level"):
                report.fail(f"composition: {pack.name} declares level {descriptor.get('pack_level')!r}, the offering has {entry.get('level')!r}")
            resolved = {item.get("descriptorPackId") for item in entry.get("dependsOn", [])}
            missing = [by_id.get(dep, dep) for dep in descriptor["depends_on"] if dep not in resolved]
            if missing:
                report.fail(f"composition: {pack.name} depends on {missing}, which the offering does not resolve")
            elif entry.get("level") == descriptor.get("pack_level"):
                report.ok(f"composition: {pack.name} at level {entry.get('level')}, {len(descriptor['depends_on'])} dependencies resolved")
        extra = sorted(set(offered) - {pack.name for pack in packs})
        if extra:
            report.fail(f"composition: the offering names packs nobody configured: {extra}")


def check_registration(jar: Path, packs: list[Path], built_in: Path, scratch: Path, report: Report) -> None:
    root = scratch / "registration"
    stage(root, [built_in])
    registrable = [pack for pack in packs if read_descriptor(pack).get("pack_level") in ("org", "project")]
    with running_service(jar, root, registration=True, log_dir=scratch) as service:
        for pack in registration_order(registrable):
            left_out: list[str] = []
            result = register(service, pack, left_out)
            if left_out:
                print(f"::notice::registration: {pack.name}: not uploaded, the service does not model them: {', '.join(left_out)}")
            if result["state"] == "succeeded":
                stored = service.get(f"/packs/{pack.name}")
                outcome = result.get("result", {}).get("outcome", "?")
                if stored.status == 200:
                    report.ok(f"registration: {pack.name} registered ({outcome}) and read back")
                else:
                    report.fail(f"registration: {pack.name} registered but GET /packs/{pack.name} answered {stored.status}", stored.json())
            else:
                report.fail(f"registration: {pack.name} was refused", result.get("problem"))
        offering = service.get("/offering")
        if offering.status == 200:
            report.ok(f"registration: the registered packs compose ({len(offering.json().get('packs', []))} in the offering)")
        else:
            report.fail(f"registration: GET /offering over the registered packs answered {offering.status}", offering.json())


def refusal_code(document: Any) -> str | None:
    return document.get("code") if isinstance(document, dict) else None


def check_invalid(jar: Path, fixtures: list[Path], built_in: Path, scratch: Path, report: Report) -> None:
    for fixture in fixtures:
        expected = parse_expected_code(fixture)
        compose_root = scratch / f"invalid-compose-{fixture.name}"
        stage(compose_root, [built_in, fixture])
        with running_service(jar, compose_root, registration=False, log_dir=scratch) as service:
            answer = service.get("/offering")
            code = refusal_code(answer.json())
            if answer.status == 200:
                report.fail(f"non-vacuity: {fixture.name} composes, but must be refused {expected['composition']}")
            elif code != expected["composition"]:
                report.fail(f"non-vacuity: {fixture.name} composition refused {code!r}, expected {expected['composition']!r}", answer.json())
            else:
                report.ok(f"non-vacuity: {fixture.name} refused at composition with {code}")
        register_root = scratch / f"invalid-register-{fixture.name}"
        stage(register_root, [built_in])
        with running_service(jar, register_root, registration=True, log_dir=scratch) as service:
            result = register(service, fixture)
            code = refusal_code(result.get("problem"))
            if result["state"] == "succeeded":
                report.fail(f"non-vacuity: {fixture.name} was registered, but must be refused {expected['registration']}")
            elif code != expected["registration"]:
                report.fail(f"non-vacuity: {fixture.name} registration refused {code!r}, expected {expected['registration']!r}", result.get("problem"))
            else:
                report.ok(f"non-vacuity: {fixture.name} refused at registration with {code}")


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--jar", type=Path, required=True, help="the charter service jar (Spring Boot, Java 25)")
    parser.add_argument("--repo", type=Path, default=here, help="the repository root (default: this checkout)")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory (roots and service logs)")
    args = parser.parse_args(argv)
    repo = args.repo
    scratch = Path(tempfile.mkdtemp(prefix="charter-service-check-"))
    report = Report()
    try:
        if not args.jar.is_file():
            raise CannotRun(f"no jar at {args.jar}")
        packs = pack_dirs(repo / "packs", repo / "tests" / "fixtures" / "valid")
        fixtures = pack_dirs(repo / "tests" / "fixtures" / "invalid")
        built_in = repo / "packs" / BUILT_IN
        if not packs or not fixtures or not (built_in / "pack.yaml").is_file():
            raise CannotRun("no pack under packs/ or tests/fixtures/valid/, no invalid fixture, or no packs/built-in: the check would prove nothing")
        for fixture in fixtures:
            parse_expected_code(fixture)  # fail closed before any service starts
        check_composition(args.jar, packs, scratch, report)
        check_registration(args.jar, packs, built_in, scratch, report)
        check_invalid(args.jar, fixtures, built_in, scratch, report)
    except CannotRun as error:
        print(f"::error::cannot run the charter service check: {error}")
        return EXIT_CANNOT_RUN
    finally:
        if args.keep:
            print(f"scratch kept at {scratch}")
        else:
            shutil.rmtree(scratch, ignore_errors=True)
    if report.failures:
        print(f"FAIL: {len(report.failures)} charter service check(s) failed")
        return EXIT_FAILED
    print("ok: the charter service accepts every pack and refuses every invalid fixture")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
