from __future__ import annotations
from functools import wraps
from src.hours import TimeRange


class TiempoLibre(TimeRange):
    aula: int

    @staticmethod
    def from_other(other: TiempoLibre):
        return TiempoLibre(other.low, other.high)

    def set_aula(self, a: int):
        self.aula = a
        return self

    @staticmethod
    def de(a: int):
        @wraps(TiempoLibre.from_other)
        def wrapper(other):
            return TiempoLibre.from_other(other).set_aula(a)

        return wrapper
