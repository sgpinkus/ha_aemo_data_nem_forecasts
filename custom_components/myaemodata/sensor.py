from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import METRICS, REGIONS, PERIODS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = entry.runtime_data
    entities = []
    for period in PERIODS:
        for metric in METRICS:
            for region in REGIONS:
                entities.append(RegionSensor(coordinator, period, metric, region))
    async_add_entities(entities)


class RegionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, period, metric, region):
        super().__init__(coordinator)
        self._region: str = region
        self._period: str = period
        self._metric: str = metric
        self._attr_unique_id = f"{period}_{metric}_{region}".lower()
        self._attr_name = f"{period} {metric} {region}".upper()
        self._attr_native_unit_of_measurement = "$/MWh"
        self._attr_icon = "mdi:chart-line"

    def _rows(self):
        return (
            [
                r[self._metric]
                for r in self.coordinator.data["5MIN"]
                if r["REGION"] == self._region and r["PERIODTYPE"] == self._period
            ]
            if self.coordinator.data["5MIN"]
            else None
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        rows = self._rows()
        if rows:
            self._attr_native_value = rows[-1 if self._period == "ACTUAL" else 0]["RRP"]
            self._attr_extra_state_attributes = {
                "series": [[r["SETTLEMENTDATE"], r[self._metric]] for r in rows]
            }
        else:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
        self.async_write_ha_state()
