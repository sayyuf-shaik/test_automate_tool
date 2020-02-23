
from helpers import log_utils as log_obj
from helpers.output_write import OutputWrite
from helpers import global_constants
import logging
import sys
import os


root_log = logging.root
log = logging.getLogger(__name__)


def script_logger(file_name, level=logging.INFO):

    # creating the file
    f_name = file_name + OutputWrite.get_time_stamp() + '.log'
    logger_file_handler = logging.FileHandler(os.path.join(get_dir_path(),
                                                           f_name))
    logger_file_handler.setLevel(level)
    logger_file_handler.setFormatter(log_obj.FileFormatter())
    return logger_file_handler


def setup_logging(file_name, level=logging.DEBUG):
    fmt = log_obj.StdFormatter()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    root_log.addHandler(stdout_handler)
    root_log.setLevel(logging.DEBUG)
    logging.getLogger("paramiko").setLevel(logging.CRITICAL + 1)
    logging.getLogger("matplotlib").setLevel(logging.CRITICAL + 1)
    script_log = script_logger(file_name, level)
    script_log.setLevel(logging.DEBUG)
    root_log.addHandler(script_log)
    return root_log


def get_dir_path():
    """
    Creates the directory structure
    :return path:
    """
    OutputWrite.change_to_script_directory(__file__)
    path = os.path.abspath(os.path.join('..', 'framework_logs',
                                        ))
    os.makedirs(path, exist_ok=True, mode=0o755)

    print('Path for log files = {0}'.format(path))
    return path


