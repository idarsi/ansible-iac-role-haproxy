"""Validation filters used by the HAProxy role."""

import ipaddress
import re


_HOSTNAME_OR_IPV4 = re.compile(r"^[A-Za-z0-9_.%-]+$")


class FilterModule:
    """Expose role-local validation filters without external dependencies."""

    @staticmethod
    def haproxy_valid_backend_address(value):
        """Accept hostnames and valid IPv4/IPv6 literals."""
        if not isinstance(value, str) or not value:
            return False
        if ":" not in value:
            # Do not accept an out-of-range dotted decimal value as a hostname.
            if "." in value and all(character.isdigit() or character == "." for character in value):
                try:
                    return ipaddress.ip_address(value).version == 4
                except ValueError:
                    return False
            return bool(_HOSTNAME_OR_IPV4.fullmatch(value))
        try:
            return ipaddress.ip_address(value).version == 6
        except ValueError:
            return False

    def filters(self):
        return {"haproxy_valid_backend_address": self.haproxy_valid_backend_address}
