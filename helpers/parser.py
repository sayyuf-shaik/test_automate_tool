import re
import logging

LOG = logging.getLogger(__name__)


class Parser(object):
    """
    class which will parse the output of the runltp and gets the test case
     pass/fail count
    """
    LOG.info('In Parser class')

    def __init__(self):
        pass

    @staticmethod
    def get_count(output):
        """
        method which will get the count of test failed and test passed
        :param output:
        :return list of failed and passed test count:
        :author sayyuf shaik:
        """
        LOG.info('In get_count')
        position_hits = []
        pattern = re.compile(r'TFAIL',
                             re.IGNORECASE | re.MULTILINE)
        result = re.findall(pattern, output)
        pattern = re.compile(r'TPASS', re.MULTILINE)
        result_2 = re.findall(pattern, output)
        count_pass = len(result_2)
        count_fail = len(result)
        position_hits.append(count_pass)
        position_hits.append(count_fail)
        LOG.debug('Test Passed = {0} and Test Failed = {1}'.format(count_pass,
                                                                   count_fail))
        return position_hits


if __name__ == '__main__':
    parse = Parser()
