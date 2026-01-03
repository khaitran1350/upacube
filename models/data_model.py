"""
Task Data Model - stores tasks and persists them to a JSON file.
Each task is represented in-memory as models.task.Task and persisted as dicts in JSON.
"""
import json
import os
from PyQt6.QtCore import QObject, pyqtSignal

from .task import Task


class DataModel(QObject):
    """
    Model class that holds task data and business logic.
    Emits signals when data or tasks change to notify observers (views/controllers).
    """

    # Signals
    data_changed = pyqtSignal(str)      # Emits when the current data string changes
    tasks_changed = pyqtSignal()        # Emits when the tasks list changes

    def __init__(self, storage_path=None):
        super().__init__()
        self._data = ""
        self._tasks: list[Task] = []
        self._next_id = 1

        # Decide storage path (project root/tasks.json by default)
        if storage_path:
            self.storage_path = storage_path
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            self.storage_path = os.path.join(base_dir, "tasks.json")

        self._load()

    # --- persistence -------------------------------------------------
    def _load(self):
        """Load tasks from the JSON storage file if it exists."""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._tasks = [Task.from_dict(d) for d in data]
                        # compute next id
                        max_id = max((t.id for t in self._tasks), default=0)
                        self._next_id = max_id + 1
                    else:
                        self._tasks = []
            else:
                # ensure file exists
                self._save()
        except Exception:
            # If loading fails, fallback to empty list (do not crash app)
            self._tasks = []

    def _save(self):
        """Save tasks to the JSON storage file (as list of dicts)."""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self._tasks], f, ensure_ascii=False, indent=2)
        except Exception:
            # best-effort save: ignore errors to avoid crashing UI
            pass

    # --- data property (current input) ------------------------------
    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, value: str):
        if self._data != value:
            self._data = value
            self.data_changed.emit(value)

    # --- tasks API --------------------------------------------------
    def add_task(self, title: str) -> Task | None:
        """Add a new Task and persist changes."""
        # Support passing a dict with extra fields
        if isinstance(title, dict):
            data = title
            title_text = str(data.get('title', '')).strip()
            if not title_text:
                return None
            description = str(data.get('description', ''))
            deadline = data.get('deadline')
            priority = str(data.get('priority', 'Normal'))
            task = Task(id=self._next_id, title=title_text, description=description, deadline=deadline, priority=priority)
        else:
            title_text = str(title).strip()
            if not title_text:
                return None
            task = Task(id=self._next_id, title=title_text)
        self._next_id += 1
        self._tasks.append(task)
        self._save()
        self.tasks_changed.emit()
        return task

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of tasks list."""
        return list(self._tasks)

    def get_task_count(self) -> int:
        return len(self._tasks)

    def clear_tasks(self):
        """Remove all tasks and persist."""
        self._tasks.clear()
        self._save()
        self.tasks_changed.emit()

    def remove_task_by_index(self, index: int) -> bool:
        """Remove task by list index (not id). Returns True if removed."""
        try:
            self._tasks.pop(index)
            self._save()
            self.tasks_changed.emit()
            return True
        except Exception:
            return False

    def toggle_task_completed(self, index: int) -> Task | None:
        """Toggle the 'completed' flag for Task at index."""
        try:
            task = self._tasks[index]
            task.completed = not bool(task.completed)
            self._save()
            self.tasks_changed.emit()
            return task
        except Exception:
            return None

    def get_task(self, index: int) -> Task | None:
        try:
            return self._tasks[index]
        except Exception:
            return None
