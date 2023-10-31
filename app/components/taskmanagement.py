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
        self.load_tasks_from_config()
        self.save_tasks_for_config()

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

    def edit_task(self, task_checkbox):
        current_text = self.text_line_edit.text()
        self.text_line_edit.setReadOnly(False)
        self.text_line_edit.setCursorPosition(len(current_text))
        self.text_line_edit.setFocus()

        self.task_widget_layout_.removeWidget(self.edit_btn)
        self.edit_btn.setParent(None)

        self.task_widget_layout_.removeWidget(self.delete_btn)
        self.delete_btn.setParent(None)

        self.task_widget_layout_.addWidget(self.save_task_btn)
        self.task_widget_layout_.addWidget(self.cancel_btn)

        self.save_task_btn.clicked.connect(lambda: self.save())
        self.cancel_btn.clicked.connect(lambda: self.cancel(current_text))
        self.text_line_edit.returnPressed(lambda: self.save())

    def delete_task(self, task_widget):
        for task_element in self.tasks:
            if task_element[3] == task_widget:
                self.tasks.remove(task_element)
                break

        task_widget.setParent(None)

    def cancel(self, current_text):
        self.text_line_edit.setText(current_text)
        self.text_line_edit.setReadOnly(True)
        self.change_btns()

    def save(self):
        self.text_line_edit.setReadOnly(True)
        self.change_btns()

    def change_btns(self):
        self.task_widget_layout_.removeWidget(self.save_task_btn)
        self.save_task_btn.setParent(None)

        self.task_widget_layout_.removeWidget(self.cancel_btn)
        self.cancel_btn.setParent(None)

        self.task_widget_layout_.addWidget(self.edit_btn)
        self.task_widget_layout_.addWidget(self.delete_btn)

    def toggle_cross(self, task_widget):
        checkbox = task_widget.findChild(QCheckBox)
        line_edit = task_widget.findChild(QLineEdit)
        edit_btn = task_widget.findChild(QPushButton)

        if checkbox and line_edit:
            if checkbox.isChecked():
                line_edit.setObjectName("task_finished")
                edit_btn.setObjectName("secondary_btn")
                self.load_stylesheet()
            else:
                line_edit.setObjectName("text_line_edit")
                edit_btn.setObjectName("primary_btn")
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

    def load_tasks_from_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            tasks_list = [(item["task"], item["checked"]) for item in config["tasks"]]
            for task_text, task_checked in tasks_list:
                self.create_task_widget(task_text, task_checked)

    def save_tasks_for_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)

        task_list = []
        for task_checkbox, edit_btn, delete_btn, task_widget in self.tasks:
            task_text = task_widget.findChild(QLineEdit).text()
            task_checked = task_checkbox.isChecked()
            task_list.append({"task": task_text, "checked": task_checked})

        config["tasks"] = task_list

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    def create_task_widget(self, task_text, task_checked=False):
        # task widget
        task_widget = QWidget()
        task_widget.setMinimumSize(150, 50)
        task_widget.setMinimumSize(150, 50)

        # task widget layout
        self.task_widget_layout_ = QHBoxLayout()
        self.task_widget_layout_.setContentsMargins(0, 0, 0, 0)
        self.task_widget_layout_.setSpacing(15)
        task_widget.setLayout(self.task_widget_layout_)

        # task checkbox
        self.task_checkbox = QCheckBox()
        self.task_widget_layout_.addWidget(self.task_checkbox)

        # text task line edit
        self.text_line_edit = QLineEdit(task_text)
        self.text_line_edit.setObjectName("text_line_edit")
        self.text_line_edit.setReadOnly(True)
        self.task_widget_layout_.addWidget(self.text_line_edit)

        # btns
        self.edit_btn = QPushButton("")
        self.edit_btn.setIcon(QIcon(QPixmap(":/svg/edit.svg")))
        self.edit_btn.setIconSize(QSize(40, 40))
        self.edit_btn.setObjectName("primary_btn")
        self.edit_btn.setMinimumSize(70, 50)
        self.edit_btn.setMaximumSize(70, 50)
        self.task_widget_layout_.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("")
        self.delete_btn.setIcon(QIcon(QPixmap(":/svg/trash-fill.svg")))
        self.delete_btn.setIconSize(QSize(40, 40))
        self.delete_btn.setObjectName("primary_btn")
        self.delete_btn.setMinimumSize(70, 50)
        self.delete_btn.setMaximumSize(70, 50)
        self.task_widget_layout_.addWidget(self.delete_btn)

        self.save_task_btn = QPushButton("")
        self.save_task_btn.setIcon(QIcon(QPixmap(":/svg/save.svg")))
        self.save_task_btn.setIconSize(QSize(40, 40))
        self.save_task_btn.setObjectName("primary_btn")
        self.save_task_btn.setMinimumSize(70, 50)
        self.save_task_btn.setMaximumSize(70, 50)

        self.cancel_btn = QPushButton("")
        self.cancel_btn.setIcon(QIcon(QPixmap(":/svg/cancel.svg")))
        self.cancel_btn.setIconSize(QSize(40, 40))
        self.cancel_btn.setObjectName("secondary_btn")
        self.cancel_btn.setMinimumSize(70, 50)
        self.cancel_btn.setMaximumSize(70, 50)

        # checkbox checked status
        if task_checked:
            self.task_checkbox.setChecked(True)
            self.text_line_edit.setObjectName("task_finished")
            self.edit_btn.setObjectName("secondary_btn")
            self.load_stylesheet()

        # add to list...
        self.tasks.append((self.task_checkbox, self.edit_btn, self.delete_btn, task_widget))
        # add to layout
        self.task_widget_layout.addWidget(task_widget)

        # connections
        self.task_checkbox.toggled.connect(lambda: self.toggle_cross(task_widget))
        self.edit_btn.clicked.connect(lambda: self.edit_task(self.task_checkbox))
        self.delete_btn.clicked.connect(lambda: self.delete_task(task_widget))
