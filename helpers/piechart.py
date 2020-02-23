from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas
from matplotlib.figure import Figure
import numpy as np
from helpers import global_constants
import logging

LOG = logging.getLogger(__name__)


class PieChart(object):
    def __init__(self, instance):

        self.instance = instance
        self.result = ''
        LOG.info('in piechart class')
        self.setup_ui()

    def setup_ui(self):
        LOG.info('In setup_ui method')
        test_passed = global_constants.TEST_PASSED_COUNT
        test_failed = global_constants.TEST_FAILED_COUNT
        test_inprogress = global_constants.TEST_IN_PROGRESS_COUNT
        self.canvas = Canvas(self.instance, width=5, height=3, result=(
            test_passed, test_failed, test_inprogress))
        self.canvas.move(0, 0)
        self.canvas.draw()

    def flush_events(self):
        self.canvas.flush_events()


class Canvas(FingureCanvas):
    def __init__(self, parent=None, width=6, height=4, dpi=100, result=()):

        fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        LOG.debug('Created the fig instance = {0}'.format(fig))
        FingureCanvas.__init__(self, fig)

        self.setParent(parent)
        self.passed = result[0]
        self.failed = result[1]
        self.in_progress = abs(result[2])
        
        self.plot()

    def plot(self):
        print(self.passed, self.failed)
        LOG.debug('Test Passed = {0} and Test Failed = {1} Test In progress ='
                  ' {2}'.format(self.passed, self.failed, self.in_progress))
        x = np.array([self.passed, self.failed])

        labels = ['Test Passed', 'Test Failed']
        ax = self.figure.add_subplot(111)
        colors = ['g', 'r', 'b']

        ax.pie(x, autopct="%.2f%%", colors=colors, labels=labels,
               textprops=dict(color="b"), center=(0, 0))
        # ax.subplots_adjust(left=0.0, bottom=0.1, right=0.45)
        wedges = 'Test Passed', 'Test Failed'
        ax.legend(wedges,
                  title='Contents',
                  loc="lower right",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        ax.set_title(global_constants.TEST_EXECUTION_NAME)
        # ax.clear()
        # ax.draw()
        # ax.pie.show()
        LOG.debug('Plotted the piechart')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()