"""
Home View - Main landing page
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt


class HomeView(QWidget):
    """
    Home page widget with navigation to other sections.
    """

    # Signal emitted when user wants to navigate to task manager
    navigate_to_tasks = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the home page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Welcome title
        title = QLabel("Welcome to UpaCube")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            padding: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Your Personal Task Management System")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            padding: 10px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Add some spacing
        layout.addStretch(1)

        # Navigation button to Task Manager
        tasks_button = QPushButton("📋 Task Manager")
        tasks_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 40px;
                border: none;
                border-radius: 8px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        tasks_button.clicked.connect(lambda: self.navigate_to_tasks.emit())
        layout.addWidget(tasks_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # More space at bottom
        layout.addStretch(2)

        # Info/version label at bottom
        info_label = QLabel("Version 1.0 | © 2026 UpaCube")
        info_label.setStyleSheet("""
            font-size: 11px;
            color: #95a5a6;
            padding: 10px;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

