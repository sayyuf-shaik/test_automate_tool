"""
Module where actions to the DDTT GUI are implemented
"""
import pony.orm as pny
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMessageBox
from helpers.parser import Parser
from helpers.console_QthreadPool import CommandThread
from helpers.output_write import OutputWrite
from helpers.yaml_utils import YamlUtils
from helpers import global_constants
from gui.test_browser import FileBrowser
from helpers.common import Common
import logging


LOG = logging.getLogger(__name__)

# -----------------------------------------------------------------------
# Creating a database
# -----------------------------------------------------------------------
unicode = str

database = pny.Database("sqlite",
                        "../resources/test.db",
                        create_db=True)


########################################################################

class Table(database.Entity):
    """
    Pony ORM model of the Artist table
    """
    name = pny.Required(unicode)
    board = pny.Required(str)
    interface = pny.Required(str)
    device = pny.Required(str)
    tests = pny.Set("Tests")


########################################################################
class Tests(database.Entity):
    """
    Pony ORM model of album table
    """
    table_name = pny.Required(Table)
    title = pny.Required(unicode)
    description = pny.Required(unicode)
    test_id = pny.Required(int)


# ------------------------------------------
# map the models to the database
# and create the tables, if they don't exist
database.generate_mapping(create_tables=True)
# -------------------------------------------


class Actions(object):
    """
    Class Actions where actions to the particular events are implemented

    """
    def __init__(self, instance):

        """
        assigning the instance of GUI to the self
        :param instance: instance of the GUI
        """
        LOG.info('Initializing the action class')
        self.gui_utils = instance
        self.parser = Parser()
        self.test_passed_count = 0
        self.test_failed_count = 0
        # Initial values when nothing is selected
        self.gui_utils.text_board = 'RPI3'
        self.gui_utils.text_interface = 'bitbSPI'
        self.gui_utils.text_device = 'RTC'
        LOG.info('Creating the instance of Yaml Utils')
        self.yaml_utils = YamlUtils()
        self.test_browser = FileBrowser()

    @pny.db_session
    def get_selected_items(self):
        """
        Getting the selected items and selected indexes of the test cases
        :return:
        """
        # DataBase.create_database()
        LOG.info('Getting the selected items')
        self.gui_utils.checked_items = []
        self.gui_utils.index_checked = []
        # Looping through the Table Widget
        LOG.info('Getting the selected items from QTableWidget')
        for index in range(self.gui_utils.count):
            # Checking whether the item is selected or not
            if self.gui_utils.tableWidget.item(index, 0).checkState() \
                    == Qt.Checked:
                # appending the selected items to a list
                LOG.debug('Checking each test cases {0}'.format(index))
                self.gui_utils.checked_items.append\
                    (self.gui_utils.tableWidget.item(index, 0).text())
                LOG.debug('Appending the items to the List'.format(
                    self.gui_utils.tableWidget.item(index, 0).text()))
                self.gui_utils.index_checked.append(index)
        LOG.info('Storing the checked items in a global variable')
        # Storing the checked items in a global variable
        global_constants.TEST_CASE_LIST_NAMES = self.gui_utils.checked_items
        # Setting no of test cases in the test case count label
        self.gui_utils.label_interface1.setText(
            str(len(self.gui_utils.checked_items)))
        """Setting the Test Execution Name in Execution Summary tab and test
         creation tab"""
        self.gui_utils.label_name_of_the_test.setText(
            self.gui_utils.test_execution_name.text())
        self.gui_utils.summary_execution_name.setText(
            self.gui_utils.test_execution_name.text())
        # storing the total selected test case count
        global_constants.TEST_COUNT = len(self.gui_utils.index_checked)
        # storing the test execution name in global variable
        global_constants.TEST_EXECUTION_NAME = self.gui_utils.\
            test_execution_name.text()

        # ----------------------------------------------------------------------
        # Checking the name in data base
        name_is_there = False
        table_names = pny.select(i.name for i in Table).fetch()
        for name in table_names:
            if global_constants.TEST_EXECUTION_NAME == name:
                name_is_there = True
        # ---------------------------------------------------------------------
        # Checking for all valid conditions
        if not global_constants.TEST_EXECUTION_NAME:
            msg = "Give Proper Test Execution Name"
            LOG.debug('No test case name')
            QMessageBox.warning(None, 'Warning', msg)
        elif not self.gui_utils.index_checked:
            msg = "Select Test cases"
            LOG.debug('Test Cases are not selected')
            QMessageBox.warning(None, 'Warning', msg)
        elif name_is_there and global_constants.FROM_DB is False:
            msg = "The Test Execution Name is already in Database. Give another" \
                  " name"
            self.message_box(msg, 'Warning')
        else:
            self.gui_utils.tab_2.setEnabled(True)
            self.gui_utils.tab_3.setEnabled(True)
            QtWidgets.QTabWidget.setCurrentIndex(
                self.gui_utils.test_count_label, 1)
            self.gui_utils.start_execution_buttion.setEnabled(True)
            LOG.debug('Valid Selection and Valid Test Case Name {0}'.format(
                global_constants.TEST_EXECUTION_NAME))

    @staticmethod
    def message_box(msg, level):
        QMessageBox.warning(None, level, msg)

    def on_board_changed(self, text='RPI3'):
        """
        called when the Board QCombobox is changed
        :param text: str of the QCombobox changed
        :return:
        """
        self.gui_utils.text_board = text
        LOG.info('Board QCombobox is changed {0}'.format(text))

    def on_interface_changed(self, text='bitbSPI'):
        """
        called when the interface QCombobox is changed
        :param text: str of the QCombobox is changed
        :return:
        """
        self.gui_utils.text_interface = text
        LOG.info('Interface QCombobox is changed to {0}'.format(text))

    def on_device_changed(self, text='RTC'):
        """
        called when the device QCombobox is changed
        :param text: str of the QCombobox is changed
        :return:
        """

        self.gui_utils.text_device = text
        LOG.info('Device QCombobox is changed to {0}'.format(text))

    # storing the configuration details
    def get_configuration_details(self):
        """
        Getting the user configuration details
        :return:
        """
        # storing the param_one
        self.gui_utils.param_one = self.gui_utils.text_param_one.text()
        # storing the param_two
        self.gui_utils.param_two = self.gui_utils.text_param_two.text()
        # storing the ip
        self.gui_utils.ip = self.gui_utils.text_ip.text()

    def on_start_button_clicked(self):
        """
            This method executes when user clicked on start button
            :Author Sayyuf Shaik:
            :return None:
        """
        LOG.info('Start Button Clicked')
        # Setting the flags
        global_constants.TEST_PASSED_COUNT = 0
        global_constants.TEST_IN_PROGRESS_COUNT = 0
        global_constants.TEST_FAILED_COUNT = 0
        global_constants.TEST_COUNT = 0
        # setting the execution start

        self.gui_utils.execution_status_lable.setText('Start')
        # disabling the start button once execution has started
        LOG.info('Disabling the start button once execution has started')
        self.gui_utils.start_execution_buttion.setEnabled(False)
        LOG.info('Enabling stop button once execution has started')
        # enabling stop button once execution has started
        self.gui_utils.stop_execution_button.setEnabled(True)
        LOG.debug('Reading the password from config file')
        # Reading the password from config file
        self.gui_utils.sudo_password = self.yaml_utils.read_yml("CONFIGURATIONS"
                                                                , "PASSWORD")
        # disabling the test case start and stop buttons
        self.gui_utils.create_test_cases_button.setEnabled(False)
        self.gui_utils.clear_test_cases_button.setEnabled(False)
        # setting the text edit area as Read Only
        self.gui_utils.text_edit.setReadOnly(True)
        # setting the color of terminal
        self.gui_utils.text_edit.setPalette(QPalette(Qt.black))
        self.gui_utils.terminal_scrollArea.setWidget(self.gui_utils.text_edit)
        print("Checked items:{0}".format(self.gui_utils.index_checked))
        # To execute SPI Related Test Cases
        if self.gui_utils.text_interface == 'SPI' or global_constants.FROM_DB:
            LOG.debug('SPI test cases are executing')
            # creating an object of CommandThread
            self.load_selected_test_cases_to_tab()
            self.gui_utils.interface = 'spi0'
            self.thread = CommandThread(self.gui_utils)
            self.thread.get_output()
        elif self.gui_utils.text_interface == 'I2C':
            """QMessageBox.about(None, 'Not Implemented', 'These Test cases not'
                                                       ' yet implemented')"""
            self.load_selected_test_cases_to_tab()
            self.gui_utils.interface = 'i2c0'
            self.thread = CommandThread(self.gui_utils)
            self.thread.get_output()
            """self.clear_checked_items()
            self.gui_utils.create_test_cases_button.setEnabled(True)
            self.gui_utils.clear_test_cases_button.setEnabled(True)"""

        elif self.gui_utils.text_interface == 'bitbSPI':
            self.load_selected_test_cases_to_tab()
            self.gui_utils.interface = 'bitbspi0'
            self.thread = CommandThread(self.gui_utils)
            self.thread.get_output()
        else:
            QMessageBox.about(None, 'Not Implemented', 'These Test cases not'
                                                       ' yet implemented')
            self.clear_checked_items()
            self.gui_utils.create_test_cases_button.setEnabled(True)
            self.gui_utils.clear_test_cases_button.setEnabled(True)
            # left for implementation of I2C and BitbangingSPI

    def clear_checked_items(self):
        """
        This method is called when the clear button is clicked.
        It clears the all checked items in the test execution selection tab
        :return None:
        :Author Sayyuf Shaik
        """
        LOG.info('Clearing the Selected items')
        # Looping through the Table Widget
        self.gui_utils.create_test_cases_button.setEnabled(True)
        try:
            for index in range(self.gui_utils.count):
                LOG.debug('Checking whether the item is selected or not')
                # Checking whether the item is selected or not
                if self.gui_utils.tableWidget.item(
                        index, 0).checkState() == Qt.Checked:
                    LOG.debug('un checking the checked items')
                    # un checking the checked items
                    self.gui_utils.tableWidget.item(
                        index, 0).setCheckState(Qt.Unchecked)
            # unchecking select all check box
            LOG.debug('unchecking select all check box')
            if self.gui_utils.select_all_check_box.checkState() == Qt.Checked:
                self.gui_utils.select_all_check_box.setCheckState(Qt.Unchecked)
            # Setting no of test cases in the test case count label
            LOG.debug('Clearing the test Execution name in QLineEdit')
            # Clearing the test Execution name in QLineEdit
            self.gui_utils.test_execution_name.clear()
            LOG.debug('Clearing the output in the terminal')
            # Clearing the output in the terminal
            self.gui_utils.text_edit.clear()
            global_constants.TEST_IN_PROGRESS_COUNT = 0
            global_constants.TEST_FAILED_COUNT = 0
            global_constants.TEST_PASSED_COUNT = 0
            global_constants.TEST_COUNT = 0
            # Clearing the values of current test execution
            # Emptying the Test execution name in test run and text summary tabs
            self.gui_utils.label_name_of_the_test.setText("")
            self.gui_utils.summary_execution_name.setText(" ")
            # Setting the progress bar to the Zero
            self.gui_utils.progressBar_completion.setValue(0)
            # Setting the test count to zero
            self.gui_utils.label_interface1.setText(
                str(0))
            # Clearing the values in Test passed and Test Failed
            self.gui_utils.passed_lcd.setText(str(
                global_constants.TEST_PASSED_COUNT))
            self.gui_utils.failed_lcd.setText(str(
                global_constants.TEST_FAILED_COUNT))
        except Exception as generic_exception:
            LOG.exception(generic_exception)

    def select_all(self):
        """
        This methods checks the all unchecked test cases
        :return None:
        :Author Sayyuf Shaik
        """
        LOG.info('Selecting the All test cases')
        try:
            # Checking whether the select all check box is checked or not
            if self.gui_utils.select_all_check_box.checkState() == Qt.Checked:

                for index in range(self.gui_utils.count):
                    LOG.debug('Checking {0} Test case'.format(index))
                    # Checking whether the item is selected or not
                    self.gui_utils.tableWidget.item(index, 0).setCheckState(
                        Qt.Checked)
            else:
                for index in range(self.gui_utils.count):
                    # Checking whether the item is selected or not
                    LOG.debug('UnChecking {0} Test case'.format(index))
                    self.gui_utils.tableWidget.item(index, 0).setCheckState(
                        Qt.Unchecked)
            # Setting no of test cases in the test case count label
        except Exception as generic_exception:
            LOG.exception(generic_exception)

    def on_submit_clicked(self):
        """
        When the submit button is clicked, this method stores the details
        :return None:
        :author sayyuf shaik:
        """
        LOG.info('Submit button is clicked')
        global_constants.FROM_DB = False
        global_constants.TEXT_BOARD = self.gui_utils.text_board
        global_constants.TEXT_INTERFACE = self.gui_utils.text_interface
        global_constants.TEXT_DEVICE = self.gui_utils.text_device
        LOG.info('The User selected "BOARD:"{0}, "INTERFACE:"{1}, "DEVICE:"{2}'.
                 format(self.gui_utils.text_board,
                        self.gui_utils.text_interface,
                        self.gui_utils.text_device))
        self.str_file_name = '{0}_{1}_{2}'.format(self.gui_utils.text_board,
                                             self.gui_utils.text_interface,
                                             self.gui_utils.text_device)
        LOG.debug('The File name Loaded {0}'.format(self.str_file_name))
        # Getting back to current script directory
        LOG.debug('Getting back to current script directory')
        OutputWrite.change_to_script_directory(__file__)
        # Opening the test case files
        LOG.debug('Opening the test case files')
        try:
            LOG.info('Getting the test cases from a file')
            with open('../resources/' + self.str_file_name, 'r') as file_obj:
                list_of_test_cases = file_obj.readlines()

                self.gui_utils.count = len(list_of_test_cases)

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
            LOG.debug('Populating the test cases to the QTableWidget')
            for i in range(self.gui_utils.count):
                test_case = list_of_test_cases[i].split(',')
                for j in range(2):
                    if j == 1:
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                      QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(test_case[j])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.gui_utils.tableWidget.setItem(i, j, item)
        except FileNotFoundError as file_error:
            LOG.exception(file_error)
            QMessageBox.warning(None, 'Warning', "Select Proper Test Case File")

    @staticmethod
    def on_stop_button_clicked():
        """
        Terminates the subprocess
        :return:
        """
        try:

            LOG.info('stop button clicked')
            global_constants.STOP_ENABLED = 1
            LOG.debug('Setting the STOP_ENABLED flag to {0}'.format(
                global_constants.STOP_ENABLED))
        except Exception as err:
            LOG.exception(err)

    @pny.db_session
    def load_selected_test_cases_to_tab(self):
        """
        Loads the selected tests cases into the QTableWidget in Execution
        Summary tab and updates the status of the individual test cases.
        :return:
        """
        """connection_obj = sqlite3.connect('../resources/Test.db')
        cur_obj = connection_obj.cursor()"""

        # Creating a database
        # create_database()

        try:
            LOG.info('Getting the test cases from a file')
            # Checking if the user has selected from the database
            if global_constants.FROM_DB is False:
                with open('../resources/' + self.str_file_name, 'r') as file_obj:
                    list_of_test_cases = file_obj.readlines()
                    print(list_of_test_cases)
            else:
                list_of_test_cases = self.list_test_cases
            self.gui_utils.count = len(list_of_test_cases)
            print(list_of_test_cases)
            item = QtWidgets.QTableWidgetItem()
            item.setText('Test Id')
            self.gui_utils.table_widget.setHorizontalHeaderItem(0, item)
            self.gui_utils.table_widget.horizontalHeaderItem(0). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            item = QtWidgets.QTableWidgetItem()
            item.setText('Description')
            self.gui_utils.table_widget.setHorizontalHeaderItem(1, item)
            self.gui_utils.table_widget.horizontalHeaderItem(1). \
                setTextAlignment(QtCore.Qt.AlignLeft)

            item = QtWidgets.QTableWidgetItem()
            item.setText('Status')
            self.gui_utils.table_widget.setHorizontalHeaderItem(2, item)
            self.gui_utils.table_widget.horizontalHeaderItem(2). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            # Setting the row count
            self.gui_utils.table_widget.setRowCount(len(
                self.gui_utils.index_checked))
            LOG.debug('Populating the test cases to the QTableWidget')
            print(self.gui_utils.index_checked)
            test_id = 0
            test_name = ''

            # ------------------------------------------------------------------
            # checking for the name in data base
            # ------------------------------------------------------------------
            name_is_there = False
            table_names = pny.select(i.name for i in Table).fetch()
            for name in table_names:
                if global_constants.TEST_EXECUTION_NAME == name:
                    name_is_there = True

            if global_constants.FROM_DB is False and name_is_there is False:
                test_name = Table(name=global_constants.TEST_EXECUTION_NAME,
                                  board=self.gui_utils.text_board,
                                  interface=self.gui_utils.text_interface,
                                  device=self.gui_utils.text_device)

            tests = []
            for i in self.gui_utils.index_checked:
                print('The value in i = {0}'.format(i))

                #global_constants.TEST_CASES_SELECTED.append(
                    #list_of_test_cases[i])
                test_case = list_of_test_cases[i].split(',')
                print(test_case)
                # Adding the data into the database
                test_list = {"table_name": test_name,
                             "title": test_case[0],
                             "description": test_case[1],
                             "test_id": test_id
                             }
                tests.append(test_list)
                for j in range(3):

                    item = QtWidgets.QTableWidgetItem()
                    if j == 2:
                        item.setText("")
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.gui_utils.table_widget.setItem(test_id, j, item)
                    else:
                        item.setText(test_case[j])
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.gui_utils.table_widget.setItem(test_id, j, item)
                test_id += 1
            print(tests)

            if global_constants.FROM_DB is False and name_is_there is False:
                for test in tests:
                    a = Tests(**test)

        except FileNotFoundError as file_error:
            LOG.exception(file_error)

    def on_load_clicked(self):
        """
        Whenever the user clicked on load button
        :return:
        """
        # Opening the db_session
        with pny.db_session:
            # Fetching the table names from the database
            table_names = pny.select(i.name for i in Table)
            board_names = pny.select(i.board for i in Table).fetch()
            interface_names = pny.select(i.interface for i in Table).fetch()
            device_names = pny.select(i.device for i in Table).fetch()
            board = self.gui_utils.text_board
            interface = self.gui_utils.text_interface
            device = self.gui_utils.text_device
            data = pny.select(item for item in Table if item.board == board and
                              item.interface == interface and
                              item.device == device)
            table_obj = data.fetch()
            list_of_tables = [table.name for table in table_obj]
            print('table names list', table_names)
            self.list_test_cases = []
            self.selected_list = []
            self.widget = QtWidgets.QWidget()
            self.list_widget = QtWidgets.QListWidget(self.widget)
            self.widget.setWindowTitle('Test Execution')
            self.list_widget.setGeometry(QtCore.QRect(10, 10, 500, 400))
            self.list_widget.setObjectName("listWidget")
            # self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            self.list_widget.itemSelectionChanged.connect(self.on_change)
            self.pushButton = QtWidgets.QPushButton(self.widget)
            self.pushButton.setGeometry(QtCore.QRect(520, 360, 89, 25))
            self.pushButton.setText("Select")
            self.pushButton.clicked.connect(self.on_close)
            self.widget.show()
            self.populate(list_of_tables, board_names, interface_names,
                          device_names)

    def on_change(self):
        self.selected_list = [(item.row(), item.data()) for item in self.list_widget.selectedIndexes()]
        print(self.selected_list)
        global_constants.TEST_EXECUTION_NAME_DB = self.selected_list[0][1]

    def populate(self, tables, board_names, interface_names,
                          device_names):
        for test_execution_name in tables:
            item = QtWidgets.QListWidgetItem()
            item.setText(test_execution_name)
            self.list_widget.addItem(item)

        """try:
            LOG.info('Creating a QTableWidget')
            item = QtWidgets.QTableWidgetItem()
            item.setText('Test Id')
            self.test_widget.setHorizontalHeaderItem(0, item)
            self.test_widget.horizontalHeaderItem(0). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            item = QtWidgets.QTableWidgetItem()
            item.setText('Description')
            self.test_widget.setHorizontalHeaderItem(1, item)
            self.test_widget.horizontalHeaderItem(1). \
                setTextAlignment(QtCore.Qt.AlignLeft)

            item = QtWidgets.QTableWidgetItem()
            item.setText('Status')
            self.gui_utils.table_widget.setHorizontalHeaderItem(2, item)
            self.gui_utils.table_widget.horizontalHeaderItem(2). \
                setTextAlignment(QtCore.Qt.AlignLeft)
            print(tables)
            print(board_names)
            print(interface_names)
            print(device_names)
        except Exception as _ex_:
            LOG.exception(_ex_)"""

    def on_close(self):
        self.widget.close()
        self.populate_test_create_tab()

    def populate_test_create_tab(self):
        Common.clear_QtableWidget(self, self.gui_utils)
        self.list_test_cases = []
        with pny.db_session:
            print('After the function')
            test = pny.select(
                    i for i in Tests if i.table_name == Table[
                        self.selected_list[0][0] + 1])

            for record in test:
                print('in for loop')
                print(record.title, record.description)
                self.list_test_cases.append("{0},{1}".format(
                 record.title, record.description))
            print(self.list_test_cases)
        # ----------------------------------------------------------------------
        # Populating Test Cases from the data base into the test create tab
        # ----------------------------------------------------------------------
        try:
            LOG.info('Getting the test cases from a file')
            # Setting the flag to True

            # global_constants.TEST_EXECUTION_NAME = ''
            list_of_test_cases = self.list_test_cases
            self.gui_utils.count = len(list_of_test_cases)

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
            LOG.debug('Populating the test cases to the QTableWidget')
            for i in range(self.gui_utils.count):
                test_case = list_of_test_cases[i].split(',')
                for j in range(2):
                    if j == 1:
                        item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                      QtCore.Qt.ItemIsEnabled)
                        item.setCheckState(QtCore.Qt.Unchecked)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(test_case[j])
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.gui_utils.tableWidget.setItem(i, j, item)

            # Populating test Execution names
            self.gui_utils.test_execution_name.setText(
                global_constants.TEST_EXECUTION_NAME_DB)
            #self.gui_utils.label_test_execution_name.setText(
             #   global_constants.TEST_EXECUTION_NAME_DB)
            self.gui_utils.summary_execution_name.setText(
                global_constants.TEST_EXECUTION_NAME_DB)
            global_constants.FROM_DB = True

        except Exception as error:
            LOG.exception(error)
