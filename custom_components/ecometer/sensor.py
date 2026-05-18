"""
Support for Ecometer / Tekelek water sensor
"""

import logging

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import ConfigEntryNotReady
from homeassistant.const import UnitOfLength
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from tek603 import TEK603

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    performs setup of the analog sensors, expects a
    reference to an Ecometer serial protocol via hass.data
    """
    if DOMAIN not in hass.data or "protocol" not in hass.data[DOMAIN]:
        raise ConfigEntryNotReady("Ecometer protocol not initialized")

    tek603 = hass.data[DOMAIN]["protocol"]
    if tek603 is None:
        raise ConfigEntryNotReady("Ecometer protocol is None")

    sensors = []
    for nbr in tek603.get_all_sensors():
        sensors.append(EcometerSensor(tek603, nbr))
    async_add_entities(sensors)


class EcometerSensor(SensorEntity):
    """
    Implementation of Ecometer Sensors.
    """

    should_poll = False
    _attr_has_entity_name = True

    def __init__(self, tek603: TEK603, dp_nbr: int) -> None:
        self._dp_nbr = dp_nbr
        self._tek603 = tek603
        unit = tek603.get_unit(dp_nbr)

        self._attr_name = tek603.get_name(dp_nbr)
        self._attr_unique_id = f"{DOMAIN}_{dp_nbr}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "Proteus")},
            "name": "Ecometer",
            "manufacturer": "Proteus",
        }
        if unit == "C":
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif unit == "cm":
            self._attr_device_class = SensorDeviceClass.DISTANCE
            self._attr_native_unit_of_measurement = UnitOfLength.CENTIMETERS
        elif unit == "l":
            self._attr_device_class = SensorDeviceClass.VOLUME_STORAGE
            self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        _LOGGER.debug("setup ecometer %s: %s in %s", dp_nbr, self._attr_name, unit)

    async def async_added_to_hass(self) -> None:
        self._tek603.register_callback(self.async_write_ha_state, self._dp_nbr)

    async def async_will_remove_from_hass(self) -> None:
        self._tek603.remove_callback(self._dp_nbr)

    @property
    def available(self) -> bool:
        return self._tek603.connected()

    @property
    def native_value(self) -> float:
        value = self._tek603.read_sensor(self._dp_nbr)
        _LOGGER.debug("set ecometer (%s) to %s", self._dp_nbr, value)
        return value
