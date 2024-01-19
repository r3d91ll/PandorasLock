# filename: pandoras_module.py

import re
import json
import random
from typing import Dict, List

class PandorasLock:
    def __init__(self, config_path: str = None):
        self.sanitization_map = {}
        self.patterns = self.load_patterns(config_path)

    def load_patterns(self, config_path: str) -> Dict[str, str]:
        # Placeholder for loading patterns from a configuration file
        # You can replace this with actual file loading logic
        return {
            "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        }

    def sanitize(self, text: str) -> str:
        for placeholder, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                sanitized = f"<{placeholder}>"
                self.sanitization_map[sanitized] = match
                text = text.replace(match, sanitized)
        return text

    def reverse_sanitization(self, sanitized_text: str) -> str:
        for sanitized, original in self.sanitization_map.items():
            sanitized_text = sanitized_text.replace(sanitized, original)
        return sanitized_text

class PandorasBox:
    def __init__(self, pandoras_lock: PandorasLock):
        self.pandoras_lock = pandoras_lock
        self.original_order_map = {}

    def process_code_block(self, code_block: str) -> str:
        lines = code_block.split('\n')
        original_order = {i: line for i, line in enumerate(lines)}
        random.shuffle(lines)
        sanitized_lines = [self.pandoras_lock.sanitize(line) for line in lines]
        self.original_order_map = {sanitized: index for index, sanitized in enumerate(sanitized_lines)}
        return '\n'.join(sanitized_lines)

    def revert_code_order(self, sanitized_code_block: str) -> str:
        lines = sanitized_code_block.split('\n')
        original_lines = [''] * len(lines)
        for line in lines:
            original_index = self.original_order_map[line]
            original_lines[original_index] = self.pandoras_lock.reverse_sanitization(line)
        return '\n'.join(original_lines)

# Example usage:
# pandoras_lock = PandorasLock()
# pandoras_box = PandorasBox(pandoras_lock)
# sanitized_code = pandoras_box.process_code_block("Sensitive code with email example@example.com")
# print(sanitized_code)
# original_code = pandoras_box.revert_code_order(sanitized_code)
# print(original_code)