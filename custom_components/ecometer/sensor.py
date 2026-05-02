"""
Support for Ecometer / Tekelek water sensor
"""

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import (
    UnitOfLength,
    UnitOfTemperature,
    UnitOfVolume,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    config_entry,
    async_add_entities,
):
    """
    performs setup of the analog sensors, expects a
    reference to an Ecometer serial protocol via hass.data
    """
    tek603 = hass.data[DOMAIN]["protocol"]
    sensors = []
    for nbr in tek603.get_all_sensors().keys():
        sensors.append(EcometerEntity(tek603, nbr))
    async_add_entities(sensors)


class EcometerEntity(SensorEntity):
    """
    Implementation of Ecometer Sensors.
    """

    should_poll = False
    _attr_has_entity_name = True

    def __init__(self, tek603, dp_nbr: int) -> None:
        self._dp_nbr = dp_nbr
        self._tek603 = tek603
        unit = tek603.get_unit(dp_nbr)

        self._attr_name = tek603.get_name(dp_nbr)
        self._attr_unique_id = str(dp_nbr)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "Proteus")},
            "name": "Ecometer",
            "manufacturer": "Proteus",
        }
        match unit:
            case "C":
                self._attr_device_class = SensorDeviceClass.TEMPERATURE
                self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            case "cm":
                self._attr_device_class = SensorDeviceClass.DISTANCE
                self._attr_native_unit_of_measurement = UnitOfLength.CENTIMETERS
            case "l":
                self._attr_device_class = SensorDeviceClass.VOLUME_STORAGE
                self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        _LOGGER.debug(f"setup ecometer {dp_nbr}: {self._attr_name} in {unit}")

    async def async_added_to_hass(self) -> None:
        self._tek603.register_callback(self.async_write_ha_state, self._dp_nbr)

    async def async_will_remove_from_hass(self) -> None:
        self._tek603.remove_callback(self._dp_nbr)

    @property
    def available(self) -> bool:
        return self._tek603.connected()

    @property
    def native_value(self):
        value = self._tek603.read_sensor(self._dp_nbr)
        _LOGGER.debug(f"set ecometer ({self._dp_nbr}) to {value}")
        return value
