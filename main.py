# main.py

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
        try:
            while not should_exit:
                await asyncio.sleep(0.01)
                app.processEvents()
        except asyncio.CancelledError:
            logger.debug("background_tasks async_main task cancelled gracefully.")

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
        try:
            await task
        except asyncio.CancelledError:
            logger.debug(f"Task {task} cancelled")
        logger.debug("Exiting background_tasks context manager")

async def run_app():
    """Run the main application loop."""
    dynamically_loaded_modules = []
    logger.debug("Starting main application loop")
    async with background_tasks():
        # Create a task for SCOUT_app.async_main()
        sc_task = asyncio.create_task(SCOUT_app.async_main())
        with task_lock:
            global_tasks.add(sc_task)
            logger.debug(f"Added task {sc_task} to global_tasks")
        try:
            await sc_task
        except asyncio.CancelledError:
            logger.info("SCOUT_app.async_main() task cancelled")
        finally:
            with task_lock:
                global_tasks.remove(sc_task)
                logger.debug(f"Removed task {sc_task} from global_tasks")

        # Load providers after async_main is cancelled
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
                importlib.reload(module)  # Changed from unload to reload for safety
                logger.debug(f"Reloaded module {module.__name__}")
            except Exception as e:
                logger.error(f"Error reloading module {module.__name__}: {e}")  

        await asyncio.gather(*global_tasks, return_exceptions=True)
        logger.debug("All tasks completed. Exiting application loop")  

async def shutdown():
    """Handles all cleanup and shutdown tasks."""
    global should_exit
    should_exit = True
    logger.info("Initiating shutdown...")

    # Signal the GUI to close
    if SCOUT_app:
        SCOUT_app.close()  # Close the GUI window

    # Quit the QApplication event loop
    app.quit()

    # Cancel all tasks except the current one
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    logger.info(f"Cancelling {len(tasks)} pending tasks.")
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    # Close databases
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

    await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logger.error(f"RuntimeError during asyncio.run: {e}")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
