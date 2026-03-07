from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, METRICS, REGIONS, PERIODS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = entry.runtime_data
    entities = []
    for period in PERIODS:
        for metric in METRICS.keys():
            for region in REGIONS:
                entities.append(RegionSensor(coordinator, period, metric, region))
    async_add_entities(entities)
    for entity in entities:
        entity._handle_coordinator_update()


class RegionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, period, metric, region):
        super().__init__(coordinator)
        self._region: str = region
        self._period: str = period
        self._metric: str = metric
        self._attr_unique_id = f"{period}_{metric}_{region}".lower()
        self._attr_name = f"{period} {metric} {region}".upper()
        self._attr_native_unit_of_measurement = METRICS[self._metric]["unit"]
        self._attr_suggested_display_precision = METRICS[self._metric]["display_precision"]
        self._attr_state_class = METRICS[self._metric]["state_class"]
        self._attr_device_class = METRICS[self._metric]["device_class"]
        self._attr_icon = "mdi:chart-line"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, region)},
            name=f"NEM {region}",
            manufacturer="AEMO",
            model="AEMO NEM",
            configuration_url="https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/data-dashboard-nem",
        )

    def _series(self):
        if self.coordinator.data and self.coordinator.data["5MIN"]:
            return [
                [r["SETTLEMENTDATE"], r[self._metric]]
                for r in self.coordinator.data["5MIN"]
                if r["REGION"] == self._region and r["PERIODTYPE"] == self._period
            ]

    @callback
    def _handle_coordinator_update(self) -> None:
        series = self._series()
        if series:
            self._attr_native_value = series[-1 if self._period == "ACTUAL" else 0][1]
            self._attr_extra_state_attributes = { "series": series }
        else:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
        self.async_write_ha_state()
