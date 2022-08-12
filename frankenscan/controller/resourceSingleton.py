import os

from PySide2.QtGui import QIcon

from frankenscan.controller.singleton import Singleton

ICONS = "/icons/"

class resourceManager(Singleton):

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        self.iconBasePath = os.path.abspath(".") + ICONS

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass

    #Returns a QIcon for a given name
    def getIcon(self, iconName):
        return QIcon(self.iconBasePath+iconName)
