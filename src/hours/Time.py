from __future__ import annotations


class Time:
    hour: int
    minute: int

    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    @staticmethod
    def from_other(other):
        return Time(other.hour, other.minute)

    @staticmethod
    def parse_time(time_str):
        try:
            hour, minute = map(int, time_str.split(':'))
            if 0 <= hour < 24 and 0 <= minute < 60:
                return Time(hour, minute)
            else:
                raise ValueError("Invalid hour or minute value")
        except ValueError as e:
            print(f"Error parsing time: {e}")
            return None

    def __str__(self):
        return f'{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}'

    def __repr__(self):
        return f'{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}'

    def __gt__(self, other):
        if self.hour > other.hour:
            return True
        elif self.hour == other.hour:
            return self.minute > other.minute
        else:
            return False

    def __ge__(self, other):
        return self > other or self == other

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __sub__(self, other):
        self_total = (self.hour * 60) + self.minute
        other_total = (other.hour * 60) + other.minute
        return self_total - other_total

    def __iter__(self):
        yield self.hour
        yield self.minute
