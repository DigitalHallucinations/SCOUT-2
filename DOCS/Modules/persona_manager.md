# DOCS/persona_manager_documentation.md

## Overview

The `persona_manager.py` file defines the `PersonaManager` class, which is responsible for managing personas within the application. This includes loading persona data from a JSON file, personalizing personas based on user-specific data, and updating the current persona when a user selects a new one.

## Table of Contents

1. [Imports](#imports)
2. [PersonaManager Class](#personamanager-class)
    - [Initialization](#initialization)
    - [Updating Persona](#updating-persona)
    - [Personalizing Persona](#personalizing-persona)
    - [Loading Personas](#loading-personas)
    - [Showing Message](#showing-message)

## Imports

The script imports necessary modules for file operations, JSON handling, user data management, and logging.

## PersonaManager Class

The `PersonaManager` class manages the personas in the application, allowing for loading, updating, and personalizing personas based on user data.

### Initialization

The `__init__` method initializes the `PersonaManager` with references to the master application and the current user. It sets a default persona name ("SCOUT"), loads personas from a JSON file, and personalizes the default persona with user-specific data.

### Updating Persona

The `updater` method updates the persona when a new one is selected. It changes the system name and updates the conversation ID in the master application, ensuring the change is reflected in the application state.

### Personalizing Persona

The `personalize_persona` method customizes the persona's content by replacing placeholders with user-specific data, such as name, profile, and system info. It returns the personalized persona, which is tailored to the current user.

### Loading Personas

The `load_personas` method loads persona definitions from a specified JSON file. It reads the file and initializes the `personas` attribute with the loaded data. This method handles errors such as file not found or invalid JSON format by logging appropriate error messages and initializing an empty personas list.

### Showing Message

The `show_message` method displays a message in the chat component of the application. It checks if the chat component exists in the master application and uses it to show the message. This ensures that messages related to persona changes are communicated to the user through the chat interface.

## Summary

The `persona_manager.py` file defines a class that manages personas within the application. It handles loading personas from a JSON file, personalizing them with user-specific data, updating the current persona based on user selection, and displaying related messages in the chat component. The class ensures that personas are dynamically tailored to the user's context, enhancing the application's interactive capabilities.