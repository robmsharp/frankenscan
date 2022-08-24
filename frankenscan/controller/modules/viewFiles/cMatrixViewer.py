from PySide2.QtGui import QFontMetrics, QTextCursor
from PySide2.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QTextEdit, QScrollBar

from PySide2.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QStackedWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import seaborn as sns

from sklearn.metrics import accuracy_score, confusion_matrix

#Source: https://www.pythonguis.com/tutorials/plotting-matplotlib/
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, y_true, predicted, parent=None, width=16, height=9, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        cm = confusion_matrix(y_true, predicted)
        ax= fig.add_subplot(111)
        sns.heatmap(cm, annot=True, fmt='g', ax=ax, annot_kws={"size": 20})

        # labels, title and ticks
        ax.set_xlabel('Predicted labels', fontsize=20)
        ax.set_ylabel('True labels', fontsize=20)
        ax.set_title('Confusion Matrix', fontsize=20)
        ax.xaxis.set_ticklabels(['Tumor','Healthy'], fontsize=20)
        ax.yaxis.set_ticklabels(['Tumor','Healthy'], fontsize=20)

        super(MplCanvas, self).__init__(fig)

class ConfusionMatrixViewer(QMainWindow):



    def __init__(self, node, y_true, predicted):

        super().__init__()

        self.data = data
        self.index = 0
        self.max = len(self.data)

        self.node = node
        #Trick to avoid window closing
        node.var = self

        #Create the layout
        container = QWidget()
        self.layout = QVBoxLayout(container)

        cm = MplCanvas(y_true, predicted)

        self.layout.addWidget(self.console)
        self.setCentralWidget(container)

        self.updateConsole()

        self.setWindowTitle("Confusion Matrix viewer")

        self.show()