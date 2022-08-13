import sys

import ryvencore_qt as rc
from PySide2 import QtCore

from PySide2.QtCore import QMimeData, QSize, QPointF
from PySide2.QtGui import QIcon, QFontMetrics, QFontDatabase
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem

from frankenscan.controller.MyStream import MyStream
from frankenscan.controller.sessionSingleton import sessionManager
from frankenscan.controller.settingsSingleton import settingsManager
from frankenscan.controller.statusSingleton import statusManager
from frankenscan.model.dataSingleton import dataManager
from frankenscan.view.Widgets.consoleTabWidget import consoleTabWidget
from frankenscan.view.Widgets.controlsTabWidget import controlsTabWidget
from frankenscan.view.Widgets.modulesTabWidget import modulesTabWidget

#Import the node classes
from frankenscan.controller.modules.modules import *

CLASSLOCATION = "frankenscan.controller.modules.modules."

# This is the main window
class MainWindow(QMainWindow):

    #Source: https://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname
    def getClass( self, kls ):

        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    def getClassList(self, list):
        classList = []
        for item in list:
            classList.append(self.getClass(CLASSLOCATION+item))
        return classList

    #Creates node when you drag module onto the view
    def eventFilter(self, object, event):

        if (object is self.view.viewport()):

            if (event.type() == QtCore.QEvent.Drop):

                mappedPos = self.view.mapToScene(event.pos())
                x = mappedPos.x()
                y = mappedPos.y()
                self.view._node_place_pos = QPointF(x,y)
                print(event.mimeData().text()+" module added to session.")
                string = CLASSLOCATION+event.mimeData().text()
                self.view.flow.create_node(self.getClass(string))

        return False

    def startSession(self):

        self.session = rc.Session()

        self.session.design.set_flow_theme(name='pure light')
        #self.session.design.set_performance_mode('pretty')

        # registering the modules as nodes
        self.session.register_nodes(
            self.getClassList(dataManager().getClasses())
        )

        self.script = self.session.create_script(title='main')

        self.session.flow_views[self.script]._stylus_modes_widget.hide()

        self.view = self.session.flow_views[self.script]

        self.view.installEventFilter(self)
        self.view.viewport().installEventFilter(self)

        sessionManager().registerSession(self.session, self.script)

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

