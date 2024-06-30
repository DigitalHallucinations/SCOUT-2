# DOCS/model_manager_documentation.md

## Overview

The `model_manager.py` file defines the `ModelManager` class, which is responsible for managing the selection and configuration of models within the application. This includes setting the active model, checking if a model is allowed, and retrieving model-specific configurations such as maximum token limits.

## Table of Contents

1. [ModelManager Class](#modelmanager-class)
    - [Initialization](#initialization)
    - [Setting Model](#setting-model)
    - [Getting Model](#getting-model)
    - [Checking Allowed Models](#checking-allowed-models)
    - [Getting Maximum Tokens](#getting-maximum-tokens)

## ModelManager Class

The `ModelManager` class handles the management of models that can be used within the application, ensuring only allowed models are used and configuring settings specific to each model.

### Initialization

The `__init__` method initializes the `ModelManager` class with default values for the model (`gpt-4o`) and maximum tokens (4000). It also defines a list of allowed models that can be used within the application.

### Setting Model

The `set_model` method sets the active model to the specified `model_name` if it is in the list of allowed models. It adjusts the `MAX_TOKENS` attribute based on the model selected. If the specified model is not allowed, it raises a `ValueError`.

### Getting Model

The `get_model` method returns the current active model. This allows other components of the application to retrieve the model being used.

### Checking Allowed Models

The `is_model_allowed` method checks if the current active model is in the list of allowed models. It returns a boolean indicating whether the model is allowed or not.

### Getting Maximum Tokens

The `get_max_tokens` method returns the maximum number of tokens allowed for the current active model. This is used to ensure that interactions with the model adhere to its token limit constraints.

## Summary

The `model_manager.py` file defines a class that manages the selection and configuration of models within the application. It ensures that only allowed models are used, adjusts settings based on the selected model, and provides methods to retrieve the current model and its configurations. This class is essential for maintaining the integrity and proper functioning of model-related operations within the application.