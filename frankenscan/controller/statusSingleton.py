from frankenscan.controller.singleton import Singleton


class statusManager(Singleton):

    def updateStatus(self, message):
        #print the message to console
        print(message)

        #Update the status bar
        self.statusBar.showMessage(message)

    def setStatusBar(self, statusBar):

        self.statusBar = statusBar

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        pass

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass