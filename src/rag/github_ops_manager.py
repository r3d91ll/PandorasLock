import os
from github import Github
from git import Repo, GitCommandError
from getpass import getpass
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubOperationsManager:
    def __init__(self):
        self.github_instance = None
        self.repo_instance = None
        self.local_repo = None

    def initialize(self, repo_name, local_path, access_token=None):
        try:
            access_token = access_token or os.getenv("GITHUB_ACCESS_TOKEN") or getpass("Enter your GitHub access token: ")
            self.github_instance = Github(access_token)
            self.repo_instance = self.github_instance.get_repo(repo_name)

            if os.path.exists(local_path):
                self.local_repo = Repo(local_path)
            else:
                self.local_repo = Repo.clone_from(self.repo_instance.clone_url, local_path)

            logger.info(f"Initialized repo: {repo_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GitHub instance or repository: {e}")

    def clone_repository(self, repo_name, local_path, access_token=None):
        try:
            access_token = access_token or os.getenv("GITHUB_ACCESS_TOKEN") or getpass("Enter your GitHub access token: ")
            self.github_instance = Github(access_token)
            self.repo_instance = self.github_instance.get_repo(repo_name)

            if os.path.exists(local_path):
                logger.info(f"Repository already exists at {local_path}")
                self.local_repo = Repo(local_path)
            else:
                logger.info(f"Cloning repository {repo_name} to {local_path}")
                self.local_repo = Repo.clone_from(self.repo_instance.clone_url, local_path)

            logger.info(f"Successfully cloned/initialized repo: {repo_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return False

    def pull_changes(self):
        try:
            origin = self.local_repo.remotes.origin
            origin.pull()
            logger.info(f"Pulled latest changes for {self.repo_instance.full_name}")
        except GitCommandError as e:
            logger.error(f"Error pulling changes: {e}")

    def push_changes(self, commit_message):
        try:
            self.local_repo.git.add(A=True)
            self.local_repo.index.commit(commit_message)
            origin = self.local_repo.remotes.origin
            origin.push()
            logger.info(f"Pushed changes to {self.repo_instance.full_name} with message: {commit_message}")
        except GitCommandError as e:
            logger.error(f"Error pushing changes: {e}")

    def create_branch(self, branch_name):
        try:
            current = self.local_repo.create_head(branch_name)
            current.checkout()
            logger.info(f"Created and switched to new branch: {branch_name}")
        except GitCommandError as e:
            logger.error(f"Error creating branch: {e}")

    def switch_branch(self, branch_name):
        try:
            self.local_repo.git.checkout(branch_name)
            logger.info(f"Switched to branch: {branch_name}")
        except GitCommandError as e:
            logger.error(f"Error switching branch: {e}")

    def create_issue(self, title, body):
        try:
            issue = self.repo_instance.create_issue(title=title, body=body)
            logger.info(f"Created issue #{issue.number}: {title}")
            return issue
        except Exception as e:
            logger.error(f"Error creating issue: {e}")

    def update_issue(self, issue_number, title=None, body=None, state=None):
        try:
            issue = self.repo_instance.get_issue(number=issue_number)
            issue.edit(title=title, body=body, state=state)
            logger.info(f"Updated issue #{issue_number}")
        except Exception as e:
            logger.error(f"Error updating issue #{issue_number}: {e}")

    def create_pull_request(self, title, body, head, base):
        try:
            pr = self.repo_instance.create_pull(title=title, body=body, head=head, base=base)
            logger.info(f"Created pull request #{pr.number}: {title}")
            return pr
        except Exception as e:
            logger.error(f"Error creating pull request: {e}")

    def update_pull_request(self, pr_number, title=None, body=None, state=None):
        try:
            pr = self.repo_instance.get_pull(number=pr_number)
            pr.edit(title=title, body=body, state=state)
            logger.info(f"Updated pull request #{pr_number}")
        except Exception as e:
            logger.error(f"Error updating pull request #{pr_number}: {e}")

    def get_file_content(self, file_path):
        try:
            full_file_path = os.path.join(self.local_repo.working_tree_dir, file_path)
            with open(full_file_path, 'r') as file:
                content = file.read()
            return content
        except IOError as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

    def update_file_content(self, file_path, new_content, commit_message):
        try:
            full_file_path = os.path.join(self.local_repo.working_tree_dir, file_path)
            with open(full_file_path, 'w') as file:
                file.write(new_content)
            self.local_repo.git.add(file_path)
            self.local_repo.index.commit(commit_message)
            logger.info(f"Updated file {file_path} in local repository")
        except IOError as e:
            logger.error(f"Error updating file {file_path}: {e}")

    def close(self):
        pass  # No resources to close for Github instance

# Test functions

def test_git_operations():
    manager = GitHubOperationsManager()
    manager.initialize("your_username/your_repo", "/path/to/local/repo")
    
    # Pull changes
    manager.pull_changes()
    
    # Create a new branch
    manager.create_branch("test-branch")
    
    # Update a file
    manager.update_file_content("README.md", "Updated content\n", "Update README")
    
    # Push changes
    manager.push_changes("Update from test script")
    
    # Switch back to main branch
    manager.switch_branch("main")
    
    manager.close()

def test_github_operations():
    manager = GitHubOperationsManager()
    manager.initialize("your_username/your_repo", "/path/to/local/repo")
    
    # Create an issue
    issue = manager.create_issue("Test Issue", "This is a test issue created by script")
    print(f"Created issue number: {issue.number}")
    
    # Update the issue
    manager.update_issue(issue.number, title="Updated Test Issue", body="This issue was updated by script")
    
    # Create a pull request
    pr = manager.create_pull_request("Test PR", "This is a test PR created by script", "test-branch", "main")
    print(f"Created PR number: {pr.number}")
    
    # Update the pull request
    manager.update_pull_request(pr.number, body="This PR was updated by script")
    
    manager.close()

if __name__ == "__main__":
    print("Select a test to run:")
    print("1. Git operations (pull, branch, update file, push)")
    print("2. GitHub operations (issues, pull requests)")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == '1':
        test_git_operations()
    elif choice == '2':
        test_github_operations()
    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")
