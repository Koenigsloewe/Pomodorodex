from PyQt5.QtCore import Qt, pyqtSignal, QTime, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton

try:
    from progress_bar_timer import ProgressBar
except ModuleNotFoundError:
    from .progress_bar_timer import ProgressBar

try:
    from app.resources import resources
except ModuleNotFoundError:
    from app.resources import resources


class Timer(QWidget):
    time_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(480)
        self.setMaximumWidth(480)

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

        # helper widget
        helper = QWidget()
        helper.setMaximumSize(480, 500)
        timer_vbox_layout.addWidget(helper)

        # helper layout
        helper_layout = QVBoxLayout()
        helper_layout.setContentsMargins(0, 0, 0, 0)
        helper.setLayout(helper_layout)

        # content
        self.modus_label = QLabel("Pomodoro")
        self.modus_label.setAlignment(Qt.AlignCenter)
        self.modus_label.setMinimumSize(100, 50)
        self.modus_label.setMaximumSize(69420, 50)
        helper_layout.addWidget(self.modus_label)

        # timer widget content
        timer_widget = QWidget()
        timer_widget.setObjectName("Timer")
        timer_widget.setMinimumSize(69, 400)
        timer_widget.setMaximumSize(400, 400)
        helper_layout.addWidget(timer_widget)

        # layout for timer content widget
        timer_widget_layout = QGridLayout()
        timer_widget.setLayout(timer_widget_layout)

        # progressbar
        self.progressbar = ProgressBar()
        timer_widget_layout.addWidget(self.progressbar)

        grouped_btn_widget = QWidget()
        grouped_btn_widget.setMinimumSize(69, 50)
        grouped_btn_widget.setMaximumSize(420, 50)
        helper_layout.addWidget(grouped_btn_widget)

        # layout for grouped_btn
        self.grouped_btn_layout = QHBoxLayout()
        grouped_btn_widget.setLayout(self.grouped_btn_layout)
        self.grouped_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.grouped_btn_layout.setSpacing(0)

        # content of group btn (start, pause and stop btn)
        self.start_btn = QPushButton("")
        self.start_btn.setIcon(QIcon(QPixmap(":/svg/play-fill.svg")))
        self.start_btn.setIconSize(QSize(40, 40))
        self.start_btn.setObjectName("primary_btn")
        self.start_btn.setMinimumSize(120, 50)
        self.start_btn.setMaximumSize(120, 50)
        self.grouped_btn_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("")
        self.pause_btn.setIcon(QIcon(QPixmap(":svg/pause-fill.svg")))
        self.pause_btn.setIconSize(QSize(40, 40))
        self.pause_btn.setObjectName("primary_btn")
        self.pause_btn.setMinimumSize(120, 50)
        self.pause_btn.setMaximumSize(120, 50)

        self.stop_btn = QPushButton("")
        self.stop_btn.setIcon(QIcon(QPixmap(":/svg/stop-fill.svg")))
        self.stop_btn.setIconSize(QSize(40, 40))
        self.stop_btn.setObjectName("primary_btn")
        self.stop_btn.setMinimumSize(120, 50)
        self.stop_btn.setMaximumSize(120, 50)

        self.resume_btn = QPushButton("")
        self.resume_btn.setIcon(QIcon(QPixmap(":/svg/play-fill.svg")))
        self.resume_btn.setIconSize(QSize(40, 40))
        self.resume_btn.setObjectName("primary_btn")
        self.resume_btn.setMinimumSize(120, 50)
        self.resume_btn.setMaximumSize(120, 50)

        # connections
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.resume_btn.clicked.connect(self.resume_timer)

        self.circle_path_timer_stylesheet = """#circle_path{
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 0, 0), stop:{stop2} rgba(255, 255, 255, 255));
                    border-radius: 149px;
                }"""

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.timeout.connect(self.sync_progressbar)

        self.stop1 = 1
        self.stop2 = 1

    def start_time_routine(self):
        routines = [
            (QTime(0, 25, 0), "Pomodoro"),
            (QTime(0, 5, 0), "Short Break"),
            (QTime(0, 25, 0), "Pomodoro"),
            (QTime(0, 5, 0), "Short Break"),
            (QTime(0, 25, 0), "Pomodoro"),
            (QTime(0, 5, 0), "Short Break"),
            (QTime(0, 25, 0), "Pomodoro"),
            (QTime(0, 5, 0), "Short Break"),
            (QTime(0, 25, 0), "Pomodoro"),
            (QTime(0, 20, 0), "Long Break")
        ]

        for time, label in routines:
            self.time_left = time
            self.modus_label.setText(label)
            self.progressbar.timer_label.setText(time.toString(Qt.TextDate))

            self.time_limit_const = - (1 / self.time_left.secsTo(QTime(0, 0)))
            self.timer.start(1000)

            if self.time_left == QTime(0, 0) :
                self.reset_progressbar()


    def sync_progressbar(self):
        self.stop2 = self.stop1 - self.time_limit_const
        print(self.stop1, self.stop2)

        # change stylesheet ## var name issue + based on time issue
        self.new_circle_path_timer_stylesheet = self.circle_path_timer_stylesheet.replace("{stop1}", str(self.stop2)).replace("{stop2}", str(self.stop1))

        self.progressbar.circle_path.setStyleSheet(self.new_circle_path_timer_stylesheet)

        self.stop1 = self.stop1 - self.time_limit_const

    def reset_progressbar(self):
        self.stop1 = 1
        self.stop2 = 0.99999

        self.new_circle_path_timer_stylesheet = self.circle_path_timer_stylesheet.replace("{stop1}",
                                                                                          str(self.stop2)).replace(
            "{stop2}", str(self.stop1))
        self.progressbar.circle_path.setStyleSheet(self.new_circle_path_timer_stylesheet)
        self.stop1 = 1
        self.stop2 = 1

    def start_timer(self):

        self.grouped_btn_layout.removeWidget(self.start_btn)
        self.start_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.pause_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

        self.start_time_routine()

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        current_time = self.time_left.toString(Qt.TextDate)
        self.progressbar.timer_label.setText(current_time)

        if self.time_left == QTime(0, 0):
            self.timer.stop()
            print("time is up")

    def pause_timer(self):
        self.timer.stop()

        self.grouped_btn_layout.removeWidget(self.pause_btn)
        self.pause_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.resume_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

    def resume_timer(self):
        self.timer.start(1000)

        self.grouped_btn_layout.removeWidget(self.resume_btn)
        self.resume_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.pause_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

    def stop_timer(self):
        self.timer.stop()
        self.time_left = QTime(0, 25, 0)
        self.progressbar.timer_label.setText("00:25:00")
        self.reset_progressbar()

        self.grouped_btn_layout.removeWidget(self.pause_btn)
        self.pause_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.resume_btn)
        self.resume_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.start_btn)
