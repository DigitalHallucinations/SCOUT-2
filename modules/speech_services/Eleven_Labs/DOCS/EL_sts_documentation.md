# DOCS/EL_sts_documentation.md

## Overview

The `EL_sts.py` file provides functionality for converting one voice to another using the Eleven Labs speech-to-speech (STS) API. It handles loading environment variables, setting up API request parameters, sending the request to the API, and saving the converted audio stream to a file.

## Table of Contents

1. [Imports](#imports)
2. [Setup and Configuration](#setup-and-configuration)
3. [Functionality](#functionality)
    - [Loading Environment Variables](#loading-environment-variables)
    - [Setting API Headers](#setting-api-headers)
    - [Defining Parameters](#defining-parameters)
    - [Sending STS Request](#sending-sts-request)
    - [Saving Audio Stream](#saving-audio-stream)

## Imports

The script imports modules for handling HTTP requests, JSON operations, environment variables, and logging.

## Setup and Configuration

The script initializes logging and loads environment variables from a `.env` file using `dotenv`. It retrieves the API key necessary for making requests to the Eleven Labs API.

### Loading Environment Variables

The `load_dotenv` function loads environment variables from a `.env` file, and the API key is retrieved using `os.getenv`. If the API key is not found, an error is logged.

### Setting API Headers

The API headers are configured to include the `xi-api-key` and the `Accept` header set to `application/json`.

## Functionality

### Defining Parameters

Several parameters are defined:
- `CHUNK_SIZE`: Size of the chunks for streaming audio data.
- `VOICE_ID`: Placeholder for the voice ID to be used in the conversion.
- `AUDIO_FILE_PATH`: Path to the input audio file.
- `OUTPUT_PATH`: Path where the converted audio will be saved.

### Sending STS Request

The `sts_url` is constructed using the base URL for the Eleven Labs STS API and the `VOICE_ID`. The request payload includes the `model_id` and `voice_settings` with various configuration options for stability, similarity boost, style, and speaker boost.

The audio file is opened in binary mode and included in the `files` dictionary for the POST request. The `requests.post` method sends the STS request to the API with the configured headers, data, and files.

### Saving Audio Stream

If the response is successful (`response.ok`), the script writes the streamed audio data to the specified output file in chunks of `CHUNK_SIZE`. If the response is not successful, the error message is logged.

## Summary

The `EL_sts.py` file provides a script for converting one voice to another using the Eleven Labs speech-to-speech API. It handles loading environment variables, setting up request headers, defining parameters, sending the API request, and saving the converted audio stream. The script ensures proper logging of actions and errors for debugging and tracking purposes.