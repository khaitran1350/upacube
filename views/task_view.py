"""
Task View - Task manager UI with back navigation
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QTextEdit, QListWidgetItem, QSplitter
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor
from .add_task_dialog import AddTaskDialog


class TaskView(QWidget):
    """
    Task management page (View).
    Contains UI elements and emits signals for user actions.
    """

    # Signals for user actions
    add_task_requested = pyqtSignal(object)   # payload: dict or title
    toggle_task_requested = pyqtSignal(int)  # payload: index (model index)
    remove_task_requested = pyqtSignal(int)  # payload: index (model index)
    clear_requested = pyqtSignal()
    navigate_back = pyqtSignal()  # Signal to go back to home

    def __init__(self):
        super().__init__()
        self._suppress_item_change = False
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header with back button and title
        header_layout = QHBoxLayout()

        back_button = QPushButton("← Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-size: 14px;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        back_button.clicked.connect(lambda: self.navigate_back.emit())
        header_layout.addWidget(back_button)

        title_label = QLabel("Task Manager")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Add button only (use dialog for full form)
        input_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task")
        input_layout.addStretch()
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)

        # Two-column area: pending (left) and done (right)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        pending_widget = QWidget()
        pending_layout = QVBoxLayout(pending_widget)
        pending_label = QLabel("Pending")
        pending_label.setStyleSheet("font-weight: bold; padding: 6px;")
        pending_layout.addWidget(pending_label)
        self.pending_list = QListWidget()
        pending_layout.addWidget(self.pending_list)

        done_widget = QWidget()
        done_layout = QVBoxLayout(done_widget)
        done_label = QLabel("Done")
        done_label.setStyleSheet("font-weight: bold; padding: 6px;")
        done_layout.addWidget(done_label)
        self.done_list = QListWidget()
        done_layout.addWidget(self.done_list)

        splitter.addWidget(pending_widget)
        splitter.addWidget(done_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # listen for checkbox changes (user toggles) on both lists
        self.pending_list.itemChanged.connect(self._on_item_changed)
        self.done_list.itemChanged.connect(self._on_item_changed)

        # Buttons row
        button_layout = QHBoxLayout()
        self.toggle_button = QPushButton("Toggle Done")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear All")
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
        # toggle/remove call internal handlers which accept optional checked param
        self.toggle_button.clicked.connect(self._on_toggle_clicked)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        self.clear_button.clicked.connect(lambda checked=False: self.clear_requested.emit())

        # Apply the preferred theme
        self.apply_light_theme()

    # --- UI event handlers -------------------------------------------
    def _on_add_clicked(self, checked=False):
        # Open modal dialog to collect task details
        dlg = AddTaskDialog(self)
        dlg.submitted.connect(lambda payload: self.add_task_requested.emit(payload))
        dlg.exec()

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

        # Determine which list the changed item lives in and get its model id
        list_widget = item.listWidget()
        row = list_widget.row(item)
        if row < 0:
            return

        tid = item.data(Qt.ItemDataRole.UserRole)
        if tid is None:
            return

        # Emit toggle request with model index resolved by id
        model_index = self._model_index_from_task_id(tid)
        if model_index is not None:
            self.toggle_task_requested.emit(model_index)

    # --- view update methods ---------------------------------------
    def update_tasks(self, tasks):
        """Repopulate the tasks lists from model data.

        Accepts either list of dict-like objects (with .get) or Task dataclass instances
        with attributes `title`, `completed`, and `id`.
        """
        # Suppress itemChanged handler while we rebuild the lists
        self._suppress_item_change = True
        self.pending_list.clear()
        self.done_list.clear()

        for idx, t in enumerate(tasks):
            # support both dict-like and dataclass-like Task
            if hasattr(t, "get"):
                completed = t.get('completed')
                title = t.get('title')
                description = t.get('description', '')
                deadline = t.get('deadline')
                priority = t.get('priority', 'Normal')
            else:
                completed = getattr(t, 'completed', False)
                title = getattr(t, 'title', str(t))
                description = getattr(t, 'description', '')
                deadline = getattr(t, 'deadline', None)
                priority = getattr(t, 'priority', 'Normal')

            # compact label: Title (Priority) [deadline]
            label = title
            if priority:
                label += f" ({priority})"
            if deadline:
                label += f" [{deadline}]"

            item = QListWidgetItem(label)
            # attach description as tooltip for more detail
            if description:
                item.setToolTip(description)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            # attach model index as UserRole so selection maps back to model
            item.setData(Qt.ItemDataRole.UserRole, idx)
            # set check state and visual cues
            if completed:
                item.setCheckState(Qt.CheckState.Checked)
                f = item.font()
                f.setStrikeOut(True)
                item.setFont(f)
                # completed items are dim gray
                item.setForeground(QColor('#6c6c6c'))
                # place in done list
                self.done_list.addItem(item)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
                # color by priority for pending tasks
                p = (priority or 'Normal').lower()
                if p == 'high':
                    item.setForeground(QColor('#c0392b'))
                elif p == 'low':
                    item.setForeground(QColor('#27ae60'))
                else:
                    # Normal or unknown: use a neutral dark color
                    item.setForeground(QColor('#2c3e50'))
                self.pending_list.addItem(item)

        self._suppress_item_change = False

    def append_status(self, message):
        self.status_text.append(message)

    def clear_status(self):
        self.status_text.clear()

    def current_selected_index(self):
        """Return the model index of the currently selected item (if any)."""
        # check pending list first, then done list
        for lst in (self.pending_list, self.done_list):
            row = lst.currentRow()
            if row >= 0:
                item = lst.item(row)
                tid = item.data(Qt.ItemDataRole.UserRole)
                if tid is not None:
                    return self._model_index_from_task_id(tid)
        return None

    def select_index(self, index: int):
        """Select the item corresponding to the given model index."""
        # find task id for model index via model lookup of tasks is not available here
        # instead, select by searching both lists for item with matching UserRole == index
        # assume callers pass a model index corresponding to the stored ids
        # we'll match by task id equal to index or by stringified id
        for lst in (self.pending_list, self.done_list):
            for i in range(lst.count()):
                item = lst.item(i)
                tid = item.data(Qt.ItemDataRole.UserRole)
                if tid == index:
                    lst.setCurrentRow(i)
                    return
        # fallback: no-op

    def clear_list(self):
        self.pending_list.clear()
        self.done_list.clear()

    # --- helpers ---------------------------------------------------
    def _model_index_from_task_id(self, task_id):
        """Here task_id is already a model index (integer). Return it if valid."""
        try:
            if isinstance(task_id, int):
                return task_id
        except Exception:
            return None
        return None

    # --- Theme ------------------------------------------------------
    def apply_light_theme(self):
        """Apply a light theme stylesheet to the task view."""
        style = """
        /* Base colors */
        QWidget {
            background-color: #fafafa;
            color: #222222;
            font-family: Segoe UI, Arial, Helvetica, sans-serif;
            font-size: 12px;
        }
        QLabel { color: #111111; }
        
        /* Input fields */
        QLineEdit {
            background-color: white;
            color: #222;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 6px 8px;
            font-size: 13px;
        }
        QLineEdit:focus {
            border: 1px solid #3498db;
        }
        
        /* Buttons */
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #21618c;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
        }
        
        /* List */
        QListWidget {
            background-color: white;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 4px;
        }
        QListWidget::item {
            padding: 6px;
            border-bottom: 1px solid #ecf0f1;
        }
        QListWidget::item:selected {
            background-color: #e8f4f8;
            color: #222;
        }
        QListWidget::item:hover {
            background-color: #f0f8ff;
        }
        
        /* Text edit (status) */
        QTextEdit {
            background-color: white;
            color: #222;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
            padding: 8px;
            font-size: 11px;
            font-family: Consolas, Courier, monospace;
        }
        """
        self.setStyleSheet(style)

