from unittest import TestCase
from datetime import date

from longevity.longevity import get_date_fields


class TestGetDateFields(TestCase):

    def test_get_date_fields_keith_richards(self):
        dob = date(1943, 12, 18)
        m, d, y = get_date_fields(dob)
        self.assertEqual("11", m)
        self.assertEqual("18", d)
        self.assertEqual("1943", y)

    def test_get_date_fields_barack_obama(self):
        dob = date(1961, 8, 4)
        m, d, y = get_date_fields(dob)
        self.assertEqual("7", m)
        self.assertEqual("04", d)
        self.assertEqual("1961", y)
