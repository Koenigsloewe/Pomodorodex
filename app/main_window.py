import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton

try:
    from components.pomodoro_timer import Timer
except ModuleNotFoundError:
    from .components.pomodoro_timer import Timer

try:
    from components.menubar import MenuBar
except ModuleNotFoundError:
    from .components.menubar import MenuBar

try:
    from components.content import Content
except ModuleNotFoundError:
    from .components.content import Content

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

        # create pomodoro timer instance
        pomodoro_timer = Timer()
        layout_for_splitting_timer_with_management_tool.addWidget(pomodoro_timer)

        # create management tool instance
        management_tool_widget = QWidget()
        layout_for_splitting_timer_with_management_tool.addWidget(management_tool_widget)

        # management tool layout
        management_tool_layout = QGridLayout()
        management_tool_layout.setContentsMargins(0, 0, 0, 0)
        management_tool_layout.setSpacing(0)
        management_tool_widget.setLayout(management_tool_layout)

        # helper 1
        helper1 = QWidget()
        helper1.setMaximumHeight(165)
        management_tool_layout.addWidget(helper1)

        helper1_layout = QGridLayout()
        helper1_layout.setContentsMargins(9, 30, 30, 30)
        helper1.setLayout(helper1_layout)

        #helper 2
        helper2 = QWidget()
        management_tool_layout.addWidget(helper2)

        helper2_layout = QGridLayout()
        helper2_layout.setContentsMargins(0, 0, 21, 21)
        helper2.setLayout(helper2_layout)

        menubar = MenuBar()
        helper1_layout.addWidget(menubar)

        content = Content()
        helper2_layout.addWidget(content)
        #print(f"h:{content.height()}, w:{content.width()},\n {management_tool_layout.spacing()}")

        with open("app/resources/styles.qss", "r") as qss_file:
            style_sheet = qss_file.read()
            self.setStyleSheet(style_sheet)

        self.to_stupid_to_close()

        # connections
        #pomodoro_timer.start_btn.clicked.connect(None)

    def to_stupid_to_close(self):
        self.exit_timer = QTimer()
        self.exit_timer.timeout.connect(self.exit)
        self.exit_timer.start(30000)

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



