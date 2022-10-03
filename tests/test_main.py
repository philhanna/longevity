from datetime import date, datetime
from unittest import TestCase

from longevity import Main


class TestMain(TestCase):

    def setUp(self):
        self.parms = {
            "name": "Keith Richards",
            "dob" : "12/18/1943",
            "sex" : "m",
            "monthofbirth": "11",
            "dayofbirth": "18",
            "yearofbirth": "1943",
        }
        main = Main(**self.parms)
        self.requester = main.run()

    def test_sex(self):
        expected = "m"
        actual = self.requester.sex
        self.assertEqual(expected, actual)

    def test_dob(self):
        expected = date.fromisoformat("1943-12-18")
        actual = self.requester.dob
        self.assertEqual(expected, actual)

    def test_death_date(self):
        death_date = self.requester.death_date
        expected = 2032
        actual = death_date.year
        self.assertEqual(expected, actual)
