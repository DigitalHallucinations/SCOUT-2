import asyncio
from contextlib import asynccontextmanager
from gui.app import SCOUT
from modules.logging.logger import setup_logger, set_logging_level, logging
from PySide6.QtWidgets import QApplication
import importlib
import threading

set_logging_level(logging.DEBUG)

logger = setup_logger('main')

should_exit = False  # Global flag to signal thread exit
global_tasks = set()  # Global set to track tasks
dynamically_loaded_modules = []  # List to track modules
task_lock = threading.Lock()  # Lock for thread-safe task management

@asynccontextmanager
async def background_tasks():
    """Manage background tasks within an asynchronous context."""
    async def async_main():
        while not should_exit:  # Check the flag
            await asyncio.sleep(0.01)
            app.processEvents()

    task = asyncio.create_task(async_main())
    with task_lock:  # Acquire lock before adding task
        global_tasks.add(task)
    try:
        yield  # Allow other code to run while tasks are active
    finally:
        global should_exit
        should_exit = True  # Set the flag to signal exit
        task.cancel()
        with task_lock:  # Acquire lock before removing task
            global_tasks.remove(task)
        await task

async def run_app():
    """Run the main application loop."""
    dynamically_loaded_modules = []  # List to track modules
    async with background_tasks():
        await SCOUT_app.async_main()
        # Populate dynamically_loaded_modules based on current providers
        current_llm_provider = SCOUT_app.provider_manager.get_current_llm_provider()
        current_background_provider = SCOUT_app.provider_manager.get_current_background_provider()

        # LLM Provider Checks
        if current_llm_provider == "OpenAI":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.OpenAI.OA_gen_response"))
        elif current_llm_provider == "Mistral":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Mistral.Mistral_gen_response"))
        elif current_llm_provider == "Google":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Google.GG_gen_response"))
        elif current_llm_provider == "HuggingFace":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.HuggingFace.HF_gen_response"))
        elif current_llm_provider == "Anthropic":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Anthropic.Anthropic_gen_response"))
        # ... (add checks for any other LLM providers) ...

        # Background Provider Checks
        if current_background_provider == "OpenAI":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.OpenAI.openai_api"))
        elif current_background_provider == "Mistral":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Mistral.Mistral_api"))
        elif current_background_provider == "Anthropic":
            dynamically_loaded_modules.append(importlib.import_module("modules.Providers.Anthropic.Anthropic_api"))
        # ... (add checks for any other background providers) ...

        for module in dynamically_loaded_modules:
            try:
                importlib.unload(module)  # Unload modules before quitting
            except Exception as e:
                logger.error(f"Error unloading module: {e}")

        # Task Cancellation Options
        # Option 1: Cancel tasks (potentially forceful)
        for task in global_tasks:
            task.cancel()

        # Option 2: Wait for tasks to complete (graceful shutdown)
        # await asyncio.gather(*global_tasks, return_exceptions=True)

        app.quit()  # This will execute after the context manager exits

def main():
    """Initialize and start the application."""
    global app, SCOUT_app
    app = QApplication([])
    SCOUT_app = SCOUT()
    logger.info("Application started.")
    asyncio.run(run_app())

if __name__ == "__main__":
    main()