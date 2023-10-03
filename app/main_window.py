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

try:
    from functions.pomodoro_timer_function import TimerApp
except ModuleNotFoundError:
    from .functions.pomodoro_timer_function import TimerApp

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

        self.menubar = MenuBar()
        helper1_layout.addWidget(self.menubar)

        self.content = Content()
        helper2_layout.addWidget(self.content)

        # btn connections
        self.menubar.task_btn.clicked.connect(self.click_task_btn)
        self.menubar.statistics_btn.clicked.connect(self.click_statistics_btn)
        self.menubar.settings_btn.clicked.connect(self.click_settings_btn)

        self.load_stylesheet()


        #self.to_stupid_to_close()

    def click_task_btn(self):
        self.content.content_stacked_widget.setCurrentWidget(self.content.page1)
        self.menubar.task_btn.setObjectName("primary_btn")
        self.menubar.statistics_btn.setObjectName("secondary_btn")
        self.menubar.settings_btn.setObjectName("secondary_btn")

        self.load_stylesheet()

    def click_statistics_btn(self):
        self.content.content_stacked_widget.setCurrentWidget(self.content.page2)
        self.menubar.task_btn.setObjectName("secondary_btn")
        self.menubar.statistics_btn.setObjectName("primary_btn")
        self.menubar.settings_btn.setObjectName("secondary_btn")

        self.load_stylesheet()


    def click_settings_btn(self):
        self.content.content_stacked_widget.setCurrentWidget(self.content.page3)
        self.menubar.task_btn.setObjectName("secondary_btn")
        self.menubar.statistics_btn.setObjectName("secondary_btn")
        self.menubar.settings_btn.setObjectName("primary_btn")

        self.load_stylesheet()

    def to_stupid_to_close(self):
        self.exit_timer = QTimer()
        self.exit_timer.timeout.connect(self.exit)
        self.exit_timer.start(30000)

    def exit(self):
        QApplication.quit()

    def load_stylesheet(self):
        with open("app/resources/styles.qss", "r") as qss_file:
            style_sheet = qss_file.read()
            self.setStyleSheet(style_sheet)

def main():
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Roboto")
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



