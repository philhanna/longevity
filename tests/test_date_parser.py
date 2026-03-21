from datetime import date

import pytest

from longevity.adapters.date_parser import parse_date

EXPECTED = date(1957, 12, 18)


@pytest.mark.parametrize("text", [
    "1957-12-18",
    "12/18/1957",
    "18/12/1957",
    "December 18, 1957",
    "Dec 18, 1957",
    "18 December 1957",
    "18 Dec 1957",
    "18-December-1957",
    "18-Dec-1957",
])
def test_parse_date_all_formats(text):
    assert parse_date(text) == EXPECTED


def test_parse_date_explicit_fmt():
    assert parse_date("18/12/1957", fmt="%d/%m/%Y") == EXPECTED


def test_parse_date_explicit_fmt_wrong_order_raises():
    # Without an explicit fmt, 01/02/2000 resolves as MM/DD (US first).
    # With an explicit European fmt, day=1 month=2.
    assert parse_date("01/02/2000", fmt="%d/%m/%Y") == date(2000, 2, 1)
    assert parse_date("01/02/2000", fmt="%m/%d/%Y") == date(2000, 1, 2)


def test_parse_date_ambiguous_prefers_us_format():
    # When day <= 12 and no fmt is given, US (MM/DD) is tried first.
    assert parse_date("01/02/2000") == date(2000, 1, 2)


def test_parse_date_invalid_raises():
    with pytest.raises(ValueError, match="cannot parse date"):
        parse_date("not-a-date")


def test_parse_date_invalid_explicit_fmt_raises():
    with pytest.raises(ValueError):
        parse_date("1957-12-18", fmt="%d/%m/%Y")
