from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QFrame

TIME = 100

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)
        self.setLayout(self.grid)

        # bg widget
        bg = QWidget()
        bg.setObjectName("bg")
        self.grid.addWidget(bg)
        bg.setMinimumSize(300, 300)
        bg.setMaximumSize(300, 300)
        self.grid.addWidget(bg)

        # bg layout
        bg_layout = QGridLayout()
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.setSpacing(0)
        bg.setLayout(bg_layout)

        # circle bg
        circle_bg_widget = QWidget()
        circle_bg_widget.setObjectName("circle_bg")
        bg_layout.addWidget(circle_bg_widget)

        # circle bg layout
        circle_bg_widget_layout = QGridLayout()
        circle_bg_widget_layout.setContentsMargins(0, 0, 0, 0)
        circle_bg_widget_layout.setSpacing(0)
        circle_bg_widget.setLayout(circle_bg_widget_layout)
        # print(f"w:{bg.width()} and h:{bg.height()}")

        # circle path
        circle_path = QWidget()
        circle_path.setObjectName("circle_path")
        circle_path.setMinimumSize(300, 300)
        circle_path.setMaximumSize(300, 300)
        circle_bg_widget_layout.addWidget(circle_path)
        # color : qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.749 rgba(0, 0, 0, 0), stop:0.75 rgba(255, 255, 255, 255))

        # layout for circle path
        circle_path_layout = QGridLayout()
        circle_path_layout.setContentsMargins(0, 0, 0, 0)
        circle_path_layout.setSpacing(0)
        circle_path.setLayout(circle_path_layout)

        # circle fg widget
        circle_fg_widget = QWidget()
        circle_fg_widget.setObjectName("circle_fg")
        circle_fg_widget.setMinimumSize(275, 275)
        circle_fg_widget.setMaximumSize(275, 275)
        circle_path_layout.addWidget(circle_fg_widget)

        # layout for circle fg widget
        circle_fg_widget_layout = QGridLayout()
        circle_fg_widget.setLayout(circle_fg_widget_layout)

        timer_label = QLabel("25:00")
        timer_label.setObjectName("timer_label")
        timer_label.setAlignment(Qt.AlignCenter)
        circle_fg_widget_layout.addWidget(timer_label)
