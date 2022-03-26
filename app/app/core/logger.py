import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

log_dir = '/var/log/vumblebot/'
log_file_path = log_dir + 'error.log'
Path(log_dir).mkdir(parents=True, exist_ok=True)
Path(log_file_path).touch(exist_ok=True)

file_error_handler = logging.FileHandler(log_file_path)
file_error_handler.setLevel(logging.ERROR)
file_error_handler.setFormatter(formatter)
logger.addHandler(file_error_handler)
