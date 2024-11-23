# GitHub Client

The GitHub Client is a module within the SCOUT (Scalable Cognitive Operations Unified Team) application that allows the LLM model to interact with the GitHub API. It provides functionality for retrieving user and repository data, creating and managing repositories, and working with issues.

## Features

1. **User Data Retrieval**: The module allows retrieving user data from GitHub by providing a username. It fetches information such as the user's name, email, bio, and other profile details.

2. **Repository Data Retrieval**: The module enables retrieving repository data from GitHub by specifying the repository owner and name. It fetches information such as the repository description, URL, language, and other repository details.

3. **Repository Management**: The module provides methods for creating new repositories, updating repository settings (description and privacy), and deleting repositories. It allows the LLM model to manage repositories programmatically.

4. **Issue Management**: The module allows retrieving issues for a specific repository, creating new issues, and updating existing issues. It provides functionality for specifying issue details such as title, body, assignee, labels, and state.

5. **Logging**: The module incorporates thorough logging using the `logging` module and a `RotatingFileHandler` to write logs to a file named `SCOUT.log`. It logs informational messages, errors, and exceptions that occur during the API requests and response handling.

## Usage

To utilize the GitHub Client module within SCOUT, follow these steps:

1. Import the `GitHubClient` class from the `github_client` module in your SCOUT application.

2. Create an instance of the `GitHubClient` class, providing a valid GitHub access token:
   ```python
   github_client = GitHubClient(access_token='your_access_token')
   ```

3. Use the available methods of the `GitHubClient` instance to interact with the GitHub API. For example:
   - Retrieve user data:
     ```python
     user_data = github_client.get_user('username')
     ```
   - Retrieve repository data:
     ```python
     repo_data = github_client.get_repository('repo_owner', 'repo_name')
     ```
   - Create a new repository:
     ```python
     new_repo = github_client.create_repository('repo_name', description='Repository description', private=True)
     ```
   - Update a repository:
     ```python
     updated_repo = github_client.update_repository('repo_owner', 'repo_name', description='Updated description', private=False)
     ```
   - Delete a repository:
     ```python
     success = github_client.delete_repository('repo_owner', 'repo_name')
     ```
   - Retrieve repository issues:
     ```python
     issues = github_client.get_repository_issues('repo_owner', 'repo_name')
     ```
   - Create a new issue:
     ```python
     new_issue = github_client.create_issue('repo_owner', 'repo_name', 'Issue title', body='Issue description', assignee='assignee_username', labels=['label1', 'label2'])
     ```
   - Update an issue:
     ```python
     updated_issue = github_client.update_issue('repo_owner', 'repo_name', issue_number, title='Updated title', body='Updated description', assignee='new_assignee', labels=['label3'], state='closed')
     ```

4. Handle the returned data and errors appropriately in your SCOUT application. The methods return the response data if the request is successful, or `None` if an error occurs.

## Configuration

The GitHub Client module requires a valid GitHub access token to authenticate and interact with the GitHub API. Make sure to obtain an access token with the necessary permissions for the desired operations (e.g., repo, user, issues).

The access token should be provided when creating an instance of the `GitHubClient` class.

## Logging

The module uses the `logging` module to log various events and errors that occur during the API requests and response handling. The logs are written to a file named `SCOUT.log` using a `RotatingFileHandler` with a maximum size of 10 MB and a backup count of 5.

The `adjust_logging_level` function allows you to dynamically adjust the logging level. You can set the desired logging level by calling `adjust_logging_level('level')`, where `'level'` can be one of the following: `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, or `'CRITICAL'`.

## Error Handling

The module handles errors and exceptions that may occur during the API requests and response handling. It logs the errors and exceptions using the `logger.error` and `logger.exception` statements, respectively.

If an error occurs during an API request, the corresponding method returns `None` to indicate the failure. It is important to handle these error cases appropriately in your SCOUT application.

## Dependencies

The GitHub Client module relies on the following dependencies:

- `requests`: Used for making HTTP requests to the GitHub API endpoints.
- `json`: Used for parsing JSON responses from the GitHub API.
- `logging`: Used for logging messages and errors.

Make sure to have these dependencies installed before using the GitHub Client module.

## Limitations

- The module assumes the presence of a valid GitHub access token. Ensure that you have obtained an access token with the necessary permissions for the desired operations.
- The module may not cover all available endpoints and functionalities of the GitHub API. It focuses on common operations such as retrieving user and repository data, managing repositories, and working with issues. Additional functionality can be added as needed.
- The module relies on the stability and availability of the GitHub API. Any changes or limitations imposed by GitHub may affect the functionality of the module.

## Troubleshooting

If you encounter any issues while using the GitHub Client module, consider the following:

- Check the `SCOUT.log` file for any error messages or exceptions that occurred during the API requests and response handling.
- Ensure that you have a valid GitHub access token with the necessary permissions for the desired operations.
- Verify that you have a stable internet connection to communicate with the GitHub API.
- Check the GitHub API documentation for any changes or updates that may affect the module's functionality.

If the issue persists, please contact the SCOUT development team for further assistance.

---

This documentation provides an overview of the GitHub Client module, its features, usage instructions, configuration, logging, error handling, dependencies, limitations, and troubleshooting tips. It serves as a comprehensive guide for users and developers working with the module within the SCOUT application.