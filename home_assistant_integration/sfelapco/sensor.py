"""Sensor platform for SFELAPCO integration."""

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SFELAPCO sensors from a config entry."""
    
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    
    # Create the data update coordinator
    coordinator = SFELAPCODataUpdateCoordinator(hass, host, port)
    
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()
    
    # Create sensors
    entities = [
        SFELAPCOGenerationChargeSensor(coordinator),
        SFELAPCOLastUpdateSensor(coordinator),
    ]
    
    async_add_entities(entities)


class SFELAPCODataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the SFELAPCO addon."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        """Initialize."""
        self.host = host
        self.port = port
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        url = f"http://{self.host}:{self.port}/api/status"
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise UpdateFailed(f"Error communicating with API: {response.status}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as ex:
            raise UpdateFailed(f"Error communicating with API: {ex}") from ex


class SFELAPCOGenerationChargeSensor(CoordinatorEntity, SensorEntity):
    """Representation of SFELAPCO Generation Charge sensor."""

    def __init__(self, coordinator: SFELAPCODataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "SFELAPCO Generation Charge"
        self._attr_unique_id = f"{coordinator.host}_{coordinator.port}_generation_charge"
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "PHP/kWh"
        self._attr_icon = "mdi:flash"

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        if self.coordinator.data and "current_charge" in self.coordinator.data:
            current_charge = self.coordinator.data["current_charge"]
            if current_charge:
                return current_charge.get("rate")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes."""
        if self.coordinator.data and "current_charge" in self.coordinator.data:
            current_charge = self.coordinator.data["current_charge"]
            if current_charge:
                return {
                    "month": current_charge.get("month"),
                    "year": current_charge.get("year"),
                    "timestamp": current_charge.get("timestamp"),
                    "last_update": self.coordinator.data.get("last_update"),
                    "history_count": self.coordinator.data.get("history_count", 0),
                }
        return None


class SFELAPCOLastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Representation of SFELAPCO Last Update sensor."""

    def __init__(self, coordinator: SFELAPCODataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "SFELAPCO Last Update"
        self._attr_unique_id = f"{coordinator.host}_{coordinator.port}_last_update"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock"

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("last_update")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes."""
        if self.coordinator.data:
            return {
                "update_interval_days": self.coordinator.data.get("update_interval_days"),
                "retain_history": self.coordinator.data.get("retain_history"),
                "max_history_days": self.coordinator.data.get("max_history_days"),
            }
        return None
