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

    def sanitize(self, text):
        account_num_counter = 0
        resource_name_counter = 0

        for pattern, replacement in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                # Generate unique placeholders
                unique_account_placeholder = f"{{arnAccountNum{account_num_counter}}}"
                unique_resource_placeholder = f"{{arnName{resource_name_counter}}}"

                # Replace account number and resource name in the replacement string
                modified_replacement = replacement.replace("{arnAccountNum}", unique_account_placeholder)
                modified_replacement = modified_replacement.replace("{arnName}", unique_resource_placeholder)

                # Replace in text
                text = re.sub(pattern, modified_replacement, text, count=1)

                # Increment counters
                account_num_counter += 1
                resource_name_counter += 1

        return text

    def reverse_sanitization(self, text):
        """
        Reverse the sanitization process using the sanitization map.
        """
        for sanitized, original in self.sanitization_map.items():
            text = text.replace(sanitized, original)
        return text

