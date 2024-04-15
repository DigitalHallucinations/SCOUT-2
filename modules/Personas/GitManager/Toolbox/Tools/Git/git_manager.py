# modules/Persona/GitManager/Toolbox/Tools/Git/git_manager.py

import os
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('git_manager.py')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(levels.get(level, logging.WARNING))

class GitManager:
    def __init__(self):
        self.username = os.getenv('GIT_USERNAME')
        self.password = os.getenv('GIT_PASSWORD')
        self.ssh_key_path = os.getenv('GIT_SSH_KEY_PATH')

        if not self.username or not (self.password or self.ssh_key_path):
            raise ValueError("Git credentials not provided or not found in the environment variables.")

    def execute_git_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            logger.info(f"Git command executed: {command}")
            logger.info(f"Output: {output}")
            return {"status": "success", "output": output}
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing Git command: {command}")
            logger.error(f"Error message: {e.output}")
            return {"status": "error", "message": e.output}
        except Exception as e:
            logger.exception(f"Unexpected error occurred while executing Git command: {command}")
            return {"status": "error", "message": str(e)}

    def init_repo(self, repo_path):
        try:
            command = f"git init {repo_path}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error initializing repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def stage_changes(self, repo_path, files):
        try:
            command = f"git -C {repo_path} add {' '.join(files)}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error staging changes in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def commit_changes(self, repo_path, message):
        try:
            command = f"git -C {repo_path} commit -m '{message}'"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error committing changes in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def create_branch(self, repo_path, branch_name):
        try:
            command = f"git -C {repo_path} branch {branch_name}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error creating branch '{branch_name}' in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def switch_branch(self, repo_path, branch_name):
        try:
            command = f"git -C {repo_path} checkout {branch_name}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error switching to branch '{branch_name}' in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def merge_branches(self, repo_path, source_branch, target_branch):
        try:
            command = f"git -C {repo_path} checkout {target_branch} && git merge {source_branch}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error merging branch '{source_branch}' into '{target_branch}' in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def push_to_remote(self, repo_path, remote_url, branch):
        try:
            command = f"git -C {repo_path} push {remote_url} {branch}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error pushing branch '{branch}' to remote '{remote_url}' in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def pull_from_remote(self, repo_path, remote_url, branch):
        try:
            command = f"git -C {repo_path} pull {remote_url} {branch}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error pulling branch '{branch}' from remote '{remote_url}' in repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def clone_repo(self, remote_url, local_path):
        try:
            command = f"git clone {remote_url} {local_path}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error cloning repository from '{remote_url}' to '{local_path}'")
            return {"status": "error", "message": str(e)}

    def get_status(self, repo_path):
        try:
            command = f"git -C {repo_path} status"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error retrieving status of repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}

    def get_log(self, repo_path, num_commits=None):
        try:
            command = f"git -C {repo_path} log"
            if num_commits:
                command += f" -n {num_commits}"
            return self.execute_git_command(command)
        except Exception as e:
            logger.exception(f"Error retrieving log of repository at path: {repo_path}")
            return {"status": "error", "message": str(e)}