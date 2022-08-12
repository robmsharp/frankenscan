from PySide2.QtCore import QSize
from PySide2.QtGui import QFontMetrics, QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QListWidget, \
    QListWidgetItem

from frankenscan.controller.resourceSingleton import resourceManager
from frankenscan.model.dataSingleton import dataManager
from frankenscan.view.Widgets.myListWidget import myListWidget

#Constants
ICONLISTWIDTH = 1000
SPACING = 10

ITEMWIDTH = 150
ITEMHEIGHT = 70

class modulesTabWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)


        #Get the module data
        modules, moduleCategories = dataManager().getModuleData()

        layout= QVBoxLayout(self)

        tabs = QTabWidget()

        layout.addWidget(tabs)

        #Create empty arrays of appropriate length
        iconListWidgets = [0] * len(moduleCategories)
        moduleWidgets = [0] * len(modules)

        #For each tab, create a list and insert an icon for each relevant module

        moduleIndex=0

        for i in range(len(moduleCategories)):

            category = moduleCategories[i]

            #Create a list widget
            iconListWidgets[i] = myListWidget()
            iconListWidgets[i].setMinimumWidth(ICONLISTWIDTH)
            iconListWidgets[i].setViewMode(QListWidget.IconMode)
            iconListWidgets[i].setAcceptDrops(False)
            iconListWidgets[i].setDragEnabled(True)
            iconListWidgets[i].setSpacing(SPACING)
            tabs.addTab(iconListWidgets[i], category)

            #Get the modules and add them to the tab
            relevantModules = dataManager().getModulesForCategory(category)

            print(relevantModules)

            for module in relevantModules:
                moduleWidgets[moduleIndex] = QListWidgetItem()
                moduleWidgets[moduleIndex].setText(module["Name"])
                moduleWidgets[moduleIndex].setIcon(resourceManager().getIcon(module["Icon"]))

                #Get the length of the name
                fm = QFontMetrics(moduleWidgets[moduleIndex].font())
                width = fm.boundingRect(module["Name"]).width()

                #1.5 seems to work not sure why
                moduleWidgets[moduleIndex].setSizeHint(QSize(width*1.5, ITEMHEIGHT))
                iconListWidgets[i].insertItem(-1, moduleWidgets[moduleIndex])

                moduleIndex+=1
