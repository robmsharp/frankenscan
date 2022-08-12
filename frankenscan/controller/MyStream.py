#For putting print statements on the console
from PySide2 import QtCore
from PySide2.QtCore import Signal

class MyStream(QtCore.QObject):
    message = Signal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))