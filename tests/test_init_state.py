from unittest import TestCase

from longevity.parser import InitState


class TestInitState(TestCase):

    def test_name(self):
        obj = InitState()
        expected = "InitState"
        actual = obj.name
        self.assertEqual(expected, actual)
