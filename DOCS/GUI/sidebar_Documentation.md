# DOCS/sidebar_Documentation.md

## Overview

The `sidebar.py` file defines the `Sidebar` class, which provides a user interface component for the SCOUT application. The sidebar allows users to switch between different personas, select language model providers and models, access chat history, and navigate to settings. The class includes various methods for creating and managing the sidebar's buttons and menus.

## Table of Contents

1. [Imports](#imports)
2. [Sidebar Class](#sidebar-class)
    - [Initialization](#initialization)
    - [load_providers](#load_providers)
    - [set_provider](#set_provider)
    - [populate_models_menu](#populate_models_menu)
    - [check_current_model](#check_current_model)
    - [set_model_and_update_button](#set_model_and_update_button)
    - [fetch_models_google_wrapper](#fetch_models_google_wrapper)
    - [fetch_models_openai_wrapper](#fetch_models_openai_wrapper)
    - [show_model_context_menu](#show_model_context_menu)
    - [fetch_model_details](#fetch_model_details)
    - [do_nothing](#do_nothing)
    - [show_providers_menu](#show_providers_menu)
    - [show_fetch_models_menu](#show_fetch_models_menu)
    - [apply_font_settings](#apply_font_settings)
    - [create_sidebar](#create_sidebar)
    - [Button Hover Effects](#button-hover-effects)
    - [handle_history_button](#handle_history_button)
    - [show_chat_page](#show_chat_page)
    - [show_persona_menu](#show_persona_menu)
    - [on_persona_selection](#on_persona_selection)
    - [show_settings_page](#show_settings_page)

## Imports

The script imports necessary modules for asynchronous operations, JSON handling, and PySide6 components for creating the graphical user interface (GUI). It also imports various functions for tooltips, chat history, and model fetching, as well as a logger for logging events.

## Sidebar Class

### Initialization

The `Sidebar` class constructor initializes the sidebar with various parameters such as parent, personas, and appearance settings. It sets up the sidebar layout and loads the available language model providers.

1. **Attributes**: Initializes attributes like personas, sidebar appearance settings, language model providers, and references to the chat component, model manager, and conversation manager.
2. **Load Providers**: Calls the `load_providers` method to load available language model providers from a JSON file.
3. **Create Sidebar**: Calls the `create_sidebar` method to set up the sidebar layout and buttons.

### load_providers

The `load_providers` method reads the list of available language model providers from a JSON file (`providers.json`) and stores it in the `llm_providers` attribute.

### set_provider

The `set_provider` method sets the current language model provider and updates the provider in the chat component's provider manager. It also updates the model manager with a default model for the selected provider and calls `populate_models_menu` to refresh the models menu.

### populate_models_menu

The `populate_models_menu` method populates the models menu with available models for the selected language model provider. It reads the models from a JSON file specific to the provider and creates menu items for each model, including options to select or view details about the model.

### check_current_model

The `check_current_model` method checks if the current model set in the model manager matches the model displayed on the sidebar's models button. It logs the result for debugging purposes.

### set_model_and_update_button

The `set_model_and_update_button` method sets the selected model in the model manager and updates the text of the models button to reflect the selected model. It also calls `check_current_model` to verify the model selection.

### fetch_models_google_wrapper

The `fetch_models_google_wrapper` method creates an asynchronous task to fetch available models from Google. It passes the chat log to the `fetch_models_google` function.

### fetch_models_openai_wrapper

The `fetch_models_openai_wrapper` method creates an asynchronous task to fetch available models from OpenAI. It handles logging and error management for the task.

### show_model_context_menu

The `show_model_context_menu` method displays a context menu for the selected model when the user right-clicks on the models menu.

### fetch_model_details

The `fetch_model_details` method creates an asynchronous task to fetch details about the selected model. It handles logging and error management for the task.

### do_nothing

A placeholder method that does nothing. It can be used for future expansion or as a default callback.

### show_providers_menu

The `show_providers_menu` method creates and displays a menu with available language model providers. It sets up actions for each provider, allowing the user to switch between them.

### show_fetch_models_menu

The `show_fetch_models_menu` method displays the models menu for the selected provider. It ensures the menu is populated with the latest models.

### apply_font_settings

The `apply_font_settings` method applies the specified font settings to the sidebar buttons, ensuring consistency in appearance based on the user's preferences.

### create_sidebar

The `create_sidebar` method sets up the sidebar layout and adds buttons for various actions, including switching providers, selecting models, viewing chat history, accessing chat, changing personas, and opening settings. It also applies hover effects to the buttons.

### Button Hover Effects

Methods for handling hover events on the sidebar buttons, changing their icons and displaying tooltips to provide feedback to the user.

### handle_history_button

The `handle_history_button` method loads the chat history using the `load_chat_history` function from `chist_functions`.

### show_chat_page

The `show_chat_page` method switches the view to the chat page in the main application interface.

### show_persona_menu

The `show_persona_menu` method displays a menu with available personas, allowing the user to switch between different personas.

### on_persona_selection

The `on_persona_selection` method handles the selection of a persona, updating the chat component with the selected persona's settings and messages.

### show_settings_page

The `show_settings_page` method switches the view to the settings page in the main application interface.

## Summary

The `sidebar.py` file defines the `Sidebar` class, which provides a user interface for managing different aspects of the SCOUT application, such as switching between personas, selecting language model providers and models, accessing chat history, and navigating to settings. The class includes various methods for creating and managing the sidebar's buttons and menus, handling hover effects, and updating the chat component based on user interactions.