""" Null ConfigFlow so the integration is discoverable and installable from the UI """
from typing import override
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    @override
    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        return self.async_create_entry(
            title="AEMO Data",
            data={},  # empty - no config needed
        )
