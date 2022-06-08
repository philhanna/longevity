from unittest import TestCase
from datetime import date

from longevity.longevity import get_date_fields, format_post_data


class TestFormatPostData(TestCase):

    def test_format_post_data_keith_richards(self):
        dob = date(1943, 12, 18)
        expected = {
            "sex" : "m",
            "monthofbirth": "11",
            "dayofbirth": "18",
            "yearofbirth": "1943",
        }
        actual = format_post_data("m", dob)
        self.assertEqual(expected, actual)

