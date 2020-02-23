import os
import time
import datetime
from helpers import global_constants
import logging

LOG = logging.getLogger(__name__)


class OutputWrite(object):

    @staticmethod
    def write_to_output(output):
        """
        module which will write the output to a text file
        :param output:
        :return None:
        :Author Sayyuf Shaik:
        """
        try:
            # changing current directory to script directory
            OutputWrite.change_to_script_directory(__file__)
            # writing the output a file
            timestamp_in_secs = time.time()
            time_stamp_readable = datetime.datetime.fromtimestamp(
                timestamp_in_secs).strftime("%Y_%m_%d-%Ih_%Mm_%Ss_%p")
            try:
                if not os.path.isdir('../results'):
                    os.chdir('..')
                    print('Current directory {0}'.format(os.getcwd()))
                    os.mkdir('./results')
                    OutputWrite.change_to_script_directory(__file__)
            except OSError as _ex_:
                print("Unable to create results directory {0}".format(_ex_))
            abspath = os.path.abspath('..')
            print('abspath of ..', abspath)
            path = OutputWrite.create_dir_structure()
            file_name = os.path.join(path, 'output_' +
                                     time_stamp_readable)
            print('The file name after joining', file_name)
            with open(file_name, 'w') as file_obj:
                file_obj.write(output)

        except FileNotFoundError as err:
            print('Unable write the test results into the file {0}'.
                  format(err))

    @staticmethod
    def make_test_dir(path, test_name):
        """
        method which will create the directory with test execution name
        :param path:
        :param test_name:
        :return path_with_test_name:
        """
        LOG.info('In make_test_dir')
        OutputWrite.change_to_script_directory(__file__)
        path_with_test_name = os.path.join(path, test_name)
        LOG.debug('Path with Test name = {0}'.format(path_with_test_name))
        os.makedirs(path_with_test_name, exist_ok=True)
        print('path with test name {0}'.format(path_with_test_name))
        return path_with_test_name

    @staticmethod
    def write_to_file(output, test_case_name, path):
        """
        which will write the logs to the individual file
        :param output:
        :param test_case_name:
        :param path:
        :return:
        """
        path_to_store = OutputWrite.make_test_dir(path, test_case_name)
        time_stamp = OutputWrite.get_time_stamp()
        try:
            LOG.debug('Changing the dir to {0}'.format(path_to_store))
            os.chdir(path_to_store)
        except Exception as _ex_:
            LOG.exception('Error :{0}'.format(_ex_))
        else:
            file_name = os.path.join(path_to_store, test_case_name +
                                     time_stamp)
            LOG.debug('The file name after joining = {0}'.format(file_name))
            try:
                LOG.debug('Writing Test case output to the file')
                with open(file_name, 'w') as file_obj:
                    file_obj.write(output)
            except FileNotFoundError as _ex_:
                LOG.exception('Error : {0}'.format(_ex_))

    @staticmethod
    def get_time_stamp():
        """
        get the current time stamp to append the log file name
        :return time_stamp_readable:
        """
        LOG.info('In get_time_stamp')
        timestamp_in_secs = time.time()
        time_stamp_readable = datetime.datetime.fromtimestamp(
            timestamp_in_secs).strftime(" %Y_%m_%d-%Ih_%Mm_%Ss_%p")
        LOG.debug('Time Stamp Readable {0}'.format(time_stamp_readable))
        return time_stamp_readable

    @staticmethod
    def change_to_script_directory(file_path):
        """
        Method which will change the current working directory to the current
        script directory
        :param file_path:
        :return d_name:
        """
        LOG.info('In change_to_script_directory')
        abspath = os.path.abspath(file_path)
        d_name = os.path.dirname(abspath)
        LOG.debug('after getting the path of the script {0}'.format(d_name))
        LOG.debug('Changing the dir to {0}'.format(d_name))
        os.chdir(d_name)
        return d_name

    @staticmethod
    def create_dir_structure():
        """
        Creates the directory structure
        :return path:
        """
        LOG.info('In create_dir_structure')
        OutputWrite.change_to_script_directory(__file__)
        path = os.path.abspath(os.path.join('..', 'results',
                                            global_constants.TEXT_BOARD,
                                            global_constants.TEXT_INTERFACE,
                                            global_constants.TEXT_DEVICE,
                                            global_constants.TEST_EXECUTION_NAME
                                            ))
        LOG.debug('Path to be Created = {0}'.format(path))
        os.makedirs(path, exist_ok=True, mode=0o755)
        for item in global_constants.TEST_CASE_LIST_NAMES:
            in_path = os.path.exists(os.path.join(path, item))
            if not os.path.exists(in_path):
                LOG.debug('Path with Test Case name = {0}'.format(in_path))
                os.mkdir(in_path)
        LOG.debug('Path = {0}'.format(path))
        return path
