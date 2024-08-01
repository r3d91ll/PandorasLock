import os
from github import Github
from git import Repo, GitCommandError
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubOperationsManager:
    def __init__(self, access_token=None):
        self.access_token = access_token or os.getenv("GITHUB_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("GitHub access token not provided and not found in environment variables.")
        self.github_instance = Github(self.access_token)
        self.repo_instance = None
        self.local_repo = None

    def initialize(self, repo_name, local_path):
        try:
            self.repo_instance = self.github_instance.get_repo(repo_name)
            if os.path.exists(local_path):
                self.local_repo = Repo(local_path)
                logger.info(f"Initialized existing repo at: {local_path}")
            else:
                self.local_repo = Repo.clone_from(self.repo_instance.clone_url, local_path)
                logger.info(f"Cloned repo to: {local_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize repository: {e}")
            return False

    def pull_changes(self):
        if not self.local_repo:
            logger.error("Local repository not initialized. Call initialize() first.")
            return False
        try:
            origin = self.local_repo.remotes.origin
            origin.pull()
            logger.info(f"Pulled latest changes for {self.repo_instance.full_name}")
            return True
        except GitCommandError as e:
            logger.error(f"Error pulling changes: {e}")
            return False

    def push_changes(self, commit_message):
        if not self.local_repo:
            logger.error("Local repository not initialized. Call initialize() first.")
            return False
        try:
            self.local_repo.git.add(A=True)
            self.local_repo.index.commit(commit_message)
            origin = self.local_repo.remotes.origin
            origin.push()
            logger.info(f"Pushed changes to {self.repo_instance.full_name} with message: {commit_message}")
            return True
        except GitCommandError as e:
            logger.error(f"Error pushing changes: {e}")
            return False

    def create_branch(self, branch_name):
        if not self.local_repo:
            logger.error("Local repository not initialized. Call initialize() first.")
            return False
        try:
            current = self.local_repo.create_head(branch_name)
            current.checkout()
            logger.info(f"Created and switched to new branch: {branch_name}")
            return True
        except GitCommandError as e:
            logger.error(f"Error creating branch: {e}")
            return False

    def switch_branch(self, branch_name):
        if not self.local_repo:
            logger.error("Local repository not initialized. Call initialize() first.")
            return False
        try:
            self.local_repo.git.checkout(branch_name)
            logger.info(f"Switched to branch: {branch_name}")
            return True
        except GitCommandError as e:
            logger.error(f"Error switching branch: {e}")
            return False

    def create_issue(self, title, body):
        if not self.repo_instance:
            logger.error("Repository not initialized. Call initialize() first.")
            return None
        try:
            issue = self.repo_instance.create_issue(title=title, body=body)
            logger.info(f"Created issue #{issue.number}: {title}")
            return issue
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return None

    def update_issue(self, issue_number, title=None, body=None, state=None):
        if not self.repo_instance:
            logger.error("Repository not initialized. Call initialize() first.")
            return False
        try:
            issue = self.repo_instance.get_issue(number=issue_number)
            issue.edit(title=title, body=body, state=state)
            logger.info(f"Updated issue #{issue_number}")
            return True
        except Exception as e:
            logger.error(f"Error updating issue #{issue_number}: {e}")
            return False

    def create_pull_request(self, title, body, head, base):
        if not self.repo_instance:
            logger.error("Repository not initialized. Call initialize() first.")
            return None
        try:
            pr = self.repo_instance.create_pull(title=title, body=body, head=head, base=base)
            logger.info(f"Created pull request #{pr.number}: {title}")
            return pr
        except Exception as e:
            logger.error(f"Error creating pull request: {e}")
            return None

    def update_pull_request(self, pr_number, title=None, body=None, state=None):
        if not self.repo_instance:
            logger.error("Repository not initialized. Call initialize() first.")
            return False
        try:
            pr = self.repo_instance.get_pull(number=pr_number)
            pr.edit(title=title, body=body, state=state)
            logger.info(f"Updated pull request #{pr_number}")
            return True
        except Exception as e:
            logger.error(f"Error updating pull request #{pr_number}: {e}")
            return False
