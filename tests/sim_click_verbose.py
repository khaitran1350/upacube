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
    ('Add', view.task_view.add_button),
    ('Toggle', view.task_view.toggle_button),
    ('Remove', view.task_view.remove_button),
    ('Clear', view.task_view.clear_button),
]

print('App instance:', QApplication.instance() is not None)
print('Window visible (before show):', view.isVisible())
view.show()
print('Window visible (after show):', view.isVisible())

for name, btn in buttons:
    try:
        print(f'-- Clicking: {name} --')
        if name == 'Add':
            view.task_view.input_field.setText('simulated')
        btn.click()
        print(f'Clicked: {name} ok')
        # print some state
        print('Tasks count:', model.get_task_count())
        print('Status lines:', getattr(view.status_text, 'toPlainText')())
    except Exception as e:
        print(f'Clicked: {name} raised exception: {e}')
        traceback.print_exc()

print('Simulation finished')
app.quit()
