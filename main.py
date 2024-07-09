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
import signal

tracemalloc.start()

set_logging_level(logging.INFO)
logger = setup_logger('main')

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
    logger.debug("Starting main application loop")
    try:
        async with background_tasks():
            await SCOUT_app.async_main()
            current_llm_provider = SCOUT_app.provider_manager.get_current_llm_provider()
            current_background_provider = SCOUT_app.provider_manager.get_current_background_provider()

            logger.debug(f"Current LLM provider: {current_llm_provider}")
            logger.debug(f"Current background provider: {current_background_provider}")

            providers = {
                "OpenAI": ("modules.Providers.OpenAI.OA_gen_response", "modules.Providers.OpenAI.openai_api"),
                "Mistral": ("modules.Providers.Mistral.Mistral_gen_response", "modules.Providers.Mistral.Mistral_api"),
                "Google": ("modules.Providers.Google.GG_gen_response", None),
                "HuggingFace": ("modules.Providers.HuggingFace.HF_gen_response", None),
                "Anthropic": ("modules.Providers.Anthropic.Anthropic_gen_response", "modules.Providers.Anthropic.Anthropic_api")
            }

            for provider, modules in providers.items():
                if current_llm_provider == provider and modules[0]:
                    dynamically_loaded_modules.append(importlib.import_module(modules[0]))
                    logger.debug(f"Loaded {provider} LLM module")
                if current_background_provider == provider and modules[1]:
                    dynamically_loaded_modules.append(importlib.import_module(modules[1]))
                    logger.debug(f"Loaded {provider} background provider module")

            await asyncio.gather(*global_tasks, return_exceptions=True)
    except Exception as e:
        logger.error(f"Error in run_app: {e}")
    finally:
        logger.debug("All tasks completed. Exiting application loop")
        for module in dynamically_loaded_modules:
            try:
                importlib.unload(module)
            except Exception as e:
                logger.error(f"Error unloading module {module.__name__}: {e}")

async def shutdown():
    global should_exit
    should_exit = True
    if SCOUT_app:
        SCOUT_app.close()
    await asyncio.gather(*global_tasks, return_exceptions=True)
    if SCOUT_app:
        SCOUT_app.user_database.close_connection()
        SCOUT_app.chat_history_database.close_connection()
    logger.info("Application shutdown complete.")

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}")
    shutdown_event.set()

async def main():
    global app, SCOUT_app
    app = QApplication([])
    SCOUT_app = SCOUT(shutdown_event=shutdown_event)
    logger.info("SCOUT application started")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await run_app()
        await shutdown_event.wait()
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
    finally:
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        logger.info("Application has shut down.")