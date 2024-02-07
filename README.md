# README.md for PandorasKey Module

## Overview

PandorasKey is a versatile Python module designed for sanitizing sensitive information within text data across various domains, including cloud environments, data analysis, and machine learning. Its primary function is to identify and obfuscate sensitive data such as IP addresses, account numbers, and personal identifiers, making it a valuable tool for a broad range of users concerned with data privacy and security.

### Key Features

- **Universal Data Obfuscation**: Suitable for a wide array of applications beyond cloud environments, including data science, machine learning, and general data processing tasks.
- **Customizable and Extensible**: Users can define custom regex patterns in a configuration file, allowing for the extension of the module to cover various types of sensitive information.
- **Reversible Obfuscation**: Applies a reversal process to all incoming prompts such that replies containing keys are immediately reversed prior to being presented to the user. Offers the capability to reverse the obfuscation process, enabling the retrieval of the original text data.
- **Stores keys**: stores keys localy through the entire conversation so that if a key is referenced again we can maintain context.
- **Context Preservation**: Ensures that the obfuscated data retains its contextual relevance, crucial for analysis and machine learning applications.

## Intended Use

- **Data Security and Privacy**: Ideal for scenarios where sensitive data needs to be protected or anonymized, such as in logs, datasets, and communication scripts.
- **Training Data Preparation**: Generates semi-synthetic datasets for machine learning, especially for NLP and LLM training, while ensuring data privacy.
- **General Data Processing**: Useful in any context where sensitive data needs to be identified and concealed without losing the integrity of the information.

## Future Enhancements

- **Advanced Network Data Handling**: Focusing on sophisticated methods for obfuscating network-related data while maintaining relational context and utility in analysis.
- **Expanding Data Type Coverage**: Aiming to broaden the range of detectable and obfuscatable data types to cater to diverse data security needs.
- **Add Human/LLM**: adding separate input pathes for human and LLM input to the module

## Usage Example


```python
from PandorasKey import PandorasKey

# Initialize with configuration file
pandoras_key = PandorasKey(config_path="path_to_config.json")

# Sanitize text containing sensitive data
sanitized_text = pandoras_key.sanitize("Sensitive text with IP: 192.168.1.1")

# Reverse the sanitization to retrieve original text
original_text = pandoras_key.reverse_sanitization(sanitized_text)

print("Sanitized Text:", sanitized_text)
print("Original Text:", original_text)
```

## Configuration

The module uses a JSON configuration file (`pandorasconfig.json`) for regex patterns. Users can modify this file for custom data types and patterns.

Example:
```json
{
    "IP_PATTERN": "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b",
    "CUSTOM_DATA_PATTERN": "custom_regex_here",
    ...
}
```

## Contributions

We encourage contributions to PandorasKey. Please feel free to submit pull requests or issues on our repository for improvements or feature requests.

## License

PandorasKey is made available under the [MIT License](https://opensource.org/licenses/MIT).

---

*Note: This README is a guide. For detailed documentation, please refer to our official documentation.*

---

End of README.md File for PandorasKey Module.