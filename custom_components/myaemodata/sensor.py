from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import METRICS, DOMAIN, REGIONS, PERIODS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = entry.runtime_data
    entities = []
    for region in REGIONS:
        for period in PERIODS:
            entities.append(RegionSensor(coordinator, region, period))
    async_add_entities(entities)


class RegionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, region, periodtype):
        super().__init__(coordinator)
        self._region = region
        self._periodtype = periodtype
        self._attr_unique_id = f"{region.lower()}_{periodtype.lower()}"
        self._attr_name = f"{region} {periodtype.title()}"
        self._attr_native_unit_of_measurement = "$/MWh"
        self._attr_icon = "mdi:chart-line"

    def _rows(self):
        return (
            [
                r
                for r in self.coordinator.data["5MIN"]
                if r["REGION"] == self._region and r["PERIODTYPE"] == self._periodtype
            ]
            if self.coordinator.data
            else None
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        rows = self._rows()
        if rows:
            self._attr_native_value = rows[-1 if self._periodtype == "ACTUAL" else 0]["RRP"]
            self._attr_extra_state_attributes = {
                "series": RegionSensor.build_series(rows)
            }
        else:
            self._attr_native_value = None
            self._attr_extra_state_attributes = {}
        self.async_write_ha_state()

    @classmethod
    def build_series(cls, rows):
        result = {}
        for metric in METRICS:
            result[metric] = [[r["SETTLEMENTDATE"], r[metric]] for r in rows]
        return result
