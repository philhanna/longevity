from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from longevity.adapters.http_requests import RequestsLongevityFetcher


def _mock_response(text="<html/>", status_code=200):
    resp = MagicMock()
    resp.text = text
    resp.status_code = status_code
    resp.raise_for_status = MagicMock()
    return resp


def test_january_month_is_zero():
    """SSA expects 0-based month (Jan=0)."""
    with patch("longevity.adapters.http_requests.requests.post", return_value=_mock_response()) as mock_post:
        RequestsLongevityFetcher().fetch(sex="m", dob=date(1986, 1, 15))
    _, kwargs = mock_post.call_args
    assert kwargs["data"]["monthofbirth"] == "0"


def test_december_month_is_eleven():
    with patch("longevity.adapters.http_requests.requests.post", return_value=_mock_response()) as mock_post:
        RequestsLongevityFetcher().fetch(sex="f", dob=date(1986, 12, 1))
    _, kwargs = mock_post.call_args
    assert kwargs["data"]["monthofbirth"] == "11"


def test_post_data_fields():
    with patch("longevity.adapters.http_requests.requests.post", return_value=_mock_response()) as mock_post:
        RequestsLongevityFetcher().fetch(sex="m", dob=date(1990, 6, 5))
    _, kwargs = mock_post.call_args
    data = kwargs["data"]
    assert data["sex"] == "m"
    assert data["dayofbirth"] == "5"
    assert data["yearofbirth"] == "1990"


def test_returns_response_text():
    with patch("longevity.adapters.http_requests.requests.post", return_value=_mock_response(text="<result/>")):
        result = RequestsLongevityFetcher().fetch(sex="m", dob=date(1990, 1, 1))
    assert result == "<result/>"


def test_http_error_propagates():
    import requests as req
    resp = _mock_response(status_code=500)
    resp.raise_for_status.side_effect = req.HTTPError("500 Server Error")
    with patch("longevity.adapters.http_requests.requests.post", return_value=resp):
        with pytest.raises(req.HTTPError):
            RequestsLongevityFetcher().fetch(sex="m", dob=date(1990, 1, 1))
