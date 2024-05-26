# modules/logging/logger.py

import logging
from logging.handlers import RotatingFileHandler

logging_level = logging.INFO

def set_logging_level(level):
    global logging_level
    logging_level = level

def get_logging_level():
    return logging_level

class CustomLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name, logging_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Ensure the log file is created in the correct directory
        file_handler = RotatingFileHandler('modules/logging/SCOUT.log', maxBytes=50*1024*1024, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.addHandler(stream_handler)

        # Disable propagation to the root logger
        self.propagate = False

def setup_logger(logger_name):
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    return logger