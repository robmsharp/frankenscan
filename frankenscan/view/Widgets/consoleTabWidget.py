from PySide2.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QLabel


class consoleTabWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        layout= QVBoxLayout(self)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        #label = QLabel("Console:")
        #layout.addWidget(label)
        layout.addWidget(self.console)

    #This is connected to signal from the stream
    def addMessage(self, message):
        print("Message recieved")
        self.console.append(message)
