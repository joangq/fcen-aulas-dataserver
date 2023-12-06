from unittest import TestCase
from src.hours import Time


class TestTimeComparison(TestCase):
    def setUp(self):
        self.time1 = Time(10, 30)
        self.time2 = Time(12, 15)
        self.time3 = Time(10, 30)

    def test_lt(self):
        self.assertTrue(self.time1 < self.time2)
        self.assertFalse(self.time2 < self.time1)
        self.assertFalse(self.time1 < self.time3)

    def test_le(self):
        self.assertTrue(self.time1 <= self.time2)
        self.assertFalse(self.time2 <= self.time1)
        self.assertTrue(self.time1 <= self.time3)

    def test_eq(self):
        self.assertFalse(self.time1 == self.time2)
        self.assertTrue(self.time1 == self.time3)

    def test_gt(self):
        self.assertFalse(self.time1 > self.time2)
        self.assertTrue(self.time2 > self.time1)
        self.assertFalse(self.time1 > self.time3)

    def test_ge(self):
        self.assertFalse(self.time1 >= self.time2)
        self.assertTrue(self.time2 >= self.time1)
        self.assertTrue(self.time1 >= self.time3)