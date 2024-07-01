import logging
import requests
from typing import List, Tuple, Dict, Any
from .exceptions import LLMConnectionError

logger = logging.getLogger(__name__)

class LLMConnector:
    def __init__(self, config: Dict[str, Any]):
        self.ollama_url = config.get('ollama_url', 'http://localhost:11434')
        self.model_name = config.get('model_name', 'llama2')

    def is_llm_available(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except requests.RequestException as e:
            logger.warning(f"LLM service is not available: {str(e)}")
            return False

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        if not self.is_llm_available():
            raise LLMConnectionError("LLM service is not available for entity extraction")

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
            logger.error(f"Error in LLM entity extraction: {str(e)}")
            raise LLMConnectionError(f"Failed to extract entities: {str(e)}")