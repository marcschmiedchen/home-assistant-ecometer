"""
Config flow for Proteus Ecometer integration
"""

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_RESOURCE
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from serial.tools.list_ports import comports

from .const import CONF_CONNECTION_TYPE
from .const import CONF_HOST
from .const import CONF_PORT
from .const import CONNECTION_TCP
from .const import CONNECTION_USB
from .const import DEFAULT_TCP_HOST
from .const import DEFAULT_TCP_PORT
from .const import DOMAIN
from .const import USB_PRODUCT
from .const import USB_VENDOR


class EcometerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    def __init__(self) -> None:
        super().__init__()
        self._connection_type: str | None = None
        self._user_input: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """First step: choose connection type."""
        if user_input is not None:
            self._connection_type = user_input[CONF_CONNECTION_TYPE]
            if self._connection_type == CONNECTION_USB:
                return await self.async_step_usb()
            else:
                return await self.async_step_tcp()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_CONNECTION_TYPE, default=CONNECTION_USB
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": CONNECTION_USB, "label": "USB Serial Port"},
                            {"value": CONNECTION_TCP, "label": "TCP Socket (ser2net)"},
                        ]
                    )
                )
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors={})

    async def async_step_usb(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Second step for USB connection: select serial port."""
        if user_input is not None:
            self._user_input.update(user_input)
            self._user_input[CONF_CONNECTION_TYPE] = CONNECTION_USB
            return self.async_create_entry(title=DOMAIN, data=self._user_input)

        ports = await self.hass.async_add_executor_job(comports)
        if not ports:
            return self.async_abort(reason="no_serial_ports")

        port_options = [
            {"value": p.device, "label": f"{p.device} - {p.description}"} for p in ports
        ]
        default_port = next(
            (
                p.device
                for p in ports
                if (p.product or "").startswith(USB_PRODUCT)
                and p.manufacturer == USB_VENDOR
            ),
            ports[0].device,
        )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_RESOURCE, default=default_port
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=port_options)
                )
            }
        )
        return self.async_show_form(step_id="usb", data_schema=schema, errors={})

    async def async_step_tcp(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Second step for TCP connection: enter host and port."""
        if user_input is not None:
            self._user_input.update(user_input)
            self._user_input[CONF_CONNECTION_TYPE] = CONNECTION_TCP
            return self.async_create_entry(title=DOMAIN, data=self._user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_TCP_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_TCP_PORT): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=65535)
                ),
            }
        )
        return self.async_show_form(step_id="tcp", data_schema=schema, errors={})
