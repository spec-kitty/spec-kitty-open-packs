"""Representatives for the Python coupling, text and skip findings."""

__test__ = False

import time
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest


def test_mock_call_interaction():
    collaborator = MagicMock()
    collaborator.run()
    assert collaborator.call_count == 1


def test_too_many_mocks():
    first = MagicMock()
    second = MagicMock()
    third = MagicMock()
    fourth = MagicMock()
    assert len([first, second, third, fourth]) == 4


def test_reads_private_attributes():
    subject = object()
    assert (subject._first, subject._second, subject._third)


def test_scans_source_literally():
    source = Path("src/example.py").read_text()
    assert "expected" in source


def test_pins_a_source_line(output):
    assert "src/example.py:42" in output


def test_uses_a_fake_mission_id():
    mission_id = "short"
    assert mission_id


def test_sleeps():
    time.sleep(0.01)
    assert 1 == 1


def test_reads_current_time():
    assert datetime.now().year >= 2026


@pytest.mark.skip(reason="fixture")
def test_is_skipped():
    assert 1 == 1
