from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QDateEdit, QComboBox, QFormLayout, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QDate
from datetime import datetime
import traceback


class TaskDetailDialog(QDialog):
    """Dialog to display and edit task details in a single dialog.

    - Starts in view mode (labels, read-only text).
    - Clicking Edit switches to edit mode (inline QLineEdit/QTextEdit/QDateEdit/QComboBox).
    - Save emits `edit_submitted(payload)` and closes. Cancel reverts to view.
    """

    edit_submitted = pyqtSignal(object)  # payload dict with edited fields (controller expects 'index')

    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.setObjectName("detailDialog")
        self.task_data = task_data or {}
        self._in_edit = False
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        # Title
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setWordWrap(True)
        self.title_edit = QLineEdit()
        self.title_edit.setObjectName("titleEdit")
        self.title_edit.hide()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_edit)

        # Meta details section
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        # Priority
        self.priority_icon_label = QLabel()
        self.priority_icon_label.setObjectName("priorityIconLabel")
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Normal", "High"])
        self.priority_combo.hide()
        form_layout.addRow("Priority:", self.priority_icon_label)
        form_layout.addRow(self.priority_combo)


        # Deadline
        self.deadline_icon_label = QLabel()
        self.deadline_icon_label.setObjectName("deadlineIconLabel")
        self.deadline_edit = QDateEdit(calendarPopup=True)
        self.deadline_edit.setDisplayFormat('yyyy-MM-dd')
        self.deadline_edit.hide()
        form_layout.addRow("Deadline:", self.deadline_icon_label)
        form_layout.addRow(self.deadline_edit)

        self.layout.addLayout(form_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(line)

        # Description
        self.desc_label = QLabel("Description")
        self.desc_label.setObjectName("headerLabel")
        self.desc_edit = QTextEdit()
        self.desc_edit.setObjectName("descriptionText")
        self.desc_edit.setReadOnly(True)
        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_edit)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setObjectName("editButton")
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("saveButton")
        self.save_btn.hide()
        self.cancel_btn = QPushButton("Close")
        self.cancel_btn.setObjectName("cancelButton")
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.save_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.button_layout)

        # Connect signals
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.save_btn.clicked.connect(self.save_and_close)
        self.cancel_btn.clicked.connect(self.cancel_and_close)

        self.populate_data()

    def populate_data(self):
        title = self.task_data.get('title', 'No Title')
        description = self.task_data.get('description', 'No description provided.')
        priority = self.task_data.get('priority', 'Normal')
        deadline_str = self.task_data.get('deadline')
        completed = self.task_data.get('completed', False)

        self.title_label.setText(title)
        self.title_edit.setText(title)
        self.desc_edit.setPlainText(description)

        # Priority
        priority_map = {"High": "🔼 High", "Normal": "⏺️ Normal", "Low": "🔽 Low"}
        self.priority_icon_label.setText(priority_map.get(priority, "⏺️ Normal"))
        self.priority_combo.setCurrentText(priority)

        # Deadline
        if deadline_str:
            try:
                deadline_dt = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                self.deadline_icon_label.setText(f"🗓️ {deadline_dt.strftime('%A, %B %d, %Y')}")
                self.deadline_edit.setDate(QDate(deadline_dt.year, deadline_dt.month, deadline_dt.day))
            except (ValueError, TypeError):
                self.deadline_icon_label.setText("🗓️ Not set")
                self.deadline_edit.setDate(QDate.currentDate())
        else:
            self.deadline_icon_label.setText("🗓️ Not set")
            self.deadline_edit.setDate(QDate.currentDate())

        self.edit_btn.setDisabled(completed)
        if completed:
            self.edit_btn.setToolTip("Completed tasks cannot be edited.")

    def toggle_edit_mode(self):
        self._in_edit = not self._in_edit

        # Toggle visibility of view/edit widgets
        self.title_label.setVisible(not self._in_edit)
        self.title_edit.setVisible(self._in_edit)
        self.priority_icon_label.setVisible(not self._in_edit)
        self.priority_combo.setVisible(self._in_edit)
        self.deadline_icon_label.setVisible(not self._in_edit)
        self.deadline_edit.setVisible(self._in_edit)

        self.desc_edit.setReadOnly(not self._in_edit)

        # Toggle buttons
        self.edit_btn.setVisible(not self._in_edit)
        self.save_btn.setVisible(self._in_edit)
        self.cancel_btn.setText("Cancel" if self._in_edit else "Close")

    def save_and_close(self):
        payload = {
            'title': self.title_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'priority': self.priority_combo.currentText(),
            'deadline': self.deadline_edit.date().toString(Qt.DateFormat.ISODate),
            'index': self.task_data.get('index')
        }
        self.edit_submitted.emit(payload)
        self.accept()

    def cancel_and_close(self):
        if self._in_edit:
            self.toggle_edit_mode() # Revert to view mode
            self.populate_data() # Reset fields to original data
        else:
            self.reject()
