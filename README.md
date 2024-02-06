# README.md for PandorasKey Module

## Overview

PandorasKey is a Python module designed for obfuscating sensitive information within text data, particularly focusing on automation tasks in cloud environments like AWS, Azure, and GCP. Its primary purpose is to enhance security by preventing the exposure of sensitive data and to facilitate the generation of semi-synthetic training data for language model training.

### Key Features

- **Obfuscation of Sensitive Data**: PandorasKey can identify and replace sensitive information such as IP addresses, AWS account numbers, and other PII (Personally Identifiable Information) with placeholders.
- **Context Preservation**: While obfuscating data, the module ensures the preservation of contextual integrity, which is crucial for the utility of data in LLM (Large Language Model) training.
- **Reversibility**: The module provides functionality to reverse the obfuscation process, enabling the restoration of the original text data.
- **Customizable Regex Patterns**: Users can define custom regex patterns for detecting and obfuscating different types of sensitive information.

## Intended Use

- **Security in Cloud Environments**: Protect sensitive information in scripts and logs within cloud environments.
- **Training Data Generation**: Generate semi-synthetic datasets for training language models, ensuring that sensitive information is concealed while maintaining context for effective learning.

## Future Plans

- **Enhanced Network Data Handling**: We are exploring methods to obfuscate network-related data (like IP addresses) while maintaining context. This is aimed at preserving the relationship between network addresses and ensuring the utility of obfuscated data in network analysis.
- **Broadening Scope of Data Types**: Plans to include more data types and patterns, catering to a wider range of sensitive information.

## Usage

```python
from PandorasKey import PandorasKey

# Initialize PandorasKey with a configuration file
pandoras_key = PandorasKey(config_path="path_to_config.json")

# Example text
text = "Example text with sensitive information"

# Sanitize the text
sanitized_text = pandoras_key.sanitize(text)

# Print sanitized text
print("Sanitized Text:", sanitized_text)

# Reverse the sanitization
original_text = pandoras_key.reverse_sanitization(sanitized_text)

# Print the original text
print("Original Text:", original_text)
```

## Configuration

PandorasKey uses a JSON configuration file (`pandorasconfig.json`) to define regex patterns for detecting sensitive information. Users can customize this file to fit their specific requirements.

Example configuration snippet:
```json
{
    "IP_PATTERN": "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b",
    "AWS_ACCOUNT_NUM_PATTERN": "\\b\\d{12}\\b",
    ...
}
```

## Contribution

Contributions to PandorasKey are welcome. Please submit pull requests or issues on our GitHub repository.

## License

PandorasKey is licensed under [MIT License](https://opensource.org/licenses/MIT).

---

*Note: This README provides a high-level overview and is not exhaustive. It is recommended to refer to the detailed documentation for comprehensive information.*

---

End of README.md File for PandorasKey Module.