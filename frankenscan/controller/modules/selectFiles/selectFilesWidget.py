from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QTextEdit, QListWidget, QVBoxLayout, \
    QLabel, QPushButton, QFileDialog
from ryvencore_qt import MWB
import ryvencore_qt as rc

from frankenscan.controller.settingsSingleton import settingsManager


class SelectFilesWidget(MWB, QWidget):

    #Used to signal changes to node
    filesSelectedSignal = Signal(object)

    def __init__(self, params):
        MWB.__init__(self, params)
        QWidget.__init__(self)

        container = QWidget(self)

        layout = QVBoxLayout(container)
        self.label = QLabel("No files selected")

        #Window that displays selected files
        self.list = QListWidget()

        #Button to select files
        button = QPushButton('Select Files')
        button.clicked.connect(self.selectFiles)

        layout.addWidget(self.label)
        layout.addWidget(self.list)
        layout.addWidget(button)

        self.widget = container
        self.widget.setMinimumSize(300,400)

    def selectFiles(self):

        dialog = QFileDialog()
        dialog.setWindowTitle("Choose files to open")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setNameFilters(["NIFTI format image (*.nii)"])
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory(settingsManager().getLatestFolder())

        filename = QtCore.QStringListModel()
        if dialog.exec_():
            files = dialog.selectedFiles()
            self.list.clear()
            numberOfFiles = 0
            for file in files:
                self.list.addItem(file)
                numberOfFiles = numberOfFiles + 1
            self.filesSelectedSignal.emit(files)
            print(files)
            self.label.setText(str(numberOfFiles) + ' files selected')
        else:
            #Do nothing if dialog cancelled
            pass
