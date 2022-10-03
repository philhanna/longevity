from datetime import date

from longevity import Requester
from tests import testdata


def test_with_keith_richards(monkeypatch):
    content = (testdata / "keith_richards.html").read_bytes()
    monkeypatch.setattr(Requester, "post_request", lambda x: content)
    sex = "m"
    dob = date.fromisoformat("1943-12-18")
    requester = Requester(sex, dob)
    assert 78.75 == requester.current_age
    assert 9.5 == requester.additional_years
    assert 88.3, requester.total_years


def test_with_barack_obama(monkeypatch):
    content = (testdata / "barack_obama.html").read_bytes()
    monkeypatch.setattr(Requester, "post_request", lambda x: content)
    sex = "m"
    dob = date.fromisoformat("1961-08-04")
    requester = Requester(sex, dob)
    assert 61 == requester.current_age
    assert 22.1 == requester.additional_years
    assert 83.3 == requester.total_years
