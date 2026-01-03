"""
Main Controller - Application coordinator that wires model and views
"""
import logging

from .home_controller import HomeController
from .task_controller import TaskController


class MainController:
    """
    Application coordinator: instantiate sub-controllers and wire views to them.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.logger = logging.getLogger(__name__)

        # Sub-controllers receive specific subviews from the main view
        self.home_controller = HomeController(model, view.home_view)
        self.task_controller = TaskController(model, view.task_view)

        # allow home controller to request navigation through this coordinator
        self.home_controller.show_task_view_callback = self.view.show_task_view

    def update_view(self):
        # Keep convenience method that delegates to task controller
        self.task_controller.update_view()
