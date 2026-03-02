from pathlib import Path

from longevity.adapters.bs4_parser import Bs4LongevityParser
from longevity.domain.services import almost_equal


def test_response_parser_keith_richards_html():
    html = Path(__file__).parent / "testdata" / "keith_richards.html"
    content = html.read_text(encoding="utf-8", errors="replace")
    parser = Bs4LongevityParser()
    current_age, additional_years, total_years = parser.parse(content)

    assert almost_equal(current_age, 78.75)
    assert almost_equal(additional_years, 9.5)
    assert almost_equal(total_years, 88.3)
