## Module: gui/tool_control.py

This module defines the `ToolControlBar` class, which is a custom Qt widget for a control bar in a GUI application. The control bar includes buttons for different functionalities such as VOIP, RSS feed, browser, and calendar. Each button changes its icon on hover and triggers the display of the corresponding application section.

---

# Imports:

- **PySide6.QtWidgets**
  - QtWidgets: Provides classes for creating a user interface.
- **PySide6.QtGui**
  - QtGui: Provides classes for window system integration, event handling, 2D graphics, basic imaging, and fonts.
- **PySide6.QtCore**
  - qtc: Provides core non-GUI functionality.

---

## Class: ToolControlBar

### Constructor
### Method: `__init__`

The constructor initializes the `ToolControlBar` widget, setting up its appearance, layout, and interactive elements. It creates buttons for VOIP, RSS feed, browser, and calendar functionalities, each with specific hover effects and click actions.

- **Parameters:**
  - `parent` (QtWidgets.QWidget, optional): The parent widget of the `ToolControlBar`.
  - `voip_app` (QtWidgets.QWidget, optional): The widget representing the VOIP application section.
  - `feed_portal` (QtWidgets.QWidget, optional): The widget representing the RSS feed portal section.
  - `browser` (QtWidgets.QWidget, optional): The widget representing the browser section.
  - `calendar` (QtWidgets.QWidget, optional): The widget representing the calendar section.

- **Returns:** None.

### Methods

## Method: `show_feed_portal`

This method displays the RSS feed portal section and hides the VOIP, browser, and calendar sections.

- **Parameters:** None.
- **Returns:** None.
  
**Example usage:**

```python
tool_control_bar.show_feed_portal()
```

## Method: `show_voip_app`

This method displays the VOIP application section and hides the RSS feed portal, browser, and calendar sections.

- **Parameters:** None.
- **Returns:** None.
  
**Example usage:**

```python
tool_control_bar.show_voip_app()
```

## Method: `show_browser`

This method displays the browser section and hides the VOIP, RSS feed portal, and calendar sections.

- **Parameters:** None.
- **Returns:** None.
  
**Example usage:**

```python
tool_control_bar.show_browser()
```

## Method: `show_calendar`

This method displays the calendar section and hides the browser, VOIP, and RSS feed portal sections.

- **Parameters:** None.
- **Returns:** None.
  
**Example usage:**

```python
tool_control_bar.show_calendar()
```

---

### Functions

This module does not contain any standalone functions.

---
