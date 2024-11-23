## Module: modules/logging/logger

The `logger` module is designed to provide a customizable logging mechanism for the application. It sets up a logging system that writes log messages to both a file and the console. The log files are managed with a rotating file handler to prevent excessive disk usage. The module allows setting and retrieving the logging level and includes a custom logger class for better control over logging behavior.

---

# Imports:  

- `logging`: A standard library module for generating log messages.
- `logging.handlers`: Provides handlers for various logging operations, including the `RotatingFileHandler`.

---

## Class: CustomLogger

### Constructor  
#### Method: `__init__`

The constructor initializes the `CustomLogger` class by setting up the logging configuration. It creates a file handler to write log messages to a file with rotation and a stream handler to output messages to the console. The formatter ensures a consistent log message format. The propagation to the root logger is disabled to avoid duplicate logging.

- **Parameters:**
  - `name` (str, required): The name of the logger.

- **Returns:** None.

---

### Methods

## Method: `set_logging_level`

Sets the global logging level for the application. This function allows dynamic adjustment of the logging level based on the application's needs.

- **Parameters:**
  - `level` (int, required): The logging level to be set. Should be one of the standard logging levels (e.g., `logging.INFO`, `logging.DEBUG`).

- **Returns:** None.

**Example usage:**


set_logging_level(logging.DEBUG)


---

## Method: `get_logging_level`

Retrieves the current global logging level of the application.

- **Parameters:** None.
- **Returns:** `int`: The current logging level.

**Example usage:**


current_level = get_logging_level()


---

## Function: `setup_logger`

Sets up a custom logger using the `CustomLogger` class. It configures the logger with the specified name and logging level.

- **Parameters:**
  - `logger_name` (str, required): The name of the logger to be created.

- **Returns:** `CustomLogger`: An instance of the custom logger configured with the specified name and logging level.

**Example usage:**


logger = setup_logger('my_logger')
logger.info('This is an info message')


---


