#TODO: add support for multiple sessions

from frankenscan.controller.singleton import Singleton


class sessionManager(Singleton):

    def run(self):
        print("run")
        for node in self.script.flow.nodes:
            node.update()

    def reset(self):
        print("reset")

    def pause(self):
        print("pause")

    def registerSession(self, session, script):
        self.session = session
        self.script = script

    def init(self):
        ##print("This is only executed when calling the singleton first time")
        ##print("calling init")
        pass

    def __init__(self):
        ##print("This is executed both first and second time")
        ##print("calling __init__")
        pass