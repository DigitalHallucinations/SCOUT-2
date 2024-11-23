# DOCS/tts_documentation.md

## Overview

The `tts.py` file provides functions to interact with the Eleven Labs text-to-speech (TTS) service, including fetching available voices, setting a specific voice, and converting text to speech. It also includes utilities for playing audio files and managing TTS settings.

## Table of Contents

1. [Imports](#imports)
2. [Constants](#constants)
3. [Global Variables](#global-variables)
4. [Functions](#functions)
    - [play_audio](#play_audio)
    - [contains_code](#contains_code)
    - [get_voices](#get_voices)
    - [text_to_speech](#text_to_speech)
    - [set_voice](#set_voice)
    - [load_voices](#load_voices)
    - [get_voice](#get_voice)
    - [set_tts](#set_tts)
    - [get_tts](#get_tts)
    - [tts](#tts)
    - [test_tts](#test_tts)

## Imports

The script imports various modules for handling environment variables, HTTP requests, regular expressions, audio playback, threading, and logging. Additionally, it imports the `datetime` module for timestamp generation.

## Constants

- `CHUNK_SIZE`: Defines the chunk size for streaming audio data.

## Global Variables

- `_use_tts`: A boolean flag to indicate whether TTS is enabled or disabled.
- `VOICE_IDS`: A list to store available voice IDs fetched from the Eleven Labs API.

## Functions

### play_audio

Plays an audio file using the `pygame` library. This function initializes the mixer, loads the audio file, and plays it. It blocks until the audio playback is finished.

### contains_code

Checks if the provided text contains any code snippets. This is done by searching for `<code>` tags within the text.

### get_voices

Fetches available voices from the Eleven Labs API. It reads the API key from environment variables, sends a request to the API, and processes the response to extract voice IDs and names. The function logs the result and returns a list of voice data.

### text_to_speech

An asynchronous function that converts text to speech using the Eleven Labs API. It checks if TTS is enabled and if the text contains code, in which case it removes the code before processing. The function sends a TTS request to the API, saves the audio stream to a file, and plays the audio file using a separate thread.

### set_voice

Sets the current voice to be used for TTS. It updates the `VOICE_IDS` list with the specified voice, ensuring the voice exists in the available voices list.

### load_voices

Loads available voices if they are not already loaded. It calls the `get_voices` function and populates the `VOICE_IDS` list with the fetched voice data.

### get_voice

Returns the currently selected voice from the `VOICE_IDS` list.

### set_tts

Enables or disables the TTS functionality by setting the `_use_tts` flag.

### get_tts

Returns the current status of the TTS functionality.

### tts

An asynchronous wrapper function for `text_to_speech`, allowing text-to-speech conversion to be called directly.

### test_tts

A test function to verify the TTS functionality. It loads voices, sets a test voice, enables TTS, and converts a test text to speech.

## Summary

The `tts.py` file provides a comprehensive interface for interacting with the Eleven Labs text-to-speech service. It includes functions for fetching and setting voices, converting text to speech, and playing audio. The script also manages TTS settings and includes a test function to verify the entire workflow. This modular approach ensures that each functionality is well-defined and easily testable.