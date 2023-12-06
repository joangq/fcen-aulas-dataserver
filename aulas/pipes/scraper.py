import os
import shutil
import pandas as pd
from datetime import datetime, timedelta
from timeit import default_timer

from aulas.logger import LoggerFactory
from aulas.pipes.xlsx import convert_from_excel
from aulas.util.files import geturl
from aulas.util.files.inout import file

log = LoggerFactory.getLogger("scraper")


def get_creation_date(file_path):
    creation_time = os.path.getctime(file_path)
    creation_date = datetime.fromtimestamp(creation_time)

    return creation_date


def get_age(fp):
    current_datetime = datetime.now()
    creation_date = get_creation_date(fp)
    age = current_datetime - creation_date
    return age


def is_old_file(fp, threshold: timedelta):
    return get_age(fp) >= threshold


def current_time():
    now = datetime.now()
    formatted_time = now.strftime("%H%M%S")
    return formatted_time


def compare_xlsxs(filename1, filename2):
    df1 = pd.read_excel(filename1)
    df2 = pd.read_excel(filename2)

    return df1.equals(df2)


def temp_download(url: str, path: None | str = None, filename: None | str = None, extension=None):
    should_process: bool

    fp = file(path + filename) + extension
    tfilename = filename + '-temp_' + current_time()
    tpath = './.temp/'
    tfp = tpath + tfilename + extension

    time_elapsed = default_timer()
    geturl(url=url, path=tpath, filename=tfilename, extension=extension)
    time_elapsed = default_timer() - time_elapsed
    log.info(f"Downloaded '{tfilename}' in {timedelta(seconds=time_elapsed)}")

    if not os.path.exists(fp):
        log.info("File doesn't exist, making it the original one.")
        shutil.move(tfp, fp)
        should_process = True
    else:
        time_elapsed = default_timer()
        should_process = override_if_neq(compare_xlsxs, fp, tfp)
        time_elapsed = default_timer() - time_elapsed
        log.info(f"Comparison took {timedelta(seconds=time_elapsed)}")

    os.rmdir(tpath)
    return should_process


def override_if_neq(compare, fp, tfp):
    files_are_equal = compare(fp, tfp)
    if files_are_equal:
        log.info('Files are equal, skipping processing.')
        os.remove(tfp)
    else:
        log.info("Files aren't equal, overriding with new one.")
        shutil.move(tfp, fp)
    return not files_are_equal



