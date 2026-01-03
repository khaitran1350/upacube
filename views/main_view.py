"""
Main View - Application container with page navigation
"""
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import pyqtSignal

from .home_view import HomeView
from .task_view import TaskView


class MainView(QMainWindow):
    """
    Main application window that manages navigation between pages.
    Uses QStackedWidget to switch between Home and Task views.
    """

    # Forward signals from TaskView for controller
    add_task_requested = pyqtSignal(object)   # payload: dict or title
    toggle_task_requested = pyqtSignal(int)  # payload: index
    remove_task_requested = pyqtSignal(int)  # payload: index
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        """Initialize the main window with page navigation"""
        self.setWindowTitle("UpaCube - Task Manager")
        # smaller default geometry for a compact view
        self.setGeometry(100, 100, 700, 550)

        # Create stacked widget to hold different   pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.home_view = HomeView()
        self.task_view = TaskView()

        # Add pages to stack
        self.stacked_widget.addWidget(self.home_view)  # index 0
        self.stacked_widget.addWidget(self.task_view)  # index 1

        # Connect navigation signals
        self.home_view.navigate_to_tasks.connect(self.show_task_view)
        self.task_view.navigate_back.connect(self.show_home_view)

        # Forward task view signals to controller
        self.task_view.add_task_requested.connect(self.add_task_requested.emit)
        self.task_view.toggle_task_requested.connect(self.toggle_task_requested.emit)
        self.task_view.remove_task_requested.connect(self.remove_task_requested.emit)
        self.task_view.clear_requested.connect(self.clear_requested.emit)

        # Start on home page
        self.show_home_view()

        # Apply global theme
        self.apply_global_theme()

    # --- Navigation methods -------------------------------------------
    def show_home_view(self):
        """Switch to home page"""
        self.stacked_widget.setCurrentWidget(self.home_view)

    def show_task_view(self):
        """Switch to task management page"""
        self.stacked_widget.setCurrentWidget(self.task_view)

    # --- Delegate methods to task_view for controller access ---------
    def update_tasks(self, tasks):
        """Forward to task view"""
        self.task_view.update_tasks(tasks)

    def append_status(self, message):
        """Forward to task view"""
        self.task_view.append_status(message)

    def clear_status(self):
        """Forward to task view"""
        self.task_view.clear_status()

    def current_selected_index(self):
        """Forward to task view"""
        return self.task_view.current_selected_index()

    def select_index(self, index: int):
        """Forward to task view"""
        self.task_view.select_index(index)

    def clear_list(self):
        """Forward to task view"""
        self.task_view.clear_list()

    # Expose status_text for logging (from task_view)
    @property
    def status_text(self):
        return self.task_view.status_text

    # --- Theme ------------------------------------------------------
    def apply_global_theme(self):
        """Apply a global theme stylesheet"""
        style = """
        QMainWindow {
            background-color: #fafafa;
        }
        """
        self.setStyleSheet(style)
