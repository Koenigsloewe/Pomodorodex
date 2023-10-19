import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QPushButton, QScrollArea, QSlider, QSpinBox, QComboBox, QSizePolicy, QTextBrowser, QFrame

try:
    from custom_widgets import SwitchButton
except ModuleNotFoundError:
    from .custom_widgets import SwitchButton

TIME_VALUES = [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 45, 60]


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        with open("config.json", "r") as f:
            config = json.load(f)
        pomodoro_duration_int = int(config["settings"][0]["pomodoroDuration"].split(":")[1])
        short_break_duration_int = int(config["settings"][1]["shortBreakDuration"].split(":")[1])
        long_break_duration_int = int(config["settings"][2]["longBreakDuration"].split(":")[1])
        pomodoro_session_int = int(config["settings"][3]["pomodoroSession"])
        ticking_sound_bool = config["settings"][4]["tickingSound"]
        custom_pomodoro_sound_selected_string = config["settings"][5]["customPomodoroSoundSelected"]
        pomodoro_sound_volume = int(config["settings"][6]["PomodoroSoundVolume"])
        break_sound_bool = config["settings"][7]["breakSound"]
        custom_break_sound_selected_string = config["settings"][8]["customBreakSoundSelected"]
        break_sound_volume = int(config["settings"][9]["BreakSoundVolume"])
        dark_mode_bool = config["settings"][10]["darkMode"]
        notification_bool = config["settings"][11]["notification"]

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
        self.ticking_sound_switch_btn.setChecked(ticking_sound_bool)
        sound_settings_widget_layout.addWidget(self.ticking_sound_switch_btn, 1, 1)
        sound_settings_widget_layout.setAlignment(self.ticking_sound_switch_btn, Qt.AlignRight | Qt.AlignVCenter)

        custom_pomodoro_sound_label = QLabel("Custom Pomodoro Sound")
        sound_settings_widget_layout.addWidget(custom_pomodoro_sound_label, 2, 0)

        self.custom_sound_combobox = QComboBox()
        self.custom_sound_combobox.setMinimumHeight(50)
        self.custom_sound_combobox.setMaximumHeight(50)
        self.custom_sound_combobox.addItem("None")
        self.custom_sound_combobox.addItem("Ticking Sound")
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
        sound_settings_widget_layout.addWidget(self.volume_slider, 5, 0, 1, 2)

        break_volume_label = QLabel("Break Sound")
        sound_settings_widget_layout.addWidget(break_volume_label, 6, 0)

        self.break_sound_switch_btn = SwitchButton()
        self.break_sound_switch_btn.setChecked(break_sound_bool)
        sound_settings_widget_layout.addWidget(self.break_sound_switch_btn, 6, 1)
        sound_settings_widget_layout.setAlignment(self.break_sound_switch_btn, Qt.AlignRight | Qt.AlignVCenter)

        break_volume_label = QLabel("Custom Break Sound")
        sound_settings_widget_layout.addWidget(break_volume_label, 7, 0)

        self.custom_break_sound_combobox = QComboBox()
        self.custom_break_sound_combobox.setMinimumHeight(50)
        self.custom_break_sound_combobox.setMaximumHeight(50)
        self.custom_break_sound_combobox.addItem("None")
        self.custom_break_sound_combobox.addItem("LoFi Music")
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
        self.dark_mode_switch_btn.setChecked(dark_mode_bool)
        desktop_settings_widget_layout.addWidget(self.dark_mode_switch_btn, 1, 1)

        notification_label = QLabel("Notification")
        desktop_settings_widget_layout.addWidget(notification_label, 2, 0)

        self.notification_switch_btn = SwitchButton()
        self.notification_switch_btn.setChecked(notification_bool)
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
        version = "alpha"
        text = f"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed volutpat risus non tellus faucibus condimentum. Aliquam sit amet pretium risus, ut vehicula erat. Aliquam pulvinar neque sollicitudin suscipit feugiat. Aenean suscipit quam a dignissim efficitur. Integer id lacus vitae diam mollis mattis vitae sit amet lacus. Fusce rutrum, metus eu condimentum pharetra, est eros porta nisl, vel feugiat nibh ex id sem. Donec condimentum suscipit urna at tempor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec dignissim enim sit amet vestibulum lacinia. Etiam dui erat, tristique sit amet laoreet eget, fermentum in nisl. Donec sollicitudin fringilla neque nec molestie.\n \n by {author}, Version: {version}"""

        about_browser = QLabel(text)
        about_browser.setObjectName("about")
        about_browser.setWordWrap(True)
        about_settings_widget_layout.addWidget(about_browser)

        self.pomodoro_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.pomodoro_duration_slider, self.pomodoro_duration_display_label))
        self.short_break_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.short_break_duration_slider, self.short_break_duration_display_label))
        self.long_break_duration_slider.valueChanged.connect(
            lambda: self.time_slider_changed(self.long_break_duration_slider, self.long_break_duration_display_label))
        self.volume_slider.valueChanged.connect(
            lambda: self.volume_slider_changed(self.volume_slider))
        self.break_volume_slider.valueChanged.connect(
            lambda: self.volume_slider_changed(self.break_volume_slider))

        self.pomodoro_sessions_before_long_break_spinbox.valueChanged.connect(
            lambda: self.spinbox_changed(self.pomodoro_sessions_before_long_break_spinbox))

        self.ticking_sound_switch_btn.stateChanged.connect(self.switchbutton_changed)
        self.break_sound_switch_btn.stateChanged.connect(self.switchbutton_changed)
        self.dark_mode_switch_btn.stateChanged.connect(self.switchbutton_changed)
        self.notification_switch_btn.stateChanged.connect(self.switchbutton_changed)

        self.custom_sound_combobox.currentIndexChanged.connect(self.combobox_changed)
        self.custom_break_sound_combobox.currentIndexChanged.connect(self.combobox_changed)

    def time_slider_changed(self, slider, label):
        value = TIME_VALUES[slider.value()]
        label.setText(f"{value} min")

    def volume_slider_changed(self, slider):
        print(slider.value())

    def spinbox_changed(self, spinbox):
        print(spinbox.value())

    def switchbutton_changed(self, state):
        print(state)

    def combobox_changed(self):
        sender = self.sender()
        selected_item = sender.currentText()
        print(f"{selected_item}")

    def rewrite_json(self):
        with open("self.config.json", "r") as f:
            config = json.load(f)