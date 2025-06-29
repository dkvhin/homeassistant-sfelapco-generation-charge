"""Config flow for SFELAPCO integration."""

import asyncio
import logging
from typing import Any

import voluptuous as vol
import aiohttp
import async_timeout

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST, default="localhost"): str,
    vol.Required(CONF_PORT, default=8099): int,
})


class SFELAPCOConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SFELAPCO."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            # Test the connection to the addon
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            
            if await self._test_connection(host, port):
                await self.async_set_unique_id(f"{host}:{port}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"SFELAPCO Monitor ({host}:{port})",
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self, host: str, port: int) -> bool:
        """Test if we can connect to the SFELAPCO addon."""
        session = async_get_clientsession(self.hass)
        url = f"http://{host}:{port}/health"
        
        try:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("service") == "SFELAPCO Monitor"
        except (aiohttp.ClientError, asyncio.TimeoutError) as ex:
            _LOGGER.warning("Error connecting to SFELAPCO addon: %s", ex)
        
        return False
