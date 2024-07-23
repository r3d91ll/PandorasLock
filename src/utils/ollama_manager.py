import os
import requests
import time
import logging
from .DockerComposeManager import DockerComposeManager
import json

class OllamaManager:
    def __init__(self, container_name, port, model, gpu=None, models_path=None, llm_path=None, docker_compose_path=None):
        self.container_name = container_name
        self.port = port
        self.model = model
        self.gpu = gpu
        self.models_path = models_path
        self.llm_path = llm_path
        
        # Ensure directories exist
        if self.models_path:
            os.makedirs(self.models_path, exist_ok=True)
        if self.llm_path:
            os.makedirs(self.llm_path, exist_ok=True)
        
        # Initialize DockerComposeManager
        self.docker_manager = DockerComposeManager(docker_compose_path)

        logging.info(f"OllamaManager initialized with models_path: {self.models_path}, llm_path: {self.llm_path}")
        logging.info(f"Using model: {self.model} on port: {self.port}")

    def ensure_model_available(self):
        if not self.model:
            raise ValueError("Model name is not set. Please specify a valid model.")
        if not self.is_model_running():
            logging.info(f"Model {self.model} not found. Attempting to download...")
            self.pull_model()
        else:
            logging.info(f"Model {self.model} is already available.")

    def pull_model(self):
        if not self.model:
            raise ValueError("Model name is not set. Cannot pull an undefined model.")
        logging.info(f"Pulling model {self.model}...")
        try:
            response = requests.post(f'http://localhost:{self.port}/api/pull', json={'name': self.model}, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    print(line.decode())
            logging.info(f"Successfully pulled model {self.model}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error pulling model: {str(e)}")
            raise RuntimeError(f"Failed to download model {self.model}. Error: {str(e)}")

    def generate_response(self, prompt):
        self.ensure_model_available()
        try:
            payload = {
                'model': self.model,
                'prompt': prompt
            }
            logging.debug(f"Sending request to Ollama API with payload: {payload}")
            logging.debug(f"API URL: http://localhost:{self.port}/api/generate")
            
            response = requests.post(
                f'http://localhost:{self.port}/api/generate',
                json=payload,
                stream=True
            )
            logging.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        logging.debug(f"Received chunk: {chunk}")
                        if 'response' in chunk:
                            token = chunk['response']
                            full_response += token
                            print(token, end='', flush=True)
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        logging.warning(f"Failed to decode JSON: {line}")
            
            print("\n")  # New line after the response
            return full_response.strip()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error generating response: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response content: {e.response.text}")
            return f"Error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

    def is_model_running(self):
        try:
            response = requests.get(f'http://localhost:{self.port}/api/tags')
            response.raise_for_status()
            models = response.json()
            logging.debug(f"Available models: {models}")
            return self.model in [model['name'] for model in models['models']]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error checking if model is running: {e}")
            return False

    def start_container(self):
        self.docker_manager.start_containers()
        logging.info(f"Started container: {self.container_name}")
        self.wait_for_ollama()
        self.ensure_model_available()

    def stop_container(self):
        self.docker_manager.stop_containers()
        logging.info(f"Stopped container: {self.container_name}")

    def wait_for_ollama(self, max_attempts=5, delay=5):
        for attempt in range(max_attempts):
            try:
                response = requests.get(f'http://localhost:{self.port}/api/tags')
                if response.status_code == 200:
                    logging.info(f"Successfully connected to Ollama on port {self.port}")
                    return True
            except requests.exceptions.RequestException:
                logging.warning(f"Attempt {attempt + 1}/{max_attempts}: Ollama on port {self.port} is not ready yet. Retrying in {delay} seconds...")
                time.sleep(delay)
        logging.error(f"Failed to connect to Ollama after {max_attempts} attempts")
        raise RuntimeError(f"Failed to connect to Ollama after {max_attempts} attempts")