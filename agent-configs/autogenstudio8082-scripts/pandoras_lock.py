# filename: pandoras_lock.py

import re
import os
import json

class PandorasLock:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.getenv('PANDORAS_LOCK_CONFIG')
        self.patterns = {}
        self.sanitization_map = {}
        self.load_patterns()

    def load_patterns(self):
        if not self.config_path or not os.path.exists(self.config_path):
            raise FileNotFoundError("Configuration file not found.")
        with open(self.config_path, 'r') as config_file:
            self.patterns = json.load(config_file)

    def sanitize(self, text):
        sanitized_text = text
        for placeholder, pattern in self.patterns.items():
            regex = re.compile(pattern)
            if matches := regex.findall(sanitized_text):
                for match in matches:
                    if match not in self.sanitization_map:
                        self.sanitization_map[match] = placeholder
                    sanitized_text = sanitized_text.replace(match, placeholder)
        return sanitized_text

    def reverse_sanitization(self, sanitized_text):
        for original, placeholder in self.sanitization_map.items():
            sanitized_text = sanitized_text.replace(placeholder, original)
        return sanitized_text

# Example usage:
# lock = PandorasLock(config_path='path_to_config.json')
# sanitized = lock.sanitize("Sensitive information here.")
# original = lock.reverse_sanitization(sanitized)