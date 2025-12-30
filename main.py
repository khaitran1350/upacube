import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler
from PyQt6.QtWidgets import QApplication, QMessageBox
import os

from models.data_model import DataModel
from views.main_view import MainView
from controllers.main_controller import MainController
from utils.logging_qt import QtHandler


def excepthook(exc_type, exc_value, exc_tb):
    tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        if QApplication.instance() is not None:
            QMessageBox.critical(None, "Unhandled Exception", tb)
    except Exception:
        pass
    logging.getLogger().exception(tb)


def main():
    sys.excepthook = excepthook

    # configure logging
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
    # rotating file in logs/ directory
    base_dir = os.path.dirname(__file__)
    logs_dir = os.path.join(base_dir, 'logs')
    try:
        os.makedirs(logs_dir, exist_ok=True)
    except Exception:
        pass
    fh_path = os.path.join(logs_dir, 'upacube.log')
    fh = RotatingFileHandler(fh_path, maxBytes=5_000_000, backupCount=3, encoding='utf-8')
    fh.setFormatter(formatter)
    root.addHandler(fh)
    # console
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    root.addHandler(ch)
    # Qt handler (view will connect emitter to its text widget)
    qh = QtHandler()
    qh.setFormatter(formatter)
    root.addHandler(qh)

    app = QApplication(sys.argv)

    model = DataModel()
    view = MainView()
    # connect Qt logging emitter to the view's status_text
    try:
        from utils.logging_qt import connect_to_textedit
        connect_to_textedit(view.status_text)
    except Exception:
        pass

    controller = MainController(model, view)
    logging.getLogger(__name__).info('Application started')
    view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
