from unittest import TestCase
import os.path

from longevity import ResponseParser
from tests import testdata


class TestResponseParser(TestCase):

    def setUp(self):
        filename = os.path.join(testdata, "keith_richards.html")
        with open(filename) as fp:
            self.rp = ResponseParser(fp)

    def test_current_age(self):
        expected = 78.75
        actual = self.rp.current_age
        self.assertEqual(expected, actual)

    def test_additional_years(self):
        expected = 9.5
        actual = self.rp.additional_years
        self.assertEqual(expected, actual)

    def test_total_years(self):
        expected = 88.3
        actual = self.rp.total_years
        self.assertEqual(expected, actual)

