# possible extension for PandorasLock. this will allow code to be sanitized and then deconstructed prior to being sent to a model for processing. 
# the deconstruction will be recorded and can be used to reconstruct the original code after the model has processed it.

class PandorasBox:
    def __init__(self, sanitizer):
        self.sanitizer = sanitizer
        self.original_order_map = {}

    def process_code_block(self, code_block):
        """
        Public function to process a code block with sanitization and deconstruction.
        """
        # Separate lines and shuffle them randomly
        lines = code_block.split("\n")
        random.shuffle(lines)

        # Apply PandorasLock and record original order
        for i in range(len(lines)):
            sanitized_line = self.sanitizer.sanitize(lines[i])
            self.original_order_map[sanitized_line] = lines[i]
            lines[i] = sanitized_line

        # Join the shuffled and sanitized lines and return
        return "\n".join(lines)

    def revert_code_order(self, sanitized_block):
        """
        Reverts the order of code lines to the original, using the original_order_map.
        """
        lines = sanitized_block.split("\n")
        reverted_lines = [self.original_order_map.get(line, line) for line in lines]
        return "\n".join(reverted_lines)

# # Example usage: PandorasLock
# # Create an instance of PandorasLock
# lock = PandorasLock()

# # Sanitize a text using the loaded regex patterns
# text = "My email is john.doe@example.com and my phone number is 123-456-7890."
# sanitized_text = lock.sanitize(text)
# print(sanitized_text)
# # Output: "My email is [EMAIL] and my phone number is [PHONE]."

# # Reverse the sanitization process
# original_text = lock.reverse_sanitization(sanitized_text)
# print(original_text)
# # Output: "My email is john.doe@example.com and my phone number is 123-456-7890."
