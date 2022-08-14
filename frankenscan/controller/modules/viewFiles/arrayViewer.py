import pyvista as pv
import numpy as np
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from pyvistaqt import BackgroundPlotter

class ArrayViewer(QMainWindow):

    def closeEvent(self, event):
        for plot in self.plot:
            plot.close()
        event.accept()

    def clickPrev(self):
        if (self.index-1)>=0:
            self.index-=1
            self.stack.setCurrentIndex(self.index)

    def clickNext(self):
        if (self.index+1)<self.max:
            self.index+=1
            self.stack.setCurrentIndex(self.index)

    def __init__(self, node, dataList):

        super().__init__()

        self.dataList = dataList
        self.index = 0
        self.max = len(self.dataList)

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

        #Set the window size
        self.setGeometry(100, 100, 800, 600)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        i = 0

        self.plot = [0] * len(dataList)

        for data in dataList:

            self.plot[i] = BackgroundPlotter(show=False)

            width = data.shape[0]
            height = data.shape[2]
            length = data.shape[1]

            grid = pv.UniformGrid()

            grid.dimensions = np.array(data.shape) + 1

            grid.cell_data["values"] = data.flatten(order="F")

            slices = grid.slice_orthogonal(x = width/2, y = length/2, z = height/2)

            actor = self.plot[i].add_mesh(slices)

            self.stack.addWidget(self.plot[i])

            i+=1

        self.setCentralWidget(container)

        self.setWindowTitle("Array viewer")


        self.show()

