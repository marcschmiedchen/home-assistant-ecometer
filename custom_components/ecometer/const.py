"""
Constants for the Proteus Ecometer integration.
"""

from typing import Final

DOMAIN: Final[str] = "ecometer"

CONF_CONNECTION_TYPE: Final[str] = "connection_type"
CONF_HOST: Final[str] = "host"
CONF_PORT: Final[str] = "port"

CONNECTION_USB: Final[str] = "usb"
CONNECTION_TCP: Final[str] = "tcp"

# Hardware configuration
BAUD_RATE: Final[int] = 115200
DEFAULT_TCP_PORT: Final[int] = 2000
DEFAULT_TCP_HOST: Final[str] = "localhost"

# USB device identifiers for CP2102
USB_VENDOR: Final[str] = "Silicon Labs"
USB_PRODUCT: Final[str] = "CP2102"
