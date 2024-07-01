class ConfigLoadError(Exception):
    """Raised when there's an error loading the configuration."""
    pass

class LLMConnectionError(Exception):
    """Raised when there's an error connecting to or using the LLM service."""
    pass

class InvalidDirectionError(ValueError):
    """Raised when an invalid direction is specified for text processing."""
    pass