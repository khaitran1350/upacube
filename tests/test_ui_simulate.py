from PyQt6.QtWidgets import QApplication
from views.main_view import MainView
from models.data_model import DataModel
from controllers.main_controller import MainController
import sys

# create app (off-screen)
app = QApplication([])
model = DataModel()
view = MainView()
controller = MainController(model, view)

# simulate button clicks by calling the handlers
view._on_add_clicked()  # empty input -> should do nothing
view.input_field.setText('Sim click task')
view._on_add_clicked()  # should add
view._on_toggle_clicked()
view._on_remove_clicked()
view.process_requested.emit()
view.clear_requested.emit()

print('simulation complete - app still running')
# don't start the event loop
app.quit()

