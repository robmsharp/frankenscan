import sys

import ryvencore_qt as rc


from PySide2.QtCore import QMimeData, QSize
from PySide2.QtGui import QIcon, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem

#Constants
from frankenscan.controller.MyStream import MyStream
from frankenscan.controller.settingsSingleton import settingsManager
from frankenscan.controller.statusSingleton import statusManager
from frankenscan.view.Widgets.consoleTabWidget import consoleTabWidget
from frankenscan.view.Widgets.controlsTabWidget import controlsTabWidget
from frankenscan.view.Widgets.modulesTabWidget import modulesTabWidget

# This is the main window
class MainWindow(QMainWindow):

    def startSession(self):

        self.session = rc.Session()

        self.session.design.set_flow_theme(name='pure light')
        self.session.design.set_performance_mode('pretty')

        # registering the nodes
        """self.session.register_nodes(
            self.getClassList(self.nodeList)
        )"""

        self.script = self.session.create_script(title='main')

        self.session.flow_views[self.script]._stylus_modes_widget.hide()

        self.view = self.session.flow_views[self.script]

        self.view.installEventFilter(self)
        self.view.viewport().installEventFilter(self)

    def __init__(self):

        super().__init__()

        container = QWidget()

        layout = QVBoxLayout(container)

        #Get the session
        self.startSession()

        myTabs = QTabWidget()

        #Create the tabs for modules
        moduleTabs = modulesTabWidget()

        #Create the console
        console = consoleTabWidget()
        #Connect the console to a stream if setting is true
        if settingsManager().getConsoleSetting():
            myStream = MyStream()
            myStream.message.connect(console.addMessage)
            sys.stdout = myStream

        #Create the controller
        controlTabs = controlsTabWidget()

        myTabs.addTab(console, "console")
        myTabs.addTab(controlTabs, "controls")
        myTabs.addTab(moduleTabs, "moduleTabs")

        #Add the ryvencore window
        layout.addWidget(self.view)

        layout.addWidget(myTabs)

        self.setCentralWidget(container)
        self.resize(settingsManager().getMainWindowSize())

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

