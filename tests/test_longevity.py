from unittest import TestCase
from datetime import date

from longevity import Longevity


class TestLongevity(TestCase):

    def test_longevity(self):
        # Keith Richards
        sex = "m"
        dob = date.fromisoformat("1943-12-18")
        long = Longevity(sex, dob)
        self.assertEqual(941/12, long.current_age)
        self.assertEqual(9.6, long.additional_years)
        self.assertEqual(88.1, long.total_years)
