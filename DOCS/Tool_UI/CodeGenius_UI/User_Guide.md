# CodeGenius UI User Guide

## Table of Contents

1. [Accessing CodeGenius UI](#accessing-codegenius-ui)
2. [Interface Overview](#interface-overview)
3. [Writing and Executing Code](#writing-and-executing-code)
4. [Viewing Results](#viewing-results)
5. [Understanding the Status Bar](#understanding-the-status-bar)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)

## Accessing CodeGenius UI

1. Open the SCOUT application.
2. Look for the tool control bar, usually located at the top of the interface.
3. Click on the "CodeGenius" button to open the CodeGenius UI.

## Interface Overview

The CodeGenius UI consists of four main areas:

1. **Code Editor**: A text editor where you can write your Python code, featuring line numbers and syntax highlighting.
2. **Toolbar**: Located below the code editor, includes Run and Stop buttons for managing code execution.
3. **Output Display**: Shows the results of your executed code.
4. **Status Bar**: Displays information about the code's asynchronous status and execution state.

## Writing and Executing Code

1. Click on the code editor area.
2. Type or paste your Python code. The editor provides line numbers and syntax highlighting for better readability.
3. Click the "Run" button on the toolbar to execute your code.

Example:

```python
print("Hello, CodeGenius!")
```

### Stopping Code Execution

If you need to stop the execution of your code, click the "Stop" button on the toolbar.

## Viewing Results

After executing your code:

1. The output will appear in the output display area below the code editor.
2. Text output will be shown as plain text.
3. Errors, if any, will be displayed in the output area.

## Understanding the Status Bar

The status bar at the bottom of the CodeGenius UI provides two key pieces of information:

1. **Async Status**: Indicates whether the current code in the editor is asynchronous.
   - "Async: No" for regular synchronous code.
   - "Async: Yes" for code containing asynchronous elements (e.g., `async def`, `await`).

2. **Execution Status**: Shows the current state of code execution.
   - "Status: Ready" when no code is running.
   - "Status: Running" when code is being executed.
   - "Status: Stopped" if execution was manually stopped.
   - "Status: Finished" when code execution is complete.

## Tips and Best Practices

- Use the line numbers to easily reference specific parts of your code.
- Take advantage of the syntax highlighting to identify different elements in your code quickly.
- Pay attention to the Async Status in the status bar when working with asynchronous code.
- Use the Stop button responsibly; stopping long-running or resource-intensive tasks may take a moment to complete.

## Troubleshooting

- If your code doesn't execute, check for syntax errors highlighted by the editor.
- Ensure you're not importing modules that aren't available in the CodeGenius environment.
- If the UI becomes unresponsive during code execution, use the Stop button and try breaking your code into smaller parts.
- For persistent issues, check the SCOUT application logs or contact support.