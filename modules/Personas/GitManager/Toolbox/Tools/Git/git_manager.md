# Git Manager Module

The `git_manager.py` module is a Python module that provides functionality for managing Git repositories. It is part of the SCOUT (Scalable Cognitive Operations Unified Team) application and is used by the GitManager persona to perform various Git operations.

## Classes

### GitManager

The `GitManager` class is the main class in the `git_manager.py` module. It provides methods for interacting with Git repositories and executing Git commands.

#### Methods

- `__init__(self)`: Initializes a new instance of the `GitManager` class.
- `execute_git_command(self, command)`: Executes a Git command using the provided command string. Returns a dictionary containing the completion status and output or error message.
- `init_repo(self, repo_path)`: Initializes a new Git repository at the specified `repo_path`.
- `stage_changes(self, repo_path, files)`: Stages changes in the Git repository located at `repo_path` for the specified `files`.
- `commit_changes(self, repo_path, message)`: Commits the staged changes in the Git repository located at `repo_path` with the provided `message`.
- `create_branch(self, repo_path, branch_name)`: Creates a new branch with the specified `branch_name` in the Git repository located at `repo_path`.
- `switch_branch(self, repo_path, branch_name)`: Switches to the branch with the specified `branch_name` in the Git repository located at `repo_path`.
- `merge_branches(self, repo_path, source_branch, target_branch)`: Merges the `source_branch` into the `target_branch` in the Git repository located at `repo_path`.
- `push_to_remote(self, repo_path, remote_url, branch)`: Pushes the specified `branch` to the `remote_url` for the Git repository located at `repo_path`.
- `pull_from_remote(self, repo_path, remote_url, branch)`: Pulls the specified `branch` from the `remote_url` for the Git repository located at `repo_path`.
- `clone_repo(self, remote_url, local_path)`: Clones a Git repository from the specified `remote_url` to the `local_path`.
- `get_status(self, repo_path)`: Retrieves the status of the Git repository located at `repo_path`.
- `get_log(self, repo_path, num_commits=None)`: Retrieves the commit log of the Git repository located at `repo_path`, optionally limited to `num_commits`.

## Functions

- `adjust_logging_level(level)`: Adjusts the logging level of the `git_manager.py` module. The `level` parameter can be one of the following: 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.

## Logging

The `git_manager.py` module uses the `logging` module for logging purposes. It writes logs to a file named `SCOUT.log` using a `RotatingFileHandler` with a maximum size of 10 MB and a backup count of 5.

The logging level can be adjusted using the `adjust_logging_level` function.

## Error Handling

The `git_manager.py` module includes error handling mechanisms to gracefully handle exceptions that may occur during the execution of Git commands. If an error occurs, the relevant error message or exception details are logged, and an error status is returned to the caller.

## Dependencies

The `git_manager.py` module relies on the following dependencies:

- `subprocess`: Used for executing Git commands in the terminal.
- `logging`: Used for logging messages and errors.

Make sure to have these dependencies available in your Python environment.

## Usage

To use the `git_manager.py` module in your SCOUT application:

1. Import the `GitManager` class from the `git_manager` module.
2. Create an instance of the `GitManager` class.
3. Use the available methods of the `GitManager` instance to perform Git operations.
4. Handle the returned results from the Git operations, which include the completion status and output or error messages.

Refer to the documentation of the GitManager persona for more detailed usage instructions and examples.

---

This documentation provides an overview of the `git_manager.py` module, its classes, methods, logging, error handling, dependencies, and usage instructions. It serves as a reference for developers working with the `git_manager.py` module within the SCOUT application.