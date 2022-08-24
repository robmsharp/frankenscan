from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QTextEdit, QListWidget, QVBoxLayout, \
    QLabel, QPushButton, QFileDialog, QTabWidget
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

        #Tabs so can view file names and file paths
        tabs = QTabWidget()

        layout = QVBoxLayout(container)
        self.label = QLabel("No files selected")

        #Window that displays selected files
        self.fileList = QListWidget()
        self.filePathList = QListWidget()

        #Button to select files
        button = QPushButton('Select Files')
        button.clicked.connect(self.selectFiles)

        layout.addWidget(self.label)
        layout.addWidget(tabs)
        layout.addWidget(button)

        tabs.addTab(self.fileList, "files")
        tabs.addTab(self.filePathList, "filePaths")

        self.widget = container
        self.widget.setMinimumSize(300,400)

    def selectFiles(self):

        dialog = QFileDialog()
        dialog.setWindowTitle("Choose files")
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setDirectory(settingsManager().getLatestFolder())

        filename = QtCore.QStringListModel()
        if dialog.exec_():
            files = dialog.selectedFiles()
            self.filePathList.clear()
            self.fileList.clear()
            numberOfFiles = 0
            for filePath in files:
                self.filePathList.addItem(filePath)
                file = filePath.split("/")[-1]
                self.fileList.addItem(file)
                numberOfFiles = numberOfFiles + 1
            #Emit the file paths
            self.filesSelectedSignal.emit(files)
            self.label.setText(str(numberOfFiles) + ' files selected')
        else:
            #Do nothing if dialog cancelled
            pass
