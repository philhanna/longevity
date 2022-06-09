from bs4 import BeautifulSoup


class ResponseParser:
    """ Extracts the life expectency results from the HTML """
    def __init__(self, fp):

        soup = BeautifulSoup(fp, 'html.parser')
        table = soup.table
        trs = [x for x in table.findAll("tr")]
        tr = trs[1]
        tds = [x for x in tr.findAll("td")]
        assert len(tds) >= 3

        self._current_age = tds[0].contents[0]
        self._additional_years = tds[1].contents[0]
        self._total_years = tds[2].contents[0]

    @property
    def current_age(self):
        return self._current_age

    @property
    def additional_years(self):
        return self._additional_years

    @property
    def total_years(self):
        return self._total_years
