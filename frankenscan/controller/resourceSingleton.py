import os

from PySide2.QtGui import QIcon

from frankenscan.controller.singleton import Singleton

from sys import platform

ICONS = "/frankenscan/model/assets/icons/"
SETTINGS = "/frankenscan/model/settings/settings.json"

#For some reason the pc os.path.abspath is to the frankenscan/frankenscan whereas on mac it is to frankenscan
ICONSPC = "/model/assets/icons/"
SETTINGSPC = "/model/settings/settings.json"

class resourceManager(Singleton):

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        if platform == "win32":
            self.iconBasePath = (os.path.abspath(".").replace('\\','/') + ICONSPC).replace('/','\\')
        else:
            self.iconBasePath = os.path.abspath(".") + ICONS

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass

    #Returns a QIcon for a given name
    def getIcon(self, iconName):
        return QIcon(self.iconBasePath+iconName)

    #Returns the settings file path
    def getSettingsFilePath(self):
        if platform == "win32":
            return (os.path.abspath(".").replace('\\','/') + SETTINGSPC).replace('/','\\')
        else:
            return os.path.abspath(".") + SETTINGS

