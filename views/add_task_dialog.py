from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QDateEdit, QDialogButtonBox
)
from PyQt6.QtCore import pyqtSignal, Qt


class AddTaskDialog(QDialog):
    """Modal dialog to collect full task details."""

    submitted = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)

        # Description
        layout.addWidget(QLabel("Description"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        layout.addWidget(self.desc_edit)

        # Deadline and priority row
        row = QHBoxLayout()
        row.addWidget(QLabel("Deadline"))
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDisplayFormat('yyyy-MM-dd')
        self.deadline_edit.setDate(self.deadline_edit.date())
        row.addWidget(self.deadline_edit)

        row.addWidget(QLabel("Priority"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Normal", "High"])
        self.priority_combo.setCurrentText("Normal")
        row.addWidget(self.priority_combo)

        layout.addLayout(row)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def on_accept(self):
        title = self.title_edit.text().strip()
        if not title:
            # do not submit empty title; keep dialog open
            return
        description = self.desc_edit.toPlainText().strip()
        deadline = self.deadline_edit.date().toString(Qt.DateFormat.ISODate)
        priority = self.priority_combo.currentText()
        payload = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority,
        }
        self.submitted.emit(payload)
        self.accept()

