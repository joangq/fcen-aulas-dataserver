import os
import errno
import json
from typing import Dict, List, Generator, TypeVar, Tuple

from pandas import DataFrame

from src.hours import TimeRange, Time
from src.util.lista import lista

A = TypeVar('A')


def file(filename: str):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return filename


def extract_intervals(df: DataFrame) -> Dict:
    result: Dict = dict()
    for t in df[['aula', 'desde', 'hasta']].itertuples(index=False):
        result.setdefault(t.aula, [])
        interval = TimeRange(t.desde, t.hasta)
        result[t.aula].append(interval)

    for aula, _ in result.items():
        result[aula].sort(key=lambda x: x.low)
    return result


def indices_merged_intervals(intervals: List[TimeRange]) -> List[List[int]]:
    if len(intervals) == 1:
        return [[0]]

    result = lista()
    for i in range(0, len(intervals) - 1, 1):
        j = i + 1
        x = intervals[i]
        y = intervals[j]

        if x.high == y.low:
            if len(result) == 0:
                result.append(set())
            result[-1].add(i)
            result[-1].add(j)
        else:
            if j != len(intervals) - 1:
                result.append({i})
            result.append({j})

    return lista(result.map(lista))


def merge_by_indices(intervals: List[TimeRange], indices: List[List[int]]) -> List[TimeRange]:
    res = []
    for junction in indices:
        i = junction[0]
        j = junction[-1]
        (l, _) = intervals[i]
        (_, h) = intervals[j]
        res.append(TimeRange(low=l, high=h))
    return res


def merge_adjacent(intervals: List[TimeRange]):
    indices = indices_merged_intervals(intervals)
    intervals = merge_by_indices(intervals, indices)
    return intervals


def pair_up(intervals: List[A]) -> Generator[Tuple[A, A], None, None]:
    """Converts a flat list to a list of 2-tuples. Drops the last element if (len(list) % 2) != 0"""
    return ((intervals[i], intervals[i + 1]) for i in range(0, len(intervals) - 1, 2))


def free_time(intervals: List[TimeRange],
              limits=TimeRange(Time(9, 0), Time(22, 0)))\
              -> List[TimeRange]:
    flat = [limits.low]
    for a, b in intervals:
        flat.append(a)
        flat.append(b)
    flat.append(limits.high)

    result = [TimeRange(low=a, high=b) for a, b in pair_up(flat) if a != b]
    return result


def extract_uptime_downtime(df):
    intervals = extract_intervals(df)
    intervals = {aula: merge_adjacent(xs) for aula, xs in intervals.items()}

    output = dict()
    for aula, xs in intervals.items():
        output.setdefault(aula, dict())
        output[aula].setdefault('ocupado', xs)
        output[aula].setdefault('libre', free_time(xs))

    return output


def export_uptime_downtime(df, filename):
    with open(file(f'./output/timetables/{filename}.timetable.json'), 'w') as f:
        json.dump(fp=f,
                  obj=extract_uptime_downtime(df),
                  cls=TimeRange.CustomEncoder,
                  indent=3)
