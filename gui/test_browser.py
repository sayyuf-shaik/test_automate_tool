from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from helpers import global_constants


class FileBrowser(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        #self.init_ui()
        self.selected_list = ''

    def init_ui(self, tables):
        self.listWidget = QtWidgets.QListWidget(self)
        self.setWindowTitle('Test Execution')
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 500, 400))
        self.listWidget.setObjectName("listWidget")
        # self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.itemSelectionChanged.connect(self.on_change)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(520, 360, 89, 25))
        self.pushButton.setText("Select")
        self.show()
        self.populate(tables)
        self.pushButton.clicked.connect(self.on_select_clicked)


    def on_change(self):
        self.selected_list = [item.row() for item in self.listWidget.selectedIndexes()]
        print(self.selected_list)
        global_constants.TESTS = self.selected_list
        print(global_constants.TESTS)

    def populate(self, tables):
        for test_execution_name in tables:
            item = QtWidgets.QListWidgetItem()
            item.setText(test_execution_name)
            self.listWidget.addItem(item)

        return self.selected_list

    def on_select_clicked(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    f = FileBrowser()
    f.show()
    sys.exit(app.exec_())