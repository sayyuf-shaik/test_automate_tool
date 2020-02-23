"""
Implementation of Logging module

"""
import logging
import os
import time
from helpers.output_write import OutputWrite


class LogHandler(logging.FileHandler):

    def __init__(self, level=logging.DEBUG):

        OutputWrite.change_to_script_directory(__file__)
        if not os.path.exists('../Logs'):
            os.makedirs(self.create_log_dir())
        file_name = 'script_logs ' + OutputWrite.get_time_stamp() + '.log'
        logging.FileHandler.__init__(self, file_name)
        self.setLevel(level)
        self.format(FileFormatter())

    @staticmethod
    def create_log_dir():
        path = os.path.abspath(os.path.join('..', 'Logs'))
        return path


class StdFormatter(logging.Formatter):

    std_format = '[%(name)s] %(funcName)s %(lineno)s %(levelname)s %(message)s'

    def __init__(self):
        logging.Formatter.__init__(self, self.std_format)


class FileFormatter(StdFormatter):

    std_format = '%(asctime)s: [%(name)s] [%(funcName)s] [%(lineno)s]' \
                 ' [%(levelname)s] %(message)s'

    def formatTime(self, record, datefmt=None):

        if datefmt:
            s = StdFormatter.formatTime(self, record, datefmt)
        else:
            time_struct = self.converter(record.created)
            s = time.strftime(
                "%Y-%m-%d %H:%M:%S.{:03.0f} %Z".format(record.msecs),
                time_struct)

        return s
