from __future__ import annotations
import re

from bs4 import BeautifulSoup

from ..domain.services import parse_float

ISO_FORMAT = "%Y-%m-%d"


def parse_current_age(text: str) -> float:
    """Parse strings like '68' or '68 and 3 months' into a float age."""
    age = 0.0
    m = re.search(r"(\d+)", text or "")
    if m:
        age = float(m.group(1))

    m2 = re.search(r" and (\d+) month", text or "")
    if m2:
        age += float(m2.group(1)) / 12.0
    return age

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
