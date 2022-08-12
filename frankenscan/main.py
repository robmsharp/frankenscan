import sys

from PySide2.QtCore import QMimeData, QSize
from PySide2.QtGui import QIcon, QFontMetrics
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem

#Constants
from frankenscan.controller.statusSingleton import statusManager

WINDOWWIDTH = 1600
WINDOWHEIGHT = 800

ICONLISTWIDTH = 1000
SPACING = 10

ITEMWIDTH = 150
ITEMHEIGHT = 70

#Custom widget that enables dropped nodes to be recognised
class myListWidget (QListWidget):

    def mimeData(self, items):
        data = QMimeData()
        data.setText(items[0].text())
        return data

# This is the main window
class MainWindow(QMainWindow):

    #Returns modules for a given Category. Returns empty list if no matches
    def getModulesForCategory(self, category, modules):

        relevantModules = []

        for module in modules:

            if module["Category"] == category:
                relevantModules.append(module)
        return relevantModules

    #Returns tabs for moduleCategories
    def getModuleTabs(self, modules, moduleCategories):
        tabs = QTabWidget()

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
            relevantModules = self.getModulesForCategory(category, modules)

            print(relevantModules)

            for module in relevantModules:
                moduleWidgets[moduleIndex] = QListWidgetItem()
                moduleWidgets[moduleIndex].setText(module["Name"])
                moduleWidgets[moduleIndex].setIcon(QIcon("/Users/robertsharp/Desktop/2022/projects/frankenscan/icons/"+module["Icon"]))

                #Get the length of the name
                fm = QFontMetrics(moduleWidgets[moduleIndex].font())
                width = fm.boundingRect(module["Name"]).width()

                #1.5 seems to work not sure why
                moduleWidgets[moduleIndex].setSizeHint(QSize(width*1.5, ITEMHEIGHT))
                iconListWidgets[i].insertItem(-1, moduleWidgets[moduleIndex])

                moduleIndex+=1

        return tabs


    #Validate the module data to ensure a category exists for every module
    #category. Also, ensure each module has a name, icon, and category
    def validateModuleData(self, modules, moduleCategories):

        for module in modules:
            assert(module["Name"]!= None)
            assert(module["Icon"]!= None)
            assert(module["Category"]!= None)
            assert(module["Category"] in moduleCategories)

    #Get the module data. Later, this should be changed to import from JSON
    def getModuleData(self):

        moduleCategories = ["File", "View", "Machine Learning"]
        modules = [{"Name":"Open File(s)", "Icon":"abacus.png", "Category": "File"},
                   {"Name":"Split Training Data", "Icon":"abacus.png", "Category": "Machine Learning"}
                   ]

        #Alphabetically sort the modules
        modules = sorted(modules, key= lambda dictionary: dictionary["Name"])

        return modules, moduleCategories

    def __init__(self):

        super().__init__()

        container = QWidget()

        #Get the module data
        modules, moduleCategories = self.getModuleData()

        #Validate the module data
        self.validateModuleData(modules, moduleCategories)

        #Create the tabs for modules
        tabs = self.getModuleTabs(modules, moduleCategories)

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

