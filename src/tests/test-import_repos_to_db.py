import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.github_ops_manager import GitHubOperationsManager
from rag.repo_db_importer import RepoDBImporter
from utils.config_utils import Config

def main():
    # Get the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Load environment variables
    load_dotenv(os.path.join(project_root, 'config', '.env'))

    # Initialize configuration
    config = Config()

    # Initialize GitHubOperationsManager
    github_manager = GitHubOperationsManager(config.GITHUB_ACCESS_TOKEN)

    # Initialize RepoDBImporter
    db_importer = RepoDBImporter(
        config.NEO4J_URI,
        config.NEO4J_USER,
        config.NEO4J_PASSWORD,
        config.POSTGRES_CONNECTION_STRING
    )

    # Get repository names from environment variable
    repo_names = os.getenv("GITHUB_REPO_NAMES", "").split(',')

    for repo_name in repo_names:
        repo_name = repo_name.strip()
        if not repo_name:
            continue

        print(f"\nProcessing repository: {repo_name}")

        # Set the local path for the repository
        local_path = os.path.join(project_root, "git", repo_name.split('/')[-1])

        # Check if the repository is already cloned
        if not os.path.exists(local_path):
            print(f"Cloning repository: {repo_name}")
            if not github_manager.initialize(repo_name, local_path):
                print(f"Failed to clone repository: {repo_name}")
                continue
        else:
            print(f"Repository already cloned: {repo_name}")

        # Import the repository to the databases
        print(f"Importing repository to databases: {repo_name}")
        db_importer.import_repo(local_path, repo_name)

    print("\nRepository import process completed.")

if __name__ == "__main__":
    main()