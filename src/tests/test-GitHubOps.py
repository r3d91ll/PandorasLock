import sys
import os
from github import GithubException
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from rag import GitHubOperationsManager

def clone_repository(manager, repo_name, git_dir):
    # Remove .git extension if present
    repo_name = repo_name.strip().rstrip('.git')
    
    # Set the local path for the repository
    local_path = os.path.join(git_dir, repo_name.split('/')[-1])

    print(f"\nAttempting to clone/initialize repository: {repo_name}")
    print(f"Target local path: {local_path}")

    try:
        if manager.initialize(repo_name, local_path):
            print(f"Successfully cloned/initialized repository: {repo_name}")
            print(f"Repository location: {local_path}")
            
            # List the contents of the cloned repository
            print("\nContents of the cloned repository:")
            for root, dirs, files in os.walk(local_path):
                level = root.replace(local_path, '').count(os.sep)
                indent = ' ' * 4 * level
                print(f"{indent}{os.path.basename(root)}/")
                sub_indent = ' ' * 4 * (level + 1)
                for file in files:
                    print(f"{sub_indent}{file}")
        else:
            print(f"Failed to clone/initialize repository: {repo_name}")
    except GithubException as e:
        if e.status == 404:
            print(f"Error: Repository '{repo_name}' not found. Please check if the repository name is correct and you have the necessary permissions.")
        elif e.status == 401:
            print("Error: Authentication failed. Please check your GitHub access token.")
        else:
            print(f"GitHub API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Get the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Construct the path to the .env file
    dotenv_path = os.path.join(project_root, 'config', '.env')
    
    # Load environment variables from .env file
    load_dotenv(dotenv_path)

    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not access_token:
        print(f"GitHub access token not found in environment variables. Checked .env file at: {dotenv_path}")
        return

    repo_names = os.getenv("GITHUB_REPO_NAMES")
    if not repo_names:
        print(f"GITHUB_REPO_NAMES not found in environment variables. Checked .env file at: {dotenv_path}")
        return

    manager = GitHubOperationsManager(access_token)

    # Create a 'git' directory at the project root
    git_dir = os.path.join(project_root, "git")
    os.makedirs(git_dir, exist_ok=True)

    # Split the repo names and process each one
    for repo_name in repo_names.split(','):
        clone_repository(manager, repo_name, git_dir)

if __name__ == "__main__":
    main()