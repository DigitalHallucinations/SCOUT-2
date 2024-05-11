import asyncio
from contextlib import asynccontextmanager
from gui.app import SCOUT
from modules.logging.logger import setup_logger, set_logging_level, logging
from PySide6.QtWidgets import QApplication
import importlib
import threading

set_logging_level(logging.DEBUG)  

logger = setup_logger('main')

should_exit = False
global_tasks = set()
dynamically_loaded_modules = []
task_lock = threading.Lock()

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
                logger.error(f"Error unloading module {module.__name__}: {e}")  # More specific error message

        # Task Cancellation Options
        # Option 1: Cancel tasks (potentially forceful)
        #for task in global_tasks:
            #task.cancel()

        # Option 2: Wait for tasks to complete (graceful shutdown)
        await asyncio.gather(*global_tasks, return_exceptions=True)
        logger.debug("All tasks completed. Exiting application loop")  # Added logging here

        app.quit()

def main():
    """Initialize and start the application."""
    global app, SCOUT_app
    app = QApplication([])
    SCOUT_app = SCOUT()
    logger.info("SCOUT application started") 
    asyncio.run(run_app())

if __name__ == "__main__":
    main()