import sys
import logging
import pytz
from datetime import datetime, timedelta, timezone


class Colors:
    RESET = "\033[0m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    GREY = "\033[0;90m"
    RED_BRIGHT = "\033[1;31m"

    @staticmethod
    def colorize(color, x):
        return color + x + Colors.RESET


__format__ = lambda logger_color: Colors.colorize(Colors.GREY, "[%(asctime)s] ") + \
                                  Colors.colorize(logger_color, "[%(levelname)s] ") + \
                                  Colors.colorize(Colors.YELLOW, "[%(name)s] ") + \
                                  "%(message)s "


class MyFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: __format__(Colors.GREEN),
        logging.INFO: __format__(Colors.BLUE),
        logging.WARNING: __format__(Colors.RED),
        logging.ERROR: __format__(Colors.RED_BRIGHT),
        logging.CRITICAL: __format__(Colors.RED_BRIGHT)
    }

    @staticmethod
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        tzinfo = pytz.timezone('Etc/GMT+3')
        return tzinfo.localize(dt)

    def formatTime(self, record, datefmt=None):
        dt = MyFormatter.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)


class LoggerFactory:

    @staticmethod
    def getLogger(name):
        logger = logging.getLogger(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(MyFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
