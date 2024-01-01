from __future__ import annotations

import logging

from homeassistant.components.water_heater import (
    ATTR_TEMPERATURE,
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_GAS,
    STATE_HEAT_PUMP,
    STATE_HIGH_DEMAND,
    STATE_PERFORMANCE,
    STATE_OFF,
    SUPPORT_AWAY_MODE,
    SUPPORT_OPERATION_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    WaterHeaterEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import TEMP_CELSIUS

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
            HotWaterHeater(coordinator),
            MainHeater(coordinator),
        ]
    )


class HotWaterHeater(TemzitEntity, WaterHeaterEntity):
    """Representation of a Climate."""
    _attr_name = "Горячая вода"
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_current_operation = STATE_OFF



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
        self._attr_unique_id = coordinator.config_entry.entry_id + "_hot_water"

        # This is the name for this *entity*, the "name" attribute from "device_info"
        # is used as the device name for device screens in the UI. This name is used on
        # entity screens, and used to build the Entity ID that's used is automations etc.


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self._attr_target_temperature = self.coordinator.data.target_hotwater_temp
        self._attr_current_temperature = self.coordinator.data.hotwater_temp
        self._attr_current_operation = STATE_ELECTRIC if self.coordinator.data.boiler_heater_is_on else STATE_OFF
        self.async_write_ha_state()

class MainHeater(TemzitEntity, WaterHeaterEntity):
    """Representation of a Climate."""
    _attr_name = "Обогрев дома"
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_current_operation = STATE_OFF



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
        self._attr_unique_id = coordinator.config_entry.entry_id + "_main"

        # This is the name for this *entity*, the "name" attribute from "device_info"
        # is used as the device name for device screens in the UI. This name is used on
        # entity screens, and used to build the Entity ID that's used is automations etc.


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self._attr_target_temperature = self.coordinator.data.target_water_temp
        self._attr_current_temperature = self.coordinator.data.return_temp
        self._attr_current_operation = STATE_PERFORMANCE if self.coordinator.data.main_heater_is_on else STATE_HEAT_PUMP
        self.async_write_ha_state()