import logging
import time
import datetime

# filename as a timestamp
_date_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H.%M.%S')
_filename = '../.log/{}.log'.format(_date_str)

# logging level
_level = logging.DEBUG

# configuration logging
logging.basicConfig(filename=_filename, level=_level)


# logging functions
# they get message and logs
def info(message):
    logging.info(message)


def debug(message):
    logging.debug(message)


def warning(message):
    logging.warning(message)


def error(message):
    logging.error(message)


def critical(message):
    logging.critical(message)


# utility functions logger
def change_level(level):
    """
    change logging level of logger
    :param level: new level to be set to logger
    :return: nothing
    """
    logging.getLogger().setLevel(level)
