# DOCS/speech_bar_Documentation.md

## Overview

The `speech_bar.py` file defines the `SpeechBar` class, which is responsible for handling speech-to-text (STT) and text-to-speech (TTS) functionalities within the SCOUT application. This class provides a user interface component that allows users to toggle these features, select speech providers, and choose voices for TTS.

## Table of Contents

1. [Imports](#imports)
2. [SpeechBar Class](#speechbar-class)
    - [Initialization](#initialization)
    - [create_speech_bar](#create_speech_bar)
    - [show_speech_provider_menu](#show_speech_provider_menu)
    - [on_speech_provider_selection](#on_speech_provider_selection)
    - [toggle_tts](#toggle_tts)
    - [populate_voice_menu](#populate_voice_menu)
    - [populate_google_voice_menu](#populate_google_voice_menu)
    - [populate_eleven_labs_voice_menu](#populate_eleven_labs_voice_menu)
    - [show_voice_menu](#show_voice_menu)
    - [on_voice_selection](#on_voice_selection)
    - [toggle_listen](#toggle_listen)
    - [Button Hover Effects](#button-hover-effects)

## Imports

The script imports necessary modules for date and time operations, PySide6 components for creating the graphical user interface (GUI), and custom modules for tooltips, speech services, provider management, and logging.

## SpeechBar Class

### Initialization

The `SpeechBar` class constructor initializes the speech bar with various parameters such as parent, model manager, and appearance settings. It sets up the speech-to-text functionality, provider manager, and calls `create_speech_bar` to configure the UI elements.

1. **Attributes**: Initializes attributes like the model manager, appearance settings, and speech-to-text service.
2. **Provider Manager**: Initializes the provider manager and loads available TTS voices.
3. **UI Setup**: Calls the `create_speech_bar` method to set up the speech bar layout and buttons.

### create_speech_bar

The `create_speech_bar` method sets up the main UI elements of the speech bar, including buttons for selecting speech providers, choosing voices, toggling TTS, and starting/stopping speech-to-text.

1. **Speech Provider Button**: Creates a button for selecting the speech provider and sets up its menu.
2. **Voice Button**: Creates a button for selecting a voice for TTS and sets up its menu.
3. **TTS Toggle Button**: Creates a button for toggling TTS on or off.
4. **Microphone Button**: Creates a button for starting and stopping speech-to-text.

### show_speech_provider_menu

The `show_speech_provider_menu` method creates and displays a menu with available speech providers. Users can select a provider from this menu.

### on_speech_provider_selection

The `on_speech_provider_selection` method handles the selection of a speech provider. It updates the provider manager with the selected provider and refreshes the voice menu to display voices available for the new provider.

### toggle_tts

The `toggle_tts` method toggles the TTS functionality on or off. It updates the provider manager and changes the icon on the TTS toggle button to reflect the current state.

### populate_voice_menu

The `populate_voice_menu` method populates the voice menu with available voices for the current speech provider. It calls specific methods to handle different providers like Google and Eleven Labs.

### populate_google_voice_menu

The `populate_google_voice_menu` method retrieves and adds available voices from Google to the voice menu.

### populate_eleven_labs_voice_menu

The `populate_eleven_labs_voice_menu` method retrieves and adds available voices from Eleven Labs to the voice menu.

### show_voice_menu

The `show_voice_menu` method displays the voice menu, allowing users to select a voice for TTS.

### on_voice_selection

The `on_voice_selection` method handles the selection of a voice for TTS. It updates the provider manager with the selected voice and updates the voice button text to reflect the chosen voice.

### toggle_listen

The `toggle_listen` method starts or stops the speech-to-text functionality. When started, it begins listening and transcribing audio input. When stopped, it transcribes the recorded audio and updates the message entry in the parent component with the transcribed text.

### Button Hover Effects

Methods for handling hover events on the speech bar buttons, changing their icons and displaying tooltips to provide feedback to the user.

- **on_microphone_button_hover**: Changes the microphone button icon and displays a tooltip when the user hovers over the button.
- **on_microphone_button_leave**: Restores the microphone button icon when the user stops hovering over the button.
- **on_tts_button_hover**: Changes the TTS button icon and displays a tooltip when the user hovers over the button.
- **on_tts_button_leave**: Restores the TTS button icon when the user stops hovering over the button.

## Summary

The `speech_bar.py` file defines the `SpeechBar` class, which provides a user interface for managing speech-to-text and text-to-speech functionalities in the SCOUT application. The class includes methods for creating and managing UI elements, handling speech provider and voice selection, toggling TTS, and starting/stopping speech-to-text. The class ensures seamless integration of speech services with the application's chat interface, enhancing user interaction through voice input and output.