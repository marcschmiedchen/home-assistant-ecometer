"""
Proteus Ecometer integration for home assistant
"""

import logging

import serial
import serial_asyncio_fast
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import ConfigEntryNotReady
from homeassistant.const import CONF_RESOURCE
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from serial.tools.list_ports import comports
from tek603 import TEK603

from .const import BAUD_RATE
from .const import CONF_CONNECTION_TYPE
from .const import CONF_HOST
from .const import CONF_PORT
from .const import CONNECTION_USB
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the custom component over the config entry."""
    hass.data.setdefault(DOMAIN, {})

    connection_type = config_entry.data.get(CONF_CONNECTION_TYPE, CONNECTION_USB)

    if connection_type == CONNECTION_USB:
        usb_port = config_entry.data.get(CONF_RESOURCE)
        ports = await hass.async_add_executor_job(comports)
        if not any(p.device == usb_port for p in ports):
            raise ConfigEntryNotReady(f"Ecometer not found on {usb_port}")
        url = usb_port
        _LOGGER.info("using USB port: %s", usb_port)
    else:  # CONNECTION_TCP
        host = config_entry.data.get(CONF_HOST)
        port = config_entry.data.get(CONF_PORT)
        url = f"socket://{host}:{port}"
        _LOGGER.info("using TCP connection: %s:%s", host, port)
    try:
        # For USB: url = device path (e.g., /dev/ttyUSB0)
        # For TCP: url = socket://host:port
        transport, protocol = await serial_asyncio_fast.create_serial_connection(
            hass.loop, TEK603, url, baudrate=BAUD_RATE
        )
    except (serial.SerialException, OSError, TimeoutError) as e:
        raise ConfigEntryNotReady(f"Failed to open {url}: {e}") from e

    hass.data[DOMAIN]["protocol"] = protocol
    hass.data[DOMAIN]["transport"] = transport

    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.SENSOR]
    )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Close the serial connection and unload platforms."""
    transport = hass.data[DOMAIN].get("transport")
    if transport and not transport.is_closing():
        try:
            transport.close()
        except (serial.SerialException, OSError) as ex:
            _LOGGER.warning("Failed to close transport: %s", ex)
    hass.data[DOMAIN].clear()
    return await hass.config_entries.async_unload_platforms(
        config_entry, [Platform.SENSOR]
    )
