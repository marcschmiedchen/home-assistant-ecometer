"""
Ecometer
"""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_RESOURCE, Platform
import serial_asyncio_fast
from .tek603 import TEK603

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """set up the custom component over the config entry"""
    hass.data.setdefault(DOMAIN, {})
    usb_port = config_entry.data[CONF_RESOURCE]
    _LOGGER.debug(f"using: {usb_port} as port")

    coro = serial_asyncio_fast.create_serial_connection(
        hass.loop, TEK603, usb_port, baudrate=115200
    )

    task = hass.loop.create_task(coro)
    await task
    if task.done():
        transport, protocol = task.result()
        _LOGGER.debug("waiting for serial data")
        hass.data[DOMAIN]["protocol"] = protocol
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, Platform.SENSOR)
        )
    return True
