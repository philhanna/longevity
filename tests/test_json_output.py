import os

from tests import testdata
from unittest.mock import patch
from unittest import TestCase
from datetime import date

from longevity import Requester


class TestJSONOutput(TestCase):

    def test_with_keith_richards(self):
        with open(os.path.join(testdata, "keith_richards.html"), "rb") as fp:
            content = fp.read()
        with patch.object(Requester, "post_request", return_value=content):
            sex = "m"
            dob = date.fromisoformat("1943-12-18")
            requester = Requester(sex, dob)
            json_dict = requester.json_output

            expected = 78.75
            actual = json_dict.get("current_age", None)
            self.assertEqual(expected, actual)

            expected = 9.5
            actual = json_dict.get("additional_years", None)
            self.assertEqual(expected, actual)

            expected = 88.3
            actual = json_dict.get("total_years", None)
            self.assertEqual(expected, actual)

            expected = "04/05/2032"
            actual = json_dict.get("death_date")
            self.assertEqual(expected, actual)

    def test_with_barack_obama(self):
        with open(os.path.join(testdata, "barack_obama.html"), "rb") as fp:
            content = fp.read()
        with patch.object(Requester, "post_request", return_value=content):
            sex = "m"
            dob = date.fromisoformat("1961-08-04")
            requester = Requester(sex, dob)
            self.assertEqual(61, requester.current_age)
            self.assertEqual(22.1, requester.additional_years)
            self.assertEqual(83.3, requester.total_years)
