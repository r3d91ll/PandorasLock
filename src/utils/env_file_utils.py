import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def append_env_vars(env_file_path: str, env_vars: str) -> None:
    """
    Append environment variables to the .env file.

    Args:
    env_file_path (str): Path to the .env file
    env_vars (str): String containing environment variables to append

    Raises:
    IOError: If there's an error reading or writing the file
    """
    try:
        # Check if file exists and is writable
        if os.path.exists(env_file_path):
            if os.access(env_file_path, os.W_OK):
                with open(env_file_path, 'a') as f:
                    f.write(env_vars)
                logger.info(f"Successfully appended configurations to .env file at {env_file_path}")
            else:
                logger.error(f"The .env file at {env_file_path} is not writable.")
        else:
            logger.error(f".env file not found at {env_file_path}. Please create it first.")
    except IOError as e:
        logger.error(f"An error occurred while writing to the .env file: {e}")
        raise

# Example usage (commented out):
# ollama_env_vars = """
# # Ollama Configuration
# OLLAMA_MODELS_PATH=./db_data/ollama_models
# # CodeLlama Configuration
# OLLAMA_CODELLAMA_CONTAINER_NAME=ragtools_ollama_codellama
# OLLAMA_CODELLAMA_PORT=11435
# OLLAMA_CODELLAMA_MODEL=codellama
# OLLAMA_CODELLAMA_PATH=./db_data/ollama_models/codellama
# OLLAMA_CODELLAMA_GPU=0  # Assign to first GPU
# OLLAMA_CODELLAMA_HOST=0.0.0.0
# # Example of another model configuration (commented out)
# # OLLAMA_LLAMA2_CONTAINER_NAME=ragtools_ollama_llama2
# # OLLAMA_LLAMA2_PORT=11436
# # OLLAMA_LLAMA2_MODEL=llama2
# # OLLAMA_LLAMA2_PATH=./db_data/ollama_models/llama2
# # OLLAMA_LLAMA2_GPU=1  # Assign to second GPU
# """
# 
# env_file_path = os.path.join('..', '..', 'config', '.env')
# try:
#     append_env_vars(env_file_path, ollama_env_vars)
#     print("Ollama environment variable setup completed.")
# except IOError as e:
#     print(f"Failed to update .env file: {e}")