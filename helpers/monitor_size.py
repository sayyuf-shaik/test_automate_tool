
from PyQt5.QtWidgets import QDesktopWidget
import logging
LOG = logging.getLogger(__name__)


class MonitorSize(object):

    @staticmethod
    def get_size_of_monitor():
        """
        allow you to get size of your current screen
        -1 is to precise that it is the current screen
        :param None
        :return height, width:
        """
        size_object = QDesktopWidget().screenGeometry(-1)
        LOG.debug('Getting the monitor size = {0}'.format(size_object))
        LOG.debug('Height = {0} Width = {1}'.format(size_object.height(),
                                                    size_object.width()))
        return size_object.height(), size_object.width()
