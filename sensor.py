"""
Support for Ecometer / Tekelek water sensor
"""

import logging

from homeassistant.const import (
    STATE_UNKNOWN,
    UnitOfTemperature,
    UnitOfVolume,
    UnitOfLength,
)
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass
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
        self._name = tek603.get_name(dp_nbr)
        self._unit = tek603.get_unit(dp_nbr)
        _LOGGER.debug(f"setup ecometer {self._dp_nbr}: {self._name} in {self._unit}")

    async def async_added_to_hass(self) -> None:
        """Register callback for this datapoint when entity is added to HA."""
        self._tek603.register_callback(self.async_write_ha_state, self._dp_nbr)

    async def async_will_remove_from_hass(self) -> None:
        """un-register callback for this datapoint when entity is removed."""
        self._tek603.remove_callback(self._dp_nbr)

    @property
    def available(self) -> bool:
        """Return True if serial connection established."""
        return self._tek603.connected()

    @property
    def name(self) -> str:
        """Return the name of this entity."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of this sensor."""
        return str(self._dp_nbr)

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "Proteus")},
            "name": "Ecometer",
            "manufacturer": "Proteus",
        }

    @property
    def state(self):
        """Read the state of the device."""
        value = self._tek603.read_sensor(self._dp_nbr)
        _LOGGER.debug(f"set state ecometer ({self._dp_nbr}) to {value}")
        return STATE_UNKNOWN if value is None else round(value, 0)

    @property
    def device_class(self) -> str:
        if self._unit == "C":
            return SensorDeviceClass.TEMPERATURE
        if self._unit == "cm":
            return SensorDeviceClass.DISTANCE
        if self._unit == "l":
            return SensorDeviceClass.VOLUME_STORAGE

    @property
    def unit_of_measurement(self) -> str:
        if self._unit == "C":
            return UnitOfTemperature.CELSIUS
        if self._unit == "cm":
            return UnitOfLength.CENTIMETERS
        if self._unit == "l":
            return UnitOfVolume.LITERS
