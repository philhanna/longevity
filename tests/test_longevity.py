from unittest import TestCase
from datetime import date

from longevity import Longevity


class TestLongevity(TestCase):

    def test_longevity(self):
        sex = "m"
        dob = date.fromisoformat("1953-12-04")
        long = Longevity(sex, dob)
        self.assertEqual(68.5, long.current_age)
        self.assertEqual(16.5, long.additional_years)
        self.assertEqual(85, long.total_years)
