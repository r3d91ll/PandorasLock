import yaml
import os
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_docker_compose(file_path: str, section: str, docker_service: Dict[str, Any]) -> None:
    """
    Update docker-compose.yml file by appending or updating content in a specific section.
    
    This function provides a reusable way to modify docker-compose.yml files across different
    projects and contexts. It checks the syntax of the existing file, updates the specified
    section, and handles potential errors.
    
    Args:
    file_path (str): Path to the docker-compose.yml file
    section (str): The section to update (e.g., 'services', 'networks', 'volumes')
    docker_service (Dict[str, Any]): The new content to append to or update in the section
    
    Raises:
    FileNotFoundError: If the specified docker-compose.yml file doesn't exist
    yaml.YAMLError: If the existing file has invalid YAML syntax
    KeyError: If the specified section doesn't exist in the file
    """
    # Check if file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"Docker Compose file not found: {file_path}")

    # Read and parse existing docker-compose.yml
    with open(file_path, 'r') as f:
        try:
            docker_compose = yaml.safe_load(f)
            logger.info(f"Successfully parsed existing docker-compose.yml: {file_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing docker-compose.yml: {e}")
            raise

    # Check if the specified section exists
    if section not in docker_compose:
        logger.error(f"Section '{section}' not found in docker-compose.yml")
        raise KeyError(f"Section '{section}' not found")

    # Update or append new content to the specified section
    if isinstance(docker_compose[section], dict):
        docker_compose[section].update(docker_service)
    elif isinstance(docker_compose[section], list):
        docker_compose[section].extend(docker_service)
    else:
        logger.error(f"Unexpected type for section '{section}': {type(docker_compose[section])}")
        raise TypeError(f"Unexpected type for section '{section}': {type(docker_compose[section])}")

    # Write updated content back to file
    with open(file_path, 'w') as f:
        yaml.dump(docker_compose, f, default_flow_style=False, sort_keys=False)
    
    logger.info(f"Successfully updated {section} in docker-compose.yml: {file_path}")

# Example usage (commented out):
# docker_compose_path = '/path/to/your/docker-compose.yml'
# docker_service = {
#     'service_name': {
#         'image': 'image_name',
#         'container_name': 'container_name',
#         # ... other service configurations ...
#     }
# }
# try:
#     update_docker_compose(docker_compose_path, 'services', docker_service)
#     print("Docker Compose file updated successfully.")
# except (FileNotFoundError, yaml.YAMLError, KeyError, TypeError) as e:
#     print(f"Failed to update Docker Compose file: {e}")