import sys

from PySide2.QtCore import QMimeData, QSize
from PySide2.QtGui import QIcon, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem

#Constants
from frankenscan.controller.statusSingleton import statusManager
from frankenscan.view.Widgets.modulesTabWidget import modulesTabWidget

WINDOWWIDTH = 1600
WINDOWHEIGHT = 800

# This is the main window
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        container = QWidget()

        #Create the tabs for modules
        tabs = modulesTabWidget()

        layout = QVBoxLayout(container)
        layout.addWidget(tabs)

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

