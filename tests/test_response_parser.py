from pathlib import Path

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
