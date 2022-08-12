from PySide2.QtCore import QSize
from PySide2.QtGui import QFontMetrics, QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QListWidget, \
    QListWidgetItem, QPushButton, QHBoxLayout

from frankenscan.controller.resourceSingleton import resourceManager
from frankenscan.model.dataSingleton import dataManager
from frankenscan.view.Widgets.myListWidget import myListWidget

#Constants
ICONLISTWIDTH = 1000
SPACING = 10

ITEMWIDTH = 150
ITEMHEIGHT = 70

class controlsTabWidget(QWidget):

    def myRun(self):
        print("Running!")

    def myReset(self):
        print("Reset!")

    def myPause(self):
        print("Paused!")

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        #Get the control data
        controls, controllerCategories = dataManager().getControlData()

        layout= QVBoxLayout(self)

        tabs = QTabWidget()

        layout.addWidget(tabs)

        #Create empty arrays of appropriate length
        layouts = [0] * len(controllerCategories)
        layoutContainers = [0] * len(controllerCategories)
        controlButtons = [0] * len(controls)

        #For each tab, create a list and insert an button for each relevant control

        controlIndex=0

        for i in range(len(controllerCategories)):

            category = controllerCategories[i]

            #Create a layout

            layoutContainers[i] = QWidget()
            layouts[i] = QHBoxLayout(layoutContainers[i])

            tabs.addTab(layoutContainers[i], category)

            #Get the modules and add them to the tab
            relevantControls = dataManager().getControlsForCategory(category)

            for control in relevantControls:
                controlButtons[controlIndex] = QPushButton(control["Name"], self)

                controlButtons[controlIndex].setIcon(resourceManager().getIcon(control["Icon"]))

                controlButtons[controlIndex].setFixedSize(QSize(ITEMWIDTH, ITEMHEIGHT))

                exec("controlButtons[controlIndex].clicked.connect(self."+control["Program"]+")")

                layouts[i].addWidget(controlButtons[controlIndex])

                controlIndex+=1
