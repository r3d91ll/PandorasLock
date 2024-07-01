import json
import logging
from typing import Dict, Any
from .exceptions import ConfigLoadError

logger = logging.getLogger(__name__)

class ConfigLoader:
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            if not isinstance(config, dict):
                raise ConfigLoadError("Invalid config format. Expected a dictionary.")
            return config
        except (FileNotFoundError, json.JSONDecodeError, ConfigLoadError) as e:
            logger.error(f"Error loading config file {config_path}: {str(e)}")
            raise ConfigLoadError(f"Failed to load configuration: {str(e)}")