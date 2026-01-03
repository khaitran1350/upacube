from models.data_model import DataModel
from controllers.task_controller import TaskController

# Create a simple dummy task-view that provides the signals and methods used by the controller
class DummyTaskView:
    def __init__(self):
        class Signal:
            def __init__(self):
                self._cb = None
            def connect(self, cb):
                self._cb = cb
            def emit(self, *args, **kwargs):
                if self._cb:
                    return self._cb(*args, **kwargs)
        self.add_task_requested = Signal()
        self.toggle_task_requested = Signal()
        self.remove_task_requested = Signal()
        self.clear_requested = Signal()
        # methods used by controller
        self._status = []
    def append_status(self, msg):
        self._status.append(msg)
    def update_tasks(self, tasks):
        # store current tasks for inspection
        self._tasks_snapshot = [t.to_dict() if hasattr(t, 'to_dict') else t for t in tasks]
    def clear_status(self):
        self._status.clear()


# run headless test
m = DataModel()
view = DummyTaskView()
controller = TaskController(m, view)

# initial
print('initial tasks:', m.get_task_count())
# add
controller.on_add_task('headless task')
print('after add tasks:', m.get_task_count())
# toggle first
if m.get_task_count() > 0:
    controller.on_toggle_task(0)
    print('after toggle first:', m.get_tasks()[0].completed)
# remove
if m.get_task_count() > 0:
    controller.on_remove_task(0)
    print('after remove tasks:', m.get_task_count())
# clear
controller.on_clear_requested()
print('after clear tasks:', m.get_task_count())
