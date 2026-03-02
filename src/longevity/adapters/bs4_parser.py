from __future__ import annotations

from bs4 import BeautifulSoup

from ..domain.services import parse_current_age, parse_float


class Bs4LongevityParser:
    """Outbound adapter: parses SSA HTML using BeautifulSoup.

    Returns:
        (current_age, additional_years, total_years)
    """

    def parse(self, html: str) -> tuple[float, float, float]:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if table is None:
            raise ValueError("no <table> found")

        trs = table.find_all("tr")
        if len(trs) < 2:
            raise ValueError(f"expected >=2 <tr> rows, found {len(trs)}")

        tds = trs[1].find_all("td")
        if len(tds) < 3:
            raise ValueError(f"not enough <td> tags. Only {len(tds)} found")

        current_age = parse_current_age(tds[0].get_text(strip=True))
        additional_years = parse_float(tds[1].get_text(strip=True))
        total_years = parse_float(tds[2].get_text(strip=True))
        return current_age, additional_years, total_years
