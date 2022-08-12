from frankenscan.controller.singleton import Singleton


class dataManager(Singleton):

    #Returns modules for a given Category. Returns empty list if no matches
    def getModulesForCategory(self, category):

        relevantModules = []

        for module in self.modules:

            if module["Category"] == category:
                relevantModules.append(module)
        return relevantModules

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

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        self.moduleCategories = ["File", "View", "Machine Learning"]
        self.modules = [{"Name":"Open File(s)", "Icon":"abacus.png", "Category": "File"},
                   {"Name":"Split Training Data", "Icon":"abacus.png", "Category": "Machine Learning"}
                   ]

        #Alphabetically sort the modules
        self.modules = sorted(self.modules, key= lambda dictionary: dictionary["Name"])

        #Validate the module data
        self.validateModuleData(self.modules, self.moduleCategories)

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass