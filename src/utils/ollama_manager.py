import requests
import json
import time
import logging

class OllamaManager:
    def __init__(self, host, port, model):
        self.base_url = f"http://{host}:{port}"
        self.model = model
        self.logger = logging.getLogger(__name__)

    def is_service_ready(self, max_retries=5, delay=2):
        for _ in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            time.sleep(delay)
        return False

    def pull_model(self):
        try:
            response = requests.post(f"{self.base_url}/api/pull", json={"name": self.model})
            response.raise_for_status()
            self.logger.info(f"Successfully pulled model: {self.model}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to pull model: {e}")

    def generate_response(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt},
                stream=True
            )
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            full_response += chunk['response']
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to decode JSON: {line}")
            
            return full_response.strip()
        except requests.RequestException as e:
            self.logger.error(f"Failed to generate response: {e}")
            return None

    def generate_response_with_details(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt},
                stream=True
            )
            response.raise_for_status()
            
            full_response = ""
            chunks = []
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        chunks.append(chunk)
                        if 'response' in chunk:
                            full_response += chunk['response']
                        if chunk.get('done', False):
                            break
                    except json.JSONDecodeError:
                        self.logger.warning(f"Failed to decode JSON: {line}")
            
            return full_response.strip(), chunks
        except requests.RequestException as e:
            self.logger.error(f"Failed to generate response: {e}")
            return None, []