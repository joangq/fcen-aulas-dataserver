import pandas as pd

from glob import glob

from catthy import lista

from src.util.prutils import apply_to_column
from src.hours import Time, TimeRange


def tuplist_to_timerange(y):
    [a, b] = lista(y).map(Time.parse_time)
    return TimeRange(a, b)


def mapplyx(s, f):
    return lista(s).map(f)


def mapply(f):
    return lambda s: mapplyx(s, f)


mapply_tuplist_to_timerange = mapply(tuplist_to_timerange)


def load(s):
    return pd.read_json(s, convert_dates=False, convert_axes=False)
