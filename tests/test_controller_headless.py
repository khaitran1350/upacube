from models.data_model import DataModel
from controllers.main_controller import MainController

# Create a simple dummy view that provides the signals and methods used by the controller
class DummyView:
    def __init__(self):
        # Instead of real Qt signals, provide callables the controller connects to
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
        self.process_requested = Signal()
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
view = DummyView()
controller = MainController(m, view)

# initial
print('initial tasks:', m.get_task_count())
# add
controller.on_add_task('headless task')
print('after add tasks:', m.get_task_count())
# toggle first
if m.get_task_count() > 0:
    controller.on_toggle_task(0)
    print('after toggle first:', m.get_tasks()[0].completed)
# process
controller.on_process_requested()
print('status logs:', view._status)
# remove
if m.get_task_count() > 0:
    controller.on_remove_task(0)
    print('after remove tasks:', m.get_task_count())
# clear
controller.on_clear_requested()
print('after clear tasks:', m.get_task_count())

