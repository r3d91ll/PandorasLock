import json
import os
import logging

class KeyBase:
    def __init__(self, config_path=None):
        default_path = 'pandorasconfig.json'  # Adjusted to a simpler default for demonstration
        self.config_path = config_path or os.getenv('PANDORACONFIG_PATH', default_path)
        self.patterns = self.load_regex_patterns()

    def load_regex_patterns(self):
        """
        Load regular expression patterns from a JSON configuration file.
        """
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
            return {k: v for k, v in config.items() if self.pattern_key in k}
        except FileNotFoundError:
            logging.error(f"Config file {self.config_path} not found.")
            return {}

    # Placeholder for the pattern key, to be specified in subclasses
    pattern_key = ""
