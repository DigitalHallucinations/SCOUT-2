# main.py

import asyncio
from gui.app import SCOUT
from modules.logging.logger import setup_logger, set_logging_level, logging
from PySide6.QtWidgets import QApplication

set_logging_level(logging.DEBUG)

logger = setup_logger('main')

def main():
    app = QApplication([])
    SCOUT_app = SCOUT()
    logger.info("Application started.")

    async def run_app():
        async def async_main():
            while True:
                await asyncio.sleep(0.01)
                app.processEvents()

        async_main_task = asyncio.create_task(async_main())
        await SCOUT_app.async_main()
        app.quit()
        await async_main_task

    asyncio.run(run_app())

if __name__ == "__main__":
    main()