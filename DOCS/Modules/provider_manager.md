# DOCS/provider_manager_documentation.md

## Overview

The `provider_manager.py` file defines the `ProviderManager` class, which is responsible for managing different providers used within the application. This includes switching between language models, speech providers, and handling related configurations.

## Table of Contents

1. [Imports](#imports)
2. [ProviderManager Class](#providermanager-class)
    - [Initialization](#initialization)
    - [Switching LLM Provider](#switching-llm-provider)
    - [Switching Speech Provider](#switching-speech-provider)
    - [Switching Background Provider](#switching-background-provider)
    - [Getting Current Providers](#getting-current-providers)
    - [Managing TTS](#managing-tts)
    - [Loading Voices](#loading-voices)
    - [Setting Voice](#setting-voice)

## Imports

The script imports necessary modules for logging and specific functionalities for text-to-speech services from Eleven Labs and Google Cloud Services.

## ProviderManager Class

The `ProviderManager` class manages various providers within the application, including language models, text-to-speech services, and background providers.

### Initialization

The `__init__` method initializes the `ProviderManager` class with references to the chat component and model manager. It sets default providers for language models, background services, and speech services, and initializes the TTS state and available voices.

### Switching LLM Provider

The `switch_llm_provider` method switches the language model provider to the specified provider. It imports the appropriate response generation module and sets the model in the `model_manager`. If an unknown provider is specified, it raises a `ValueError`.

### Switching Speech Provider

The `switch_speech_provider` method switches the speech provider to the specified provider. It imports the appropriate modules for handling text-to-speech functionalities and sets the current speech provider. If an unknown provider is specified, it raises a `ValueError`.

### Switching Background Provider

The `switch_background_provider` method sets the background provider to the specified provider and logs the switch. Additional setup for the background provider can be added if necessary.

### Getting Current Providers

The `get_current_speech_provider`, `get_current_model`, and `get_current_llm_provider` methods return the current speech provider, current model, and current LLM provider, respectively. These methods allow other components to retrieve the current configurations.

### Managing TTS

The `set_tts` and `get_tts` methods manage the text-to-speech (TTS) functionality. `set_tts` enables or disables TTS, while `get_tts` returns the current TTS status.

### Loading Voices

The `load_voices` method loads available voices from the current speech provider. It sets the `voices` attribute with the loaded voices and logs the operation.

### Setting Voice

The `set_voice` method sets the voice for the current speech provider. It calls the appropriate function to set the voice based on the current speech provider.

## Summary

The `provider_manager.py` file defines a class that manages various providers within the application, including language models and text-to-speech services. It allows switching between providers, managing TTS functionality, and handling voice configurations. This class ensures that the application can dynamically switch and configure different services as needed.