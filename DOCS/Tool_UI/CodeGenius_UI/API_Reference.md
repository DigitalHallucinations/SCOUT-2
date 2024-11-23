# CodeGenius UI API Reference

## CodeEditor

### Class: CodeEditor(QPlainTextEdit)

#### Methods

`__init__(self, parent=None)`
- Initializes the CodeEditor widget
- Sets up line numbering and syntax highlighting

`lineNumberAreaWidth(self) -> int`
- Calculates and returns the width of the line number area

`updateLineNumberAreaWidth(self, _)`
- Updates the viewport margins to accommodate the line number area

`updateLineNumberArea(self, rect: QRect, dy: int)`
- Updates the line number area when the editor's viewport has changed

`resizeEvent(self, event: QResizeEvent)`
- Handles resize events to adjust the line number area

`lineNumberAreaPaintEvent(self, event: QPaintEvent)`
- Paints the line numbers in the line number area

`highlightCurrentLine(self)`
- Highlights the current line in the editor

## CodeExecutionWidget

### Class: CodeExecutionWidget(QFrame)

#### Methods

`__init__(self, python_interpreter: PythonInterpreter, parent=None)`
- Initializes the CodeExecutionWidget
- Sets up the UI components including CodeEditor and toolbar

`setup_ui(self)`
- Sets up the user interface components

`add_toolbar_buttons(self)`
- Adds and configures the Run and Stop buttons

`execute_code(self)`
- Initiates code execution in a separate thread

`stop_execution(self)`
- Stops the currently running code execution

`on_execution_finished(self, result: dict)`
- Handles the completion of code execution
- Publishes the `code_executed` event with the result

## CodeGeniusUI

### Class: CodeGeniusUI(QWidget)

#### Methods

`__init__(self)`
- Initializes the CodeGeniusUI widget
- Sets up the UI and subscribes to relevant events

`setup_ui(self)`
- Sets up the overall user interface layout

`on_code_executed(self, code: str, result: dict)`
- Handles the `code_executed` event
- Updates the UI with execution results

`update_async_indicator(self, is_async: bool)`
- Updates the async status indicator in the UI

`update_execution_status(self, status: str)`
- Updates the execution status indicator in the UI

`show(self)`
- Shows the CodeGeniusUI widget
- Overrides QWidget.show() to include logging

`hide(self)`
- Hides the CodeGeniusUI widget
- Overrides QWidget.hide() to include logging

## Event System

### Events

`code_executed`
- Published when code execution is complete
- Parameters: `code` (str), `result` (dict)

`async_status_changed`
- Published when the async status of the code changes
- Parameters: `is_async` (bool)

`execution_status_changed`
- Published when the execution status changes
- Parameters: `status` (str)

For more detailed information on usage and implementation, please refer to the User Guide and Technical Documentation.