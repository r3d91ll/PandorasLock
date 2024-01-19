# filename: pandoras_box.py

import random
from pandoras_lock import PandorasLock

class PandorasBox:
    def __init__(self, pandoras_lock):
        if not isinstance(pandoras_lock, PandorasLock):
            raise ValueError("pandoras_lock must be an instance of PandorasLock")
        self.pandoras_lock = pandoras_lock
        self.original_order_map = {}

    def process_code_block(self, code_block):
        lines = code_block.split('\n')
        original_order = {index: line for index, line in enumerate(lines)}
        shuffled_lines = random.sample(lines, len(lines))
        sanitized_lines = [self.pandoras_lock.sanitize(line) for line in shuffled_lines]
        self.original_order_map = {sanitized: original for original, sanitized in zip(original_order, sanitized_lines)}
        return '\n'.join(sanitized_lines)

    def revert_code_order(self, sanitized_code_block):
        lines = sanitized_code_block.split('\n')
        original_lines = [self.original_order_map[line] for line in lines if line in self.original_order_map]
        return '\n'.join(original_lines)

# Example usage:
# lock = PandorasLock(config_path='path_to_config.json')
# box = PandorasBox(lock)
# processed_code = box.process_code_block("Sensitive code block here.")
# reverted_code = box.revert_code_order(processed_code)