from unittest import TestCase


class SomeTests(TestCase):
    def setUp(self):
        self.a = 'abc'

    def test_lt(self):
        self.assertTrue(self.a == 'abc')
