from datetime import date

import requests

from longevity import ResponseParser, SSA_URL


class Requester:

    def __init__(self, sex: str, dob: date):
        """ Main method. Looks up life expectancy for specified sex and date of birth """
        self._sex = sex
        self._dob = dob
        postdata = Requester.format_post_data(sex, dob)
        content = self.post_request(postdata)
        self._rp = ResponseParser(content)
        self._death_date = self._rp.get_death_date(dob)

    @property
    def sex(self) -> str:
        return self._sex

    @property
    def dob(self) -> date:
        return self._dob

    @property
    def current_age(self) -> float:
        return self._rp.current_age

    @property
    def additional_years(self) -> float:
        return self._rp.additional_years

    @property
    def total_years(self) -> float:
        return self._rp.total_years

    @property
    def death_date(self) -> date:
        return self._death_date

    @staticmethod
    def post_request(postdata) -> bytes:
        """Posts the request and gets the response.

        :param postdata: a dictionary of the parameters, e.g., for Keith Richards:
        {
            "sex" : "m",
            "monthofbirth": "11",   # Note: website expects actual month - 1
            "dayofbirth": "18",
            "yearofbirth": "1943",
        }

        Separated from the mainline so that this function can be mocked
        and test data used instead of a live call to the URL.
        """
        response = requests.post(SSA_URL, data=postdata)
        content = response.content
        return content

    @staticmethod
    def get_date_fields(dob: date) -> tuple[str, str, str]:
        """ Extracts date fields and formats them in the way the
        cgi program expects them.

        Output fields:

        - monthofbirth is the month field minus 1 (0-11)
        - dayofbirth is the day field with leading zero if less than 10
        - yearofbirth is a 4-digit year field

        These fields are returned as tuple of 3 strings
        """
        monthofbirth = f"{dob.month - 1}"
        dayofbirth = f"{dob.day:02d}"
        yearofbirth = f"{dob.year}"
        return monthofbirth, dayofbirth, yearofbirth

    @staticmethod
    def format_post_data(sex: str, dob: date) -> dict:
        """ Creates a dictionary of the data that will be used in the POST method """
        mm, dd, yyyy = Requester.get_date_fields(dob)
        postdata = {
            "sex": sex,
            "monthofbirth": mm,
            "dayofbirth": dd,
            "yearofbirth": yyyy,
        }
        return postdata
