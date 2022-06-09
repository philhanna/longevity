from unittest import TestCase
import os.path

from longevity import ResponseParser


class TestResponseParser(TestCase):

    def setUp(self):
        filename = os.path.abspath("long.html")
        with open(filename) as fp:
            self.rp = ResponseParser(fp)

    def test_current_age(self):
        expected = "68 and 6 months"
        actual = self.rp.current_age
        self.assertEqual(expected, actual)

    def test_additional_years(self):
        expected = "16.5"
        actual = self.rp.additional_years
        self.assertEqual(expected, actual)

    def test_total_years(self):
        expected = "85.0"
        actual = self.rp.total_years
        self.assertEqual(expected, actual)

