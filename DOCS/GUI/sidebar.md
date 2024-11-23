## Module: gui/sidebar.py

This module defines the Sidebar class, which is a Qt-based graphical user interface (GUI) component for managing large language model (LLM) providers and models in a chatbot application. The sidebar allows users to switch between different LLM providers, select specific models, view model details, and navigate various components of the chat interface.

---

# Imports:

- `asyncio`: Standard library for asynchronous programming.
- `json`: Standard library for JSON manipulation.
- `PySide6.QtWidgets`: Qt library for creating GUI elements.
- `PySide6.QtGui`: Qt library for GUI-related functions.
- `PySide6.QtCore`: Qt library for core functionalities.
- `gui.tooltip.ToolTip`: Custom module for tooltips.
- `gui.chist_functions as cf`: Custom module for chat history functions.
- `gui.fetch_models.OA_fetch_models.fetch_models_openai`: Function to fetch models from OpenAI.
- `gui.fetch_models.GG_fetch_models.fetch_models_google, fetch_model_details`: Functions to fetch models and details from Google.
- `modules.logging.logger.setup_logger`: Custom module for setting up logging.

---

## Class: Sidebar

### Constructor
**Method:** `__init__`

Initializes the Sidebar class, setting up the user interface components and loading available LLM providers.

- **Parameters:**
  - `parent` (QtWidgets.QWidget, optional): The parent widget of the sidebar.
  - `personas` (list, optional): List of persona configurations.
  - `sidebar_frame_bg` (str, optional): Background color of the sidebar frame.
  - `sidebar_font_color` (str, optional): Font color of the sidebar text.
  - `sidebar_font_size` (int, optional): Font size of the sidebar text.
  - `sidebar_font_family` (str, optional): Font family of the sidebar text.
  - `model_manager` (object, optional): Manager for handling model selection and configuration.
  - `conversation_manager` (object, optional): Manager for handling conversation logic.

- **Returns:** None.

---

### Methods

## Method: `load_providers`

Loads the available LLM providers from a JSON file.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.load_providers()
```

## Method: `set_provider`

Sets the current LLM provider and updates the UI and model manager accordingly.

- **Parameters:**
  - `llm_provider` (str, required): The name of the LLM provider to set.

- **Returns:** None.

**Example usage:**
```python
sidebar.set_provider('OpenAI')
```

## Method: `populate_models_menu`

Populates the models menu with available models for the current LLM provider.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.populate_models_menu()
```

## Method: `check_current_model`

Checks if the currently selected model matches the model displayed in the UI.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.check_current_model()
```

## Method: `set_model_and_update_button`

Sets the selected model and updates the corresponding button in the UI.

- **Parameters:**
  - `model` (str, required): The name of the model to set.

- **Returns:** None.

**Example usage:**
```python
sidebar.set_model_and_update_button('gpt-4o')
```

## Method: `fetch_models_google_wrapper`

Fetches models from Google asynchronously.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.fetch_models_google_wrapper()
```

## Method: `fetch_models_openai_wrapper`

Fetches models from OpenAI asynchronously.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.fetch_models_openai_wrapper()
```

## Method: `show_model_context_menu`

Displays the context menu for a selected model.

- **Parameters:**
  - `pos` (QtCore.QPoint, required): The position to show the context menu.

- **Returns:** None.

**Example usage:**
```python
sidebar.show_model_context_menu(position)
```

## Method: `fetch_model_details`

Fetches detailed information about a specific model.

- **Parameters:**
  - `chat_log` (object, required): The chat log object.
  - `model_name` (str, required): The name of the model to fetch details for.

- **Returns:** None.

**Example usage:**
```python
sidebar.fetch_model_details(chat_log, 'gpt-4o')
```

## Method: `do_nothing`

A placeholder method that does nothing.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.do_nothing()
```

## Method: `show_providers_menu`

Displays the providers menu.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.show_providers_menu()
```

## Method: `show_fetch_models_menu`

Displays the models menu.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.show_fetch_models_menu()
```

## Method: `apply_font_settings`

Applies the specified font settings to the sidebar components.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.apply_font_settings()
```

## Method: `create_sidebar`

Creates and sets up the sidebar UI components.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.create_sidebar()
```

## Method: `on_providers_button_hover`

Handles the hover event for the providers button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_providers_button_hover(event)
```

## Method: `on_providers_button_leave`

Handles the leave event for the providers button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_providers_button_leave(event)
```

## Method: `on_models_button_hover`

Handles the hover event for the models button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_models_button_hover(event)
```

## Method: `on_models_button_leave`

Handles the leave event for the models button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_models_button_leave(event)
```

## Method: `on_history_button_hover`

Handles the hover event for the history button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_history_button_hover(event)
```

## Method: `on_history_button_leave`

Handles the leave event for the history button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_history_button_leave(event)
```

## Method: `handle_history_button`

Handles the click event for the history button.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.handle_history_button()
```

## Method: `on_chat_button_hover`

Handles the hover event for the chat button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_chat_button_hover(event)
```

## Method: `on_chat_button_leave`

Handles the leave event for the chat button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_chat_button_leave(event)
```

## Method: `show_chat_page`

Displays the chat page.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.show_chat_page()
```

## Method: `on_persona_button_hover`

Handles the hover event for the persona button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_persona_button_hover(event)
```

## Method: `on_persona_button_leave`

Handles the leave event for the persona button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_persona_button_leave(event)
```

## Method: `show_persona_menu`

Displays the persona selection menu.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.show_persona_menu()
```

## Method: `on_persona_selection`

Handles the persona selection event asynchronously.

- **Parameters:**
  - `persona_name` (str, required): The name of the selected persona.

- **Returns:** None.

**Example usage:**
```python
await sidebar.on_persona_selection('default')
```

## Method: `on_settings_button_hover`

Handles the hover event for the settings button.

- **Parameters:**
  - `event` (QtCore.QEvent

, required): The hover event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_settings_button_hover(event)
```

## Method: `on_settings_button_leave`

Handles the leave event for the settings button.

- **Parameters:**
  - `event` (QtCore.QEvent, required): The leave event.

- **Returns:** None.

**Example usage:**
```python
sidebar.on_settings_button_leave(event)
```

## Method: `show_settings_page`

Displays the settings page.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**
```python
sidebar.show_settings_page()
```
