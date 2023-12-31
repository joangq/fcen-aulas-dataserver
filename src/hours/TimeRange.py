from __future__ import annotations
from .Time import Time
import json


class TimeRange:
    low: Time
    high: Time

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @staticmethod
    def from_other(other: TimeRange):
        return TimeRange(other.low, other.high)

    def __contains__(self, t: Time):
        h, m = t
        return self.low.hour <= h <= self.high.hour \
            and self.low.minute <= m < self.high.minute

    def __repr__(self):
        return f'{repr(self.low)} -- {repr(self.high)}'

    def __str__(self):
        return f'{str(self.low)} -- {str(self.high)}'

    def __gt__(self, other):
        return self.low > other.low and self.high > other.high

    def __eq__(self, other):
        return self.low == other.low and self.high == other.high

    def __ge__(self, other):
        return self > other or self == other

    def __iter__(self):
        yield self.low
        yield self.high

    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, TimeRange):
                (l, h) = obj
                return str(l), str(h)
            return super().default(obj)
