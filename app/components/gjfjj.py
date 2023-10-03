import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.button = QPushButton('Button')
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeStylesheet)
        self.timer.start(1000)  # Set timer interval to 1000 milliseconds (1 second)

    def changeStylesheet(self):
        # Toggle the stylesheet every second
        if self.button.styleSheet() == "":
            self.button.setStyleSheet("background-color: red;")
        else:
            self.button.setStyleSheet("")


app = QApplication(sys.argv)
ex = Example()
ex.show()
sys.exit(app.exec_())
