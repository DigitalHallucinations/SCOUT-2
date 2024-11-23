# GitManager Persona

The GitManager persona is a specialized persona within the SCOUT (Scalable Cognitive Operations Unified Team) application that focuses on managing Git repositories. It provides a range of capabilities to interact with Git repositories, perform version control operations, and assist users in their Git workflow.

## Capabilities

The GitManager persona offers the following capabilities:

1. **Repository Initialization**: Initialize new Git repositories at specified paths.
2. **Staging Changes**: Stage changes in a Git repository, preparing them for committing.
3. **Committing Changes**: Commit staged changes in a Git repository with a provided commit message.
4. **Branch Management**: Create new branches, switch between branches, and merge branches in a Git repository.
5. **Remote Repository Interaction**: Push changes to remote repositories and pull changes from remote repositories.
6. **Repository Cloning**: Clone remote repositories to local paths.
7. **Repository Status**: Retrieve the current status of a Git repository, including modified files and staged changes.
8. **Commit Log**: Retrieve the commit log of a Git repository, optionally specifying the number of commits to retrieve.

## Usage

To utilize the GitManager persona within the SCOUT application, follow these steps:

1. Ensure that the necessary dependencies and configurations are in place, including the `git_manager.py` module and the `maps.py` file.

2. Import the `GitManager` class from the `git_manager` module in your SCOUT application.

3. Create an instance of the `GitManager` class:
   ```python
   git_manager = GitManager()
   ```

4. Use the available methods of the `GitManager` instance to perform Git operations. For example:
   - Initialize a new repository:
     ```python
     result = git_manager.init_repo('/path/to/repo')
     ```
   - Stage changes in a repository:
     ```python
     result = git_manager.stage_changes('/path/to/repo', ['file1.txt', 'file2.txt'])
     ```
   - Commit changes in a repository:
     ```python
     result = git_manager.commit_changes('/path/to/repo', 'Commit message')
     ```
   - Create a new branch:
     ```python
     result = git_manager.create_branch('/path/to/repo', 'new-branch')
     ```
   - Push changes to a remote repository:
     ```python
     result = git_manager.push_to_remote('/path/to/repo', 'https://github.com/user/repo.git', 'main')
     ```

5. Handle the returned results from the Git operations, which include the completion status and output or error messages.

## Logging

The GitManager persona incorporates logging functionality to track the execution of Git commands and any errors that occur. The logs are written to a file named `SCOUT.log` using a `RotatingFileHandler` with a maximum size of 10 MB and a backup count of 5.

The logging level can be adjusted using the `adjust_logging_level` function, which accepts a logging level string ('DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL').

## Error Handling

The GitManager persona includes error handling mechanisms to gracefully handle exceptions that may occur during the execution of Git commands. If an error occurs, the relevant error message or exception details are logged, and an error status is returned to the caller.

## Dependencies

The GitManager persona relies on the following dependencies:

- `subprocess`: Used for executing Git commands in the terminal.
- `logging`: Used for logging messages and errors.

Make sure to have these dependencies available in your Python environment.

## Limitations

- The GitManager persona assumes that the Git executable is available in the system's PATH. Ensure that Git is properly installed and accessible.
- The GitManager persona relies on the underlying Git commands and their output. Any changes or limitations in the Git command-line interface may affect the functionality of the persona.

## Troubleshooting

If you encounter any issues while using the GitManager persona, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the execution of Git commands.
- Ensure that the Git executable is properly installed and accessible in the system's PATH.
- Verify that the provided repository paths, branch names, and remote URLs are correct and valid.
- Make sure that you have the necessary permissions to perform Git operations in the specified repositories.

If the issue persists, please contact the SCOUT development team for further assistance.

---

This documentation provides an overview of the GitManager persona, its capabilities, usage instructions, logging, error handling, dependencies, limitations, and troubleshooting tips. It serves as a comprehensive guide for users and developers working with the GitManager persona within the SCOUT application.