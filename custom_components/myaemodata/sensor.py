from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, METRICS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    regions = set(r["REGION"] for r in coordinator.data["5MIN"])

    entities = []
    for region in regions:
        for period in ["ACTUAL", "FORECAST"]:
            entities.append(RegionSensor(coordinator, region, period))

    async_add_entities(entities)


def build_series(rows):
    result = {}
    for metric in METRICS:
        result[metric] = [[r["SETTLEMENTDATE"], r[metric]] for r in rows]
    return result


class RegionSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, region, periodtype):
        super().__init__(coordinator)
        self._region = region
        self._periodtype = periodtype
        self._attr_name = f"{region} {periodtype.lower()}"
        self._attr_unique_id = f"{region}_{periodtype.lower()}"

    @property
    def state(self):
        rows = self._rows()
        return rows[-1]["RRP"] if rows else None

    @property
    def extra_state_attributes(self):
        rows = self._rows()
        return {"series": build_series(rows)}

    def _rows(self):
        return [
            r
            for r in self.coordinator.data["5MIN"]
            if r["REGION"] == self._region and r["PERIODTYPE"] == self._periodtype
        ]
