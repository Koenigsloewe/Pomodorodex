import sqlite3

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton, QCheckBox, QScrollArea, QInputDialog
import json

try:
    from app.resources import resources
except ModuleNotFoundError:
    from app.resources import resources


class TaskManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        task_management_widget = QWidget()
        self.layout.addWidget(task_management_widget)

        task_management_widget_layout = QVBoxLayout()
        task_management_widget_layout.setContentsMargins(30, 30, 30, 0)
        task_management_widget.setLayout(task_management_widget_layout)

        # scroll area for task widget
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll_area")
        task_management_widget_layout.addWidget(scroll_area)

        # task widget
        task_widget = QWidget()
        task_widget.setObjectName("task_widget")
        scroll_area.setWidget(task_widget)
        scroll_area.setWidgetResizable(True)

        self.task_widget_layout = QVBoxLayout()
        self.task_widget_layout.setContentsMargins(30, 30, 30, 30)
        self.task_widget_layout.setAlignment(Qt.AlignTop)
        self.task_widget_layout.setSpacing(30)
        task_widget.setLayout(self.task_widget_layout)

        # task input form group
        task_input_form_group = QWidget()
        task_input_form_group.setMinimumHeight(100)
        task_input_form_group.setMaximumHeight(100)
        task_management_widget_layout.addWidget(task_input_form_group)

        task_input_form_group_layout = QHBoxLayout()
        task_input_form_group_layout.setContentsMargins(0, 0, 0, 0)
        task_input_form_group_layout.setSpacing(30)
        task_input_form_group.setLayout(task_input_form_group_layout)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Define Your Task")
        self.line_edit.setObjectName("line_edit")
        self.line_edit.setMinimumHeight(50)
        self.line_edit.setMaximumHeight(50)
        task_input_form_group_layout.addWidget(self.line_edit)

        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("primary_btn")
        self.save_btn.setMinimumSize(120, 50)
        self.save_btn.setMaximumSize(120, 50)
        task_input_form_group_layout.addWidget(self.save_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondary_btn")
        self.clear_btn.setMinimumSize(120, 50)
        self.clear_btn.setMaximumSize(120, 50)
        task_input_form_group_layout.addWidget(self.clear_btn)

        # task lists
        self.tasks = []
        self.load_tasks_from_db()

        # conncections
        self.line_edit.returnPressed.connect(self.save_task)
        self.save_btn.clicked.connect(self.save_task)
        self.clear_btn.clicked.connect(self.clear_task)

    def save_task(self):
        task_text = self.line_edit.text()

        if task_text:
            self.create_task_widget(task_text)

            self.clear_task()

    def clear_task(self):
        self.line_edit.clear()

    def edit_task(self, text_line_edit, task_widget_layout, edit_btn, delete_btn, save_task_btn, cancel_btn):
        current_text = text_line_edit.text()
        text_line_edit.setReadOnly(False)
        text_line_edit.setCursorPosition(len(current_text))
        text_line_edit.setFocus()

        task_widget_layout.removeWidget(edit_btn)
        edit_btn.setParent(None)

        task_widget_layout.removeWidget(delete_btn)
        delete_btn.setParent(None)

        task_widget_layout.addWidget(save_task_btn)
        task_widget_layout.addWidget(cancel_btn)

    def delete_task(self, task_widget):
        for task_element in self.tasks:
            if task_element[3] == task_widget:
                self.tasks.remove(task_element)
                break

        task_widget.setParent(None)

    def cancel(self, text_line_edit, current_text, task_widget_layout, save_task_btn, cancel_btn, edit_btn, delete_btn):
        text_line_edit.setText(current_text)
        text_line_edit.setReadOnly(True)
        self.change_btns(task_widget_layout, save_task_btn, cancel_btn, edit_btn, delete_btn)

    def save(self, text_line_edit, task_widget_layout, save_task_btn, cancel_btn, edit_btn, delete_btn):
        text_line_edit.setReadOnly(True)
        self.change_btns(task_widget_layout, save_task_btn, cancel_btn, edit_btn, delete_btn)

    def change_btns(self, task_widget_layout, save_task_btn, cancel_btn, edit_btn, delete_btn):
        task_widget_layout.removeWidget(save_task_btn)
        save_task_btn.setParent(None)

        task_widget_layout.removeWidget(cancel_btn)
        cancel_btn.setParent(None)

        task_widget_layout.addWidget(edit_btn)
        task_widget_layout.addWidget(delete_btn)

    def toggle_cross(self, task_widget, edit_btn, delete_btn):
        checkbox = task_widget.findChild(QCheckBox)
        line_edit = task_widget.findChild(QLineEdit)

        if checkbox and line_edit:
            if checkbox.isChecked():
                line_edit.setObjectName("task_finished")
                edit_btn.setObjectName("secondary_btn")
                delete_btn.setObjectName("secondary_btn")
                self.load_stylesheet()
            else:
                line_edit.setObjectName("text_line_edit")
                edit_btn.setObjectName("primary_btn")
                delete_btn.setObjectName("primary_btn")
                self.load_stylesheet()

    def load_stylesheet(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)
            self.dark_mode_bool = self.config["settings"][10]["darkMode"]
        if self.dark_mode_bool:
            with open("app/resources/styles.qss", "r") as qss_file:
                style_sheet = qss_file.read()
                self.setStyleSheet(style_sheet)
        elif not self.dark_mode_bool:
            with open("app/resources/lightmode.qss", "r") as qss_file:
                style_sheet = qss_file.read()
                self.setStyleSheet(style_sheet)

    def load_tasks_from_db(self):
        try:
            conn = sqlite3.connect("app/components/pomodorodex.db")
            cursor = conn.cursor()
            cursor.execute("SELECT task, status FROM task_list")
            tasks_list = cursor.fetchall()
            for task_text, task_checked in tasks_list:
                if task_checked == "True":
                    task_checked = True
                else:
                    task_checked = False
                self.create_task_widget(task_text, task_checked)

        except sqlite3.Error as e:
            print("An error occurred:", e)
        finally:
            conn.close()

    def save_tasks_for_db(self):
        try:
            conn = sqlite3.connect("app/components/pomodorodex.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM task_list")
            conn.commit()

            for task_checkbox, edit_btn, delete_btn, task_widget, _ in self.tasks:
                task_text = task_widget.findChild(QLineEdit).text()
                task_checked = 'True' if task_checkbox.isChecked() else 'False'
                cursor.execute("INSERT INTO task_list (task, status) VALUES (?, ?)", (task_text, task_checked))
            conn.commit()

        except sqlite3.Error as e:
            print("An error occurred:", e)
        finally:
            conn.close()

    def create_task_widget(self, task_text, task_checked=False):
        # task widget
        task_widget = QWidget()
        task_widget.setMinimumSize(150, 50)
        task_widget.setMinimumSize(150, 50)

        # task widget layout
        task_widget_layout = QHBoxLayout()
        task_widget_layout.setContentsMargins(0, 0, 0, 0)
        task_widget_layout.setSpacing(15)
        task_widget.setLayout(task_widget_layout)

        # task checkbox
        task_checkbox = QCheckBox()
        task_widget_layout.addWidget(task_checkbox)

        # text task line edit
        text_line_edit = QLineEdit(task_text)
        text_line_edit.setObjectName("text_line_edit")
        text_line_edit.setReadOnly(True)
        task_widget_layout.addWidget(text_line_edit)

        # btns
        edit_btn = QPushButton("")
        edit_btn.setIcon(QIcon(QPixmap(":/svg/edit.svg")))
        edit_btn.setIconSize(QSize(40, 40))
        edit_btn.setObjectName("primary_btn")
        edit_btn.setMinimumSize(70, 50)
        edit_btn.setMaximumSize(70, 50)
        task_widget_layout.addWidget(edit_btn)

        delete_btn = QPushButton("")
        delete_btn.setIcon(QIcon(QPixmap(":/svg/trash-fill.svg")))
        delete_btn.setIconSize(QSize(40, 40))
        delete_btn.setObjectName("primary_btn")
        delete_btn.setMinimumSize(70, 50)
        delete_btn.setMaximumSize(70, 50)
        task_widget_layout.addWidget(delete_btn)

        save_task_btn = QPushButton("")
        save_task_btn.setIcon(QIcon(QPixmap(":/svg/save.svg")))
        save_task_btn.setIconSize(QSize(40, 40))
        save_task_btn.setObjectName("primary_btn")
        save_task_btn.setMinimumSize(70, 50)
        save_task_btn.setMaximumSize(70, 50)

        cancel_btn = QPushButton("")
        cancel_btn.setIcon(QIcon(QPixmap(":/svg/cancel.svg")))
        cancel_btn.setIconSize(QSize(40, 40))
        cancel_btn.setObjectName("secondary_btn")
        cancel_btn.setMinimumSize(70, 50)
        cancel_btn.setMaximumSize(70, 50)

        # checkbox checked status
        if task_checked:
            task_checkbox.setChecked(True)
            text_line_edit.setObjectName("task_finished")
            edit_btn.setObjectName("secondary_btn")
            delete_btn.setObjectName("secondary_btn")
            self.load_stylesheet()
        else:
            task_checkbox.setChecked(False)

        # add to list...
        self.tasks.append((task_checkbox, edit_btn, delete_btn, task_widget, text_line_edit, ))
        # add to layout
        # add to layout
        self.task_widget_layout.addWidget(task_widget)

        # connections
        task_checkbox.toggled.connect(lambda: self.toggle_cross(task_widget, edit_btn, delete_btn))
        edit_btn.clicked.connect(lambda: self.edit_task(text_line_edit, task_widget_layout, edit_btn,
                                                        delete_btn, save_task_btn, cancel_btn))
        delete_btn.clicked.connect(lambda: self.delete_task(task_widget))
        save_task_btn.clicked.connect(lambda: self.save(text_line_edit, task_widget_layout, save_task_btn,
                                                        cancel_btn, edit_btn, delete_btn))
        cancel_btn.clicked.connect(lambda: self.cancel(text_line_edit, text_line_edit.text(), task_widget_layout,
                                                       save_task_btn, cancel_btn, edit_btn, delete_btn))
