import datetime
import locale
from time import sleep

from catthy import lista

from aulas.logger import LoggerFactory
from aulas.pipes.excel_parser import apply_to_column
from aulas.util.files.inout import load, file
from aulas.util.strings import clean
from aulas.util.structs.time import Time, mapply_tuplist_to_timerange

logger = LoggerFactory.getLogger("digest")


def get_weekday_locale(now):
    return now.strftime('%A')


def get_month_locale(now):
    return now.strftime("%B")


def get_month(now):
    return now.month


def get_cuat(month_n):
    return '1c' if month_n in range(3, 6 + 1) else \
        '2c' if month_n in range(8, 11 + 1) else 'ci'


def get_qday(now) -> str:
    return f'{clean(get_weekday_locale(now))}-{get_cuat(get_month(now))}'


# =========================================================================================== #

def __filter_timeranges__(now, x):
    return [s for s in filter(lambda l: l.low < l.high and l.high > now >= l.low, x)]


def filter_timeranges(now):
    return lambda x: __filter_timeranges__(now, x)


def __filter_cols__(now, x):
    y = x.apply(filter_timeranges(now))
    y = y[y.apply(lambda s: len(s) > 0)].dropna()
    return y


def filter_cols(now):
    return lambda x: __filter_cols__(now, x)


# =========================================================================================== #


def comparison_over_series(f):
    return lambda s: s.sort_index(ascending=True).map(f)


def compare_timeranges(now):
    return lambda t: (t.high - now, t.low)


def compare_timerange_lists(f):
    return lambda ts: f(ts[0])


# =========================================================================================== #


def loads(day):
    df = load('./resources/timetables/' + day + '.timetable.json')
    for col in df.columns:
        apply_to_column(df, col, mapply_tuplist_to_timerange)
    return df


def init_aulas(dt_now):
    today: str = get_qday(dt_now)
    df = loads(today)

    output = ''
    output += f'┌─────────────────────────────────┐\n'
    output += f'│ {today.ljust(12)}                    │\n'
    output += '└─────────────────────────────────┘'

    return df, output


def digest_aulas(df, t_now):
    aulas_ahora = df.T.iloc[:, ::-1].apply(filter_cols(t_now))
    libre = aulas_ahora['libre'].dropna()
    # ocupado = aulas_ahora['ocupado'].dropna()

    compare_from_now = compare_timeranges(t_now)

    comparator = comparison_over_series(compare_timerange_lists(compare_from_now))

    libre = libre.sort_values(key=comparator, ascending=False)

    output = ''
    output += '┌─────────────────────────────────┐\n'
    output += f'│ Hora actual: {t_now}              │\n'
    output += '├────────┬────────────────┬───────┤\n'
    output += '│ Aula   │    Horario     │ Queda │\n'
    output += '├────────┼────────────────┼───────┤\n'
    for aula, tiempo in lista(libre.index).zip(map(lambda x: x[0], libre)):
        time_ahead = tiempo.high - t_now
        time_ahead = Time(*divmod(time_ahead, 60))
        output += f'│ {str(aula).ljust(6)} │ {tiempo} │ {time_ahead} │\n'
    output += '└────────┴────────────────┴───────┘'

    return output


def update_latest_cache(now: datetime):
    df, day_str = init_aulas(now)

    table = digest_aulas(df, Time.now(now))
    output = day_str+'\n'+table
    with open(file('./cache/latest.txt'), 'w') as fp:
        fp.write(output)
        logger.info('Wrote to latest cache.')
