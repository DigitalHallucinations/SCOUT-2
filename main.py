# SCOUT/main.py

from gui.app import SCOUT   
from modules.logging.logger import setup_logger, set_logging_level, logging

set_logging_level(logging.DEBUG)  

logger = setup_logger('main')


def main():
    SCOUT_app = SCOUT()  
    logger.info("Application started.")
    SCOUT_app.run_asyncio_loop()

if __name__ == "__main__":
    main() 