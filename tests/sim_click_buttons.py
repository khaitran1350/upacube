from PyQt6.QtWidgets import QApplication
from views.main_view import MainView
from models.data_model import DataModel
from controllers.main_controller import MainController

import traceback

app = QApplication([])
model = DataModel()
view = MainView()
controller = MainController(model, view)

buttons = [
    ('Add', view.add_button),
    ('Process', view.process_button),
    ('Toggle', view.toggle_button),
    ('Remove', view.remove_button),
    ('Clear', view.clear_button),
]

print('Starting button click simulation')
for name, btn in buttons:
    try:
        print(f'Clicking: {name}')
        # ensure input for Add
        if name == 'Add':
            view.input_field.setText('simulated')
        btn.click()
        print(f'Clicked: {name} ok')
    except Exception:
        print(f'Clicked: {name} raised')
        traceback.print_exc()

print('Simulation finished')
app.quit()

