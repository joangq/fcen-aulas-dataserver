import pandas as pd
import errno
import os


def file(filename: str):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return filename


def load(s):
    return pd.read_json(s, convert_dates=False, convert_axes=False)
