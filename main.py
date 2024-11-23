# main.py

import sys
import traceback
import asyncio
from contextlib import asynccontextmanager
from gui.app import SCOUT  
from modules.logging.logger import setup_logger, set_logging_level, logging
from PySide6.QtWidgets import QApplication
import importlib
import threading
import tracemalloc

tracemalloc.start()

# Set logging level
set_logging_level(logging.INFO)

# Setup main logger
logger = setup_logger('main')

# Custom exception hook to log uncaught exceptions
def custom_excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = custom_excepthook

should_exit = False
global_tasks = set()
dynamically_loaded_modules = []
task_lock = threading.Lock()

shutdown_event = asyncio.Event()

@asynccontextmanager
async def background_tasks():
    """Manage background tasks within an asynchronous context."""
    logger.debug("Entering background_tasks context manager")

    async def async_main():
        while not should_exit:
            await asyncio.sleep(0.01)
            app.processEvents()

    task = asyncio.create_task(async_main())
    with task_lock:
        global_tasks.add(task)
        logger.debug(f"Added task {task} to global_tasks")
    try:
        yield
    finally:
        global should_exit
        should_exit = True
        task.cancel()
        with task_lock:
            global_tasks.remove(task)
            logger.debug(f"Removed task {task} from global_tasks")
        await task
        logger.debug("Exiting background_tasks context manager")

async def run_app():
    """Run the main application loop."""
    dynamically_loaded_modules = []
    logger.debug("Starting main application loop")
    async with background_tasks():
        await SCOUT_app.async_main()
        current_llm_provider = SCOUT_app.provider_manager.get_current_llm_provider()
        current_background_provider = SCOUT_app.provider_manager.get_current_background_provider()

        logger.debug(f"Current LLM provider: {current_llm_provider}")
        logger.debug(f"Current background provider: {current_background_provider}")

        if current_llm_provider == "OpenAI":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.OpenAI.OA_gen_response"))
            logger.debug("Loaded OpenAI LLM module")
        elif current_llm_provider == "Mistral":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Mistral.Mistral_gen_response"))
            logger.debug("Loaded Mistral LLM module")
        elif current_llm_provider == "Google":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Google.GG_gen_response"))
            logger.debug("Loaded Google LLM module")
        elif current_llm_provider == "HuggingFace":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.HuggingFace.HF_gen_response"))
            logger.debug("Loaded HuggingFace LLM module")
        elif current_llm_provider == "Anthropic":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Anthropic.Anthropic_gen_response"))
            logger.debug("Loaded Anthropic LLM module")

        if current_background_provider == "OpenAI":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.OpenAI.openai_api"))
            logger.debug("Loaded OpenAI background provider module")
        elif current_background_provider == "Mistral":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Mistral.Mistral_api"))
            logger.debug("Loaded Mistral background provider module")
        elif current_background_provider == "Anthropic":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Anthropic.Anthropic_api"))
            logger.debug("Loaded Anthropic background provider module")

        for module in dynamically_loaded_modules:
            try:
                importlib.unload(module)
            except Exception as e:
                logger.error(f"Error unloading module {module.__name__}: {e}")  

        await asyncio.gather(*global_tasks, return_exceptions=True)
        logger.debug("All tasks completed. Exiting application loop")  

async def shutdown():
    """Handles all cleanup and shutdown tasks."""
    global should_exit
    should_exit = True
    # Signal the GUI to close
    if SCOUT_app:
        SCOUT_app.close()  # Close the GUI window
    # Cancel and await asyncio tasks
    await asyncio.gather(*global_tasks, return_exceptions=True)
    if SCOUT_app:
        SCOUT_app.user_database.close_connection()
        SCOUT_app.chat_history_database.close_connection()
    logger.info("Application shutdown complete.")

async def main():
    """Initialize and start the application."""
    global app, SCOUT_app
    app = QApplication([])
    SCOUT_app = SCOUT(shutdown_event=shutdown_event)  
    logger.info("SCOUT application started")
    await run_app()

    await shutdown_event.wait()

    loop = asyncio.get_running_loop()
    await loop.run_until_complete(shutdown())

if __name__ == "__main__":
    asyncio.run(main())