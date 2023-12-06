from functools import partial
from numpy import nan
from operator import and_

from catthy import foldr, foldl
from pandas import DataFrame, ExcelFile, Index, notna
from pandas.core.series import Series
from unidecode import unidecode
from typing import Callable, TypeAlias, Iterable, Any, Generator, TypeVar

from datetime import time as dtime_object
from datetime import datetime as date_time

from src.hours import Time


def parse_time(x: str) -> dtime_object:
    return date_time.strptime(x, "%H:%M").time()


NaN: TypeAlias = float
"""Inteded for typehinting `numpy.nan`. This is a workaround because Pylance 
    doesn't detect Literal[numpy.nan] as a valid return type. 
    Instead, it insists that `numpy.nan` = `float`"""

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def compose2(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    def composed(*a: A, **kw: A):
        return f(g(*a, **kw))

    return composed


def compose(*fs):
    return foldl(compose2, fs)


def apply_to_column(df: DataFrame, col: A, f: Callable[[A], B]) -> None:
    """Mutates a DataFrame by mapping a function over a column."""
    # using .loc[*, col] to avoid chained indexing
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    df.loc[:, col] = df.loc[:, col].map(f)  # type: ignore


def clean(x: str) -> str:
    return unidecode(x).replace(' ', '-').lower()


def remove_dot(x: str) -> str:
    return x.replace('.', '')


def drop_first_row(df: DataFrame) -> DataFrame:
    """Mutates a DataFrame by replacing the header witht the [next] first row"""
    return df.rename(columns=df.iloc[0]).iloc[1:]  # type: ignore


def drop_nan_cols(df: DataFrame) -> DataFrame:
    """Mutates a DataFrame by dropping all columns with `numpy.nan` headers"""
    return df.loc[:, df.columns.notna()]


clean_str_: Callable[[str], str]
"""Helper function for cleaning columns"""
clean_str_ = compose(remove_dot, clean)


def clean_columns(df: DataFrame) -> DataFrame:
    """Mutates a DataFrame by replacing the header names with clean names. (See `clean_str_`)"""
    df.columns = df.columns.map(clean_str_)
    return df


# This is for normalization of the tables.
# Contents COULD change from month to month,
# so this must be FIXME'd everytime
TIMERANGE_MAP = {'inicio': 'desde', 'fin': 'hasta'}


def fix_timerange(df: DataFrame) -> DataFrame:
    """Mutates a DataFrame by mapping column names to fixed column names.
        This is to normalizethem for later use."""
    df.columns = Index(x if x not in TIMERANGE_MAP.keys() else TIMERANGE_MAP[x] for x in df.columns)
    return df


def notna_all(args: 'Iterable[Series[Any]]') -> 'Generator[Series[bool], None, None]':
    """Equivalent to: (arg1.notna(), arg2.notna(), ...)"""
    return (x.notna() for x in args)


def cols_to_filters(df: DataFrame, *cols: Any) -> 'Generator[Series[Any], None, None]':
    """Equivalent to: (df[col1], df[col2], ...)"""
    return (df[x] for x in cols)


def dropna_rows(df: DataFrame, *args: Any) -> DataFrame:
    """Equivalent to: df[df[arg1].notna() & df[arg2].notna() & ...]

      Mutates a DataFrame by dropping rows containing `numpy.nan` values"""
    filters: Series[bool] = foldr(and_, notna_all(cols_to_filters(df, *args)))
    return df[filters]


# Curried version of dropna_rows
def dropna_rowsx(*args):
    """Curried version of `dropna_rows`"""
    return lambda df: dropna_rows(df, *args)


dropna_timeranges: Callable[[DataFrame], DataFrame]
"""Mutates a DataFrame by dropping rows containing `numpy.nan` values in columns 'hasta', 'desde'."""
dropna_timeranges = dropna_rowsx('hasta', 'desde')


def format_date(x: date_time) -> str:
    return date_time.strftime(x, r"%d/%m/%Y")


def formate_valid_dates(x: date_time | Any) -> str | NaN:
    return format_date(x) if isinstance(x, date_time) \
            else x if isinstance(x, str) \
            else nan


def format_col_dates(df: DataFrame, col) -> DataFrame:
    apply_to_column(df, col, formate_valid_dates)
    return df


# Curried version of format_col_dates
def format_col_datesx(col):
    return lambda df: format_col_dates(df, col)


format_fecha = format_col_datesx('fecha')


def convert_time(x: str | dtime_object):
    if isinstance(x, str):
        # FIXME: Imlpement a better way to deal with broken strings.
        # The offenders are (regex):
        #   - [0-9]{2};[0-9]{2}
        #   - [0-9]{2}[;:]
        x = x.replace(';', ':')
        if len(x) < 4:
            x = ''.join(reversed(''.join(reversed(x)).zfill(4)))
        return convert_time(parse_time(x))
    elif isinstance(x, dtime_object):
        return Time(x.hour, x.minute)


column_to_time = partial(apply_to_column, f=convert_time)
desde_to_time = partial(column_to_time, col='desde')
hasta_to_time = partial(column_to_time, col='hasta')


def timeranges_to_time(df: DataFrame) -> DataFrame:
    desde_to_time(df)
    hasta_to_time(df)
    return df


class ExcelParser:
    @staticmethod
    # Function space forms a semigroup over composition (or a monoid with the identity function)
    def get(excel: ExcelFile) -> Callable:
        """Helper function for parsing an Excel (see `parse`).

           Composes together other functions and applies the result to an ExcelFile."""
        return compose(format_fecha,
                       timeranges_to_time,  # Fix broken timeranges and convert them
                       dropna_timeranges,   # Drop rows with 'nan' timeranges
                       fix_timerange,       # Normalize [start,end] -> ['desde', 'hasta']
                       clean_columns,       # Clean header names
                       drop_nan_cols,       # Drop cols with 'nan' header
                       drop_first_row,      # Set 1st row as header
                       excel.parse)         # Use the file's parser
