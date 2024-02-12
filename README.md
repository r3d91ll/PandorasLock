# PandorasLock Module

## Overview

`PandorasLock` is a versatile Python module designed for the sanitization of sensitive information within text data, with a particular focus on network-related information such as IP addresses and subnets. It provides a flexible framework for obfuscating identifiable information while preserving or not preserving the relational network context, according to the needs of the application.

### Key Components
- **PandorasLock**: The core class responsible for managing the sanitization process.
- **KeyBase**: An abstract base class for defining common functionalities across different types of keys.
- **DefaultKey**: Handles general data patterns for sanitization.
- **NetworkKey**: Specialized in network data sanitization, with options to preserve network context.

## Installation

To install `PandorasLock`, clone or download the repository to your local environment:

```
git clone git@github.com:r3d91ll/PandorasLock.git
```

Ensure you have Python 3.x installed and navigate into the module directory. The module can be imported directly into your Python scripts.

## Usage

```python
from pandoraslock import PandorasLock, DefaultKey, NetworkKey

# Initialize the core class
pandoras_lock = PandorasLock()

# Example text to sanitize
original_text = "Sensitive information here with IP 192.168.1.1"
network_data = "Network configuration for subnet 192.168.1.0/24"

# Sanitize using DefaultKey for general data
sanitized_text = pandoras_lock.sanitize(original_text, DefaultKey())

# Sanitize using NetworkKey for network data, preserving network context
sanitized_network_data = pandoras_lock.sanitize(network_data, NetworkKey(preserve_network_context=True))
```

## Scenarios in Which PandorasLock Could Be Useful
- **Data Privacy Compliance**: Ensuring sensitive data within documents or logs is obfuscated before sharing or analysis.
- **Network Configuration Management**: Sanitizing network configurations for documentation or educational purposes, without revealing actual IP allocations.
- **Machine Learning Data Preparation**: Preparing datasets that contain sensitive information by sanitizing identifiable data, making the datasets suitable for training without compromising privacy.
- **Security Incident Reporting**: Anonymizing sensitive information in incident reports or logs that need to be shared with external parties.

## Note on Usage
`PandorasLock` is designed with flexibility in mind, allowing users to easily extend its functionality to suit various sanitization needs. While it provides robust mechanisms for data sanitization, always review sanitized outputs to ensure they meet your specific privacy and security requirements.

