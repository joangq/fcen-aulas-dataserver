from pandas import DataFrame
from typing import Dict, List, Generator, TypeVar, Tuple
from aulas.util.structs import lista
from aulas.util.structs.time import TimeRange, Time

A = TypeVar('A')


def extract_intervals(df: DataFrame) -> Dict:
    """Extracts the time intervals from the dataframe.
    Basically pairs up the from->to columns.

    e.g:
        INPUT:
            1103: {from: [11:00, 14:00]
                   to: [14:00, 17:00]}
        OUTPUT:
            1103: [11:00--14:00, 14:00--17:00]
    """
    result: Dict = dict()
    for t in df[['aula', 'desde', 'hasta']].itertuples(index=False):
        result.setdefault(t.aula, [])
        interval = TimeRange(t.desde, t.hasta)
        result[t.aula].append(interval)

    for aula, _ in result.items():
        result[aula].sort(key=lambda x: x.low)
    return result


def indices_merged_intervals(intervals: List[TimeRange]) -> List[List[int]]:
    """Takes in a list of timeranges and returns a list of list of merged indices.

    e.g:
        INPUT: [11:00 -- 14:00, 14:00 -- 17:00, 19:00 -- 22:00]
        OUTPUT: [[0, 1], [2]]
    """
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
    """Takes in a list of indices and a list of intervals, and merges them by the index list.

    e.g:
        INPUT: [11:00 -- 14:00, 14:00 -- 17:00, 19:00 -- 22:00], [[0, 1], [2]]
        OUTPUT: [11:00 -- 17:00, 19:00 -- 22:00]"""
    res = []
    for junction in indices:
        i = junction[0]
        j = junction[-1]
        (l, _) = intervals[i]
        (_, h) = intervals[j]
        res.append(TimeRange(low=l, high=h))
    return res


def merge_adjacent(intervals: List[TimeRange]):
    """Merges adjacent timeranges.

    e.g:
        INPUT:
            [11:00--14:00, 14:00--17:00]
        OUTPUT:
            [11:00--17:00]
    """
    indices = indices_merged_intervals(intervals)
    intervals = merge_by_indices(intervals, indices)
    return intervals


def pair_up(intervals: List[A]) -> Generator[Tuple[A, A], None, None]:
    """Converts a flat list to a list of 2-tuples. Drops the last element if (len(list) % 2) != 0"""
    return ((intervals[i], intervals[i + 1]) for i in range(0, len(intervals) - 1, 2))


def free_time(intervals: List[TimeRange],
              limits=TimeRange(Time(9, 0), Time(22, 0))) \
        -> List[TimeRange]:
    """Given a list of busy timeranges, returns a list of free timeranges.
    It needs the time limits. Essentially calculates the complement of the range (with respect to the limits)."""
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
