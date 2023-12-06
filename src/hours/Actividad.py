from .TimeRange import TimeRange
from typing import Any


class Actividad(TimeRange):
    actividad: Any

    def set_actividad(self, *args):
        self.actividad = args
        return self
