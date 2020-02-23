from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
from helpers import global_constants


class PieChart(QWidget):

    def __init__(self, instance):
        super().__init__(instance)
        self.widget = QWidget(instance)
        self.m_donuts = []
        self.setGeometry(QRect(500, 330, 500, 300))
        self.chartView = QChartView()
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chart = self.chartView.chart()
        self.chart.legend().setVisible(True)
        self.chart.setTitle(global_constants.TEST_EXECUTION_NAME)
        # self.chart.setAnimationOptions(QChart.AllAnimations)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        donut = QPieSeries()
        donut.setPieSize(6)
        values = [global_constants.TEST_PASSED_COUNT,
                  global_constants.TEST_FAILED_COUNT,
                  global_constants.TEST_IN_PROGRESS_COUNT]
        names = ['Test Passed', 'Test Failed', 'Test In Progress']
        sliceCount = 3
        colors = [QColor(0, 255, 0), QColor(255, 0, 0), QColor(0, 0, 255)]
        for j in range(sliceCount):
            value = values[j]
            slice_ = QPieSlice(str(names[j]), value)
            slice_.setLabelVisible(False)
            slice_.setColor(colors[j])
            slice_.setLabelPosition(QPieSlice.LabelInsideTangential)
            donut.append(slice_)

        self.m_donuts.append(donut)
        self.chartView.chart().addSeries(donut)
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.chartView, 1, 1)
        self.chartView.show()


if __name__ == '__main__':

    a = QApplication([])
    w = PieChart()
    w.show()
    a.exec_()
