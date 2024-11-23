#modules/Personas/CodeGenius/Toolbox/GitHub/github_client.py

import os
import requests
import json
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('github_client.py')

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

class GitHubClient:
    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv('GITHUB_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("GitHub access token not provided or not found in the environment variables.")
        self.base_url = 'https://api.github.com'

    def send_request(self, endpoint, method='GET', data=None):
        logger.info(f"Sending {method} request to endpoint: {endpoint}")
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f"Bearer {self.access_token}",
                'Accept': 'application/vnd.github+json'
            }
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(data))
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                logger.error(f"Invalid request method: {method}")
                return None

            logger.info(f"Request sent to endpoint: {endpoint}")
            logger.info(f"Response status code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Response data: {data}")
                return data
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                logger.error(f"Response content: {response.text}")
                return None
        except Exception as e:
            logger.exception(f"Error occurred while sending request: {str(e)}")
            return None

    def get_user(self, username):
        logger.info(f"Retrieving user data for: {username}")
        endpoint = f"users/{username}"
        data = self.send_request(endpoint)
        if data:
            logger.info(f"User data retrieved for: {username}")
            return data
        else:
            logger.error(f"Failed to retrieve user data for: {username}")
            return None

    def get_repository(self, repo_owner, repo_name):
        logger.info(f"Retrieving repository data for {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}"
        data = self.send_request(endpoint)
        if data:
            logger.info(f"Repository data retrieved for {repo_owner}/{repo_name}")
            return data
        else:
            logger.error(f"Failed to retrieve repository data for {repo_owner}/{repo_name}")
            return None

    def create_repository(self, name, description=None, private=False):
        logger.info(f"Creating repository: {name}")
        endpoint = 'user/repos'
        data = {
            'name': name,
            'description': description,
            'private': private
        }
        response_data = self.send_request(endpoint, method='POST', data=data)
        if response_data:
            logger.info(f"Repository created: {name}")
            return response_data
        else:
            logger.error(f"Failed to create repository: {name}")
            return None

    def update_repository(self, repo_owner, repo_name, description=None, private=None):
        logger.info(f"Updating repository: {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}"
        data = {}
        if description is not None:
            data['description'] = description
        if private is not None:
            data['private'] = private
        response_data = self.send_request(endpoint, method='PATCH', data=data)
        if response_data:
            logger.info(f"Repository updated: {repo_owner}/{repo_name}")
            return response_data
        else:
            logger.error(f"Failed to update repository: {repo_owner}/{repo_name}")
            return None

    def delete_repository(self, repo_owner, repo_name):
        logger.info(f"Deleting repository: {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}"
        response_data = self.send_request(endpoint, method='DELETE')
        if response_data is None:
            logger.info(f"Repository deleted: {repo_owner}/{repo_name}")
            return True
        else:
            logger.error(f"Failed to delete repository: {repo_owner}/{repo_name}")
            return False

    def get_repository_issues(self, repo_owner, repo_name):
        logger.info(f"Retrieving issues for repository: {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}/issues"
        data = self.send_request(endpoint)
        if data:
            logger.info(f"Issues retrieved for repository: {repo_owner}/{repo_name}")
            return data
        else:
            logger.error(f"Failed to retrieve issues for repository: {repo_owner}/{repo_name}")
            return None

    def create_issue(self, repo_owner, repo_name, title, body=None, assignee=None, labels=None):
        logger.info(f"Creating issue in repository: {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}/issues"
        data = {
            'title': title,
            'body': body,
            'assignee': assignee,
            'labels': labels
        }
        response_data = self.send_request(endpoint, method='POST', data=data)
        if response_data:
            logger.info(f"Issue created in repository: {repo_owner}/{repo_name}")
            return response_data
        else:
            logger.error(f"Failed to create issue in repository: {repo_owner}/{repo_name}")
            return None

    def update_issue(self, repo_owner, repo_name, issue_number, title=None, body=None, assignee=None, labels=None, state=None):
        logger.info(f"Updating issue #{issue_number} in repository: {repo_owner}/{repo_name}")
        endpoint = f"repos/{repo_owner}/{repo_name}/issues/{issue_number}"
        data = {}
        if title is not None:
            data['title'] = title
        if body is not None:
            data['body'] = body
        if assignee is not None:
            data['assignee'] = assignee
        if labels is not None:
            data['labels'] = labels
        if state is not None:
            data['state'] = state
        response_data = self.send_request(endpoint, method='PATCH', data=data)
        if response_data:
            logger.info(f"Issue #{issue_number} updated in repository: {repo_owner}/{repo_name}")
            return response_data
        else:
            logger.error(f"Failed to update issue #{issue_number} in repository: {repo_owner}/{repo_name}")
            return None