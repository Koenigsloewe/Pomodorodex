from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QStackedWidget

try:
    from taskmanagement import TaskManagement
except ModuleNotFoundError:
    from .taskmanagement import TaskManagement

try:
    from statistic import Statistic
except ModuleNotFoundError:
    from .statistic import Statistic

try:
    from settings import Settings
except ModuleNotFoundError:
    from .settings import Settings


class Content(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        content_widget = QWidget()
        content_widget.setObjectName("content_widget")
        content_widget.setMinimumHeight(480)
        content_widget.setMaximumHeight(100000)
        self.layout.addWidget(content_widget)

        content_widget_layout = QGridLayout()
        content_widget_layout.setContentsMargins(0, 0, 0, 0)
        content_widget.setLayout(content_widget_layout)

        self.content_stacked_widget = QStackedWidget()
        content_widget_layout.addWidget(self.content_stacked_widget)

        # page 1
        self.page1 = TaskManagement()
        self.content_stacked_widget.addWidget(self.page1)

        # page 2
        self.page2 = Statistic()
        self.content_stacked_widget.addWidget(self.page2)

        # page 3
        self.page3 = Settings()
        self.content_stacked_widget.addWidget(self.page3)

        self.content_stacked_widget.setCurrentWidget(self.page1)