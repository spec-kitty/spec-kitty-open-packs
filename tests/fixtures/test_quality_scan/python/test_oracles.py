"""One representative for each Python oracle finding."""

__test__ = False

import pytest


def operation():
    return "payload"


def assert_payload(payload):
    assert payload == "payload"


def test_without_an_oracle():
    operation()


def test_only_checks_non_none():
    value = operation()
    assert value is not None


def test_only_checks_type():
    value = operation()
    assert isinstance(value, str)


def test_catches_any_exception():
    with pytest.raises(Exception):
        operation()


def test_uses_a_local_asserting_helper():
    assert_payload(operation())


def test_compares_the_result():
    assert operation() == "payload"
