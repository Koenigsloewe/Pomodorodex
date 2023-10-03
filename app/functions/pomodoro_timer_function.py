from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

TIME = 60 * 25


class TimerApp():
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = QTime(0, 25, 0)

    def start_timer(self):
        self.timer.start(1000)

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        print(self.time_left.toString(Qt.TextDate))

        if self.time_left == QTime(0, 0):
            self.timer.stop()
            print("time is up")
