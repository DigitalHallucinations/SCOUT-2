# SCOUT/main.py
from gui.app import SCOUT   
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('main.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

# Create rotating file handler for file logging
rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Create stream handler for console logging
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Attach handlers to the logger
logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    """Adjust the logging level.
    
    Parameters:
    - level (str): Desired logging level. Can be 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    logger.setLevel(levels.get(level, logging.WARNING))

def main():
    SCOUT_app = SCOUT()  
    logger.info("Application started.")
    SCOUT_app.run_asyncio_loop()

if __name__ == "__main__":
    main() 