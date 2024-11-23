# modules\Personas\GitManager\Toolbox\maps.py

from modules.Tools.Base_Tools.Google_search import GoogleSearch
from modules.Personas.GitManager.Toolbox.Tools.TerminalCommand import TerminalCommand
from modules.Personas.GitManager.Toolbox.Tools.Git.git_manager import GitManager

google_search_instance = GoogleSearch()
git_manager_instance = GitManager()

function_map = {
    "google_search": google_search_instance._search,
    "terminal_command": TerminalCommand,
    "init_repo": git_manager_instance.init_repo,
    "stage_changes": git_manager_instance.stage_changes,
    "commit_changes": git_manager_instance.commit_changes,
    "create_branch": git_manager_instance.create_branch,
    "switch_branch": git_manager_instance.switch_branch,
    "merge_branches": git_manager_instance.merge_branches,
    "push_to_remote": git_manager_instance.push_to_remote,
    "pull_from_remote": git_manager_instance.pull_from_remote,
    "clone_repo": git_manager_instance.clone_repo,
    "get_status": git_manager_instance.get_status,
    "get_log": git_manager_instance.get_log
}