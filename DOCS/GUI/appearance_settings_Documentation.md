# DOCS/appearance_settings_Documentation

## Overview

The `appearance_settings.py` file defines the `AppearanceSettings` class, which provides a user interface for customizing the appearance settings of the SCOUT application. This includes setting the font style, font size, font color, and other UI-related properties. It also allows users to configure certain chat-related settings such as temperature, top-p, and top-k for language model responses.

## Table of Contents

1. [Imports](#imports)
2. [AppearanceSettings Class](#appearancesettings-class)
    - [Initialization](#initialization)
    - [create_appearance_widgets Method](#create_appearance_widgets-method)
    - [save_font_settings Method](#save_font_settings-method)
    - [load_appearance_settings Method](#load_appearance_settings-method)
    - [update_window_font Method](#update_window_font-method)
    - [set_font_size Method](#set_font_size-method)
    - [set_font_family Method](#set_font_family-method)
    - [update_font_size Method](#update_font_size-method)
    - [choose_font_color Method](#choose_font_color-method)
    - [update_font_color Method](#update_font_color-method)
    - [apply_message_box_style Method](#apply_message_box_style-method)
    - [update_chat_component Method](#update_chat_component-method)
    - [show_font_style_menu Method](#show_font_style_menu-method)

## Imports

The script imports necessary modules from the PySide6 library to create graphical user interface (GUI) components and handle logging.

## AppearanceSettings Class

### Initialization

The `AppearanceSettings` class constructor initializes the appearance settings dialog with parameters for the parent widget and user. It sets up the initial appearance settings, including background color and font settings, by calling the `load_appearance_settings` method. It then creates the various widgets for the appearance settings window by calling the `create_appearance_widgets` method.

1. **Attributes**: Initializes attributes such as appearance settings, font settings, and user-related information.
2. **UI Setup**: Sets the background color and initializes font settings.
3. **Widget Creation**: Calls `create_appearance_widgets` to set up the appearance settings widgets.

### create_appearance_widgets Method

The `create_appearance_widgets` method sets up the various widgets for the appearance settings window. This includes buttons for selecting font style and font color, a spinbox for adjusting font size, and spinboxes for configuring chat settings such as temperature, top-p, and top-k.

1. **Font Style Frame and Button**: Creates a frame and button for selecting the font style. The button displays a menu with available font families.
2. **Font Color Frame and Button**: Creates a frame and button for selecting the font color. The button opens a color picker dialog.
3. **Font Size Frame and Spinbox**: Creates a frame and spinbox for adjusting the font size.
4. **LLM Settings**: Creates frames and spinboxes for adjusting temperature, top-p, and top-k settings.
5. **Layout**: Adds all the created widgets to the main layout of the dialog.

### save_font_settings Method

The `save_font_settings` method saves the current font settings (font family, size, and color) to a configuration file (`config.ini`). This ensures that the user's customizations are preserved across sessions.

### load_appearance_settings Method

The `load_appearance_settings` method loads the font and appearance settings from a configuration file (`config.ini`). It returns a tuple of settings including font family, size, color, and various other appearance-related properties.

### update_window_font Method

The `update_window_font` method updates the font settings of the appearance settings window and its child widgets. It sets the font family, size, and color for all relevant widgets.

### set_font_size Method

The `set_font_size` method updates the font size based on the value selected in the font size spinbox. It calls `update_window_font` to apply the new font size and `save_font_settings` to save the change.

### set_font_family Method

The `set_font_family` method updates the font family based on the selected font from the font style menu. It updates the font style button text, calls `update_window_font` to apply the new font family, and saves the change using `save_font_settings`.

### update_font_size Method

The `update_font_size` method updates the font size based on the value provided. It calls `update_window_font` to apply the new font size and `save_font_settings` to save the change.

### choose_font_color Method

The `choose_font_color` method opens a color picker dialog to allow the user to select a font color. If a valid color is selected, it updates the font color and calls `update_font_color`.

### update_font_color Method

The `update_font_color` method updates the font color based on the selected color. It calls `update_window_font` to apply the new font color and saves the change using `save_font_settings`.

### apply_message_box_style Method

The `apply_message_box_style` method applies custom styles to message boxes, ensuring they match the appearance settings configured by the user.

### update_chat_component Method

The `update_chat_component` method updates the chat component settings based on the values of the temperature, top-p, and top-k spinboxes. It assigns these values to the parent window's attributes.

### show_font_style_menu Method

The `show_font_style_menu` method displays a menu with available font families. When a font family is selected, it calls `set_font_family` to update the font settings.

## Summary

The `appearance_settings.py` file defines the `AppearanceSettings` class, which provides a user interface for customizing the appearance settings of the SCOUT application. The class includes methods for setting the font style, size, and color, as well as configuring chat settings such as temperature, top-p, and top-k. These settings are saved to and loaded from a configuration file to ensure persistence across sessions. The class also includes methods for applying custom styles to message boxes and updating the chat component with the configured settings.