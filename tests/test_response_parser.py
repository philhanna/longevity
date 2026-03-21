from pathlib import Path

import pytest

from longevity.adapters.bs4_parser import Bs4LongevityParser, parse_current_age
from longevity.domain.services import almost_equal


def test_parse_current_age_cases():
    assert parse_current_age("68") == 68.0
    assert almost_equal(parse_current_age("68 and 3 months"), 68.25)
    assert almost_equal(parse_current_age("68 and 1 month"), 68.0 + 1.0 / 12.0)
    assert parse_current_age("bogus") == 0.0


def test_response_parser_keith_richards_html():
    html = Path(__file__).parent / "testdata" / "keith_richards.html"
    content = html.read_text(encoding="utf-8", errors="replace")
    parser = Bs4LongevityParser()
    current_age, additional_years, total_years = parser.parse(content)

    assert almost_equal(current_age, 78.75)
    assert almost_equal(additional_years, 9.5)
    assert almost_equal(total_years, 88.3)


def test_parse_raises_when_no_table():
    parser = Bs4LongevityParser()
    with pytest.raises(ValueError, match="no <table> found"):
        parser.parse("<html><body><p>no table here</p></body></html>")


def test_parse_raises_when_table_has_fewer_than_two_rows():
    parser = Bs4LongevityParser()
    html = "<table><tr><td>only one row</td></tr></table>"
    with pytest.raises(ValueError, match="expected >=2 <tr> rows"):
        parser.parse(html)


def test_parse_raises_when_second_row_has_fewer_than_three_tds():
    parser = Bs4LongevityParser()
    html = "<table><tr><th>Header</th></tr><tr><td>one</td><td>two</td></tr></table>"
    with pytest.raises(ValueError, match="not enough <td> tags"):
        parser.parse(html)
