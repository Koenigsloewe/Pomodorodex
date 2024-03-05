import json

from PyQt5.QtCore import Qt, pyqtSignal, QTime, QTimer, QSize, QUrl, QElapsedTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt5.QtMultimedia import QSoundEffect, QMediaPlayer, QMediaContent

try:
    from progress_bar_timer import ProgressBar
except ModuleNotFoundError:
    from .progress_bar_timer import ProgressBar

try:
    from app.resources import resources
except ModuleNotFoundError:
    from app.resources import resources


class Timer(QWidget):
    routine_started = pyqtSignal()

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
        self.modus_label = QLabel("")
        self.modus_label.setObjectName("headline")
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

        self.circle_path_timer_stylesheet = """#circle_path{
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 0, 0), stop:{stop2} rgba(255, 255, 255, 255));
                    border-radius: 149px;
                }"""
        # setup
        with open("config.json", "r") as f:
            config = json.load(f)
            self.routines = [(QTime.fromString(item["time"], "hh:mm:ss"), item["label"]) for item in config["routines"]]
            self.timer_sound_int = int(config["settings"][6]["pomodoroSoundVolume"])
            self.break_sound_int = int(config["settings"][9]["breakSoundVolume"])
            self.timer_sound_path = config["settings"][5]["customPomodoroSoundSelected"]
            self.break_sound_path = config["settings"][8]["customBreakSoundSelected"]
            self.timer_sound_bool = config["settings"][4]["tickingSound"]
            self.break_sound_bool = config["settings"][7]["breakSound"]
            self.notification_bool = config["settings"][11]["notification"]

        self.start_time = self.routines[0][0].toString(Qt.TextDate)
        start_text = self.routines[0][1]
        self.progressbar.timer_label.setText(self.start_time)
        self.modus_label.setText(start_text)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.timeout.connect(self.sync_progressbar)

        self.routine_started.connect(self.play_break_sound_notification)

        self.timer_sound_player = QMediaPlayer()
        self.play_ticking_timer_sound()
        self.break_sound_player = QMediaPlayer()
        self.play_break_sound()
        self.break_sound = QSoundEffect()
        self.active_player = QMediaPlayer()

        self.start_time_phase = []
        self.pomodoro_durations = []
        self.break_durations = []

        self.stop1 = 1
        self.stop2 = 1
        # connections
        self.start_btn.clicked.connect(lambda : self.start_timer(self.routines))
        self.pause_btn.clicked.connect(self.pause_timer)
        self.stop_btn.clicked.connect(self.stop_timer)
        self.resume_btn.clicked.connect(self.resume_timer)

    def start_time_routine(self, routines, index=0):
        self.reset_progressbar()

        if index < len(routines):
            time, label = routines[index]
            self.time_left = time
            self.modus_label.setText(label)
            self.progressbar.timer_label.setText(time.toString(Qt.TextDate))

            self.time_limit_const = - (1 / self.time_left.secsTo(QTime(0, 0)))

            try:
                self.start_time_phase.append(QTime.currentTime())
            except:
                pass

            try:
                self.difference = self.start_time_phase[-2].secsTo(self.start_time_phase[-1]) / 60
            except:
                self.difference = 0

            if index != 0:
                self.routine_started.emit()

            if label == "Short Break" or label == "Long Break":
                self.active_player.stop()
                self.active_player = self.break_sound_player
                self.pomodoro_durations.append(self.difference)

            elif label == "Pomodoro":
                self.active_player.stop()
                self.active_player = self.timer_sound_player
                self.break_durations.append(self.difference)

            # Use a QTimer to call the next routine
            QTimer.singleShot(time.msecsSinceStartOfDay(), lambda: self.start_time_routine(routines, index + 1))

        else:
            QTimer.singleShot(0, lambda: self.start_time_routine(routines, 0))

    def update_routines(self, new_routines):
        self.routines = new_routines
        self.reset_timer()

    def reset_timer(self):
        # Stop the timer if it's running
        self.timer.stop()

        # Reset the media players
        self.timer_sound_player.stop()
        self.break_sound_player.stop()

        # Reset the progress bar and labels to initial state
        self.reset_progressbar()
        if self.routines:
            self.start_time = self.routines[0][0].toString(Qt.TextDate)
            start_text = self.routines[0][1]
            self.progressbar.timer_label.setText(self.start_time)
            self.modus_label.setText(start_text)

        # Reset other internal states as needed
        self.start_time_phase = []
        self.pomodoro_durations = []
        self.break_durations = []
        self.stop1 = 1
        self.stop2 = 1

        # Ensure the start button is visible and others are hidden
        self.grouped_btn_layout.removeWidget(self.pause_btn)
        self.pause_btn.setParent(None)
        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)
        self.grouped_btn_layout.removeWidget(self.resume_btn)
        self.resume_btn.setParent(None)
        if not self.grouped_btn_layout.indexOf(self.start_btn) >= 0:
            self.grouped_btn_layout.addWidget(self.start_btn)

    def sync_progressbar(self):
        self.stop2 = self.stop1 - self.time_limit_const

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

    def start_timer(self, routine):
        self.grouped_btn_layout.removeWidget(self.start_btn)
        self.start_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.pause_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

        self.start_time_routine(routine, 0)
        self.timer.start(1000)
        self.active_player.play()

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        current_time = self.time_left.toString(Qt.TextDate)
        self.progressbar.timer_label.setText(current_time)

        if self.time_left == QTime(0, 0):
            self.timer.stop()

    def pause_timer(self):
        self.timer.stop()
        self.active_player.pause()
        #self.fade_timer.start(100)

        self.grouped_btn_layout.removeWidget(self.pause_btn)
        self.pause_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.resume_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

    def resume_timer(self):
        self.timer.start(1000)
        self.active_player.play()

        self.grouped_btn_layout.removeWidget(self.resume_btn)
        self.resume_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.pause_btn)
        self.grouped_btn_layout.addWidget(self.stop_btn)

    def stop_timer(self):
        self.timer.stop()

        self.active_player.stop()

        self.progressbar.timer_label.setText(self.start_time)
        self.reset_progressbar()

        self.grouped_btn_layout.removeWidget(self.pause_btn)
        self.pause_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.stop_btn)
        self.stop_btn.setParent(None)

        self.grouped_btn_layout.removeWidget(self.resume_btn)
        self.resume_btn.setParent(None)

        self.grouped_btn_layout.addWidget(self.start_btn)

        if self.start_time_phase is not None:
            end_time = QTime.currentTime()
            duration = self.start_time_phase[-1].secsTo(end_time) / 60

            self.start_time_phase = None

            # Depending on the phase, append the duration to the corresponding list
            if self.modus_label.text() == "Pomodoro":
                self.pomodoro_durations.append(duration)
            elif self.modus_label.text() == "Short Break" or self.modus_label.text() == "Long Break":
                self.break_durations.append(duration)

    def play_ticking_timer_sound(self):
        # get file
        media_content = QMediaContent(QUrl.fromLocalFile(self.timer_sound_path))

        # sound setup
        self.timer_sound_player.setMedia(media_content)
        self.timer_sound_player.setVolume(self.timer_sound_int)
        self.timer_sound_player.setMuted(self.timer_sound_bool)
        self.timer_sound_player.mediaStatusChanged.connect(self.on_media_status_changed)

    def play_break_sound(self):
        # get file
        media_content2 = QMediaContent(QUrl.fromLocalFile(self.break_sound_path))

        # sound setup
        self.break_sound_player.setMedia(media_content2)
        self.break_sound_player.setVolume(self.break_sound_int)
        self.break_sound_player.setMuted(self.break_sound_bool)
        self.break_sound_player.mediaStatusChanged.connect(self.on_media_status_changed)

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.active_player.setPosition(0)
            self.active_player.play()

    def play_break_sound_notification(self):
        url = QUrl.fromLocalFile(":/sound/change_modus_sound.wav")

        self.break_sound.setSource(url)
        self.break_sound.setVolume(self.break_sound_int)
        self.break_sound.setMuted(self.notification_bool)
        self.break_sound.play()

    def set_volume(self, value):
        if self.active_player == self.timer_sound_player:
            self.active_player.setVolume(value)
        elif self.active_player == self.break_sound_player:
            self.active_player.setVolume(value)

    def update_timer_sound(self, path):
        if path:  # Ensure the path is not empty or invalid
            if self.timer_sound_player.state() == QMediaPlayer.PlayingState:
                self.timer_sound_player.stop()
            self.timer_sound_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            if self.timer.isActive():  # Check if the timer is running
                self.timer_sound_player.play()

    def update_break_sound(self, path):
        if path:
            if self.break_sound_player.state() == QMediaPlayer.PlayingState:
                self.break_sound_player.stop()
            self.break_sound_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            if self.timer.isActive() and self.modus_label.text().startswith("Break"):
                self.break_sound_player.play()
