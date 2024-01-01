"""Sensor platform for integration_blueprint."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass, UnitOfTemperature
from homeassistant.const import UnitOfPower
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN
from .coordinator import TemzitUpdateCoordinator
from .entity import TemzitEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="temzit",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        (
            IndoorSensor(coordinator),
            OutdoorSensor(coordinator),
            HotWaterSensor(coordinator),
            ConsumptionSensor(coordinator),
            SupplySensor(coordinator),
            ReturnSensor(coordinator),
        )
    )


class IndoorSensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Температура в доме"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_indoor_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.indoor_temp
        self.async_write_ha_state()


class OutdoorSensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Температура на улице"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_outdoor_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.outdoor_temp
        self.async_write_ha_state()

class HotWaterSensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Температура ГВС"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_hotwater_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.hotwater_temp
        self.async_write_ha_state()

class SupplySensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Подача"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_supply_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.supply_temp
        self.async_write_ha_state()

class ReturnSensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Обратка"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_return_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.return_temp
        self.async_write_ha_state()

class ConsumptionSensor(TemzitEntity, SensorEntity):
    """Representation of a sensor."""

    _attr_name = "Потребление электричества"
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + "_consumption"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data.consumption
        self.async_write_ha_state()