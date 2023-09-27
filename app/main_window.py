import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton

try :
    from components.pomodoro_timer import *
except ModuleNotFoundError:
    from .components.pomodoro_timer import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Pomodorodex")
        self.setMinimumSize(1280, 720)
        self.setWindowIcon(QIcon("app/resources/icons/pomodorodex.ico"))

        # create centralWidget
        centralwidget = QWidget()
        centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(centralwidget)

        # create Layout for centralWidget
        layout_for_splitting_timer_with_management_tool = QHBoxLayout()
        centralwidget.setLayout(layout_for_splitting_timer_with_management_tool)
        layout_for_splitting_timer_with_management_tool.setContentsMargins(0, 0, 0, 0)

        #crate pomodoro timer instance
        pomodoro_timer = Timer()
        layout_for_splitting_timer_with_management_tool.addWidget(pomodoro_timer)

        management_tool_widget = QWidget()
        layout_for_splitting_timer_with_management_tool.addWidget(management_tool_widget)

        management_tool_layout = QVBoxLayout()
        management_tool_widget.setLayout(management_tool_layout)

        menubar = Menubar()
        management_tool_layout.addWidget(menubar)

        with open("app/resources/styles.qss", "r") as qss_file:
            style_sheet = qss_file.read()
            self.setStyleSheet(style_sheet)

        self.to_stupid_to_close()

    def to_stupid_to_close(self):
        self.exit_timer = QTimer()
        self.exit_timer.timeout.connect(self.exit)
        self.exit_timer.start(10000)

    def exit(self):
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Roboto")
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



