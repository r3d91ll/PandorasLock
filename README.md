# PandorasLock Project

## IMPORTANT NOTE: This code is currently under testing and is NOT ready for production use

## Overview

PandorasLock is a project containing the PandorasKey module, a versatile Python tool designed for securing sensitive information within text data across various domains, including cloud environments, data analysis, and machine learning. Inspired by the myth of Pandora's Box, this tool acts as the lock that should have been placed on the box, helping to keep secrets secure.

The PandorasKey module's primary function is to identify and obfuscate sensitive data such as IP addresses, account numbers, and personal identifiers, making it a valuable tool for a broad range of users concerned with data privacy and security.

### Key Features

- **Universal Data Obfuscation**: Suitable for a wide array of applications beyond cloud environments, including data science, machine learning, and general data processing tasks.
- **Customizable and Extensible**: Users can define custom regex patterns in a configuration file, allowing for the extension of the module to cover various types of sensitive information.
- **Reversible Obfuscation**: Applies a reversal process to all incoming prompts such that replies containing keys are immediately reversed prior to being presented to the user. Offers the capability to reverse the obfuscation process, enabling the retrieval of the original text data.
- **Key Storage**: Stores keys locally throughout the entire conversation to maintain context when a key is referenced again.
- **Context Preservation**: Ensures that the obfuscated data retains its contextual relevance, crucial for analysis and machine learning applications.
- **LLM Integration**: Utilizes a locally hosted Language Model (via Ollama) for enhanced entity recognition and classification.
- **Modular Design**: Separates concerns into distinct classes for configuration loading, LLM interaction, and core sanitization functionality.

## Intended Use

- **Data Security and Privacy**: Ideal for scenarios where sensitive data needs to be protected or anonymized, such as in logs, datasets, and communication scripts.
- **Training Data Preparation**: Generates semi-synthetic datasets for machine learning, especially for NLP and LLM training, while ensuring data privacy.
- **General Data Processing**: Useful in any context where sensitive data needs to be identified and concealed without losing the integrity of the information.

## Recent Updates

- **Improved Modularity**: Restructured the code to separate configuration loading, LLM interaction, and core sanitization functionality into distinct classes.
- **Enhanced Error Handling**: Implemented comprehensive error handling for external dependencies and potential failure points.
- **Logging Implementation**: Added proper logging with different levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) for better diagnostics and monitoring.
- **LLM Integration**: Incorporated local LLM capabilities using Ollama for improved entity recognition.
- **Directional Sanitization**: Introduced separate methods for sanitizing egress (outgoing) and ingress (incoming) text.

## Future Enhancements

- **Advanced Network Data Handling**: Focusing on sophisticated methods for obfuscating network-related data while maintaining relational context and utility in analysis.
- **Expanding Data Type Coverage**: Aiming to broaden the range of detectable and obfuscatable data types to cater to diverse data security needs.
- **Human/LLM Input Paths**: Planning to add separate input paths for human and LLM input to the module.
- **Performance Optimization**: Improve processing speed for large volumes of text.
- **Extended LLM Support**: Explore integration with other LLM providers and models.

## Usage Example

```python
from pandoras_key import PandorasKey

# Initialize with configuration file
pandoras_key = PandorasKey(config_path="path_to_config.json")

# Sanitize outgoing text containing sensitive data
sanitized_text, entities = pandoras_key.process_text("Sensitive text with IP: 192.168.1.1", direction="egress")

# Process incoming text (reverse sanitization)
original_text, _ = pandoras_key.process_text(sanitized_text, direction="ingress")

print("Sanitized Text:", sanitized_text)
print("Extracted Entities:", entities)
print("Original Text:", original_text)

# Clear the sanitization cache when done
pandoras_key.clear_sanitization_cache()
```

## Configuration

The module uses a JSON configuration file (`pandorasconfig.json`) for regex patterns and LLM settings. Users can modify this file for custom data types, patterns, and LLM configuration.

Example:

```json
{
    "patterns": {
        "IP_PATTERN": "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b",
        "CUSTOM_DATA_PATTERN": "custom_regex_here"
    },
    "ollama_url": "http://localhost:11434",
    "model_name": "llama2"
}
```

## Dependencies

- Python 3.7+
- requests
- Ollama (for local LLM functionality)

## Installation

(Note: As the project is still under development, installation instructions will be provided once a stable version is released.)

## Contributions

We encourage contributions to PandorasLock. Please feel free to submit pull requests or issues on our repository for improvements or feature requests.

## License

PandorasLock is made available under the [MIT License](https://opensource.org/licenses/MIT).
