import hashlib
import ipaddress

class NetworkKey(KeyBase):
    pattern_key = "_NETWORK"

    def __init__(self, config_path=None, preserve_network_context=True):
        super().__init__(config_path)
        self.preserve_network_context = preserve_network_context

    def apply_filters(self, text, sanitization_map):
        # This implementation now uses the ipaddress module to identify and process IP addresses
        updated_map = {}
        words = text.split()  # Simplistic splitting; consider more sophisticated parsing depending on the context
        for word in words:
            try:
                # Attempt to create an IPv4Address or IPv6Address object
                ip_obj = ipaddress.ip_address(word)
                original_ip = str(ip_obj)
                if self.preserve_network_context:
                    obfuscated_ip = self._preserve_network_context(ip_obj, sanitization_map)
                else:
                    obfuscated_ip = self._without_network_context(ip_obj, sanitization_map)
                updated_map[original_ip] = obfuscated_ip
            except ValueError:
                # Not a valid IP address, move to the next word
                continue
        
        # Apply the updated map to the text
        for original, obfuscated in updated_map.items():
            text = text.replace(original, obfuscated)

        return text

    def _preserve_network_context(self, ip_obj, sanitization_map):
        # Implement logic to obfuscate the IP while preserving network context
        # Example: Using a network-based hash or encoding
        network = ipaddress.ip_network(ip_obj, strict=False)
        obfuscated_network = hashlib.sha256(str(network.network_address).encode()).hexdigest()[:8]
        return f"{obfuscated_network}_{ip_obj}"

    def _without_network_context(self, ip_obj, sanitization_map):
        # Obfuscate the IP without considering its network context
        return hashlib.sha256(str(ip_obj).encode()).hexdigest()[:8]
