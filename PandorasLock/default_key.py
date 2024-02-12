import re

class DefaultKey(KeyBase):
    pattern_key = "_DEFAULT"

    def __init__(self, config_path=None):
        super().__init__(config_path)

    def apply_filters(self, text, sanitization_map):
        updated_map = {}
        for pattern_name, pattern in self.patterns.items():
            # Compiling the regex pattern for efficiency
            regex = re.compile(pattern)
            for match in regex.finditer(text):
                original_text = match.group(0)
                
                # Check if the text is already in the sanitization map
                if original_text in sanitization_map:
                    # Use the existing obfuscated value
                    obfuscated_text = sanitization_map[original_text]
                else:
                    # Generate a new obfuscated value
                    obfuscated_text = self._generate_obfuscated_value(original_text, pattern_name, sanitization_map)
                    # Update the map with the new obfuscated value
                    sanitization_map[original_text] = obfuscated_text
                    updated_map[original_text] = obfuscated_text
                
                # Replace the original text with its obfuscated counterpart in the main text
                text = text.replace(original_text, obfuscated_text)

        return text

    def _generate_obfuscated_value(self, original_text, pattern_name, sanitization_map):
        # Placeholder for generating an obfuscated value based on the pattern
        # This could involve a simple replacement strategy or a more complex, secure hashing mechanism
        # For demonstration, let's use a simple incremental ID approach
        placeholder = pattern_name.replace("_DEFAULT", "").lower()
        count = len(sanitization_map)
        return f"{placeholder}_{count}"