from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton


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

        # task widget
        task_widget = QWidget()
        task_widget.setObjectName("")
        task_management_widget_layout.addWidget(task_widget)

        task_widget_layout = QVBoxLayout()
        task_widget_layout.setContentsMargins(0, 0, 0, 0)
        task_widget.setLayout(task_widget_layout)

        # task input form group
        task_input_form_group = QWidget()
        task_input_form_group.setMinimumHeight(100)
        task_input_form_group.setMaximumHeight(100)
        task_management_widget_layout.addWidget(task_input_form_group)

        task_input_form_group_layout = QHBoxLayout()
        task_input_form_group_layout.setContentsMargins(0, 0, 0, 0)
        task_input_form_group_layout.setSpacing(30)
        task_input_form_group.setLayout(task_input_form_group_layout)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Define Your Task")
        line_edit.setObjectName("line_edit")
        line_edit.setMinimumHeight(50)
        line_edit.setMaximumHeight(50)
        task_input_form_group_layout.addWidget(line_edit)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary_btn")
        save_btn.setMinimumSize(120, 50)
        save_btn.setMaximumSize(120, 50)
        task_input_form_group_layout.addWidget(save_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondary_btn")
        clear_btn.setMinimumSize(120, 50)
        clear_btn.setMaximumSize(120, 50)
        task_input_form_group_layout.addWidget(clear_btn)



