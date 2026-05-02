"""
Proteus Ecometer integration for home assistant
"""

import logging

import serial_asyncio_fast
from homeassistant.config_entries import ConfigEntry, ConfigEntryNotReady
from homeassistant.const import CONF_RESOURCE, Platform
from homeassistant.core import HomeAssistant
from serial.tools.list_ports import comports
from tek603 import TEK603

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the custom component over the config entry."""
    hass.data.setdefault(DOMAIN, {})
    usb_port = config_entry.data[CONF_RESOURCE]
    _LOGGER.info(f"using: {usb_port} as port")

    ports = await hass.async_add_executor_job(comports)
    if not any(p.device == usb_port for p in ports):
        raise ConfigEntryNotReady(f"Ecometer not found on {usb_port}")

    try:
        transport, protocol = await serial_asyncio_fast.create_serial_connection(
            hass.loop, TEK603, usb_port, baudrate=115200
        )
    except Exception as e:
        raise ConfigEntryNotReady(f"Failed to open {usb_port}: {e}") from e

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
        transport.close()
    hass.data[DOMAIN].clear()
    return await hass.config_entries.async_unload_platforms(
        config_entry, [Platform.SENSOR]
    )
