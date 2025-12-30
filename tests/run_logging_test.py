import logging
from models.data_model import DataModel
from views.main_view import MainView
from controllers.main_controller import MainController

logging.basicConfig(level=logging.INFO)
print('starting test')
model = DataModel()
view = MainView()
controller = MainController(model, view)
logging.getLogger(__name__).info('controller initialized')
print('done')

