from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, \
    QPushButton, QCheckBox, QScrollArea, QInputDialog


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

        # conncections
        self.save_btn.clicked.connect(self.save_task)
        self.clear_btn.clicked.connect(self.clear_task)


    def save_task(self):
        task_text = self.line_edit.text()

        if task_text:
            # task widget
            task_widget = QWidget()
            task_widget.setMinimumSize(150, 50)
            task_widget.setMinimumSize(150, 50)

            # task widget layout
            task_widget_layout = QHBoxLayout()
            task_widget_layout.setContentsMargins(0, 0, 0, 0)
            task_widget_layout.setSpacing(30)
            task_widget.setLayout(task_widget_layout)

            # task checkbox
            task_checkbox = QCheckBox(task_text)
            task_widget_layout.addWidget(task_checkbox)

            # btns
            self.edit_btn = QPushButton("Edit")
            self.edit_btn.setObjectName("primary_btn")
            self.edit_btn.setMinimumSize(120, 50)
            self.edit_btn.setMaximumSize(120, 50)
            task_widget_layout.addWidget(self.edit_btn)

            self.delete_btn = QPushButton("Delete")
            self.delete_btn.setObjectName("primary_btn")
            self.delete_btn.setMinimumSize(120, 50)
            self.delete_btn.setMaximumSize(120, 50)
            task_widget_layout.addWidget(self.delete_btn)

            # add to list...
            self.tasks.append((task_checkbox, self.edit_btn, self.delete_btn, task_widget))
            print(self.tasks)
            # add to layout
            self.task_widget_layout.addWidget(task_widget)

            # connections
            self.edit_btn.clicked.connect(lambda: self.edit_task(task_checkbox))
            self.delete_btn.clicked.connect(lambda: self.delete_task(task_widget))

            self.clear_task()

    def clear_task(self):
        self.line_edit.clear()

    def edit_task(self, task_checkbox):
        new_text, ok = QInputDialog.getText(self, 'Edit Task', 'New Task Description:', QLineEdit.Normal,
                                            task_checkbox.text())
        if ok and new_text:
            task_checkbox.setText(new_text)

    def delete_task(self, task_widget):
        for task_element in self.tasks:
            if task_element[3] == task_widget:
                self.tasks.remove(task_element)
                break

        task_widget.setParent(None)
