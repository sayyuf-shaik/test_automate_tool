#! /usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit
import os
import sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.actions import Actions
from helpers.monitor_size import MonitorSize
from helpers import logger

LOG = logging.getLogger(__name__)


class Ui_MainWindow(object):
    def __init__(self):
        # creating instance for actions
        LOG.info('Creating the instance of Actions')
        self.action_instance = Actions(self)

    def setupUi(self, MainWindow):
        # QRect(x, y, w, h)
        MainWindow.setObjectName("MainWindow")
        # getting the size of the monitor
        monitor_size = MonitorSize.get_size_of_monitor()
        LOG.debug('Got the Monitor Size {0} {1}'.format(monitor_size[0],
                                                        monitor_size[1]))
        # Resizing the application to the monitor size
        MainWindow.resize(monitor_size[1], monitor_size[0])
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Creating a horizontal Layout
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.group_box_main_window = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_main_window.setMinimumSize(QtCore.QSize(1020, 678))
        self.group_box_main_window.setMaximumSize(QtCore.QSize(monitor_size[1],
                                                               monitor_size[0]))
        self.group_box_main_window.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.group_box_main_window)
        self.widget.setGeometry(QtCore.QRect(0, 30, 600, 601))
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(0, 10, 261, 271))
        self.widget_2.setObjectName("widget_2")
        self.group_box_environment = QtWidgets.QGroupBox(self.widget_2)
        self.group_box_environment.setGeometry(QtCore.QRect(10, 30, 251, 171))
        self.group_box_environment.setObjectName("group_box_environment")
        self.label = QtWidgets.QLabel(self.group_box_environment)
        self.label.setGeometry(QtCore.QRect(10, 30, 61, 31))
        self.label.setObjectName("label")
        # QComboBox for selecting the Board
        self.combo_box_board = QtWidgets.QComboBox(self.group_box_environment)
        self.combo_box_board.setGeometry(QtCore.QRect(90, 30, 141, 31))
        self.combo_box_board.setObjectName("combo_box_board")
        self.combo_box_board.addItem("")
        self.combo_box_board.addItem("")
        self.combo_box_board.addItem("")
        # getting the selected item from the combo box
        self.combo_box_board.activated[str].connect(
            self.action_instance.on_board_changed)
        self.label_interface = QtWidgets.QLabel(self.group_box_environment)
        self.label_interface.setGeometry(QtCore.QRect(10, 80, 68, 31))
        self.label_interface.setObjectName("label_interface")
        # QComboBox for selecting the Interface
        self.combo_box_interface = QtWidgets.QComboBox(
            self.group_box_environment)
        self.combo_box_interface.setGeometry(QtCore.QRect(90, 80, 141, 31))
        self.combo_box_interface.setObjectName("combo_box_interface")
        self.combo_box_interface.addItem("")
        self.combo_box_interface.addItem("")
        self.combo_box_interface.addItem("")
        # when the index is changed respective method is called
        self.combo_box_interface.activated[str].connect(
            self.action_instance.on_interface_changed)
        self.label_device = QtWidgets.QLabel(self.group_box_environment)
        self.label_device.setGeometry(QtCore.QRect(10, 130, 68, 31))
        self.label_device.setObjectName("label_device")
        # QComboBox for selecting the Device
        self.combo_box_device = QtWidgets.QComboBox(self.group_box_environment)
        self.combo_box_device.setGeometry(QtCore.QRect(90, 130, 141, 31))
        self.combo_box_device.setObjectName("combo_box_device")
        self.combo_box_device.addItem("")
        self.combo_box_device.addItem("")
        self.combo_box_device.addItem("")
        self.combo_box_device.activated[str].connect(
            self.action_instance.on_device_changed)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(9, 289, 251, 301))
        self.widget_3.setObjectName("widget_3")
        self.group_box_configurations = QtWidgets.QGroupBox(self.widget_3)
        self.group_box_configurations.setGeometry(QtCore.QRect(0, 20, 251, 281))
        self.group_box_configurations.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.group_box_configurations.setObjectName("group_box_configurations")
        # label for configurations
        self.label_param_one = QtWidgets.QLabel(self.group_box_configurations)
        self.label_param_one.setGeometry(QtCore.QRect(10, 40, 71, 31))
        self.label_param_one.setObjectName("label_param_one")
        # getting input configuration param one from user
        self.text_param_one = QtWidgets.QLineEdit(self.group_box_configurations)
        self.text_param_one.setGeometry(QtCore.QRect(90, 40, 141, 31))
        self.text_param_one.setObjectName("text_param_one")
        self.label_param_two = QtWidgets.QLabel(self.group_box_configurations)
        self.label_param_two.setGeometry(QtCore.QRect(10, 90, 71, 31))
        self.label_param_two.setObjectName("label_param_two")

        # getting input configuration param two from user
        self.text_param_two = QtWidgets.QLineEdit(self.group_box_configurations)
        self.text_param_two.setGeometry(QtCore.QRect(90, 90, 141, 31))
        self.text_param_two.setObjectName("text_param_two")
        self.label_ip = QtWidgets.QLabel(self.group_box_configurations)
        self.label_ip.setGeometry(QtCore.QRect(10, 150, 68, 31))
        self.label_ip.setObjectName("label_ip")
        # getting input ip from user
        self.text_ip = QtWidgets.QLineEdit(self.group_box_configurations)
        self.text_ip.setGeometry(QtCore.QRect(90, 150, 141, 31))
        self.text_ip.setObjectName("text_ip")
        # self.get_configuration_details()
        self.param_one = self.text_param_one.text()
        self.param_two = self.text_param_two.text()
        self.ip = self.text_ip.text()
        # Push button to submit the configuration and environment
        self.submit_button = QtWidgets.QPushButton(self.group_box_configurations)
        self.submit_button.setGeometry(QtCore.QRect(0, 230, 99, 27))
        self.submit_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.submit_button.setObjectName("submit_button")
        # when the button is clicked then the on_submit_clicked is called
        self.submit_button.clicked.connect(
            self.action_instance.on_submit_clicked)
        # -----------------------------------------------
        # Push button to Load the previous Test Execution
        self.load_button = QtWidgets.QPushButton(
            self.group_box_configurations)
        self.load_button.setGeometry(QtCore.QRect(140, 230, 99, 27))
        self.load_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.load_button.setObjectName("load_button")
        # when the button is clicked then the on_load_clicked is called
        self.load_button.clicked.connect(
            self.action_instance.on_load_clicked)
        # ------------------------------------------------
        self.horizontalLayoutWidget = QtWidgets.QWidget(
            self.group_box_main_window)
        # 861
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 900, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.
                                                        horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.app_title = QtWidgets.QLabel(self.horizontalLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        self.app_title.setPalette(palette)
        self.app_title.setAutoFillBackground(True)
        self.app_title.setObjectName("app_title")
        self.horizontalLayout_3.addWidget(self.app_title)
        self.test_count_label = QtWidgets.QTabWidget(self.group_box_main_window)
        self.test_count_label.setGeometry(QtCore.QRect(270, 30, 1000, 650))
        self.test_count_label.setTabsClosable(False)
        self.test_count_label.setMovable(False)
        self.test_count_label.setObjectName("test_count_label")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        # Check box for selecting all test cases
        self.select_all_check_box = QtWidgets.QCheckBox(self.tab)
        self.select_all_check_box.setText('Select All')
        # self.select_all_check_box.clicked.connect(
         #   self.action_instance.select_all)
        self.select_all_check_box.clicked.connect(
            self.action_instance.select_all)

        # self.select_all_check_box.setGeometry(QtCore.QRect(0, 51, 50, 50))
        # table widget for population test cases
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        # self.tableWidget.setGeometry(QtCore.QRect(0, 11, 571, 421))
        self.tableWidget.setGeometry(QtCore.QRect(0, 61, 990, 421))
        self.tableWidget.setObjectName("tableWidget")
        # removing the vertical header
        self.table_view = QtWidgets.QHeaderView(QtCore.Qt.Vertical)
        self.table_view.hide()
        self.tableWidget.setVerticalHeader(self.table_view)
        # setting the count of the table widget to 2
        self.tableWidget.setColumnCount(2)
        # Creating the Horizontal Header View With two columns
        item = QtWidgets.QTableWidgetItem()
        item.setText('Test Id')
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeaderItem(0).\
            setTextAlignment(QtCore.Qt.AlignLeft)
        item = QtWidgets.QTableWidgetItem()

        item.setText('Description')
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeaderItem(1). \
            setTextAlignment(QtCore.Qt.AlignLeft)
        # disabling the grid
        self.tableWidget.setShowGrid(False)
        # Setting the width of the column
        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.setColumnWidth(1, 688)
        # Text Execution Name label
        self.text_execution_name_label = QtWidgets.QLabel(self.tab)
        self.text_execution_name_label.setText('Text Execution name:')
        self.text_execution_name_label.setGeometry(QtCore.QRect(30, 500, 200, 41))
        # Text Execution QTextEdit
        self.test_execution_name = QtWidgets.QLineEdit(self.tab)
        self.test_execution_name.setGeometry(QtCore.QRect(180, 500, 200, 41))
        # button create
        self.create_test_cases_button = QtWidgets.QPushButton(self.tab)
        self.create_test_cases_button.setGeometry(QtCore.QRect(50, 550, 89, 41))
        self.create_test_cases_button.setObjectName("create_test_cases_button")

        self.create_test_cases_button.clicked.connect(self.action_instance.
                                                      get_selected_items)
        # button clear
        self.clear_test_cases_button = QtWidgets.QPushButton(self.tab)
        self.clear_test_cases_button.setGeometry(QtCore.QRect(150, 550, 89, 41))
        self.clear_test_cases_button.setObjectName("clear_test_cases_button")
        self.clear_test_cases_button.clicked.connect(self.action_instance.
                                                     clear_checked_items)
        self.test_count_label.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.start_execution_buttion = QtWidgets.QPushButton(self.tab_2)
        self.start_execution_buttion.setGeometry(QtCore.QRect(110, 150, 99, 27))
        self.start_execution_buttion.setObjectName("start_execution_buttion")
        self.start_execution_buttion.clicked.connect(self.action_instance.
                                                     on_start_button_clicked)
        self.stop_execution_button = QtWidgets.QPushButton(self.tab_2)
        self.stop_execution_button.setGeometry(QtCore.QRect(360, 150, 99, 27))
        self.stop_execution_button.setObjectName("stop_execution_button")
        self.stop_execution_button.clicked.connect(
            self.action_instance.on_stop_button_clicked)
        self.stop_execution_button.setEnabled(False)
        self.label_terminal = QtWidgets.QLabel(self.tab_2)
        self.label_terminal.setGeometry(QtCore.QRect(30, 180, 68, 17))
        self.label_terminal.setObjectName("label_terminal")
        # terminal output area
        self.terminal_scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.terminal_scrollArea.setGeometry(QtCore.QRect(30, 200, 900, 400))
        self.terminal_scrollArea.setWidgetResizable(True)
        self.terminal_scrollArea.setObjectName("terminal_scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 589, 359))
        self.scrollAreaWidgetContents_3.setObjectName(
            "scrollAreaWidgetContents_3")

        self.terminal_scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.label_test_execution_name = QtWidgets.QLabel(self.tab_2)
        self.label_test_execution_name.setGeometry(QtCore.QRect(10, 20, 151, 17))
        self.label_test_execution_name.setObjectName("label_test_execution_name")
        self.label_name_of_the_test = QtWidgets.QLabel(self.tab_2)
        self.label_name_of_the_test.setGeometry(QtCore.QRect(180, 20, 141, 17))
        self.label_name_of_the_test.setObjectName("label_name_of_the_test")
        self.label_test_count = QtWidgets.QLabel(self.tab_2)
        self.label_test_count.setGeometry(QtCore.QRect(10, 50, 151, 17))
        self.label_test_count.setObjectName("label_test_count")
        self.label_device_count = QtWidgets.QLabel(self.tab_2)
        self.label_device_count.setGeometry(QtCore.QRect(10, 80, 151, 17))
        self.label_device_count.setObjectName("label_device_count")
        self.label_status = QtWidgets.QLabel(self.tab_2)
        self.label_status.setGeometry(QtCore.QRect(10, 110, 151, 20))
        self.label_status.setObjectName("label_status")
        self.execution_status_lable = QtWidgets.QLabel(self.tab_2)
        self.execution_status_lable.setGeometry(QtCore.QRect(180, 110, 131, 17))
        self.execution_status_lable.setObjectName("execution_status_lable")
        self.label_interface1 = QtWidgets.QLabel(self.tab_2)
        self.label_interface1.setGeometry(QtCore.QRect(180, 50, 68, 17))
        self.label_interface1.setObjectName("label_interface1")

        self.device_count_lable = QtWidgets.QLabel(self.tab_2)
        self.device_count_lable.setGeometry(QtCore.QRect(180, 80, 68, 17))
        self.device_count_lable.setObjectName("device_count_lable")
        self.test_count_label.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        # --------------------------------------------------------
        # QTableWidget for displaying the selected test cases status
        self.table_widget = QtWidgets.QTableWidget(self.tab_3)
        self.table_widget.setGeometry(QtCore.QRect(10, 61, 970, 250))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(3)
        self.table_view = QtWidgets.QHeaderView(QtCore.Qt.Vertical)
        self.table_view.hide()
        # Disabling the working header
        self.table_widget.setVerticalHeader(self.table_view)
        # self.table_widget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        item.setText('Test Id')
        self.table_widget.setHorizontalHeaderItem(0, item)
        # Text Alignment to Left Align
        self.table_widget.horizontalHeaderItem(0). \
            setTextAlignment(QtCore.Qt.AlignLeft)
        item = QtWidgets.QTableWidgetItem()
        item.setText('Description')
        self.table_widget.setHorizontalHeaderItem(1, item)
        # Text Alignment to Left Align
        self.table_widget.horizontalHeaderItem(1). \
            setTextAlignment(QtCore.Qt.AlignLeft)
        item = QtWidgets.QTableWidgetItem()
        item.setText('Status')
        self.table_widget.setHorizontalHeaderItem(2, item)
        # Text Alignment to Left Align
        self.table_widget.horizontalHeaderItem(2). \
            setTextAlignment(QtCore.Qt.AlignLeft)

        self.table_widget.setShowGrid(False)
        # Setting the width of the column
        self.table_widget.setColumnWidth(0, 200)
        self.table_widget.setColumnWidth(1, 565)
        self.table_widget.setColumnWidth(2, 203)

        # --------------------------------------------------------
        # Group Box for Execution Summary
        self.group_box_summary = QtWidgets.QGroupBox(self.tab_3)
        self.group_box_summary.setGeometry(QtCore.QRect(10, 320, 480, 311))
        self.group_box_summary.setObjectName("group_box_summary")
        self.label_test_execution_name_tab_3 = QtWidgets.QLabel(
            self.group_box_summary)
        self.label_test_execution_name_tab_3.setGeometry(QtCore.QRect(10, 40, 111, 17))
        self.label_test_execution_name_tab_3.setObjectName(
            "label_test_execution_name_tab_3")
        self.summary_execution_name = QtWidgets.QTextBrowser(
            self.group_box_summary)
        self.summary_execution_name.setGeometry(QtCore.QRect(130, 30, 300, 31))
        self.summary_execution_name.setObjectName("summary_execution_name")
        self.label_passed = QtWidgets.QLabel(self.group_box_summary)
        self.label_passed.setGeometry(QtCore.QRect(10, 90, 68, 17))
        self.label_passed.setObjectName("label_passed")
        # lcd to display failed test cases
        self.passed_lcd = QtWidgets.QLabel(self.group_box_summary)
        self.passed_lcd.setGeometry(QtCore.QRect(130, 85, 100, 17))
        self.passed_lcd.setObjectName("passed_lcd")

        self.label_test_failed_count = QtWidgets.QLabel(self.group_box_summary)
        self.label_test_failed_count.setGeometry(QtCore.QRect(10, 140, 68, 17))
        self.label_test_failed_count.setObjectName("label_test_failed_count")
        # lcd to display failed test cases
        self.failed_lcd = QtWidgets.QLabel(self.group_box_summary)
        self.failed_lcd.setGeometry(QtCore.QRect(130, 145, 100, 17))
        self.failed_lcd.setObjectName("failed_lcd")
        self.pallete_lcd = self.failed_lcd.palette()
        self.pallete_lcd.setColor(self.pallete_lcd.Light,
                                  QtGui.QColor(255, 0, 0))
        self.failed_lcd.setPalette(self.pallete_lcd)
        self.label_completed = QtWidgets.QLabel(self.group_box_summary)
        self.label_completed.setGeometry(QtCore.QRect(10, 210, 101, 17))
        self.label_completed.setObjectName("label_completed")
        # Progress Bar
        self.progressBar_completion = QtWidgets.QProgressBar(
            self.group_box_summary)
        self.progressBar_completion.setGeometry(QtCore.QRect(130, 210, 300, 23))
        self.progressBar_completion.setProperty("value", 0)
        self.progressBar_completion.setObjectName("progressBar_completion")
        self.test_count_label.addTab(self.tab_3, "")
        self.horizontalLayout_2.addWidget(self.group_box_main_window)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRaspberrypie = QtWidgets.QAction(MainWindow)
        self.actionRaspberrypie.setCheckable(True)
        self.actionRaspberrypie.setObjectName("actionRaspberrypie")
        # instance of text edit
        self.text_edit = QPlainTextEdit()
        # Creating a widget for plotting the piechart
        self.pie_widget = QtWidgets.QWidget(self.tab_3)
        # Pie Chart label to indicate the Piechart widget
        self.label_pie_chart = QtWidgets.QLabel(self.tab_3)
        # self.pie_widget.setGeometry(QtCore.QRect(10, 350, 900, 700))
        self.pie_widget.setGeometry(QtCore.QRect(500, 350, 900, 700))
        self.label_pie_chart.setGeometry(QtCore.QRect(500, 320, 101, 17))
        self.label_pie_chart.setText('Pie Chart')

        self.retranslateUi(MainWindow)
        self.test_count_label.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.text_param_two, self.text_ip)
        MainWindow.setTabOrder(self.text_ip, self.text_param_one)
        MainWindow.setTabOrder(self.text_param_one, self.test_count_label)
        MainWindow.setTabOrder(self.test_count_label, self.combo_box_board)
        MainWindow.setTabOrder(self.combo_box_board, self.combo_box_interface)
        MainWindow.setTabOrder(self.combo_box_interface, self.combo_box_device)
        MainWindow.setTabOrder(self.combo_box_device, self.submit_button)
        # disabling the two tabs
        self.tab_2.setEnabled(False)
        self.tab_3.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Device Driver Testing Tool"))
        self.group_box_environment.setTitle(
            _translate("MainWindow", "Environment"))
        self.label.setText(_translate("MainWindow", "Board"))
        self.combo_box_board.setItemText(0, _translate("MainWindow", "RPI3"))
        self.combo_box_board.setItemText(1, _translate(
            "MainWindow", "IntelNuc"))
        self.combo_box_board.setItemText(2, _translate(
            "MainWindow", "DellWyse"))
        self.label_interface.setText(_translate("MainWindow", "Interface"))
        self.combo_box_interface.setItemText(
            0, _translate("MainWindow", "bitbSPI"))
        self.combo_box_interface.setItemText(1, _translate("MainWindow", "I2C"))
        self.combo_box_interface.setItemText(2, _translate("MainWindow", "SPI"))
        self.label_device.setText(_translate("MainWindow", "Device"))
        self.combo_box_device.setItemText(0, _translate("MainWindow", "RTC"))
        self.combo_box_device.setItemText(1, _translate("MainWindow", "ADC"))
        self.combo_box_device.setItemText(2, _translate("MainWindow", "X86"))
        self.group_box_configurations.setTitle(
            _translate("MainWindow", "Configurations"))
        self.label_param_one.setText(_translate("MainWindow", "ParamOne"))
        self.label_param_two.setText(_translate("MainWindow", "ParamTwo"))
        self.label_ip.setText(_translate("MainWindow", "IP"))
        self.submit_button.setText(_translate("MainWindow", "Submit"))
        self.load_button.setText(_translate("MainWindow", "Load"))
        self.app_title.setText(_translate("MainWindow", ""
                                        "  LTP Test Execution Framework"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.create_test_cases_button.setText(_translate("MainWindow", "Create"))
        self.clear_test_cases_button.setText(_translate("MainWindow", "Clear"))
        self.test_count_label.setTabText(
            self.test_count_label.indexOf(self.tab), _translate(
                "MainWindow", "Create Test Execution"))
        self.start_execution_buttion.setText(_translate("MainWindow", "Start"))
        self.stop_execution_button.setText(_translate("MainWindow", "Stop"))
        self.label_terminal.setText(_translate("MainWindow", "Terminal"))
        self.label_test_execution_name.setText(_translate(
            "MainWindow", "Test Execution name :"))
        self.label_name_of_the_test.setText(_translate(
            "MainWindow", " "))
        self.label_test_count.setText(_translate(
            "MainWindow", "Test Count                    :"))
        self.label_device_count.setText(_translate(
            "MainWindow", "Device Count               :"))
        self.label_status.setText(_translate(
            "MainWindow", "Status                             :"))
        self.execution_status_lable.setText(
            _translate("MainWindow", "Start/Stop"))
        # self.label_interface1.setText(_translate("MainWindow", "3"))
        self.device_count_lable.setText(_translate("MainWindow", "1"))
        self.test_count_label.setTabText(
            self.test_count_label.indexOf(self.tab_2), _translate(
                "MainWindow", "Start Execution"))
        self.group_box_summary.setTitle(_translate("MainWindow", "Summary"))
        self.label_test_execution_name_tab_3.setText(
            _translate("MainWindow", "Execution name"))
        self.summary_execution_name.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))
        self.label_passed.setText(_translate("MainWindow", "Passed:"))
        self.label_test_failed_count.setText(_translate("MainWindow", "Failed:"))
        self.label_completed.setText(_translate("MainWindow", "Completed"))
        self.test_count_label.setTabText(
            self.test_count_label.indexOf(self.tab_3), _translate(
                "MainWindow", "Execution Summary"))
        self.actionRaspberrypie.setText(_translate(
            "MainWindow", "raspberrypie"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    log_obj = logger.setup_logging('Script_logs ')
    sys.exit(app.exec_())

