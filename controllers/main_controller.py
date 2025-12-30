"""
Main Controller - Connects Model and View, handles task logic
"""
from datetime import datetime
import logging


class MainController:
    """
    Controller class that connects the Model and View.
    Handles user interactions and updates the model/view accordingly.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.logger = logging.getLogger(__name__)

        # Connect view signals to controller methods
        self.view.add_task_requested.connect(self.on_add_task)
        self.view.toggle_task_requested.connect(self.on_toggle_task)
        self.view.remove_task_requested.connect(self.on_remove_task)
        self.view.process_requested.connect(self.on_process_requested)
        self.view.clear_requested.connect(self.on_clear_requested)

        # Connect model signals to view updates
        self.model.tasks_changed.connect(self.update_task_list)
        self.model.data_changed.connect(self.on_model_data_changed)

        # Initialize view with model data
        self.update_view()

    # --- view handlers ------------------------------------------------
    def on_add_task(self, title: str):
        self.logger.info('on_add_task start: %r', title)
        try:
            task = self.model.add_task(title)
            if task:
                ts = datetime.now().strftime("%H:%M:%S")
                self.view.append_status(f"[{ts}] Added task: {task.title}")
        except Exception:
            self.logger.exception('on_add_task exception')
            try:
                self.view.append_status("Error adding task")
            except Exception:
                pass

    def on_toggle_task(self, index: int):
        self.logger.info('on_toggle_task start: %r', index)
        try:
            task = self.model.toggle_task_completed(index)
            if task:
                ts = datetime.now().strftime("%H:%M:%S")
                status = "Done" if getattr(task, "completed", False) else "Not done"
                title = getattr(task, "title", "(unknown)")
                self.view.append_status(f"[{ts}] Toggled task '{title}' -> {status}")
        except Exception:
            self.logger.exception('on_toggle_task exception')
            try:
                self.view.append_status("Error toggling task")
            except Exception:
                pass

    def on_remove_task(self, index: int):
        self.logger.info('on_remove_task start: %r', index)
        try:
            task = self.model.get_task(index)
            title = getattr(task, "title", "(unknown)") if task else "(unknown)"
            ok = self.model.remove_task_by_index(index)
            if ok:
                ts = datetime.now().strftime("%H:%M:%S")
                self.view.append_status(f"[{ts}] Removed task: {title}")
        except Exception:
            self.logger.exception('on_remove_task exception')
            try:
                self.view.append_status("Error removing task")
            except Exception:
                pass

    def on_process_requested(self):
        self.logger.info('on_process_requested start')
        try:
            tasks = self.model.get_tasks()
            total = len(tasks)
            completed = sum(1 for t in tasks if getattr(t, "completed", False))
            pending = total - completed
            ts = datetime.now().strftime("%H:%M:%S")
            self.view.append_status(f"[{ts}] Processing tasks: total={total}, completed={completed}, pending={pending}")
            if tasks:
                titles = ", ".join(getattr(t, "title", str(t)) for t in tasks)
                self.view.append_status(f"[{ts}] Titles: {titles}")
        except Exception:
            self.logger.exception('on_process_requested exception')
            try:
                self.view.append_status("Error during processing")
            except Exception:
                pass

    def on_clear_requested(self):
        self.logger.info('on_clear_requested start')
        try:
            self.model.clear_tasks()
            self.model.data = ""
            ts = datetime.now().strftime("%H:%M:%S")
            self.view.append_status(f"[{ts}] Cleared all tasks")
        except Exception:
            self.logger.exception('on_clear_requested exception')
            try:
                self.view.append_status("Error clearing tasks")
            except Exception:
                pass

    # --- model handlers ------------------------------------------------
    def on_model_data_changed(self, new_data):
        # Keep the view display in sync if needed; we append a short update
        self.view.append_status(f"Current input changed: {new_data}")

    # --- helpers -------------------------------------------------------
    def update_task_list(self):
        tasks = self.model.get_tasks()
        self.view.update_tasks(tasks)

    def update_view(self):
        # populate tasks and any other initial state
        self.update_task_list()
        self.view.clear_status()
