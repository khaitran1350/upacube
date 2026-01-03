"""
TaskController - Handles TaskView interactions and model updates
"""
from datetime import datetime
import logging
from typing import Any


class TaskController:
    """
    Handles task-related user actions and updates the model and view.
    """

    def __init__(self, model: Any, view: Any):
        self.model = model
        self.view = view
        self.logger = logging.getLogger(__name__)

        # Wire view signals to controller methods
        self.view.add_task_requested.connect(self.on_add_task)
        self.view.toggle_task_requested.connect(self.on_toggle_task)
        self.view.remove_task_requested.connect(self.on_remove_task)
        self.view.clear_requested.connect(self.on_clear_requested)

        # Listen to model signals
        if hasattr(self.model, 'tasks_changed'):
            self.model.tasks_changed.connect(self.update_task_list)
        if hasattr(self.model, 'data_changed'):
            self.model.data_changed.connect(self.on_model_data_changed)

        # Initialize view
        self.update_view()

    def on_add_task(self, payload: Any):
        self.logger.info('on_add_task start: %r', payload)
        try:
            task = self.model.add_task(payload)
            if task:
                ts = datetime.now().strftime("%H:%M:%S")
                # include brief details in status
                info = f"{task.title}"
                if getattr(task, 'priority', None):
                    info += f" (priority={task.priority})"
                if getattr(task, 'deadline', None):
                    info += f" deadline={task.deadline}"
                self.view.append_status(f"[{ts}] Added task: {info}")
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

    def on_model_data_changed(self, new_data):
        self.view.append_status(f"Current input changed: {new_data}")

    def update_task_list(self):
        tasks = self.model.get_tasks()
        self.view.update_tasks(tasks)

    def update_view(self):
        self.update_task_list()
        self.view.clear_status()
