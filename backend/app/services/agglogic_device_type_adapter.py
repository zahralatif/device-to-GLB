DEVICE_TYPE_MAPPING = {
    "switch": "Switch",
    "ethernet_switch": "Switch",
    "network_switch": "Switch",

    "server": "Server",

    "router": "Router",

    "firewall": "Firewall",

    "storage": "Storage",

    "ups": "UPS",

    "pdu": "PDU",
}


def normalize_device_type(name: str) -> str:
    """
    Convert Agglogic device type names
    into internal catalog names.
    """

    key = name.strip().lower()

    return DEVICE_TYPE_MAPPING.get(key, name.strip())