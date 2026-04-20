"""
Module for gathering info from TEK603
"""

import logging
import asyncio
import serial_asyncio_fast
from serial.tools.list_ports import comports


class TEK603(asyncio.Protocol):
    """
    This protocol class is invoked to listen to USB serial messages
    from TEK603
    """

    DP_NAME = 0  # index of datapoint name
    DP_UNIT = 1  # index of unit description
    DATAPOINTS = {
        1: ("Temperatur", "C"),
        2: ("Fluessigkeitspegel", "cm"),
        3: ("Nutzkapazitaet", "l"),
        4: ("Gesamtkapazitaet", "l"),
    }

    @staticmethod
    def get_name(idx):
        """returns datapoint name from static data"""
        return TEK603.DATAPOINTS.get(idx, (None, None, None))[TEK603.DP_NAME]

    @staticmethod
    def get_unit(idx):
        """returns datapoint unit from static data"""
        return TEK603.DATAPOINTS.get(idx, (None, None, None))[TEK603.DP_UNIT]

    @staticmethod
    def get_all_sensors():
        """returns pointer all possible values of TEK603 datapoints"""
        return TEK603.DATAPOINTS

    def __init__(self):
        self._dp_values = {}
        self._transport = None
        self._connected = False
        # the callbacks for all datapoints are stored in a dictionary
        self._callback_on_data = {}
        self._LOGGER = logging.getLogger(__name__)

    def connection_made(self, transport):
        """is called as soon as an TEK603 connects to server"""
        self._transport = transport
        self._LOGGER.info("Connected to serial port")
        self._connected = True

    def connection_lost(self, exc):
        """
        Is called when connection ends. closes socket.
        """
        self._LOGGER.debug("TEK603 closed the connection.Stopping")
        self._transport.close()
        self._connected = False

    def register_callback(self, cb, dp_nbr):
        self._callback_on_data.update({dp_nbr: cb})

    def remove_callback(self, dp_nbr):
        self._callback_on_data.pop(dp_nbr)

    def connected(self):
        return self._connected

    @staticmethod
    def _crc16(data: bytes) -> int:
        crc = 0
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                crc = (crc << 1) ^ 0x1021 if crc & 0x8000 else crc << 1
            crc &= 0xFFFF
        return crc

    def data_received(self, data):
        """is called whenever data is ready"""
        self._LOGGER.debug(f"received: {data}")
        if len(data) < 4:
            self._LOGGER.debug("serial data too short, discarded.")
            return

        if data[0:2] != b"SI":
            self._LOGGER.debug("header (SI) not received, discarded.")
            return

        data_length = data[2] * 256 + data[3]
        if len(data) != data_length or data_length < 22:
            self._LOGGER.debug("data length inconsistent, discarded.")
            return

        if not (data[5] & 0x10):
            self._LOGGER.debug("live data flag not set, discarded.")
            return

        if self._crc16(data[:-2]) != (data[-2] << 8 | data[-1]):
            self._LOGGER.warning("CRC-16 check failed, discarded.")
            return

        self.decode_temperature(data)
        self.decode_level(data)
        self.decode_available_capacity(data)
        self.decode_max_capacity(data)

        for callback in self._callback_on_data.values():
            callback()

    def decode_max_capacity(self, data):
        self._dp_values[4] = data[18] * 256 + data[19]
        self._LOGGER.debug(f"max_capactiy: {self._dp_values[4]} l")

    def decode_available_capacity(self, data):
        self._dp_values[3] = data[16] * 256 + data[17]
        self._LOGGER.debug(f"available_capacity: {self._dp_values[3]} l")

    def decode_level(self, data):
        self._dp_values[2] = data[14] * 256 + data[15]
        self._LOGGER.debug(f"level: {self._dp_values[2]} cm")

    def decode_temperature(self, data):
        temperature_fahrenheit = data[13] - 40
        temperature_celsius = (temperature_fahrenheit - 32) / 1.8
        self._dp_values[1] = temperature_celsius
        self._LOGGER.debug(f"tempF: {temperature_fahrenheit}")
        self._LOGGER.debug(f"tempC: {temperature_celsius}")

    def read_sensor(self, idx: int):
        """
        Returns sensor value from private array of sensor-readings
        """
        return self._dp_values.get(idx, None)


if __name__ == "__main__":

    testmsg = b"SI\x00\x16\x02\x10\x1099\x03\xe6\x06\xd0h\x00Y\x16\xb8\x18+\xa6n"

    logging.basicConfig()
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.setLevel(logging.DEBUG)

    tek603_port = [
        x
        for x in comports()
        if (x.product or "").startswith("CP2102") and x.manufacturer == "Silicon Labs"
    ]
    if not tek603_port:
        _LOGGER.error("No TEK603 device found on any serial port")
        raise SystemExit(1)
    _LOGGER.debug(f"found possible TEK603 on {tek603_port[0].device}")
    _LOGGER.debug(f"product: {tek603_port[0].product}")
    _LOGGER.debug(f"manufacturer: {tek603_port[0].manufacturer}")

    _eventloop = asyncio.get_event_loop()
    coro = serial_asyncio_fast.create_serial_connection(
        _eventloop, TEK603, tek603_port[0].device, baudrate=115200
    )
    transport, protocol = _eventloop.run_until_complete(coro)

    _LOGGER.debug("Waiting for serial data")

    protocol.decode_max_capacity(testmsg)
    protocol.decode_available_capacity(testmsg)
    protocol.decode_level(testmsg)
    protocol.decode_temperature(testmsg)

    _LOGGER.debug(protocol._dp_values[1])
    _LOGGER.debug(protocol._dp_values[1])
    #_LOGGER.debug(protocol._dp_values[5])

    _eventloop.run_forever()
