from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton


class MenuBar(QWidget):
    def __init__(self):
        super().__init__()

        # menubar layout
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # menubar widget
        menubar_widget = QWidget()
        menubar_widget.setObjectName("menubar_widget")
        menubar_widget.setMinimumHeight(100)
        menubar_widget.setMaximumHeight(100)
        self.layout.addWidget(menubar_widget)

        # menubar content layout
        menubar_content_layout = QHBoxLayout()
        menubar_widget.setLayout(menubar_content_layout)

        # grouped btn widget
        grouped_btn_widget = QWidget()
        grouped_btn_widget.setMaximumWidth(450)
        menubar_content_layout.addWidget(grouped_btn_widget)

        # layout for grouped btn widget
        grouped_btn_layout = QHBoxLayout()
        grouped_btn_widget.setLayout(grouped_btn_layout)

        # btn
        self.task_btn = QPushButton("Task")
        self.task_btn.setObjectName("primary_btn")
        self.task_btn.setMinimumSize(120, 50)
        self.task_btn.setMaximumSize(120, 50)
        grouped_btn_layout.addWidget(self.task_btn)

        self.statistics_btn = QPushButton("Statistics")
        self.statistics_btn.setObjectName("secondary_btn")
        self.statistics_btn.setMinimumSize(120, 50)
        self.statistics_btn.setMaximumSize(120, 50)
        grouped_btn_layout.addWidget(self.statistics_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setObjectName("secondary_btn")
        self.settings_btn.setMinimumSize(120, 50)
        self.settings_btn.setMaximumSize(120, 50)
        grouped_btn_layout.addWidget(self.settings_btn)

