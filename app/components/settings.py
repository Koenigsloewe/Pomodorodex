import json
import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QPushButton, QScrollArea, QSlider, QSpinBox, QComboBox, QSizePolicy, QTextBrowser, QFrame, QFileDialog

try:
    from custom_widgets import SwitchButton
except ModuleNotFoundError:
    from .custom_widgets import SwitchButton

TIME_VALUES = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 45, 59]
SETTING_INDEX_MAP = {
    "Pomodoro": [0, "pomodoroDuration"],
    "Short Break": [1, "shortBreakDuration"],
    "Long Break": [2, "longBreakDuration"],
    "Pomodoro Session": [3, "pomodoroSession"],
    "Ticking Sound": [4, "tickingSound"],
    "Custom Pomodoro Sound Selected": [5, "customPomodoroSoundSelected"],
    "Pomodoro Sound Volume": [6, "pomodoroSoundVolume"],
    "Break Sound": [7, "breakSound"],
    "Custom Break Sound Selected": [8, "customBreakSoundSelected"],
    "Break Sound Volume": [9, "breakSoundVolume"],
    "Dark Mode": [10, "darkMode"],
    "Notification": [11, "notification"]
}


class Settings(QWidget):
    pomodoro_sound_changed = pyqtSignal(int)
    break_sound_changed = pyqtSignal(int)
    ticking_sound_bool_changed = pyqtSignal(bool)
    break_sound_bool_changed = pyqtSignal(bool)
    notification_changed = pyqtSignal(bool)
    dark_mode_changed = pyqtSignal(bool)
    timer_mediaplayer_sound_changed = pyqtSignal(str)
    break_mediaplayer_sound_changed = pyqtSignal(str)
    routine_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        with open("config.json", "r") as f:
            self.config = json.load(f)
        pomodoro_duration_int = int(self.config["settings"][0]["pomodoroDuration"].split(":")[1])
        short_break_duration_int = int(self.config["settings"][1]["shortBreakDuration"].split(":")[1])
        long_break_duration_int = int(self.config["settings"][2]["longBreakDuration"].split(":")[1])
        pomodoro_session_int = int(self.config["settings"][3]["pomodoroSession"])
        ticking_sound_bool = self.config["settings"][4]["tickingSound"]
        custom_pomodoro_sound_selected_string = self.config["settings"][5]["customPomodoroSoundSelected"]
        pomodoro_sound_volume = int(self.config["settings"][6]["pomodoroSoundVolume"])
        break_sound_bool = self.config["settings"][7]["breakSound"]
        custom_break_sound_selected_string = self.config["settings"][8]["customBreakSoundSelected"]
        break_sound_volume = int(self.config["settings"][9]["breakSoundVolume"])
        dark_mode_bool = self.config["settings"][10]["darkMode"]
        notification_bool = self.config["settings"][11]["notification"]

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout)

        # scroll area for settings widget
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        settings_widget = QWidget()
        scroll_area.setWidget(settings_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        settings_widget.setObjectName("task_widget")

        settings_widget_layout = QVBoxLayout()
        settings_widget_layout.setContentsMargins(15, 0, 15, 0)
        settings_widget_layout.setSpacing(60)
        settings_widget.setLayout(settings_widget_layout)

        """timer widget setup"""
        timer_settings_widget = QWidget()
        settings_widget_layout.addWidget(timer_settings_widget)

        timer_settings_widget_layout = QGridLayout()
        timer_settings_widget_layout.setContentsMargins(0, 0, 0, 0)
        timer_settings_widget_layout.setSpacing(15)
        timer_settings_widget.setLayout(timer_settings_widget_layout)

        timer_headline_label = QLabel("Timer")
        timer_headline_label.setObjectName("headline")
        timer_settings_widget_layout.addWidget(timer_headline_label, 0, 0, 1, 2)

        pomodoro_duration_label = QLabel("Pomodoro duration")
        timer_settings_widget_layout.addWidget(pomodoro_duration_label, 1, 0)

        self.pomodoro_duration_display_label = QLabel(f"{pomodoro_duration_int} min")
        self.pomodoro_duration_display_label.setObjectName("display")
        self.pomodoro_duration_display_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        timer_settings_widget_layout.addWidget(self.pomodoro_duration_display_label, 1, 1)

        # QSlider
        self.pomodoro_duration_slider = QSlider()
        self.pomodoro_duration_slider.setOrientation(Qt.Horizontal)
        self.pomodoro_duration_slider.setRange(0, len(TIME_VALUES) - 1)
        self.pomodoro_duration_slider.setTickInterval(1)
        self.pomodoro_duration_slider.setValue(TIME_VALUES.index(pomodoro_duration_int))
        timer_settings_widget_layout.addWidget(self.pomodoro_duration_slider, 2, 0, 1, 2)

        short_break_duration_label = QLabel("Short Break Duration")
        timer_settings_widget_layout.addWidget(short_break_duration_label, 3, 0)

        self.short_break_duration_display_label = QLabel(f"{short_break_duration_int} min")
        self.short_break_duration_display_label.setObjectName("display")
        self.short_break_duration_display_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        timer_settings_widget_layout.addWidget(self.short_break_duration_display_label, 3, 1)

        # QSlider
        self.short_break_duration_slider = QSlider()
        self.short_break_duration_slider.setOrientation(Qt.Horizontal)
        self.short_break_duration_slider.setRange(0, len(TIME_VALUES) - 1)
        self.short_break_duration_slider.setTickInterval(1)
        self.short_break_duration_slider.setValue(TIME_VALUES.index(short_break_duration_int))
        timer_settings_widget_layout.addWidget(self.short_break_duration_slider, 4, 0, 1, 2)

        long_break_duration_label = QLabel("Long Break Duration")
        timer_settings_widget_layout.addWidget(long_break_duration_label, 5, 0)

        self.long_break_duration_display_label = QLabel(f"{long_break_duration_int} min")
        self.long_break_duration_display_label.setObjectName("display")
        self.long_break_duration_display_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        timer_settings_widget_layout.addWidget(self.long_break_duration_display_label, 5, 1)

        # QSlider
        self.long_break_duration_slider = QSlider()
        self.long_break_duration_slider.setOrientation(Qt.Horizontal)
        self.long_break_duration_slider.setRange(0, len(TIME_VALUES) - 1)
        self.long_break_duration_slider.setTickInterval(1)
        self.long_break_duration_slider.setValue(TIME_VALUES.index(long_break_duration_int))
        timer_settings_widget_layout.addWidget(self.long_break_duration_slider, 6, 0, 1, 2)

        pomodoro_sessions_before_long_break_label = QLabel("Pomodoro Sessions before long break")
        timer_settings_widget_layout.addWidget(pomodoro_sessions_before_long_break_label, 7, 0)

        self.pomodoro_sessions_before_long_break_spinbox = QSpinBox()
        self.pomodoro_sessions_before_long_break_spinbox.setMinimumWidth(100)
        self.pomodoro_sessions_before_long_break_spinbox.setMaximumWidth(100)
        self.pomodoro_sessions_before_long_break_spinbox.setMinimum(1)
        self.pomodoro_sessions_before_long_break_spinbox.setMaximum(8)
        self.pomodoro_sessions_before_long_break_spinbox.setValue(pomodoro_session_int)
        self.pomodoro_sessions_before_long_break_spinbox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        timer_settings_widget_layout.addWidget(self.pomodoro_sessions_before_long_break_spinbox, 7, 1)

        """sound widget setup"""
        sound_settings_widget = QWidget()
        settings_widget_layout.addWidget(sound_settings_widget)

        sound_settings_widget_layout = QGridLayout()
        sound_settings_widget_layout.setContentsMargins(0, 0, 0, 0)
        sound_settings_widget_layout.setSpacing(15)
        sound_settings_widget.setLayout(sound_settings_widget_layout)

        sound_headline_label = QLabel("Sound")
        sound_headline_label.setObjectName("headline")
        sound_settings_widget_layout.addWidget(sound_headline_label, 0, 0, 1, 2)

        ticking_sound_label = QLabel("Ticking Sound")
        sound_settings_widget_layout.addWidget(ticking_sound_label, 1, 0)

        self.ticking_sound_switch_btn = SwitchButton()
        self.ticking_sound_switch_btn.setObjectName("toggle")
        self.ticking_sound_switch_btn.setChecked(not ticking_sound_bool)
        sound_settings_widget_layout.addWidget(self.ticking_sound_switch_btn, 1, 1)
        sound_settings_widget_layout.setAlignment(self.ticking_sound_switch_btn, Qt.AlignRight | Qt.AlignVCenter)

        custom_pomodoro_sound_label = QLabel("Custom Pomodoro Sound")
        sound_settings_widget_layout.addWidget(custom_pomodoro_sound_label, 2, 0)

        self.custom_sound_combobox = QComboBox()
        self.custom_sound_combobox.setMinimumHeight(50)
        self.custom_sound_combobox.setMaximumHeight(50)
        self.custom_sound_combobox.addItem("None")
        self.custom_sound_combobox.addItem("Ticking Sound")
        self.custom_sound_combobox.addItem("LoFi")
        self.custom_sound_combobox.insertSeparator(200)
        self.custom_sound_combobox.addItem("Custom Music")
        self.custom_sound_combobox.setCurrentText(custom_pomodoro_sound_selected_string)
        sound_settings_widget_layout.addWidget(self.custom_sound_combobox, 2, 1)
        sound_settings_widget_layout.setAlignment(self.custom_sound_combobox, Qt.AlignRight | Qt.AlignVCenter)

        ticking_volume_label = QLabel("Ticking Volume")
        sound_settings_widget_layout.addWidget(ticking_volume_label, 3, 0)

        volume_down_label = QLabel()
        volume_down_label.setPixmap(QIcon(":/svg/volume-down.svg").pixmap(30, 30))
        sound_settings_widget_layout.addWidget(volume_down_label, 4, 0)

        volume_up_label = QLabel()
        volume_up_label.setPixmap(QIcon(":/svg/volume-up.svg").pixmap(30, 30))
        volume_up_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sound_settings_widget_layout.addWidget(volume_up_label, 4, 1)

        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setValue(pomodoro_sound_volume)
        sound_settings_widget_layout.addWidget(self.volume_slider, 5, 0, 1, 2)

        break_volume_label = QLabel("Break Sound")
        sound_settings_widget_layout.addWidget(break_volume_label, 6, 0)

        self.break_sound_switch_btn = SwitchButton()
        self.break_sound_switch_btn.setChecked(not break_sound_bool)
        sound_settings_widget_layout.addWidget(self.break_sound_switch_btn, 6, 1)
        sound_settings_widget_layout.setAlignment(self.break_sound_switch_btn, Qt.AlignRight | Qt.AlignVCenter)

        break_volume_label = QLabel("Custom Break Sound")
        sound_settings_widget_layout.addWidget(break_volume_label, 7, 0)

        self.custom_break_sound_combobox = QComboBox()
        self.custom_break_sound_combobox.setMinimumHeight(50)
        self.custom_break_sound_combobox.setMaximumHeight(50)
        self.custom_break_sound_combobox.addItem("None")
        self.custom_break_sound_combobox.addItem("Classic")
        self.custom_break_sound_combobox.insertSeparator(200)
        self.custom_break_sound_combobox.addItem("Custom Music")
        self.custom_break_sound_combobox.setCurrentText(custom_break_sound_selected_string)
        sound_settings_widget_layout.addWidget(self.custom_break_sound_combobox, 7, 1)
        sound_settings_widget_layout.setAlignment(self.custom_break_sound_combobox, Qt.AlignRight | Qt.AlignVCenter)

        break_volume_label = QLabel("Break Sound Volume")
        sound_settings_widget_layout.addWidget(break_volume_label, 8, 0)

        volume_down_label = QLabel()
        volume_down_label.setPixmap(QIcon(":/svg/volume-down.svg").pixmap(30, 30))
        sound_settings_widget_layout.addWidget(volume_down_label, 9, 0)

        volume_up_label = QLabel()
        volume_up_label.setPixmap(QIcon(":/svg/volume-up.svg").pixmap(30, 30))
        volume_up_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sound_settings_widget_layout.addWidget(volume_up_label, 9, 1)

        self.break_volume_slider = QSlider()
        self.break_volume_slider.setOrientation(Qt.Horizontal)
        self.break_volume_slider.setRange(0, 100)
        self.break_volume_slider.setTickInterval(1)
        self.break_volume_slider.setValue(break_sound_volume)
        sound_settings_widget_layout.addWidget(self.break_volume_slider, 10, 0, 1, 2)

        """desktop widget setup"""
        desktop_settings_widget = QWidget()
        settings_widget_layout.addWidget(desktop_settings_widget)

        desktop_settings_widget_layout = QGridLayout()
        desktop_settings_widget_layout.setContentsMargins(0, 0, 0, 0)
        desktop_settings_widget_layout.setSpacing(15)
        desktop_settings_widget.setLayout(desktop_settings_widget_layout)

        desktop_headline_label = QLabel("Desktop")
        desktop_headline_label.setObjectName("headline")
        desktop_settings_widget_layout.addWidget(desktop_headline_label, 0, 0, 1, 2)

        dark_mode_label = QLabel("Dark Mode")
        desktop_settings_widget_layout.addWidget(dark_mode_label, 1, 0)

        self.dark_mode_switch_btn = SwitchButton()
        self.dark_mode_switch_btn.setChecked(not dark_mode_bool)
        desktop_settings_widget_layout.addWidget(self.dark_mode_switch_btn, 1, 1)

        notification_label = QLabel("Notification")
        desktop_settings_widget_layout.addWidget(notification_label, 2, 0)

        self.notification_switch_btn = SwitchButton()
        self.notification_switch_btn.setChecked(not notification_bool)
        desktop_settings_widget_layout.addWidget(self.notification_switch_btn, 2, 1)

        # about widget setup
        about_settings_widget = QWidget()
        settings_widget_layout.addWidget(about_settings_widget)

        about_settings_widget_layout = QVBoxLayout()
        about_settings_widget_layout.setContentsMargins(0, 0, 0, 0)
        about_settings_widget_layout.setSpacing(15)
        about_settings_widget.setLayout(about_settings_widget_layout)

        about_headline_label = QLabel("About")
        about_headline_label.setObjectName("headline")
        about_settings_widget_layout.addWidget(about_headline_label)

        author = "Königslöwe"
        version = "0.1"
        about_text = f"""
Welcome to Pomodorodex - Your Ultimate Productivity Companion!

Version: {version}
Created by {author}
Copywriting assistance by Chat-GPT 3.5

Pomodorodex is more than just a productivity app; it's a tool I designed to help boost my own focus and productivity. I believe that effective time management and focused work sessions are crucial for achieving our goals.

Key Features:

- 🍅 Pomodoro Timer: Customize work intervals and breaks to suit your workflow, ensuring you stay in the zone.

- 📋 Task Management: Organize your tasks, projects, and to-do lists seamlessly, so you can focus on what matters most.

- 📊 Stats Tracking: Gain valuable insights into your work habits. Track your productivity trends over time, allowing you to make informed decisions for continuous improvement.

Open Source Acknowledgment:

Pomodorodex uses the PyQt5 framework for its intuitive user interface. Big thanks to the PyQt5 development team for their exceptional work!

License:

Pomodorodex is a personal project, not intended for commercial use.

Thank you for using Pomodorodex! I hope it helps you on your productivity journey.

{author}
        """

        about_label = QLabel(about_text)
        about_label.setObjectName("about")
        about_label.setWordWrap(True)
        about_settings_widget_layout.addWidget(about_label)

        self.pomodoro_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.pomodoro_duration_slider, self.pomodoro_duration_display_label, "Pomodoro"))
        self.short_break_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.short_break_duration_slider, self.short_break_duration_display_label, "Short Break"))
        self.long_break_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.long_break_duration_slider, self.long_break_duration_display_label, "Long Break"))
        self.volume_slider.valueChanged.connect(
            lambda: self.volume_slider_changed(self.volume_slider, "Pomodoro Sound Volume"))
        self.break_volume_slider.valueChanged.connect(
            lambda: self.volume_slider_changed(self.break_volume_slider, "Break Sound Volume"))

        self.pomodoro_sessions_before_long_break_spinbox.valueChanged.connect(
            lambda: self.spinbox_changed(self.pomodoro_sessions_before_long_break_spinbox))

        self.ticking_sound_switch_btn.stateChanged.connect(
            lambda state, key="Ticking Sound": self.switchbutton_changed(state, key))
        self.break_sound_switch_btn.stateChanged.connect(
            lambda state, key="Break Sound": self.switchbutton_changed(state, key))
        self.dark_mode_switch_btn.stateChanged.connect(
            lambda state, key="Dark Mode": self.switchbutton_changed(state, key))
        self.notification_switch_btn.stateChanged.connect(
            lambda state, key="Notification": self.switchbutton_changed(state, key))

        self.custom_sound_combobox.currentIndexChanged.connect(
            lambda index, key="Custom Pomodoro Sound Selected": self.combobox_changed(self.custom_sound_combobox.itemText(index), key))
        self.custom_break_sound_combobox.currentIndexChanged.connect(
            lambda index, key="Custom Break Sound Selected": self.combobox_changed(self.custom_break_sound_combobox.itemText(index), key))

    def time_slider_changed(self, slider, label, setting_key):
        with open("config.json", "r+") as f:
            config = json.load(f)
            value = TIME_VALUES[slider.value()]
            minutes = TIME_VALUES[slider.value()]
            hours = minutes // 60
            minutes %= 60
            formatted_time = f"{hours:02d}:{minutes:02d}:00"
            label.setText(f"{value} min")
            for routine in config["routines"]:
                if routine["label"] == setting_key:
                    routine["time"] = formatted_time

            index, setting = SETTING_INDEX_MAP[setting_key]
            config["settings"][index][setting] = formatted_time
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()

            self.routine_changed.emit(True)

    def volume_slider_changed(self, slider, setting_key):
        with open("config.json", "r+") as f:
            config = json.load(f)
            value = (slider.value())
            index, setting = SETTING_INDEX_MAP[setting_key]
            config["settings"][index][setting] = f"{value}"

            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        if setting_key == "Pomodoro Sound Volume":
            slider.valueChanged.connect(self.pomodoro_sound_changed.emit)
        elif setting_key == "Break Sound Volume":
            slider.valueChanged.connect(self.break_sound_changed.emit)

    def spinbox_changed(self, spinbox):
        print(spinbox.value())  # Verify that the correct value is being received

        with open("config.json", "r+") as f:
            config = json.load(f)

            # Clear the existing routines
            config['routines'] = []

            # Add new routines based on spinbox value
            for i in range(spinbox.value()):
                config['routines'].append({"time": "00:25:00", "label": "Pomodoro"})
                config['routines'].append({"time": "00:05:00", "label": "Short Break"})

                if (i + 1) % spinbox.value() == 0:  # Add a Long Break after every 4 Pomodoros
                    config['routines'].pop()  # Remove the last Short Break
                    config['routines'].append({"time": "00:30:00", "label": "Long Break"})

            # Update the pomodoro session setting
            config['settings'][3]['pomodoroSession'] = str(spinbox.value())

            # Save the modified config back to the file
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()

    def switchbutton_changed(self, state, setting_key):
        with open("config.json", "r+") as f:
            config = json.load(f)
            index, setting = SETTING_INDEX_MAP[setting_key]
            if state == 2:
                config["settings"][index][setting] = False
                value = False
            elif state == 0:
                config["settings"][index][setting] = True
                value = True
            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
        print(f"Setting '{setting_key}' state changed to {state}")
        if setting_key == "Ticking Sound":
            self.ticking_sound_bool_changed.emit(value)
        elif setting_key == "Break Sound":
            self.break_sound_bool_changed.emit(value)
        elif setting_key == "Notification":
            self.notification_changed.emit(value)
        elif setting_key == "Dark Mode":
            self.dark_mode_changed.emit(value)

    def combobox_changed(self, text, setting_key):
        with open("config.json", "r+") as f:
            config = json.load(f)
            index_setting, setting = SETTING_INDEX_MAP[setting_key]

            if text == "None":
                path = "None"
                config["settings"][index_setting][setting] = path

            elif text == "Ticking Sound":
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\resources\sound\ticking_sound.mp3')
                config["settings"][index_setting][setting] = path
                self.timer_mediaplayer_sound_changed.emit(path)

            elif text == "LoFi":
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\resources\sound\LAKEY_INSPIRED_-Blue_Boi.mp3')
                config["settings"][index_setting][setting] = path
                self.timer_mediaplayer_sound_changed.emit(path)

            elif text == "Classic":
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)),  r'..\resources\sound\eine_kleine_nachtmusik.mp3')
                config["settings"][index_setting][setting] = path

            elif text == "Custom Music":
                option = QFileDialog.Options()
                option |= QFileDialog.ReadOnly
                path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", '/', "Audio Files (*.mp3);;All Files (*)", options=option)

                config["settings"][index_setting][setting] = path

            if setting_key == "Custom Pomodoro Sound Selected":
                self.timer_mediaplayer_sound_changed.emit(path)
            elif setting_key == "Custom Break Sound Selected":
                self.break_mediaplayer_sound_changed.emit(path)

            f.seek(0)
            json.dump(config, f, indent=4)
            f.truncate()
