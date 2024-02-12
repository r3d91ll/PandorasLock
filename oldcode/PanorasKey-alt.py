import os
import json
import re
import logging
import random
import string

class PandorasKey:
    """
    A class to sanitize sensitive information in text using regular expressions
    and to reverse the sanitization in AI responses.
    """
    def __init__(self, config_path=None):
        # Set a default path and allow override by an environment variable or direct argument
        default_path = 'PandorasLock/pandorasconfig.json'
        self.config_path = config_path or os.getenv('PANDORACONFIG_PATH', default_path)
        self.patterns = self.load_regex_patterns()
        self.sanitization_map = {}  # To keep track of original and sanitized data

    def load_regex_patterns(self):
        """
        Load regular expression patterns from a JSON configuration file.
        """
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Config file {self.config_path} not found.")
            return {}

    def generate_unique_key(self, pattern):
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{pattern}_{random_id}"
        
    def sanitize(self, text):
        for key, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                found_match = match.group(0)
                unique_placeholder = self.generate_unique_key(key)
                self.sanitization_map[unique_placeholder] = found_match
                text = text.replace(found_match, unique_placeholder)

        return text

    def reverse_sanitization(self, text):
        """
        Reverse the sanitization process using the sanitization map.
        """
        for sanitized, original in self.sanitization_map.items():
            text = text.replace(sanitized, original)
        return text

    def clear_cache(self):
        """
        Clear the sanitization map.
        """
        self.sanitization_map.clear()
