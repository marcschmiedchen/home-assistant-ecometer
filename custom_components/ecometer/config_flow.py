"""
Config flow for Proteus Ecometer integration
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_RESOURCE
from homeassistant.helpers import selector
from serial.tools.list_ports import comports

from .const import DOMAIN


class EcometerCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=DOMAIN, data=user_input)

        ports = await self.hass.async_add_executor_job(comports)
        if not ports:
            return self.async_abort(reason="no_serial_ports")

        port_options = [
            {"value": p.device, "label": f"{p.device} – {p.description}"} for p in ports
        ]
        default_port = next(
            (
                p.device
                for p in ports
                if (p.product or "").startswith("CP2102")
                and p.manufacturer == "Silicon Labs"
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
        return self.async_show_form(step_id="user", data_schema=schema, errors={})
