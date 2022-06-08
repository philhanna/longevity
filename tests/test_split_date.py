from unittest import TestCase
from datetime import date

from longevity.longevity import split_date


class TestSplitDate(TestCase):

    def test_split_date_keith_richards(self):
        dob = date(1943, 12, 18)
        m, d, y = split_date(dob)
        self.assertEqual("11", m)
        self.assertEqual("18", d)
        self.assertEqual("1943", y)

    def test_split_date_barack_obama(self):
        dob = date(1961, 8, 4)
        m, d, y = split_date(dob)
        self.assertEqual("7", m)
        self.assertEqual("04", d)
        self.assertEqual("1961", y)
