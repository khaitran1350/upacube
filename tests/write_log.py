import logging, os
from logging.handlers import RotatingFileHandler
base_dir = os.path.dirname(os.path.dirname(__file__))
logs_dir = os.path.join(base_dir, 'logs')
os.makedirs(logs_dir, exist_ok=True)
fh_path = os.path.join(logs_dir, 'upacube_test.log')
handler = RotatingFileHandler(fh_path, maxBytes=100000, backupCount=1, encoding='utf-8')
fmt = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')
handler.setFormatter(fmt)
logger = logging.getLogger('write_log_test')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('write_log test entry')
print('wrote', fh_path)

