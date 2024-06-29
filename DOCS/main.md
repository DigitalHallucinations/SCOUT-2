# main.py Documentation

## Overview

This script initializes and runs the SCOUT application, managing logging, exception handling, and dynamically loading modules based on selected LLM (Large Language Model) and background providers. The script also ensures proper shutdown and cleanup of tasks and resources.

## Table of Contents

1. [Imports](#imports)
2. [Setup Logging](#setup-logging)
3. [Custom Exception Hook](#custom-exception-hook)
4. [Global Variables](#global-variables)
5. [Context Managers](#context-managers)
6. [Main Application Loop](#main-application-loop)
7. [Shutdown Procedure](#shutdown-procedure)
8. [Main Function](#main-function)
9. [Entry Point](#entry-point)

## Imports

The script imports several modules and functions for logging, exception handling, asynchronous management, GUI application, dynamic module loading, threading, and memory tracing.


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


## Setup Logging

Logging is configured with a custom logger. The memory tracing is started to help with debugging memory usage.


tracemalloc.start()
set_logging_level(logging.INFO)
logger = setup_logger('main')


## Custom Exception Hook

A custom exception hook is defined to log uncaught exceptions. This helps in debugging by providing detailed error information in the logs.


def custom_excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = custom_excepthook


## Global Variables

Several global variables are defined to manage the application's state, tasks, and dynamic modules.


should_exit = False
global_tasks = set()
dynamically_loaded_modules = []
task_lock = threading.Lock()
shutdown_event = asyncio.Event()


## Context Managers

An asynchronous context manager is defined to handle background tasks, ensuring they are properly managed and cleaned up.


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


## Main Application Loop

The `run_app` function handles the main application loop, dynamically loading modules based on the selected LLM and background providers.


async def run_app():
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


## Shutdown Procedure

The `shutdown` function handles cleanup and shutdown tasks, ensuring all resources and connections are properly closed.


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


## Main Function

The `main` function initializes and starts the application, running the main application loop and waiting for the shutdown event.


async def main():
    global app, SCOUT_app
    app = QApplication([])
    SCOUT_app = SCOUT(shutdown_event=shutdown_event)  
    logger.info("SCOUT application started")
    await run_app()

    await shutdown_event.wait()

    loop = asyncio.get_running_loop()
    await loop.run_until_complete(shutdown())


## Entry Point

The script's entry point ensures the `main` function is run within an asyncio event loop.


if __name__ == "__main__":
    asyncio.run(main())


This documentation provides a detailed overview of the `main.py` script, explaining its components and functionality.