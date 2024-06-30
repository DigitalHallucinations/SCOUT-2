## Module: `speech_bar.py`
The `speech_bar.py` module is responsible for managing the speech bar component of the GUI, enabling functionalities related to speech-to-text and text-to-speech. It provides the interface for users to select speech providers, voices, and toggle between different speech functionalities. The module integrates various services, including Google's text-to-speech and speech-to-text services, and manages these interactions through a unified user interface.

---

# Imports:

- `datetime` (standard library): For logging timestamps.
- `PySide6.QtWidgets` (third-party library): Provides the necessary GUI components for creating the speech bar.
- `PySide6.QtGui` (third-party library): Provides the graphical components and utilities.
- `PySide6.QtCore` (third-party library): Core functionalities for PySide6.
- `QMessageBox` (third-party library): For displaying message boxes.
- `ToolTip` (internal module): Manages tooltip display.
- `SpeechToText` (internal module): Manages speech-to-text functionality.
- `ProviderManager` (internal module): Manages different speech providers and their settings.
- `texttospeech` (Google Cloud library): Provides Google's text-to-speech capabilities.
- `setup_logger` (internal module): Sets up logging for the module.

---

## Class: `SpeechBar`

### Constructor  
**Method: `__init__`**

The constructor initializes the `SpeechBar` class, setting up the necessary components and configurations for the speech bar. It configures the appearance, initializes speech services, and sets up the provider manager to handle different speech providers.

- **Parameters:**
  - `parent` (optional): The parent widget of the speech bar.
  - `model_manager` (optional): Manages the model associated with the speech bar.
  - `speechbar_frame_bg` (optional): Background color for the speech bar frame.
  - `speechbar_font_color` (optional): Font color for the speech bar.
  - `speechbar_font_family` (optional): Font family for the speech bar.
  - `speechbar_font_size` (optional): Font size for the speech bar.
- **Returns:** None.

### Methods

## Method: `create_speech_bar`

Creates and configures the speech bar's GUI components, including buttons for selecting speech providers and voices, and toggling text-to-speech and speech-to-text functionalities.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar = SpeechBar(parent, model_manager, "#fff", "#000", "Arial", 12)
speech_bar.create_speech_bar()
```

---

## Method: `show_speech_provider_menu`

Displays a menu for selecting the speech provider.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.show_speech_provider_menu()
```

---

## Method: `on_speech_provider_selection`

Handles the selection of a speech provider and updates the speech provider button.

- **Parameters:**
  - `speech_provider` (str, required): The selected speech provider.
- **Returns:** None.

**Example usage:**


speech_bar.on_speech_provider_selection("Google")
```

---

## Method: `toggle_tts`

Toggles the text-to-speech functionality on or off.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.toggle_tts()
```

---

## Method: `populate_voice_menu`

Populates the voice menu based on the selected speech provider.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.populate_voice_menu()
```

---

## Method: `populate_google_voice_menu`

Populates the voice menu with Google voices.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.populate_google_voice_menu()
```

---

## Method: `populate_eleven_labs_voice_menu`

Populates the voice menu with Eleven Labs voices.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.populate_eleven_labs_voice_menu()
```

---

## Method: `show_voice_menu`

Displays the voice menu.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.show_voice_menu()
```

---

## Method: `on_voice_selection`

Handles the selection of a voice and updates the voice button.

- **Parameters:**
  - `voice` (dict, required): The selected voice.
- **Returns:** None.

**Example usage:**


speech_bar.on_voice_selection(voice)
```

---

## Method: `toggle_listen`

Toggles the speech-to-text listening functionality on or off.

- **Parameters:** None.
- **Returns:** None.

**Example usage:**


speech_bar.toggle_listen()
```

---

## Method: `on_microphone_button_hover`

Handles the hover event for the microphone button.

- **Parameters:**
  - `event` (QEvent, required): The hover event.
- **Returns:** None.

**Example usage:**


speech_bar.on_microphone_button_hover(event)
```

---

## Method: `on_microphone_button_leave`

Handles the leave event for the microphone button.

- **Parameters:**
  - `event` (QEvent, required): The leave event.
- **Returns:** None.

**Example usage:**


speech_bar.on_microphone_button_leave(event)
```

---

## Method: `on_tts_button_hover`

Handles the hover event for the text-to-speech button.

- **Parameters:**
  - `event` (QEvent, required): The hover event.
- **Returns:** None.

**Example usage:**


speech_bar.on_tts_button_hover(event)
```

---

## Method: `on_tts_button_leave`

Handles the leave event for the text-to-speech button.

- **Parameters:**
  - `event` (QEvent, required): The leave event.
- **Returns:** None.

**Example usage:**


speech_bar.on_tts_button_leave(event)
