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

        content_stacked_widget = QStackedWidget()
        content_widget_layout.addWidget(content_stacked_widget)

        # page 1
        page1 = TaskManagement()
        content_stacked_widget.addWidget(page1)

        # page 2
        page2 = Statistic()
        content_stacked_widget.addWidget(page2)

        # page 3
        page3 = Settings()
        content_stacked_widget.addWidget(page3)
