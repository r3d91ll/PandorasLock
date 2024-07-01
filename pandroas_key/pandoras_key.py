import os
import re
import logging
from typing import List, Tuple, Dict
from .config_loader import ConfigLoader
from .llm_connector import LLMConnector
from .exceptions import InvalidDirectionError

logger = logging.getLogger(__name__)

class PandorasKey:
    def __init__(self, config_path: str = None):
        default_path = 'config/pandorasconfig.json'
        self.config_path = config_path or os.getenv('PANDORACONFIG_PATH', default_path)
        self.config = ConfigLoader.load_config(self.config_path)
        self.patterns = self.config.get('patterns', {})
        self.sanitization_map: Dict[str, str] = {}
        self.llm_connector = LLMConnector(self.config)

    def extract_custom_entities(self, text: str) -> List[Tuple[str, str]]:
        custom_entities = []
        for key, pattern in self.patterns.items():
            try:
                matches = re.finditer(pattern, text)
                for match in matches:
                    custom_entities.append((match.group(), key.replace('_PATTERN', '')))
            except re.error as e:
                logger.error(f"Error in regex pattern {key}: {str(e)}")
        return custom_entities

    def sanitize_egress(self, text: str) -> str:
        llm_entities = self.llm_connector.extract_entities(text)
        custom_entities = self.extract_custom_entities(text)
        all_entities = llm_entities + custom_entities
        
        for entity, entity_type in all_entities:
            if entity not in self.sanitization_map:
                placeholder = f"{{{entity_type}}}"
                self.sanitization_map[entity] = placeholder
            
            text = text.replace(entity, self.sanitization_map[entity])
        
        return text

    def sanitize_ingress(self, text: str) -> str:
        for sanitized, original in self.sanitization_map.items():
            text = text.replace(original, sanitized)
        return text

    def clear_sanitization_cache(self) -> None:
        self.sanitization_map.clear()
        logger.debug("Sanitization cache cleared")

    def process_text(self, text: str, direction: str = "egress") -> Tuple[str, List[Tuple[str, str]]]:
        if direction == "egress":
            sanitized_text = self.sanitize_egress(text)
        elif direction == "ingress":
            sanitized_text = self.sanitize_ingress(text)
        else:
            raise InvalidDirectionError("Invalid direction. Use 'egress' or 'ingress'.")

        all_entities = self.llm_connector.extract_entities(text) + self.extract_custom_entities(text)
        return sanitized_text, all_entities