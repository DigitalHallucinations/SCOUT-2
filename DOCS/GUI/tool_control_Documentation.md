# DOCS/tool_control_Documentation.md

## Overview

The `tool_control.py` file defines the `ToolControlBar` class, which provides a user interface component for managing various tools within the SCOUT application. The `ToolControlBar` includes buttons for accessing a VoIP application, an RSS feed portal, a browser, and a calendar. Each button has associated hover effects and actions to show or hide the respective tools.

## Table of Contents

1. [Imports](#imports)
2. [ToolControlBar Class](#toolcontrolbar-class)
    - [Initialization](#initialization)
    - [create_buttons Method](#create_buttons-method)
    - [show_feed_portal Method](#show_feed_portal-method)
    - [show_voip_app Method](#show_voip_app-method)
    - [show_browser Method](#show_browser-method)
    - [show_calendar Method](#show_calendar-method)

## Imports

The script imports necessary modules from the PySide6 library to create graphical user interface (GUI) components and handle events.

## ToolControlBar Class

### Initialization

The `ToolControlBar` class constructor initializes the tool control bar with various parameters such as parent, VoIP application, feed portal, browser, and calendar. It sets up the appearance of the control bar and calls the `create_buttons` method to add buttons for each tool.

1. **Attributes**: Initializes attributes for the VoIP application, feed portal, browser, and calendar.
2. **Appearance**: Sets the height and style of the control bar, including background color and border radius.
3. **Layout**: Configures the horizontal layout with margins and spacing.

### create_buttons Method

The `create_buttons` method sets up the buttons for each tool, including VoIP, RSS feed portal, browser, and calendar. Each button is configured with an icon, hover effects, and a click action.

1. **VoIP Button**:
    - **Icon**: Sets the initial icon and size for the button.
    - **Hover Effect**: Changes the icon when the button is hovered over.
    - **Click Action**: Connects the button to the `show_voip_app` method.

2. **RSS Button**:
    - **Icon**: Sets the initial icon and size for the button.
    - **Hover Effect**: Changes the icon when the button is hovered over.
    - **Click Action**: Connects the button to the `show_feed_portal` method.

3. **Browser Button**:
    - **Icon**: Sets the initial icon and size for the button.
    - **Hover Effect**: Changes the icon when the button is hovered over.
    - **Click Action**: Connects the button to the `show_browser` method.

4. **Calendar Button**:
    - **Icon**: Sets the initial icon and size for the button.
    - **Hover Effect**: Changes the icon when the button is hovered over.
    - **Click Action**: Connects the button to the `show_calendar` method.

5. **Layout Stretch**: Adds a stretchable space at the end of the layout to ensure proper alignment of the buttons.

### show_feed_portal Method

The `show_feed_portal` method displays the RSS feed portal and hides the other tools (VoIP application, browser, and calendar). This ensures that only one tool is visible at a time.

### show_voip_app Method

The `show_voip_app` method displays the VoIP application and hides the other tools (RSS feed portal, browser, and calendar).

### show_browser Method

The `show_browser` method displays the browser and hides the other tools (VoIP application, RSS feed portal, and calendar).

### show_calendar Method

The `show_calendar` method displays the calendar and hides the other tools (VoIP application, RSS feed portal, and browser).

## Summary

The `tool_control.py` file defines the `ToolControlBar` class, which provides a user interface component for managing various tools within the SCOUT application. The class includes methods for creating buttons for each tool, handling hover effects, and switching between tools. This ensures that the user can easily access and switch between different functionalities like VoIP, RSS feeds, browsing, and calendar management.