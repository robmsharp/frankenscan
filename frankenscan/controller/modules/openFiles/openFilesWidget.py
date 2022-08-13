from PySide2.QtWidgets import QWidget, QTextEdit
from ryvencore_qt import MWB
import ryvencore_qt as rc

class OpenFilesWidget(MWB, QWidget):

    def __init__(self, params):
        MWB.__init__(self, params)
        QWidget.__init__(self)
        self.widget = QTextEdit(self)
        self.widget.setMinimumSize(300,400)
