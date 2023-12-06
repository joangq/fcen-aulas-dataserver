from unittest import TestCase

from glob import glob

from catthy import lista
from pandas import read_json

from src.digest.timetables import load, mapply_tuplist_to_timerange
from src.util.prutils import apply_to_column


def __test_timetable__(s):
    try:
        df = load(s)
        for col in df.columns:
            apply_to_column(df, col, mapply_tuplist_to_timerange)
        return None
    except Exception as e:
        return e


def did_fail(x):
    return isinstance(x, Exception)


def parsing_successful(x):
    return not did_fail(__test_timetable__(x))


class TimetablesTests(TestCase):

    def setUp(self):
        self.timetables = lista(x for x in glob('../output/timetables/*'))

    def test_timetables(self):
        self.assertTrue(all(self.timetables.map(parsing_successful)))
