import os
from dotenv import load_dotenv
from src import GitHubOperationsManager

def main():
    # Load environment variables from .env file
    load_dotenv()

    manager = GitHubOperationsManager()
    
    repo_name = "r3d91ll/RouteLLM"
    local_path = os.path.expanduser("~/RouteLLM")  # Clone to user's home directory
    
    # Get the access token from the environment variable
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    
    if not access_token:
        print("GitHub access token not found. Please set it in your .env file.")
        return

    success = manager.clone_repository(repo_name, local_path, access_token)
    
    if success:
        print(f"Repository cloned successfully to {local_path}")
        # You can add more operations here, like listing files, checking branches, etc.
    else:
        print("Failed to clone repository")

if __name__ == "__main__":
    main()