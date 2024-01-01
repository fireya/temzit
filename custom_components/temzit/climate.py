"""Platform for climate integration."""
from __future__ import annotations

from datetime import timedelta
import logging

import async_timeout

from homeassistant.components import climate
from homeassistant.components.climate import ClimateEntity, HVACMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback

from .entity import TemzitEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
) -> None:
    """Add cover for passed config_entry in HA."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Add all entities to HA
    async_add_entities(
        [
            TemzitClimate(coordinator),
        ]
    )


class TemzitClimate(TemzitEntity, ClimateEntity):
    """Representation of a Climate."""
    _attr_name = "Термостат"
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]



    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        # """Initialize the sensor."""
        # # Usual setup is done here. Callbacks are added in async_added_to_hass.
        # self.api = api

        # A unique_id for this entity with in this domain. This means for example if you
        # have a sensor on this cover, you must ensure the value returned is unique,
        # which is done here by appending "_cover". For more information, see:
        # https://developers.home-assistant.io/docs/entity_registry_index/#unique-id-requirements
        # Note: This is NOT used to generate the user visible Entity ID used in automations.
        self._attr_unique_id = coordinator.config_entry.entry_id + "climate"

        # This is the name for this *entity*, the "name" attribute from "device_info"
        # is used as the device name for device screens in the UI. This name is used on
        # entity screens, and used to build the Entity ID that's used is automations etc.


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self._attr_current_temperature
        self.async_write_ha_state()

    @property
    def hvac_mode(self) -> HVACMode | None:
        return HVACMode.OFF

    @property
    def current_temperature(self) -> float | None:
        return self.coordinator.data.indoor_temp