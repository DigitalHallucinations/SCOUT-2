# CodeGenius UI Technical Documentation

## Architecture Overview

CodeGenius UI is built using the PySide6 framework, providing a rich set of tools for creating desktop applications with a modern look and feel. The architecture is designed to be modular and extensible, allowing for easy integration of new features.

## Components

### CodeGeniusUI

The main user interface component that integrates various features of the CodeGenius environment.

#### Methods

- `__init__(self)`
  - Initializes the CodeGeniusUI widget and subscribes to the `code_executed` event.
- `setup_ui(self)`
  - Sets up the user interface components, including the code input and output display areas.
- `on_code_executed(self, code: str, result: dict)`
  - Handles the `code_executed` event and updates the UI with execution results.
- `show(self)`
  - Shows the CodeGeniusUI widget and includes logging.
- `hide(self)`
  - Hides the CodeGeniusUI widget and includes logging.

### PythonInterpreter

Handles the execution of Python code and returns the results.

#### Methods

- `__init__(self, ...)`
  - Initializes the PythonInterpreter and sets up the execution environment.
- `run(self, command: str) -> dict`
  - Executes the given Python code and returns a dictionary with execution results.
  - Publishes `code_executed` event upon completion.

### EventSystem

Manages custom events and allows for callback subscriptions.

#### Methods

- `__init__(self)`
  - Initializes the event system.
- `subscribe(self, event_name: str, callback: Callable)`
  - Subscribes a callback to an event.
- `publish(self, event_name: str, *args, **kwargs)`
  - Publishes an event, calling all subscribed callbacks.

### CodeExecutionWidget

A widget that provides the code input area and toolbar with Run and Stop buttons.

#### Methods

- `__init__(self, python_interpreter: PythonInterpreter, parent=None)`
  - Initializes the CodeExecutionWidget and sets up the UI components, including the toolbar.
- `setup_ui(self)`
  - Sets up the user interface components, including the code input area and toolbar.
- `add_toolbar_buttons(self)`
  - Adds the Run and Stop buttons to the toolbar, configures button icons and hover effects.
- `execute_code(self)`
  - Executes the code in the code input area by starting a new thread for execution.
- `stop_execution(self)`
  - Stops the code execution thread if running.
- `on_execution_finished(self, result: dict)`
  - Handles the completion of code execution and publishes the `code_executed` event with the result.

## Usage

Refer to the User Guide for detailed instructions on how to use the various features of CodeGenius UI.

## Contributing

For information on contributing to the development of CodeGenius UI, please refer to the CONTRIBUTING.md file.
