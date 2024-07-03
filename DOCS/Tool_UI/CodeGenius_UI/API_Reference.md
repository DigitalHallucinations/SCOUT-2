# CodeGenius UI API Reference

## CodeGeniusUI

### Class: CodeGeniusUI

#### Methods

`__init__(self)`
- Initializes the CodeGeniusUI widget
- Subscribes to the `code_executed` event

`setup_ui(self)`
- Sets up the user interface components
- Creates code input and output display areas

`on_code_executed(self, code: str, result: dict)`
- Handles the `code_executed` event
- Updates the UI with execution results

`show(self)`
- Shows the CodeGeniusUI widget
- Overrides QWidget.show() to include logging

`hide(self)`
- Hides the CodeGeniusUI widget
- Overrides QWidget.hide() to include logging

## PythonInterpreter

### Class: PythonInterpreter

#### Methods

`__init__(self, ...)`
- Initializes the PythonInterpreter
- Sets up the execution environment

`run(self, command: str) -> dict`
- Executes the given Python code
- Returns a dictionary with execution results
- Publishes `code_executed` event

## EventSystem

### Class: EventSystem

#### Methods

`__init__(self)`
- Initializes the event system

`subscribe(self, event_name: str, callback: Callable)`
- Subscribes a callback to an event

`publish(self, event_name: str, *args, **kwargs)`
- Publishes an event, calling all subscribed callbacks

## ToolControlBar

### Class: ToolControlBar

#### Methods

`__init__(self, parent=None, ...)`
- Initializes the ToolControlBar
- Sets up buttons for different tools, including CodeGenius

`show_code_genius_ui(self)`
- Shows the CodeGeniusUI and hides other tools

## SCOUT

### Class: SCOUT

#### Methods

`__init__(self, shutdown_event=None)`
- Initializes the SCOUT application
- Creates instances of CodeGeniusUI and other components

`session_manager(self, user)`
- Manages user sessions
- Integrates CodeGeniusUI into the application layout

## CodeExecutionWidget

### Class: CodeExecutionWidget

#### Methods

`__init__(self, python_interpreter: PythonInterpreter, parent=None)`
- Initializes the CodeExecutionWidget
- Sets up the UI components, including the toolbar with Run and Stop buttons

`setup_ui(self)`
- Sets up the user interface components
- Creates the code input area and toolbar

`add_toolbar_buttons(self)`
- Adds the Run and Stop buttons to the toolbar
- Configures button icons and hover effects

`execute_code(self)`
- Executes the code in the code input area
- Starts a new thread for execution

`stop_execution(self)`
- Stops the code execution thread if running

`on_execution_finished(self, result: dict)`
- Handles the completion of code execution
- Publishes the `code_executed` event with the result

For more detailed information on usage and implementation, please refer to the User Guide and Technical Documentation.
