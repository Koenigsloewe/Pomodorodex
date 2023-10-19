from PyQt5.QtCore import Qt, QPoint, QEasingCurve, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox


class SwitchButton(QCheckBox):
    def __init__(self,
                 width=60,
                 bg_color="#777",
                 circle_color="#DDD",
                 active_color="#5647ae",
                 animation_curve=QEasingCurve.InOutCubic):
        super().__init__()

        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._circle_position = 3

        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)

        self.toggled.connect(self.start_transition)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self):
        self.animation.stop()

        if self.isChecked():
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)

        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        rect = self.rect()

        if not self.isChecked():
            brush = QBrush(QColor(self._bg_color))
        else:
            brush = QBrush(QColor(self._active_color))

        p.setBrush(brush)
        p.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        brush.setColor(QColor(self._circle_color))
        p.setBrush(brush)
        if not self.isChecked():
            p.drawEllipse(int(self._circle_position), 3, 22, 22)
        else:
            p.drawEllipse(int(self._circle_position), 3, 22, 22)
