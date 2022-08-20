
from PySide2.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QStackedWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#Source: https://www.pythonguis.com/tutorials/plotting-matplotlib/
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, image=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #Reshape the numpy array
        reshapedImage = image.reshape((image.shape[1],image.shape[2],image.shape[0]))
        self.axes.imshow(reshapedImage)
        super(MplCanvas, self).__init__(fig)

class DataLoaderViewer(QMainWindow):

    def clickPrev(self):
        if (self.index-1)>=0:
            self.index-=1
            self.stack.setCurrentIndex(self.index)

    def clickNext(self):
        if (self.index+1)<self.max:
            self.index+=1
            self.stack.setCurrentIndex(self.index)

    def __init__(self, node, dataLoader):

        super().__init__()

        self.dataLoader = dataLoader
        self.index = 0
        self.max = len(self.dataLoader)

        self.node = node
        #Trick to avoid window closing
        node.var = self

        #Create the layout
        container = QWidget()
        self.layout = QVBoxLayout(container)

        #Add nivation to the top:
        self.navigationLayout = QHBoxLayout()
        self.next = QPushButton("Next")
        self.prev = QPushButton("Prev")
        self.navigationLayout = QHBoxLayout()
        self.navigationLayout.addWidget(self.prev)
        self.navigationLayout.addWidget(self.next)
        self.layout.addLayout(self.navigationLayout)

        self.prev.clicked.connect(self.clickPrev)
        self.next.clicked.connect(self.clickNext)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.plot = [0] * self.max
        self.labels = [0] * self.max
        self.widgets = [0] * self.max
        self.layouts = [0] * self.max

        for i in range(self.max):

            self.widgets[i] = QWidget()
            self.layouts[i] = QVBoxLayout(self.widgets[i])
            self.plot[i] = MplCanvas(self, width=5, height=4, dpi=100, image = self.dataLoader[i]['image'])
            if self.dataLoader[i]['label'] > 0:
                self.labels[i] = QLabel("Tumor")
            else:
                self.labels[i] = QLabel("Healthy")
            self.layouts[i].addWidget(self.labels[i])
            self.layouts[i].addWidget(self.plot[i])
            self.stack.addWidget(self.widgets[i])

        self.setGeometry(100, 100, 800, 600)

        self.setWindowTitle("Data viewer")

        self.setCentralWidget(container)

        self.show()