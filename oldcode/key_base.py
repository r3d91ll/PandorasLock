import json
import os
import logging

class KeyBase:
    def __init__(self, config_path='pandorasconfig.json'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        Load the configuration from a JSON file.
        """
        try:
            with open(self.config_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logging.error(f"Failed to load configuration from {self.config_path}: {e}")
            return {}

    def update_config(self, updates, save_to_file=False):
        """
        Update the configuration in memory with the provided updates and
        optionally write the updated configuration back to the file.

        Args:
            updates (dict): A dictionary containing updates to the configuration.
            save_to_file (bool): Whether to save the updated configuration to the file.
        """
        self.config.update(updates)
        if save_to_file:
            self.save_config()

    def save_config(self):
        """
        Write the current configuration back to the configuration file.
        """
        try:
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            logging.error(f"Failed to save configuration to {self.config_path}: {e}")
