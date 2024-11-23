# CodeGenius UI Technical Documentation

## Architecture Overview

CodeGenius UI is built using the PySide6 framework, providing a rich set of tools for creating desktop applications with a modern look and feel. The architecture is designed to be modular and extensible, allowing for easy integration of new features.

## Key Components

### CodeEditor

A custom widget extending `QPlainTextEdit` that provides line numbering and syntax highlighting capabilities.

#### Key Methods:
- `lineNumberAreaWidth()`: Calculates the width of the line number area.
- `updateLineNumberAreaWidth(int)`: Updates the viewport margins to accommodate the line number area.
- `updateLineNumberArea(QRect, int)`: Updates the line number area when the editor's viewport has changed.
- `lineNumberAreaPaintEvent(QPaintEvent)`: Handles the painting of line numbers.
- `highlightCurrentLine()`: Highlights the current line in the editor.

### CodeExecutionWidget

Combines the CodeEditor with execution controls (Run and Stop buttons).

#### Key Methods:
- `setup_ui()`: Sets up the user interface components.
- `add_toolbar_buttons()`: Adds and configures the Run and Stop buttons.
- `execute_code()`: Initiates code execution in a separate thread.
- `stop_execution()`: Stops the currently running code execution.

### CodeExecutionThread

Manages the actual execution of code in a separate thread to prevent UI freezing.

#### Key Methods:
- `run_code()`: Executes the code using the Python interpreter and emits the result.

### CodeGeniusUI

The main user interface component that integrates various features of the CodeGenius environment.

#### Key Methods:
- `setup_ui()`: Sets up the overall user interface layout.
- `on_code_executed(str, dict)`: Handles the code execution result and updates the UI.
- `update_async_indicator(bool)`: Updates the async status in the UI.
- `update_execution_status(str)`: Updates the execution status in the UI.

## Event System

CodeGenius UI uses a custom event system to handle communication between components:

- `code_executed`: Emitted when code execution is complete, with the code and result.
- `async_status_changed`: Emitted when the async status of the code changes.
- `execution_status_changed`: Emitted when the execution status changes.

## Styling

The UI uses a dark theme with custom styles for each component, enhancing readability and providing a modern look. Styles are applied using Qt StyleSheets.

## Python Interpreter Integration

CodeGenius UI integrates with a custom Python interpreter that supports both synchronous and asynchronous code execution. The interpreter runs in a separate thread to prevent UI freezing during code execution.

## Future Considerations

1. **Code Completion**: Implement an intelligent code completion system.
2. **Debugging Tools**: Integrate step-by-step debugging capabilities.
3. **Multiple File Support**: Allow working with multiple files or projects simultaneously.
4. **Performance Optimization**: Implement caching mechanisms for frequently executed code snippets.
5. **Extended Library Support**: Pre-load additional common Python libraries.