"""Tools for querying IP interface properties of the system.
"""
import ifaddr
import ipaddress
import json
import os

VALID_PREFIXES = json.loads(os.getenv('INTERFACE_VALID_PREFIXES',
                                      '["eth","wlan"]'))


def get_interfaces(valid_prefixes: 'list[str]' = VALID_PREFIXES,
                   target: str = None,
                   ) -> dict:
    """Returns a dictionary of IP interfaces with IP addresses.
    
    Args:
        valid_prefixes: A list of prefixes to include in the search e.g. `eth`
        target: (optional) A specific interface to check for its IP address

    Returns:
        { "interface_name": "ip_address" }
    
    """
    interfaces = {}
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        if not any(adapter.name.startswith(x) for x in valid_prefixes):
            continue
        for ip in adapter.ips:
            if '.' in ip.ip:
                interfaces[adapter.name] = ip.ip
                break
        if target is not None and adapter.name == target:
            break
    return interfaces


def is_address_in_subnet(ipv4_address: str, subnetv4: str) -> bool:
    """Returns True if the IP address is part of the IP subnetwork.
    
    Args:
        ipv4_address: Address e.g. 192.168.1.101
        subnetv4: Subnet e.g. 192.168.0.0/16
    
    Returns:
        True if the IP address is within the subnet range.

    """
    subnet = ipaddress.ip_network(subnetv4)
    ip_address = ipaddress.ip_address(ipv4_address)
    if ip_address in subnet:
        return True
    return False


def is_valid_ip(ipv4_address: str) -> bool:
    try:
        ip_address = ipaddress.ip_address(ipv4_address)
        return True
    except ValueError:
        return False
    