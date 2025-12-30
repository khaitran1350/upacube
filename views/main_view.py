"""
Main View - Task manager UI
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QTextEdit, QListWidgetItem
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class MainView(QMainWindow):
    """
    Main application window (View).
    Contains UI elements and emits signals for user actions.
    """

    # Signals for user actions
    add_task_requested = pyqtSignal(str)   # payload: title
    toggle_task_requested = pyqtSignal(int)  # payload: index
    remove_task_requested = pyqtSignal(int)  # payload: index
    process_requested = pyqtSignal()
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._suppress_item_change = False
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Task Manager - PyQt MVC")
        self.setGeometry(100, 100, 600, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("Task Manager")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title_label)

        # Input row
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter new task title...")
        self.add_button = QPushButton("Add Task")
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        # Tasks list
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)
        # listen for checkbox changes (user toggles)
        self.list_widget.itemChanged.connect(self._on_item_changed)

        # Buttons row
        button_layout = QHBoxLayout()
        self.process_button = QPushButton("Process")
        self.toggle_button = QPushButton("Toggle Done")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear All")
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        # Status area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(120)
        main_layout.addWidget(self.status_text)

        # Connect UI actions
        self.add_button.clicked.connect(self._on_add_clicked)
        self.input_field.returnPressed.connect(self._on_add_clicked)
        # Use lambdas to avoid passing the clicked(bool) argument into signal.emit
        self.process_button.clicked.connect(lambda checked=False: self.process_requested.emit())
        # toggle/remove call internal handlers which accept optional checked param
        self.toggle_button.clicked.connect(self._on_toggle_clicked)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        self.clear_button.clicked.connect(lambda checked=False: self.clear_requested.emit())

        # Apply the preferred theme
        self.apply_light_theme()

    # --- UI event handlers -------------------------------------------
    def _on_add_clicked(self, checked=False):
        title = self.input_field.text()
        import logging
        logging.getLogger(__name__).info('ui: add clicked')
        if title.strip():
            self.add_task_requested.emit(title.strip())
            self.input_field.clear()

    def _on_toggle_clicked(self, checked=False):
        import logging
        logging.getLogger(__name__).info('ui: toggle clicked')
        index = self.current_selected_index()
        if index is not None:
            self.toggle_task_requested.emit(index)

    def _on_remove_clicked(self, checked=False):
        import logging
        logging.getLogger(__name__).info('ui: remove clicked')
        index = self.current_selected_index()
        if index is not None:
            self.remove_task_requested.emit(index)

    def _on_item_changed(self, item: QListWidgetItem):
        """Handle checkbox toggles from the user and emit toggle signal.

        This method ignores programmatic changes when `_suppress_item_change` is True.
        """
        if self._suppress_item_change:
            return

        row = self.list_widget.row(item)
        # emit toggle request for this row
        if row >= 0:
            self.toggle_task_requested.emit(row)

    # --- view update methods ---------------------------------------
    def update_tasks(self, tasks):
        """Repopulate the tasks list from model data.

        Accepts either list of dict-like objects (with .get) or Task dataclass instances
        with attributes `title`, `completed`, and `id`.
        """
        # Suppress itemChanged handler while we rebuild the list
        self._suppress_item_change = True
        self.list_widget.clear()
        for t in tasks:
            # support both dict-like and dataclass-like Task
            if hasattr(t, "get"):
                completed = t.get('completed')
                title = t.get('title')
                tid = t.get('id')
            else:
                # assume object with attributes
                completed = getattr(t, 'completed', False)
                title = getattr(t, 'title', str(t))
                tid = getattr(t, 'id', None)

            # Use a checkbox in the list to represent completion state
            text = title
            item = QListWidgetItem(text)
            # set checkbox state
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            if completed:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

            # Visual cues: strike-through and dim color for completed tasks
            if completed:
                f = item.font()
                f.setStrikeOut(True)
                item.setFont(f)
                item.setForeground(QColor('#6c6c6c'))

            # store task id in item data for reference (use Qt.UserRole) if available
            if tid is not None:
                item.setData(Qt.ItemDataRole.UserRole, tid)

            self.list_widget.addItem(item)
        self._suppress_item_change = False

    def append_status(self, message):
        self.status_text.append(message)

    def clear_status(self):
        self.status_text.clear()

    def current_selected_index(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            return row
        return None

    def select_index(self, index: int):
        if 0 <= index < self.list_widget.count():
            self.list_widget.setCurrentRow(index)

    def clear_list(self):
        self.list_widget.clear()

    # --- Theme ------------------------------------------------------
    def apply_light_theme(self):
        """Apply a light theme stylesheet to the main view."""
        style = """
        /* Base colors */
        QMainWindow, QWidget {
            background-color: #fafafa;
            color: #222222;
            font-family: Segoe UI, Arial, Helvetica, sans-serif;
            font-size: 12px;
        }
        QLabel { color: #111111; }
        QLineEdit, QTextEdit, QListWidget {
            background-color: #ffffff;
            color: #111111;
            border: 1px solid #d0d0d0;
        }
        QPushButton {
            background-color: #f3f6f9;
            color: #111111;
            border: 1px solid #cfcfcf;
            padding: 6px 10px;
            border-radius: 4px;
        }
        QPushButton:hover { background-color: #e9eef5; }
        QPushButton:pressed { background-color: #dfe9f2; }
        QListWidget::item:selected {
            background-color: #d0e7ff;
            color: #000000;
        }
        QTextEdit { background-color: #ffffff; }
        QScrollBar:vertical { background: #f0f0f0; width: 12px; }
        """
        self.setStyleSheet(style)

