from frankenscan.controller.settingsSingleton import settingsManager
from frankenscan.controller.singleton import Singleton


class dataManager(Singleton):

    #Returns modules for a given Category. Returns empty list if no matches
    def getModulesForCategory(self, category):

        relevantModules = []

        for module in self.modules:

            if module["Category"] == category:
                relevantModules.append(module)
        return relevantModules

    #Returns controls for a given Category. Returns empty list if no matches
    def getControlsForCategory(self, category):

        relevantControls = []

        for control in self.controls:

            if control["Category"] == category:
                relevantControls.append(control)
        return relevantControls

    #Validate the control data to ensure a category exists for every control
    #category. Also, ensure each control has a name, icon, and category
    def validateControllerData(self, controls, controllerCategories):

        for control in controls:
            assert(control["Name"]!= None)
            assert(control["Icon"]!= None)
            assert(control["Category"]!= None)
            assert(control["Program"]!= None)
            assert(control["Category"] in controllerCategories)

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

        return self.modules, self.moduleCategories

    #Get the control data
    def getControlData(self):

        return self.controls, self.controllerCategories

    #Return a list of classes
    def getClasses(self):
        classes = []
        for module in self.modules:
            classes.append(module["Name"])
        return classes

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")

        #Data for module
        self.moduleCategories = settingsManager().getModulesTabs()
        self.modules = settingsManager().getModules()

        #Alphabetically sort the modules
        self.modules = sorted(self.modules, key= lambda dictionary: dictionary["Name"])

        #Validate the module data
        self.validateModuleData(self.modules, self.moduleCategories)

        #Data for controller
        self.controllerCategories = settingsManager().getControlsTabs()
        self.controls = settingsManager().getControlsButtons()

        #Validate the controller data
        self.validateControllerData(self.controls, self.controllerCategories)


    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass