import json
import sys

from PyQt5.QtCore import QUrl, QTime
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaContent
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
        self.setWindowIcon(QIcon(":/icons/pomodorodex.ico"))

        # create centralWidget
        centralwidget = QWidget()
        centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(centralwidget)

        # create Layout for centralWidget
        layout_for_splitting_timer_with_management_tool = QHBoxLayout()
        centralwidget.setLayout(layout_for_splitting_timer_with_management_tool)
        layout_for_splitting_timer_with_management_tool.setContentsMargins(0, 0, 0, 0)

        # create pomodoro timer instance
        self.pomodoro_timer = Timer()
        layout_for_splitting_timer_with_management_tool.addWidget(self.pomodoro_timer)

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

        # init for load_stylesheet
        with open("config.json", "r") as f:
            self.config = json.load(f)
            self.dark_mode_bool = self.config["settings"][10]["darkMode"]

        # btn connections
        self.menubar.task_btn.clicked.connect(self.click_task_btn)
        self.menubar.statistics_btn.clicked.connect(self.click_statistics_btn)
        self.menubar.settings_btn.clicked.connect(self.click_settings_btn)

        self.content.page3.pomodoro_sound_changed.connect(lambda value: self.pomodoro_timer.timer_sound_player.setVolume(value))
        self.content.page3.break_sound_changed.connect(lambda value: self.pomodoro_timer.break_sound_player.setVolume(value))

        self.content.page3.ticking_sound_bool_changed.connect(lambda set_bool: self.pomodoro_timer.timer_sound_player.setMuted(set_bool))
        self.content.page3.break_sound_bool_changed.connect(lambda set_bool: self.pomodoro_timer.break_sound_player.setMuted(set_bool))
        self.content.page3.notification_changed.connect(lambda set_bool: self.pomodoro_timer.break_sound.setMuted(set_bool))
        self.content.page3.dark_mode_changed.connect(lambda set_bool: self.change_stylesheet(set_bool))

        self.content.page3.timer_mediaplayer_sound_changed.connect(
            lambda path: self.timer_sound_changed(path))
        self.content.page3.break_mediaplayer_sound_changed.connect(
            lambda path: self.pomodoro_timer.break_sound_player.setMedia(QMediaContent(QUrl.fromLocalFile(path))))

        self.content.page3.routine_changed.connect(lambda mylist: self.change_routine())

        self.load_stylesheet()

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

    def load_stylesheet(self):
        if self.dark_mode_bool:
            with open("app/resources/styles.qss", "r") as qss_file:
                style_sheet = qss_file.read()
                self.setStyleSheet(style_sheet)
        elif not self.dark_mode_bool:
            with open("app/resources/lightmode.qss", "r") as qss_file:
                style_sheet = qss_file.read()
                self.setStyleSheet(style_sheet)

    def change_stylesheet(self, value):
        self.dark_mode_bool = value
        self.load_stylesheet()

    def change_routine(self):
        self.routines = []
        self.pomodoro_timer.start_time_routine(self.routines)

        with open("config.json", "r") as f:
            config = json.load(f)
            self.routines = [(QTime.fromString(item["time"], "hh:mm:ss"), item["label"]) for item in config["routines"]]

        #self.pomodoro_timer.start_time_routine(self.routines)
        self.pomodoro_timer.start_timer(self.routines)

    def timer_sound_changed(self, path):
        self.pomodoro_timer.timer_sound_player.stop()
        self.pomodoro_timer.timer_sound_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.pomodoro_timer.timer_sound_player.play()
        
    def break_sound_changed(self, path):
        self.pomodoro_timer.break_sound_player.stop()
        self.pomodoro_timer.break_sound_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.pomodoro_timer.break_sound_player.play()

    def closeEvent(self, event):
        self.content.page1.save_tasks_for_config()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Roboto")
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



