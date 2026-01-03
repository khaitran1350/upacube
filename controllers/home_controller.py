"""
HomeController - Handles HomeView interactions
"""
import logging
from typing import Any, Callable, Optional


class HomeController:
    """
    Handles navigation from HomeView. It delegates navigation requests to a
    coordinator callback set by MainController.
    """

    def __init__(self, model: Any, view: Any):
        self.model = model
        self.view = view
        self.logger = logging.getLogger(__name__)

        # callback set by coordinator to perform navigation (callable with no args)
        self.show_task_view_callback: Optional[Callable[[], None]] = None

        # wire view signal
        self.view.navigate_to_tasks.connect(self.on_navigate_to_tasks)

    def on_navigate_to_tasks(self):
        self.logger.info('HomeView requested navigation to tasks')
        if callable(self.show_task_view_callback):
            self.show_task_view_callback()
        else:
            self.logger.warning('No navigation callback set on HomeController')

