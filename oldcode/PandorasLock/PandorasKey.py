import os
import json
import re
import logging
import subprocess
import requests
from typing import List, Tuple, Dict, Any

class PandorasKey:
    """
    A class to sanitize sensitive information in text using Ollama-served LLM for NER, 
    custom patterns, and regular expressions.
    """
    def __init__(self, config_path: str = None):
        default_path = 'PandorasLock/pandorasconfig.json'
        self.config_path = config_path or os.getenv('PANDORACONFIG_PATH', default_path)
        self.config = self.load_config()
        self.patterns = self.config.get('patterns', {})
        self.sanitization_map: Dict[str, str] = {}
        self.ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
        self.model_name = self.config.get('model_name', 'llama2')
        
        if not self.is_ollama_running():
            self.start_ollama()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
            if not isinstance(config, dict):
                raise ValueError("Invalid config format. Expected a dictionary.")
            return config
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.error(f"Error loading config file {self.config_path}: {str(e)}")
            return {}

    def is_ollama_running(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def start_ollama(self):
        try:
            subprocess.Popen(["ollama", "run", self.model_name])
            logging.info(f"Started Ollama with model {self.model_name}")
        except subprocess.SubprocessError as e:
            logging.error(f"Failed to start Ollama: {str(e)}")
            raise

    def extract_entities_with_llm(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract named entities from the text using Ollama-served LLM.
        """
        prompt = f"Extract named entities from the following text and classify them. Format the output as a list of (entity, type) tuples:\n\n{text}"
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model_name, "prompt": prompt}
            )
            response.raise_for_status()
            result = response.json()
            entities = eval(result['response'].strip())
            return entities
        except (requests.RequestException, ValueError) as e:
            logging.error(f"Error in LLM entity extraction: {str(e)}")
            return []

    def extract_custom_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract entities based on custom regex patterns.
        """
        custom_entities = []
        for key, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                custom_entities.append((match.group(), key.replace('_PATTERN', '')))
        return custom_entities

    def sanitize(self, text: str) -> str:
        """
        Sanitize the text using a combination of Ollama-based NER and custom patterns.
        """
        llm_entities = self.extract_entities_with_llm(text)
        custom_entities = self.extract_custom_entities(text)
        all_entities = llm_entities + custom_entities
        
        for entity, entity_type in all_entities:
            if entity not in self.sanitization_map:
                placeholder = f"{{{entity_type}}}"
                self.sanitization_map[entity] = placeholder
            
            text = text.replace(entity, self.sanitization_map[entity])
        
        return text

    def reverse_sanitization(self, text: str) -> str:
        """
        Reverse the sanitization process using the sanitization map.
        """
        for sanitized, original in self.sanitization_map.items():
            text = text.replace(original, sanitized)
        return text

    def clear_cache(self) -> None:
        """
        Clear the sanitization map.
        """
        self.sanitization_map.clear()

    def process_text(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Process the text: sanitize it and return both the sanitized text and extracted entities.
        """
        llm_entities = self.extract_entities_with_llm(text)
        custom_entities = self.extract_custom_entities(text)
        all_entities = llm_entities + custom_entities
        sanitized_text = self.sanitize(text)
        return sanitized_text, all_entities

# Example usage
if __name__ == "__main__":
    pandora = PandorasKey()
    sample_text = "John Doe works at Apple Inc. His email is john.doe@apple.com and SSN is 123-45-6789. The server IP is 192.168.1.1 and the instance ID is i-1234abcd."
    sanitized, entities = pandora.process_text(sample_text)
    print(f"Sanitized text: {sanitized}")
    print(f"Extracted entities: {entities}")
    print(f"Reversed: {pandora.reverse_sanitization(sanitized)}")