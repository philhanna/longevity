import re
from datetime import timedelta, date

from bs4 import BeautifulSoup


class ResponseParser:
    """Extracts the life expectency results from the HTML"""

    def __init__(self, fp):

        soup = BeautifulSoup(fp, 'html.parser')
        table = soup.table
        trs = [x for x in table.findAll("tr")]
        tr = trs[1]
        tds = [x for x in tr.findAll("td")]
        assert len(tds) >= 3

        current_age_string = tds[0].contents[0]
        age = 0
        m = re.match(r'(\d+)', current_age_string)
        if m:
            age = float(m.group(1))
        m = re.search(r' and (\d+) months', current_age_string)
        if m:
            age += float(m.group(1)) / 12.0

        self._current_age: float = age
        self._additional_years: float = float(tds[1].contents[0])
        self._total_years: float = float(tds[2].contents[0])

    def get_death_date(self, dob) -> date:
        """Estimates the date of death"""
        return dob + timedelta(days=self.total_years * 365.25)
        # Yes, I know this is only an approximation ... 365.25

    @property
    def current_age(self) -> float:
        return self._current_age

    @property
    def additional_years(self) -> float:
        return self._additional_years

    @property
    def total_years(self) -> float:
        return self._total_years
