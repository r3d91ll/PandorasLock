import threading
import re
import json
import os
import logging

class PandorasLock:
    def __init__(self, config_path='pandorasconfig.json'):
        self.sanitization_map = {}
        self.counter = {}  # Initialize a counter for each regex pattern
        self.config = self.load_config(config_path)
        self.reset_timer = None

    def load_config(self, config_path):
        # Adjust the path to point to the correct location of pandorasconfig.json
        actual_path = os.path.join(os.path.dirname(__file__), '..', 'PandorasLock', 'pandorasconfig.json')
        try:
            with open(actual_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Failed to load configuration from {actual_path}: {e}")
            return {"REGEX": {}, "LITERAL": {}}
        
    def sanitize(self, text):
        text = self.apply_literal_replacements(text, self.config["LITERAL"])
        text = self.apply_regex_patterns(text, self.config["REGEX"])
        return text

    def apply_literal_replacements(self, text, literals):
        for literal, replacement in literals.items():
            text = text.replace(literal, replacement)
        return text

    def apply_regex_patterns(self, text, regex_patterns):
        for category, patterns in regex_patterns.items():
            for pattern_name, pattern in patterns.items():
                self._apply_pattern(text, pattern, pattern_name)
        return text

    def _apply_pattern(self, text, pattern, pattern_name):
        regex = re.compile(pattern)
        def replacement_func(match):
            match_text = match.group(0)
            if match_text not in self.sanitization_map:
                if pattern_name not in self.counter:
                    self.counter[pattern_name] = 1
                else:
                    self.counter[pattern_name] += 1
                placeholder = f"{{{{ {pattern_name}{self.counter[pattern_name]} }}}}"
                self.sanitization_map[match_text] = placeholder
            return self.sanitization_map[match_text]
        return regex.sub(replacement_func, text)

    def reverse_sanitization(self, text):
        for original, obfuscated in self.sanitization_map.items():
            text = text.replace(obfuscated, f"{{{{ {original} }}}}")
        return text

    def clear_cache(self):
        self.sanitization_map.clear()
        self.counter.clear()

    def schedule_reset(self, delay_seconds):
        if self.reset_timer is not None:
            self.reset_timer.cancel()
        self.reset_timer = threading.Timer(delay_seconds, self.clear_cache)
        self.reset_timer.start()

if __name__ == "__main__":
    pandoras_lock = PandorasLock()
    sanitized_text = pandoras_lock.sanitize("Example text with IP 192.168.1.1 and email example@example.com.")
    print(sanitized_text)
