# modules\Personas\GitHubGenius\Toolbox\maps.py

from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Personas.GitHubGenius.Toolbox.Tools.TerminalCommand import TerminalCommand
from modules.Personas.GitHubGenius.Toolbox.Tools.GitHub.github_client import GitHubClient

google_search_instance = GoogleSearch()
github_client_instance = GitHubClient()

function_map = {
    "google_search": google_search_instance._search,
    "terminal_command": TerminalCommand,
    "send_request": github_client_instance.send_request,
    "get_user": github_client_instance.get_user,
    "get_repository": github_client_instance.get_repository,
    "create_repository": github_client_instance.create_repository,
    "update_repository": github_client_instance.update_repository,
    "delete_repository": github_client_instance.delete_repository,
    "get_repository_issues": github_client_instance.get_repository_issues,
    "create_issue": github_client_instance.create_issue,
    "update_issue": github_client_instance.update_issue
}
