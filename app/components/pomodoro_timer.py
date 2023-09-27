from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton

try :
    from progress_bar_timer import ProgressBar
except ModuleNotFoundError:
    from .progress_bar_timer import ProgressBar

# QWidget[class="appswidget"] whats that  kind or reference?

class Timer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(480, 720)
        self.setMaximumSize(480, 720)

        # layout for frame
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.layout)

        # timer content widget
        timer_content_widget = QWidget()
        timer_content_widget.setObjectName("myTimer")
        self.layout.addWidget(timer_content_widget)

        # layout for timer content widget
        timer_vbox_layout = QGridLayout()
        timer_vbox_layout.setContentsMargins(30, 60, 30, 60)
        timer_vbox_layout.setSpacing(30)
        timer_content_widget.setLayout(timer_vbox_layout)

        # content
        modus_label = QLabel("Pomodoro")
        modus_label.setAlignment(Qt.AlignCenter)
        modus_label.setMinimumSize(100, 50)
        modus_label.setMaximumSize(69420, 50)
        timer_vbox_layout.addWidget(modus_label)

        # timer widget content
        timer_widget = QWidget()
        timer_widget.setObjectName("Timer")
        timer_widget.setMinimumSize(69, 400)
        timer_widget.setMaximumSize(400, 400)
        timer_vbox_layout.addWidget(timer_widget)

        # layout for timer content widget
        timer_widget_layout = QGridLayout()
        timer_widget.setLayout(timer_widget_layout)

        # progressbar
        progressbar = ProgressBar()
        timer_widget_layout.addWidget(progressbar)

        grouped_btn_widget = QWidget()
        grouped_btn_widget.setMinimumSize(69, 50)
        grouped_btn_widget.setMaximumSize(420, 50)
        timer_vbox_layout.addWidget(grouped_btn_widget)

        # layout for grouped_btn
        grouped_btn_layout = QHBoxLayout()
        grouped_btn_widget.setLayout(grouped_btn_layout)
        grouped_btn_layout.setContentsMargins(0, 0, 0, 0)
        grouped_btn_layout.setSpacing(0)

        # content of group btn (start, pause and stop btn)
        start_btn = QPushButton("Start")
        start_btn.setMinimumSize(120, 50)
        start_btn.setMaximumSize(120, 50)
        grouped_btn_layout.addWidget(start_btn)


        