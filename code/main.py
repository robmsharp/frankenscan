import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
    QVBoxLayout

#Constants
WINDOWWIDTH = 1600
WINDOWHEIGHT = 800

# This is the main window
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        container = QWidget()

        label = QLabel("Hello world")

        layout = QVBoxLayout(container)
        layout.addWidget(label)

        self.setCentralWidget(container)
        self.resize(WINDOWWIDTH, WINDOWHEIGHT)

# This launches the main window
if __name__ == '__main__':
    app = QApplication()

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

