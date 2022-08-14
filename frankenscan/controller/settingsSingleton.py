import os
import json

from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon

from frankenscan.controller.resourceSingleton import resourceManager
from frankenscan.controller.singleton import Singleton

ICONS = "/icons/"

class settingsManager(Singleton):

    #Returns latest opened folder
    #TODO: implement this loading from settings file and updating on opening
    #new folder locations
    def getLatestFolder(self):
        #return "/Users/robertsharp/Desktop/2022/scanData/Task04_Hippocampus/imagesTr/"
        return os.path.abspath(".")

    #Returns a dictionary containing the settings data
    def readConfigFromFile(self):

        fp = resourceManager().getSettingsFilePath()

        try:
            with open(fp, "r") as f:
                return json.loads(f.read())

        #TODO: show an alert and close the program
        except Exception as e:
            print("An exception occurred importing settings: {}".format(e))

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        self.settings = self.readConfigFromFile()

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass

    #Returns window size settings
    def getMainWindowSize(self):
        width = self.settings["MainWindow"]["width"]
        height = self.settings["MainWindow"]["height"]
        return QSize(width, height)

    #Returns true if the console should capture print statements
    #Turn off to help with debugging errors
    def getConsoleSetting(self):
        return self.settings["Console"]["capturePrintStatements"]

    #Return the module icon constants
    def getModuleConstants(self):
        return self.settings["Modules"]["iconListWidth"], self.settings["Modules"]["spacing"], self.settings["Modules"]["itemWidth"], self.settings["Modules"]["itemHeight"]

    #Return the control button constants
    def getControlConstants(self):
        return self.settings["Controls"]["itemWidth"], self.settings["Controls"]["itemHeight"]