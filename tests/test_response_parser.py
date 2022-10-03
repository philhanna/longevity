import pytest

from longevity import ResponseParser
from tests import testdata


@pytest.fixture
def rp():
    filename = testdata / "keith_richards.html"
    text = filename.read_text()
    rp = ResponseParser(text)
    return rp


def test_current_age(rp):
    assert rp.current_age == 78.75


def test_additional_years(rp):
    assert rp.additional_years == 9.5


def test_total_years(rp):
    assert rp.total_years == 88.3
