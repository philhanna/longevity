import json
from datetime import date

from longevity import Requester
from tests import testdata


def test_with_keith_richards(monkeypatch):
    content = (testdata / "keith_richards.html").read_bytes()
    monkeypatch.setattr(Requester, "post_request", lambda x: content)
    sex = "m"
    dob = date.fromisoformat("1943-12-18")
    requester = Requester(sex, dob)
    jsonstr = requester.get_json_output()
    data = json.loads(jsonstr)

    assert data.get("current_age", None) == 78.75
    assert data.get("additional_years", None) == 9.5
    assert data.get("total_years", None) == 88.3
    assert data.get("death_date") == "2032-04-05"


def test_with_barack_obama(monkeypatch):
    content = (testdata / "barack_obama.html").read_bytes()
    monkeypatch.setattr(Requester, "post_request", lambda x: content)
    sex = "m"
    dob = date.fromisoformat("1961-08-04")
    requester = Requester(sex, dob)
    jsonstr = requester.get_json_output()
    data = json.loads(jsonstr)

    assert data.get("current_age", None) == 61
    assert data.get("additional_years", None) == 22.1
    assert data.get("total_years", None) == 83.3
    assert data.get("death_date") == "2044-11-21"
