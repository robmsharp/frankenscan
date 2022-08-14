from PySide2.QtGui import QFontMetrics, QTextCursor
from PySide2.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QTextEdit, QScrollBar


class HeaderViewer(QMainWindow):

    def clickPrev(self):
        if (self.index-1)>=0:
            self.index-=1
            self.updateConsole()


    def clickNext(self):
        if (self.index+1)<self.max:
            self.index+=1
            self.updateConsole()

    def updateConsole(self):

        self.console.clear()

        viewingData = self.data[self.index]

        #The window size gets updated to fit the largest line
        maxWidth = 0

        for line in viewingData:

            stringLabel = QLabel(line)
            fm = QFontMetrics(stringLabel.font())
            maxWidth = max(maxWidth, fm.width(stringLabel.text()))

            self.console.append(line)


        self.setGeometry(100, 100, maxWidth, 600)

        #Scroll to the top
        self.console.moveCursor(QTextCursor.Start)

    def __init__(self, node, data):

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

        #Add navigation to the top:
        self.navigationLayout = QHBoxLayout()
        self.next = QPushButton("Next")
        self.prev = QPushButton("Prev")
        self.navigationLayout = QHBoxLayout()
        self.navigationLayout.addWidget(self.prev)
        self.navigationLayout.addWidget(self.next)
        self.layout.addLayout(self.navigationLayout)

        self.prev.clicked.connect(self.clickPrev)
        self.next.clicked.connect(self.clickNext)

        #Add the console
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.layout.addWidget(self.console)
        self.setCentralWidget(container)

        self.updateConsole()

        self.setWindowTitle("Header viewer")

        self.show()