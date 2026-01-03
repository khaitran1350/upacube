from PyQt6.QtWidgets import QApplication
from views.main_view import MainView
from models.data_model import DataModel
from controllers.main_controller import MainController

# create app (off-screen)
app = QApplication([])
model = DataModel()
view = MainView()
controller = MainController(model, view)

# simulate add by emitting a payload (dialog would normally emit this)
payload = {'title': 'Sim click task', 'description': 'simulated', 'deadline': None, 'priority': 'Normal'}
view.task_view.add_task_requested.emit(payload)

# simulate toggle/remove using selection and controller calls
view.task_view._on_toggle_clicked()
view.task_view._on_remove_clicked()
view.clear_requested.emit()

print('simulation complete - app still running')
# don't start the event loop
app.quit()
