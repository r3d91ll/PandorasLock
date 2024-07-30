import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_config_utils(file_path: str, new_configs: Dict[str, Any]) -> None:
    """
    Update the Config class in config_utils.py with new configurations.

    Args:
    file_path (str): Path to the config_utils.py file
    new_configs (Dict[str, Any]): Dictionary containing new configurations to add

    Raises:
    FileNotFoundError: If the specified config_utils.py file doesn't exist
    IOError: If there's an error reading or writing the file
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"config_utils.py file not found: {file_path}")

        # Read existing content
        with open(file_path, 'r') as f:
            existing_content = f.read()

        # Prepare new configurations
        new_config_lines = []
        for key, value in new_configs.items():
            if isinstance(value, str):
                new_config_lines.append(f"        self.{key} = os.getenv('{key}')")
            elif isinstance(value, int):
                new_config_lines.append(f"        self.{key} = int(os.getenv('{key}', {value}))")
            else:
                new_config_lines.append(f"        self.{key} = os.getenv('{key}')")

        new_config_block = '\n'.join(new_config_lines)

        # Find the position to insert the new configurations
        lines = existing_content.split('\n')
        insert_line = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('def get_postgres_connection_params(self):'):
                insert_line = i
                break

        if insert_line == -1:
            # If method not found, insert at the end of __init__
            for i, line in enumerate(reversed(lines)):
                if line.strip().startswith('self.') and '=' in line:
                    insert_line = len(lines) - i
                    break

        # Insert the new configurations
        if insert_line != -1:
            updated_lines = lines[:insert_line] + [new_config_block] + lines[insert_line:]
            updated_content = '\n'.join(updated_lines)
        else:
            logger.error("Could not find appropriate insertion point. Please update manually.")
            return

        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)

        logger.info(f"Successfully updated config_utils.py with new configurations: {file_path}")

    except IOError as e:
        logger.error(f"An error occurred while updating config_utils.py: {e}")
        raise

# Example usage (commented out):
# config_utils_path = os.path.join('..', 'src', 'utils', 'config_utils.py')
# new_configs = {
#     'OLLAMA_MODELS_PATH': '',
#     'OLLAMA_CODESTRALL_CONTAINER_NAME': '',
#     'OLLAMA_CODESTRALL_PORT': 11435,
#     'OLLAMA_CODESTRALL_MODEL': '',
#     'OLLAMA_CODESTRALL_PATH': '',
#     'OLLAMA_CODESTRALL_GPU': 0,
#     'OLLAMA_CODESTRALL_HOST': ''
# }
# try:
#     update_config_utils(config_utils_path, new_configs)
#     print("config_utils.py updated successfully.")
# except (FileNotFoundError, IOError) as e:
#     print(f"Failed to update config_utils.py: {e}")