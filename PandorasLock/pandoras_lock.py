from KeyBase import KeyBase
import threading

class PandorasLock:
    def __init__(self):
        self.sanitization_map = {}
        self.reset_timer = None

    def sanitize(self, text, key_class):
        """
        Applies the sanitization process using the specified key class (DefaultKey or NetworkKey).
        """
        # Call the apply_filters method of the provided key class, passing in the text and sanitization map.
        sanitized_text = key_class.apply_filters(text, self.sanitization_map)
        return sanitized_text

    def reverse_sanitization(self, text):
        """
        Reverses the sanitization process using the sanitization map, replacing obfuscated values with their original counterparts.
        """
        for obfuscated, original in self.sanitization_map.items():
            text = text.replace(obfuscated, original)
        return text

    def clear_cache(self):
        """
        Clears the sanitization map immediately, removing all stored mappings between original and obfuscated values.
        """
        self.sanitization_map.clear()

    def schedule_reset(self, delay_seconds):
        """
        Schedules the sanitization map to be cleared after a specified delay, ensuring mappings do not persist indefinitely.
        """
        if self.reset_timer is not None:
            self.reset_timer.cancel()  # Cancel any existing timer
        self.reset_timer = threading.Timer(delay_seconds, self.clear_cache)
        self.reset_timer.start()

""" # Example usage and configuration path setup would be here

# Example usage
pandoras_lock = PandorasLock()
default_key = DefaultKey()
network_key = NetworkKey()

# Sanitize general data
sanitized_text = pandoras_lock.sanitize(original_text, default_key)

# Sanitize network data
sanitized_network_data = pandoras_lock.sanitize(network_data, network_key)
 """