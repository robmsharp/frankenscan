#Custom widget that enables dropped nodes to be recognised
from PySide2.QtCore import QMimeData
from PySide2.QtWidgets import QListWidget


class myListWidget (QListWidget):

    def mimeData(self, items):
        data = QMimeData()
        data.setText(items[0].text())
        return data