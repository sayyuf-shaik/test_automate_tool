import yaml
import os
import logging

LOG = logging.getLogger(__name__)


class YamlUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def read_yml(key, sub_key):
        """

        :param key:
        :param sub_key:
        :return value of the particular key:
        :Author Sayyuf Shaik:
        """
        try:
            # changing current directory to script directory
            abspath = os.path.abspath(__file__)
            d_name = os.path.dirname(abspath)
            os.chdir(d_name)
            # getting the password from config.yaml file
            LOG.debug('Getting the password from config.yaml file')
            with open('../resources/config.yaml', 'r') as file_obj:
                config_data = yaml.load(file_obj)
            value = str(config_data[key][sub_key])
            return value
        except Exception as generic_exception:
            LOG.exception('Unable get the {0}:{1} from config file {2}'.
                          format(key, sub_key, generic_exception))

    @staticmethod
    def file_write(file_path, data):
        """
        To write the data into the file
        :param file_path: Path of the file
        :param data: Data to write into the file
        :return None:
        :author Sayyuf Shaik:
        """
        try:
            with open(file_path, 'w') as file_obj:
                file_obj.write(data)
        except FileNotFoundError as _ex_:
            LOG.exception('Unable to found the file Error = {0}'.format(_ex_))

    @staticmethod
    def file_read(file_path):
        """
        To read from a file
        :param file_path:
        :return Data: Read from the file
        """
        try:
            with open(file_path, 'r') as file_obj:
                data = file_obj.readlines()
            return data

        except FileNotFoundError as _ex_:
            LOG.exception('Unable to found the file Error = {0}'.format(_ex_))




