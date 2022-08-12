import sys

from PySide2.QtCore import QMimeData, QSize
from PySide2.QtGui import QIcon, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem

#Constants
from frankenscan.controller.MyStream import MyStream
from frankenscan.controller.statusSingleton import statusManager
from frankenscan.view.Widgets.consoleTabWidget import consoleTabWidget
from frankenscan.view.Widgets.modulesTabWidget import modulesTabWidget

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800

# This is the main window
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        container = QWidget()

        layout = QVBoxLayout(container)

        myTabs = QTabWidget()

        #Create the tabs for modules
        moduleTabs = modulesTabWidget()

        #Create the console
        console = consoleTabWidget()
        #Connect the console to a stream
        myStream = MyStream()
        myStream.message.connect(console.addMessage)
        sys.stdout = myStream

        #Create the controller

        myTabs.addTab(console, "console")
        myTabs.addTab(moduleTabs, "moduleTabs")

        layout.addWidget(myTabs)


        self.setCentralWidget(container)
        self.resize(WINDOWWIDTH, WINDOWHEIGHT)

        #Create a status Manager singleton and assign the status bar to it
        self.statusManager = statusManager()
        self.statusManager.setStatusBar(self.statusBar())
        self.statusManager.updateStatus("Frankenscan loaded")

# This launches the main window
if __name__ == '__main__':
    app = QApplication()

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

