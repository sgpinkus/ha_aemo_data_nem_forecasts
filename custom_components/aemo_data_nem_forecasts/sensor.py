from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import RestoreSensor, SensorEntity, SensorExtraStoredData
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, METRICS, REGIONS, PERIODS


@dataclass
class AemoSensorExtraStoredData(SensorExtraStoredData):
    """Extend HA's SensorExtraStoredData to also persist the time series."""

    series: list[list] | None

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["series"] = self.series
        return base

    @classmethod
    def from_dict(cls, restored: dict[str, Any]) -> Self | None:
        base = SensorExtraStoredData.from_dict(restored)
        if base is None:
            return None
        return cls(
            native_value=base.native_value,
            native_unit_of_measurement=base.native_unit_of_measurement,
            series=restored.get("series"),
        )


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


class RegionSensor(CoordinatorEntity, RestoreSensor, SensorEntity):
    # Exclude 'series' from recorder snapshots — it's persisted via
    # extra_restore_state_data instead, so the recorder only ever sees the
    # scalar state value.
    _unrecorded_attributes = frozenset({"series"})

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
        self._series: list[list] | None = None

    async def async_added_to_hass(self) -> None:
        """Restore persisted series on startup for ACTUAL sensors."""
        await super().async_added_to_hass()
        if self._period == "ACTUAL":
            last_state = await self.async_get_last_extra_data()
            if last_state:
                restored = AemoSensorExtraStoredData.from_dict(last_state.as_dict())
                if restored and restored.series:
                    self._series = restored.series
                    self._attr_extra_state_attributes = {"series": self._series}

    @property
    def extra_restore_state_data(self) -> AemoSensorExtraStoredData:
        """Called by HA to persist extra data on shutdown / periodic saves.
        Stored in .storage/core.restore_state, NOT the recorder DB."""
        return AemoSensorExtraStoredData(
            native_value=self._attr_native_value,
            native_unit_of_measurement=self._attr_native_unit_of_measurement,
            series=self._series,
        )

    def _fresh_series(self) -> list[list] | None:
        """Return the series from the latest coordinator fetch for this sensor."""
        if self.coordinator.data and self.coordinator.data.get("5MIN"):
            return [
                [r["SETTLEMENTDATE"], r[self._metric]]
                for r in self.coordinator.data["5MIN"]
                if r["REGION"] == self._region and r["PERIODTYPE"] == self._period
            ]
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        fresh = self._fresh_series()
        if not fresh:
            self._attr_native_value = None
            self._series = None
            self._attr_extra_state_attributes = {}
            self.async_write_ha_state()
            return

        if self._period == "FORECAST":
            # FORECAST: always replace — it's a shifting window, not a log.
            self._series = fresh
        else:
            # ACTUAL: append only dates we haven't seen before.
            if self._series:
                known = {entry[0] for entry in self._series}
                new_entries = [e for e in fresh if e[0] not in known]
                self._series = self._series + new_entries
            else:
                self._series = fresh

        self._attr_native_value = self._series[-1 if self._period == "ACTUAL" else 0][1]
        self._attr_extra_state_attributes = {"series": self._series}
        self.async_write_ha_state()