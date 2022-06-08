from unittest import TestCase
from datetime import date

from longevity import Longevity


class TestFormatPostData(TestCase):

    def test_format_post_data_keith_richards(self):
        dob = date.fromisoformat("1943-12-18")
        expected = {
            "sex" : "m",
            "monthofbirth": "11",
            "dayofbirth": "18",
            "yearofbirth": "1943",
        }
        actual = Longevity.format_post_data("m", dob)
        self.assertEqual(expected, actual)

    def test_format_post_data_barack_obama(self):
        dob = date.fromisoformat("1961-08-04")
        expected = {
            "sex" : "m",
            "monthofbirth": "7",
            "dayofbirth": "04",
            "yearofbirth": "1961",
        }
        actual = Longevity.format_post_data("m", dob)
        self.assertEqual(expected, actual)

