import logging
import os

logger = logging.getLogger("reservation")
logger.setLevel(logging.INFO)

log_file = os.path.join(os.path.dirname(__file__), "..", "logs", "app.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logger.addHandler(file_handler)