import re
from .key_base import KeyBase

class DefaultKey(KeyBase):
    def __init__(self, config, config_path=None):
        # Initialize with the full config dictionary instead of just a path
        super().__init__(config_path)
        self.config = config

    def apply_filters(self, text):
        # Apply literal replacements first
        text = self.apply_literal_replacements(text, self.config["LITERAL"])

        # Apply regex patterns
        text = self.apply_regex_patterns(text, self.config["REGEX"])
        
        return text

    def apply_literal_replacements(self, text, literals):
        for literal, replacement in literals.items():
            text = text.replace(literal, replacement)
        return text

    def apply_regex_patterns(self, text, regex_patterns):
        for category, patterns in regex_patterns.items():
            for pattern_name, pattern in patterns.items():
                regex = re.compile(pattern)
                text = regex.sub(lambda m: self._generate_obfuscated_value(m.group(0), pattern_name), text)
        return text

    def _generate_obfuscated_value(self, original_text, pattern_name):
        # Enhanced method for generating an obfuscated value
        placeholder = pattern_name.lower()
        # This is a placeholder for the actual obfuscation logic
        return f"{placeholder}_obfuscated"
