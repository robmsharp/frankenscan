
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
        readImage = plt.imread(image)
        self.axes.imshow(readImage)
        super(MplCanvas, self).__init__(fig)

class ImageViewer(QMainWindow):

    def clickPrev(self):
        if (self.index-1)>=0:
            self.index-=1
            self.stack.setCurrentIndex(self.index)

    def clickNext(self):
        if (self.index+1)<self.max:
            self.index+=1
            self.stack.setCurrentIndex(self.index)

    def __init__(self, node, data):

        super().__init__()

        print(data)

        self.data = data
        self.index = 0
        self.max = len(self.data)

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

        i = 0

        self.plot = [0] * len(data)

        for data in data:

            #Add the console
            self.plot[i] = MplCanvas(self, width=5, height=4, dpi=100, image = self.data[i])

            self.stack.addWidget(self.plot[i])

            i+=1

        self.setGeometry(100, 100, 800, 600)

        self.setWindowTitle("Image viewer")

        self.setCentralWidget(container)

        self.show()