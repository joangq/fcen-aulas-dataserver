from unittest import TestCase
from src.hours import Time, TimeRange


class TimeRangeTests(TestCase):
    def test_exclusion(self):
        self.assertNotIn(Time(8, 29),
                         TimeRange(low=Time(8, 30), high=Time(15, 35)))

        self.assertNotIn(Time(15, 35),
                         TimeRange(low=Time(8, 30), high=Time(15, 35)))

    def test_inclusion(self):
        self.assertIn(Time(8, 30),
                      TimeRange(low=Time(8, 30), high=Time(15, 35)))

        self.assertIn(Time(15, 34),
                      TimeRange(low=Time(8, 30), high=Time(15, 35)))
