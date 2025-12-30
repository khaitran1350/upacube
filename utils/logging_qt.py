import logging
from PyQt6.QtCore import QObject, pyqtSignal


class QtLogEmitter(QObject):
    log = pyqtSignal(str)


_emitter = QtLogEmitter()


class QtHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            _emitter.log.emit(msg)
        except Exception:
            pass


def connect_to_textedit(textedit):
    _emitter.log.connect(textedit.append)

