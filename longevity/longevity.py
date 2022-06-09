import requests
from datetime import date

from longevity import ResponseParser

SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"


class Longevity:

    @staticmethod
    def get_date_fields(dob: date):
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
        mm, dd, yyyy = Longevity.get_date_fields(dob)
        postdata = {
            "sex": sex,
            "monthofbirth": mm,
            "dayofbirth": dd,
            "yearofbirth": yyyy,
        }
        return postdata

    def __init__(self, sex: str, dob: date):
        """ Main method. Looks up life expectancy for specified sex and date of birth """
        self.sex = sex
        self.dob = dob
        postdata = Longevity.format_post_data(sex, dob)
        response = requests.post(SSA_URL, data=postdata)
        content = response.content
        self.rp = ResponseParser(content)

    @property
    def current_age(self):
        return self.rp.current_age

    @property
    def additional_years(self):
        return self.rp.additional_years

    @property
    def total_years(self):
        return self.rp.total_years
