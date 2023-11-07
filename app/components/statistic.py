from datetime import datetime
import sqlite3

import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, \
    QPushButton, QStackedWidget
from scipy.interpolate import make_interp_spline

BAR_COLOR = ["#5647ae", "#808080"]


class Statistic(QWidget):
    stylesheet_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        grouped_button_menubar = QWidget()
        grouped_button_menubar.setMinimumHeight(100)
        grouped_button_menubar.setMaximumHeight(100)
        self.layout.addWidget(grouped_button_menubar)

        grouped_button_menubar_layout = QHBoxLayout()
        grouped_button_menubar.setLayout(grouped_button_menubar_layout)

        grouped_button_widget = QWidget()
        grouped_button_widget.setMaximumWidth(450)
        grouped_button_menubar_layout.addWidget(grouped_button_widget)

        grouped_button_widget_layout = QHBoxLayout()
        grouped_button_widget.setLayout(grouped_button_widget_layout)

        self.day_btn = QPushButton("Show Day")
        self.day_btn.setObjectName("primary_btn")
        self.day_btn.setMinimumSize(120, 50)
        self.day_btn.setMaximumSize(120, 50)
        grouped_button_widget_layout.addWidget(self.day_btn)

        self.week_btn = QPushButton("Show Week")
        self.week_btn.setObjectName("secondary_btn")
        self.week_btn.setMinimumSize(120, 50)
        self.week_btn.setMaximumSize(120, 50)
        grouped_button_widget_layout.addWidget(self.week_btn)

        self.month_btn = QPushButton("Show Month")
        self.month_btn.setObjectName("secondary_btn")
        self.month_btn.setMinimumSize(120, 50)
        self.month_btn.setMaximumSize(120, 50)
        grouped_button_widget_layout.addWidget(self.month_btn)

        self.statistics_stacked_widget = QStackedWidget()
        self.layout.addWidget(self.statistics_stacked_widget)

        session_data = self.get_data_from_db()
        self.create_day_view(session_data)
        self.create_week_view(session_data)
        self.create_month_view(session_data)

        # conenction
        self.day_btn.clicked.connect(self.show_day)
        self.week_btn.clicked.connect(self.show_week)
        self.month_btn.clicked.connect(self.show_month)

    def show_day(self):
        self.day_btn.setObjectName("primary_btn")
        self.week_btn.setObjectName("secondary_btn")
        self.month_btn.setObjectName("secondary_btn")

        self.statistics_stacked_widget.setCurrentIndex(0)

        self.stylesheet_changed.emit()

    def show_day(self):
        self.day_btn.setObjectName("primary_btn")
        self.week_btn.setObjectName("secondary_btn")
        self.month_btn.setObjectName("secondary_btn")

        self.statistics_stacked_widget.setCurrentIndex(0)

        self.stylesheet_changed.emit(True)

    def show_week(self):
        self.day_btn.setObjectName("secondary_btn")
        self.week_btn.setObjectName("primary_btn")
        self.month_btn.setObjectName("secondary_btn")

        self.statistics_stacked_widget.setCurrentIndex(1)

        self.stylesheet_changed.emit(True)

    def show_month(self):
        self.day_btn.setObjectName("secondary_btn")
        self.week_btn.setObjectName("secondary_btn")
        self.month_btn.setObjectName("primary_btn")

        self.statistics_stacked_widget.setCurrentIndex(2)

        self.stylesheet_changed.emit(True)

    def create_day_view(self, data):
        day_stacked_widget = QStackedWidget()

        for item in data:
            chart_page = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 15)
            chart_page.setLayout(layout)

            # create a figure for the canvas
            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            # data of sql db
            date = item[0]
            pomodoro_time = item[1]
            break_time = item[2]

            # create bar chart
            ax.bar(["Focus Time", "Break Time"], [pomodoro_time, break_time], color=BAR_COLOR)
            ax.set_facecolor("#2a2929")
            figure.set_facecolor("#2a2929")

            ax.set_xlabel(f"Pomodoro Sessions").set_color("white")
            ax.set_ylabel(f"Time [min]").set_color("white")
            ax.set_title(f"Daily Tracking - {date}").set_color("white")

            for label in ax.get_xticklabels():
                label.set_color("white")

            for label in ax.get_yticklabels():
                label.set_color("white")

            for spine in ax.spines.values():
                spine.set_color("white")

            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")

            ax.grid(True, axis="y", linestyle="--", alpha=0.7, color="white")

            canvas.draw()

            layout.addWidget(canvas)
            day_stacked_widget.addWidget(chart_page)

        day_toolbar = QWidget()
        day_toolbar_layout = QHBoxLayout()
        day_toolbar_layout.setContentsMargins(0, 0, 30, 0)
        day_toolbar.setLayout(day_toolbar_layout)

        day_previous_btn = QPushButton()
        day_previous_btn.setIcon(QIcon(QPixmap(":/svg/backward-fill.svg")))
        day_previous_btn.setObjectName("secondary_btn")
        day_previous_btn.setMinimumSize(70, 50)
        day_previous_btn.setMaximumSize(70, 50)
        day_toolbar_layout.addWidget(day_previous_btn)

        day_next_btn = QPushButton()
        day_next_btn.setIcon(QIcon(QPixmap(":/svg/forward-fill.svg")))
        day_next_btn.setObjectName("secondary_btn")
        day_next_btn.setMinimumSize(70, 50)
        day_next_btn.setMaximumSize(70, 50)
        day_toolbar_layout.addWidget(day_next_btn)

        day_view_layout = QHBoxLayout()
        day_view_layout.addWidget(day_stacked_widget)
        day_view_layout.addWidget(day_toolbar)

        day_view = QWidget()
        day_view.setLayout(day_view_layout)

        self.statistics_stacked_widget.addWidget(day_view)

        # connection
        day_previous_btn.clicked.connect(lambda: self.previous_chart(day_stacked_widget))
        day_next_btn.clicked.connect(lambda: self.next_chart(day_stacked_widget))

    def create_week_view(self, data):
        week_stacked_widget = QStackedWidget()

        grouped_dates = {}
        for date_str, value1, value2 in data:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            week_number = date.isocalendar()[1]
            if week_number not in grouped_dates:
                grouped_dates[week_number] = [(date_str, value1, value2)]
            else:
                grouped_dates[week_number].append((date_str, value1, value2))

        for week, data in grouped_dates.items():
            chart_page = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            chart_page.setLayout(layout)

            dates = [entry[0] for entry in data]
            focus_time = [entry[1] for entry in data]
            break_time = [entry[2] for entry in data]

            x = np.arange(len(data))
            width = 0.35

            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            ax.bar(x - width / 2, focus_time, width, label="Focus Time", color=BAR_COLOR[0])
            ax.bar(x + width / 2, break_time, width, label="Break Time", color=BAR_COLOR[1])

            ax.set_facecolor("#2a2929")
            figure.set_facecolor("#2a2929")

            ax.set_xlabel("Date").set_color("white")
            ax.set_ylabel("Time (min)").set_color("white")
            ax.set_title(f"Focus Time and Break Time per Day (Week {week})").set_color("white")
            ax.set_xticks(x)
            ax.set_xticklabels(dates, rotation=0)
            ax.legend(loc="upper right")

            for label in ax.get_xticklabels():
                label.set_color("white")

            for label in ax.get_yticklabels():
                label.set_color("white")

            for spine in ax.spines.values():
                spine.set_color("white")

            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")

            ax.grid(True, axis="y", linestyle="--", alpha=0.7, color="white")

            canvas.draw()

            layout.addWidget(canvas)
            week_stacked_widget.addWidget(chart_page)

        week_toolbar = QWidget()
        week_toolbar_layout = QHBoxLayout()
        week_toolbar_layout.setContentsMargins(0, 0, 30, 0)
        week_toolbar.setLayout(week_toolbar_layout)

        week_previous_btn = QPushButton()
        week_previous_btn.setIcon(QIcon(QPixmap(":/svg/backward-fill.svg")))
        week_previous_btn.setObjectName("secondary_btn")
        week_previous_btn.setMinimumSize(70, 50)
        week_previous_btn.setMaximumSize(70, 50)
        week_toolbar_layout.addWidget(week_previous_btn)

        week_next_btn = QPushButton()
        week_next_btn.setIcon(QIcon(QPixmap(":/svg/forward-fill.svg")))
        week_next_btn.setObjectName("secondary_btn")
        week_next_btn.setMinimumSize(70, 50)
        week_next_btn.setMaximumSize(70, 50)
        week_toolbar_layout.addWidget(week_next_btn)

        week_view_layout = QHBoxLayout()
        week_view_layout.addWidget(week_stacked_widget)
        week_view_layout.addWidget(week_toolbar)

        week_view = QWidget()
        week_view.setLayout(week_view_layout)

        self.statistics_stacked_widget.addWidget(week_view)

        # connection
        week_previous_btn.clicked.connect(lambda: self.previous_chart(week_stacked_widget))
        week_next_btn.clicked.connect(lambda: self.next_chart(week_stacked_widget))

    def create_month_view(self, data):
        month_stacked_widget = QStackedWidget()

        grouped_by_month = {}
        for entry in data:
            date = entry[0]
            month = date.split("-")[1]
            if month not in grouped_by_month:
                grouped_by_month[month] = []
            grouped_by_month[month].append(entry)

        for month, data in grouped_by_month.items():
            chart_page = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            chart_page.setLayout(layout)

            dates = [entry[0] for entry in data]
            focus_time = [entry[1] for entry in data]
            break_time = [entry[2] for entry in data]

            x_fine = np.linspace(0, len(dates) - 1, 300)
            focus_time_smooth = make_interp_spline(range(len(dates)), focus_time, k=3)(x_fine)
            break_time_smooth = make_interp_spline(range(len(dates)), break_time, k=3)(x_fine)

            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)

            ax.fill_between(x_fine, 0, focus_time_smooth, color=BAR_COLOR[0])
            ax.fill_between(x_fine, 0, break_time_smooth, color=BAR_COLOR[1])

            ax.plot(x_fine, focus_time_smooth, label="Focus Time", color=BAR_COLOR[0])
            ax.plot(x_fine, break_time_smooth, label="Break Time", color=BAR_COLOR[1])

            ax.set_facecolor("#2a2929")
            figure.set_facecolor("#2a2929")

            ax.set_xlabel("Date").set_color("white")
            ax.set_ylabel("Time (min)").set_color("white")
            ax.set_title(f"Focus Time and Break Time per Day (Month {month})").set_color("white")
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels([date.split("-")[2] for date in dates], rotation=45)
            ax.legend(loc="upper right")

            for label in ax.get_xticklabels():
                label.set_color("white")

            for label in ax.get_yticklabels():
                label.set_color("white")

            for spine in ax.spines.values():
                spine.set_color("white")

            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")

            ax.grid(True, linestyle="--", alpha=0.7)

            canvas.draw()
            layout.addWidget(canvas)
            month_stacked_widget.addWidget(chart_page)

        month_toolbar = QWidget()
        month_toolbar_layout = QHBoxLayout()
        month_toolbar_layout.setContentsMargins(0, 0, 30, 0)
        month_toolbar.setLayout(month_toolbar_layout)

        month_previous_btn = QPushButton()
        month_previous_btn.setIcon(QIcon(QPixmap(":/svg/backward-fill.svg")))
        month_previous_btn.setObjectName("secondary_btn")
        month_previous_btn.setMinimumSize(70, 50)
        month_previous_btn.setMaximumSize(70, 50)
        month_toolbar_layout.addWidget(month_previous_btn)

        month_next_btn = QPushButton()
        month_next_btn.setIcon(QIcon(QPixmap(":/svg/forward-fill.svg")))
        month_next_btn.setObjectName("secondary_btn")
        month_next_btn.setMinimumSize(70, 50)
        month_next_btn.setMaximumSize(70, 50)
        month_toolbar_layout.addWidget(month_next_btn)

        month_view_layout = QHBoxLayout()
        month_view_layout.addWidget(month_stacked_widget)
        month_view_layout.addWidget(month_toolbar)

        month_view = QWidget()
        month_view.setLayout(month_view_layout)

        self.statistics_stacked_widget.addWidget(month_view)

        month_previous_btn.clicked.connect(lambda: self.previous_chart(month_stacked_widget))
        month_next_btn.clicked.connect(lambda: self.next_chart(month_stacked_widget))

    def get_data_from_db(self):
        try:
            conn = sqlite3.connect("app/components/pomodorodex.db")
            cursor = conn.cursor()
            cursor.execute("SELECT date, focus_time, break_time FROM pomodoro_sessions")
            data = cursor.fetchall()
            return data

        except sqlite3.Error as e:
            print("An error occurred:", e)
        finally:
            conn.close()

    def previous_chart(self, stackedwidget):
        current_index = stackedwidget.currentIndex()
        if current_index > 0:
            stackedwidget.setCurrentIndex(current_index - 1)

    def next_chart(self, stackedwidget):
        current_index = stackedwidget.currentIndex()
        if current_index < stackedwidget.count() - 1:
            stackedwidget.setCurrentIndex(current_index + 1)