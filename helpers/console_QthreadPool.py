from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import os
import sys
from time import sleep
import time
import paramiko
import socket
import logging
from io import StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.yaml_utils import YamlUtils
from helpers.ping import Ping
from helpers.piechart_qtchart import PieChart
from helpers.output_write import OutputWrite
from helpers.parser import Parser
from helpers import global_constants
LOG = logging.getLogger(__name__)


class WorkerSignals(QObject):
    # creating a qt signal
    LOG.info('In class WorkerSignals')
    LOG.debug('Signals Are registered')
    signalStatus = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()
    test_name = QtCore.pyqtSignal(str, int)
    each_test_case_output = QtCore.pyqtSignal(str)
    progress_bar_completion = QtCore.pyqtSlot(int)
    pie_chart_slot = QtCore.pyqtSignal()
    LOG.debug('Signals Are registered')


class Worker(QRunnable):

    def __init__(self, instance, interface):
        super(Worker, self).__init__()
        LOG.info('In Worker Class')
        self.instance = instance
        self.interface = interface
        self.signals = WorkerSignals()
        self.yaml_utils = YamlUtils()
        self.parser = Parser()
        self.ssh = self.ssh_login()
        global_constants.TEST_IN_PROGRESS_COUNT = len(
            self.instance.index_checked)
        self.instance.pie_chart = PieChart(self.instance.tab_3)

    @QtCore.pyqtSlot()
    def run(self):
        LOG.info("In Run method")
        try:
            LOG.info('Executing the selected Test cases')
            # self.instance.start_execution_buttion.setEnabled(False)
            test_index = 0

            print('Signals Emitting to piechart')

            #self.gui_utils.pie_chart = PieChart(self.gui_utils.tab_3)

            for test_number in self.instance.index_checked:
                LOG.info("########################################")
                LOG.debug("Trying for {0} time:".format(test_number + 1))
                LOG.info("########################################")
                LOG.debug('global_constants.STOP_ENABLED'.format(
                    global_constants.STOP_ENABLED))
                if global_constants.STOP_ENABLED == 1:
                    LOG.debug('Closing the SSH connection')
                    self.ssh.close()
                    LOG.debug('Breaking from the Loop')
                    global_constants.STOP_ENABLED = 0
                    break

                LOG.debug('Executing the test case {0}'.format(
                    global_constants.TEST_CASE_LIST_NAMES[test_index]))
                output = self.ssh_exe_cmd(test_case_number=test_number,
                                          sudo_flag=True,
                                          ip=None)
                QtWidgets.QApplication.processEvents()
                LOG.debug("****Test Execution Completed*****")
                LOG.debug('Test Name {0}'.format(
                    self.instance.checked_items[test_index]))
                self.signals.test_name.emit(
                    self.instance.checked_items[test_index], test_index)
                test_index += 1
                LOG.debug('test_index - {0}'.format(test_index))
                LOG.debug('len of index - {0}'.format(len(
                    self.instance.index_checked)))

                value = int((test_index/len(self.instance.index_checked))*100)
                LOG.debug('value = {0}'.format(value))
                print(self.instance.index_checked)
                # self.signals.progress_bar_completion.emit(value)
                # self.instance.progressBar_completion.setValue(value)
                self.update_execution_summary(value, test_index)
                global_constants.TEST_IN_PROGRESS_COUNT -= 1

                self.signals.pie_chart_slot.emit()

        except Exception as err:
            LOG.exception(err)

        finally:
            LOG.info('******Executed Test Cases******')
            self.signals.signalStatus.emit('******Executed Test Cases******')
            print('control in final block')
            self.instance.execution_status_lable.setText('Stop')
            self.instance.stop_execution_button.setEnabled(False)
            self.instance.start_execution_buttion.setEnabled(False)

            try:
                self.ssh.close()
            except AttributeError as _ex_:
                LOG.exception(_ex_)

    def ssh_login(self, ip=None):
        """
        :Function Name  : ssh_login
        :Description    : Function for ssh login to client
        :param ip: None/string
        :return: connection object
        Author: sailaja.n

        """
        LOG.info('In ssh_login')
        try:
            if ip is not None:
                ip_address = ip
            else:
                ip_address = self.yaml_utils.read_yml("IP", "SSH_IP")
            LOG.debug('Got the IP = {0}'.format(ip_address))
            user_name = self.yaml_utils.read_yml("IP", "SSH_UNAME")
            LOG.debug('Got the User Name = {0}'.format(user_name))
            user_pass = self.yaml_utils.read_yml("IP", "SSH_PASSWD")
            ssh = paramiko.SSHClient()
            LOG.debug('Got the SSH object {0}'.format(ssh))
            ssh.load_system_host_keys()
            # add to list of known host if not present
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            QtWidgets.QApplication.processEvents()
            LOG.info('Pingiing to {0}'.format(ip_address))
            ping_status = Ping.ping_host(ip_address)
            if ping_status is False:
                print("ping to host failed")
                err = 'ping to host {0} failed'.format(ip_address)
                LOG.error(err)
                QMessageBox.warning(None, 'Network Error', err)
                self.instance.create_test_cases_button.setEnabled(True)
                self.gui_utils.clear_test_cases_button.setEnabled(True)
                return False
            ssh.connect(ip_address, username=user_name, password=user_pass)
            LOG.debug('connected to host {0} with user name {1}'.format(
                ip_address, user_name))
            return ssh
        except Exception as generic_except:
            print("Got Exception {0}".format(generic_except))
            err = "{0}".format(generic_except)
            QMessageBox.warning(None, 'Warning', err)
            LOG.error(err)
            return False

    def ssh_exe_cmd(self, test_case_number, sudo_flag=False, ip=None):
        """
        used to execute ssh cmd's
        :param cmd: cmd name
        :param sudo_flag: True/False
        :param ip: None/string
        :return: boolean/string if False and boolean/SSH object if True
        Author: sailaja.n
        """
        try:
            LOG.debug("inside ssh_exe_cmd")
            LOG.debug('ret_val ssh_login function {0}'.format(self.ssh))
            if self.ssh is False:
                return

            test_number = test_case_number
            timestamp_in_secs = time.gmtime()
            time_stamp_readable = time.strftime("%Y_%m_%d-%Hh_%Mm_%Ss",
                                                timestamp_in_secs)
            command = './runltp -s ' + self.interface + str(test_number + 1) + \
                       ' -p -l RUN_LTP_ON-' + time_stamp_readable + '.log'
            LOG.debug("Command to Execute {0}".format(command))
            if sudo_flag is True:
                ssh_passwd = self.yaml_utils.read_yml("IP", "SSH_PASSWD")
                sudo_cmd = "cd /opt/ltp/;echo '{0}' | sudo -S {1}"\
                    .format(ssh_passwd, command)
                command = sudo_cmd
                LOG.debug('ssh cmd is {0}'.format(command))
            # ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
            channel = self.ssh.get_transport().open_session()
            channel.settimeout(10800)
            LOG.debug('channel = {0}'.format(channel))
            try:
                LOG.info("Executing the command")
                channel.exec_command(command)
                output = ''
                # Getting the data from the buffer
                data = channel.recv(1024)
                output = output + data.decode()
                self.signals.signalStatus.emit(data.decode())
                # print('data = {0}'.format(data))

                # capturing data from a buffer Untill data becomes false
                LOG.info('Going into the while loop')
                while data:

                    data = channel.recv(1024).decode()
                    self.signals.signalStatus.emit(data)
                    output = output + data
                    # print(data)

                LOG.info("Got the data from the buffer")
            except socket.timeout:
                raise socket.timeout
            # Emitting the output after completing of each test case
            self.signals.each_test_case_output.emit(output)
            return [True, output]
        except Exception as _ex_:
            LOG.exception(_ex_)

    def update_execution_summary(self, value, test_index):
        # Dynamically Updating the value of the progress bar
        self.instance.progressBar_completion.setValue(value)
        # global_constants.TEST_COMPLETED_COUNT = test_index


class CommandThread(QtWidgets.QWidget):

    def __init__(self, text_edit):

        QtWidgets.QWidget.__init__(self)
        self.thread_pool = QThreadPool()
        self.gui_utils = text_edit
        self.text_edit = text_edit.text_edit
        self.output = ''
        self.worker = Worker(text_edit, self.gui_utils.interface)
        self.parser = Parser()
        self.thread_pool.start(self.worker)
        self.each_test_case_output_slot = ''
        self.path = OutputWrite.create_dir_structure()
        self.worker.signals.signalStatus.connect(self.update_status)
        self.worker.signals.finished.connect(self.get_output)
        self.worker.signals.test_name.connect(self.write_output)
        self.worker.signals.each_test_case_output.connect(
            self.each_test_case_output)
        self.worker.signals.pie_chart_slot.connect(self.pie_chart_slot)

    @QtCore.pyqtSlot(str)
    def update_status(self, status):
        try:
            self.text_edit.appendPlainText(status)
            self.output = self.output + status
        except Exception as _ex_:
            LOG.exception(_ex_)

    @QtCore.pyqtSlot(str)
    def each_test_case_output(self, data):
        self.each_test_case_output_slot = data

    @QtCore.pyqtSlot(str, int)
    def write_output(self, test_name, test_index):
        try:
            LOG.debug('Writing to the file path = {0} and test name = {1}'
                      .format(self.path, test_name))
            OutputWrite.write_to_file(self.each_test_case_output_slot,
                                      test_name,
                                      self.path)

            # Parsing Each Test Case output
            result = self.parser.get_count(self.each_test_case_output_slot)
            if result[0]:
                global_constants.TEST_PASSED_COUNT += 1
                item = QtWidgets.QTableWidgetItem()
                item.setText("Passed")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.gui_utils.table_widget.setItem(test_index, 2, item)
            else:
                global_constants.TEST_FAILED_COUNT += 1
                global_constants.TEST_FAILED_LIST.append(test_index)
                item = QtWidgets.QTableWidgetItem()
                item.setText("Failed")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.gui_utils.table_widget.setItem(test_index, 2, item)
            self.gui_utils.passed_lcd.setText(str(
                global_constants.TEST_PASSED_COUNT))
            self.gui_utils.failed_lcd.setText(str(
                global_constants.TEST_FAILED_COUNT))

        except AttributeError as _ex_:
            LOG.exception('Got Exception {0}'.format(_ex_))

    @QtCore.pyqtSlot()
    def get_output(self):
        # OutputWrite.write_to_output(self.output)

        # self.gui_utils.pie_chart = PieChart(self.gui_utils.pie_widget)

        # self.gui_utils.pie_chart.flush_events()
        # self.gui_utils.pie_chart.setup_ui()
        result = self.parser.get_count(self.output)

        # self.gui_utils.progressBar_completion.setProperty("value", 100)
        print('This control is in this slot')
        # self.gui_utils.execution_status_lable.setText('Stop')
        self.gui_utils.clear_test_cases_button.setEnabled(True)
        # self.gui_utils.start_execution_buttion.setEnabled(True)

    @QtCore.pyqtSlot(int)
    def progress_bar_slot(self, value):
        self.gui_utils.progressBar_completion.setProperty(value)

    @QtCore.pyqtSlot()
    def pie_chart_slot(self):
        LOG.debug('Updating the PieChart')
        self.gui_utils.pie_chart = PieChart(self.gui_utils.tab_3)

    @QtCore.pyqtSlot()
    def end_button_func(self):
        self.event_stop.set()

