from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QTextEdit, QListWidget, QVBoxLayout, \
    QLabel, QPushButton, QFileDialog, QTabWidget
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.settingsSingleton import settingsManager

class SelectIntWidget(MWB, QWidget):

    #Used to signal changes to node
    intSelectedSignal = Signal(object)

    def __init__(self, params):
        MWB.__init__(self, params)
        QWidget.__init__(self)

        container = QWidget(self)

        #Tabs so can view file names and file paths
        tabs = QTabWidget()

        layout = QVBoxLayout(container)

        self.intInput = QTextEdit()
        self.intInput.setMaximumHeight(50)

        #Button to select files
        button = QPushButton('Update value')
        button.clicked.connect(self.updateValue)

        layout.addWidget(self.intInput)
        layout.addWidget(button)

        self.widget = container
        self.widget.setMinimumSize(300,200)

    def updateValue(self):

        myInt = int(self.intInput.toPlainText())

        self.intSelectedSignal.emit(myInt)
