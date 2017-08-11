import logging
import time
import datetime
import os
from src.strings import paths


class Logger:
    """
    Logger class which log every information on log file
    depends on logging level.
    """

    def __init__(self):
        # directory path
        __path = os.path.join(paths.project, '.log')

        # create .log directory if not exists
        self.__make_dir(__path)

        # filename as a timestamp
        __date_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H.%M')
        __filename = '{}.log'.format(__date_str)

        # logging level
        # change it if you want to change logging level of Logger
        __level = logging.DEBUG

        # configuration logging
        logging.basicConfig(filename=os.path.join(__path, __filename), level=__level)

        # change level of other libraries logger
        self.change_level("neo4j.bolt", logging.WARNING)

    # ==================================================================================================================
    # Public
    # ==================================================================================================================
    @staticmethod
    def debug(message):
        """
        logs debug messages, level:0
        :param message: that will log
        """
        logging.info(message)

    @staticmethod
    def info(message):
        """
        logs informative messages, level:1
        :param message: that will log
        """
        logging.info(message)

    @staticmethod
    def warning(message):
        """
        logs warning messages, level:2
        :param message: that will log
        """
        logging.info(message)

    @staticmethod
    def error(message):
        """
        logs error messages, level:3
        :param message: that will log
        """
        logging.info(message)

    @staticmethod
    def critical(message):
        """
        logs important error (critical) messages, level:4
        :param message: that will log
        """
        logging.info(message)

    @staticmethod
    def change_level(logger_name, level):
        """
        change logging level of logger
        :param logger_name: logger that is changing level
        :param level: new level to be set to logger
        """
        logging.getLogger(logger_name).setLevel(level)

    # ==================================================================================================================
    # Private
    # ==================================================================================================================
    @staticmethod
    def __make_dir(path):
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
                print path + ' is created.'
            except WindowsError:
                print 'Something wrong creating directory!'
