import os
import json
import re
import logging

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
        
    def sanitize(self, text):
        placeholder_counter = {}

        for key, pattern in self.patterns.items():
            placeholder = key.replace("_PATTERN", "")
            matches = re.finditer(pattern, text)
            for match in matches:
                if "ARN" in key or "ID" in key:
                    # For ARN and ID patterns with a single capture group
                    found_match = match.group(1)
                else:
                    # General handling for other patterns
                    found_match = match.group(0)

                existing_key = next((k for k, v in self.sanitization_map.items() if v == found_match), None)

                if existing_key:
                    text = text.replace(found_match, existing_key)
                else:
                    placeholder_counter.setdefault(placeholder, -1)
                    placeholder_counter[placeholder] += 1
                    unique_placeholder = f"{{{placeholder}{placeholder_counter[placeholder]}}}"
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
