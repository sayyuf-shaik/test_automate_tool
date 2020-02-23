from PyQt5 import QtWidgets, QtCore
from helpers import global_constants
import logging

LOG = logging.getLogger(__name__)


class Common(object):

    def clear_QtableWidget(self, instance):
        self.gui_utils = instance
        try:
            LOG.info('Getting the test cases from a file')
            # Setting the flag to True
            # global_constants.FROM_DB = True
            # global_constants.TEST_EXECUTION_NAME = ''

            item = QtWidgets.QTableWidgetItem()
            item.setText('Test Id')
            self.gui_utils.tableWidget.setHorizontalHeaderItem(0, item)
            self.gui_utils.tableWidget.horizontalHeaderItem(0). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            item = QtWidgets.QTableWidgetItem()
            item.setText('Description')
            self.gui_utils.tableWidget.setHorizontalHeaderItem(1, item)
            self.gui_utils.tableWidget.horizontalHeaderItem(1). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            # adding the checkboxes to the table widget
            self.gui_utils.tableWidget.setRowCount(self.gui_utils.count)
            LOG.debug('Clearing the Test Cases')
            for i in range(self.gui_utils.count):
                for j in range(2):
                    if j == 1:
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText('')
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.gui_utils.tableWidget.setItem(i, j, item)
        except Exception as _ex_:
            LOG.exception(_ex_)
