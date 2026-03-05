from typing import Any, Literal
from logging import Logger, getLogger
from homeassistant.const import (
    CURRENCY_DOLLAR,
    UnitOfEnergy,
)
from homeassistant.components.sensor import SensorDeviceClass

MetricNameType = Literal["RRP", "TOTALDEMAND", "NETINTERCHANGE", "SCHEDULEDGENERATION", "SEMISCHEDULEDGENERATION", "APCFLAG"]

LOGGER: Logger = getLogger(__package__)
DOMAIN = "aemo_data_nem_forecasts"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
METRICS: dict[MetricNameType, dict[str, Any]] = {
    "RRP": {
        "unit": f"{CURRENCY_DOLLAR}/{UnitOfEnergy.MEGA_WATT_HOUR}",
        "device_class": SensorDeviceClass.MONETARY,
        "display_precision": 2,
    },
    "TOTALDEMAND": {
        "unit": UnitOfEnergy.MEGA_WATT_HOUR,
        "device_class": SensorDeviceClass.POWER,
        "display_precision": 3,
    },
    "NETINTERCHANGE": {
        "unit": UnitOfEnergy.MEGA_WATT_HOUR,
        "device_class": SensorDeviceClass.POWER,
        "display_precision": 3,
    },
    "SCHEDULEDGENERATION": {
        "unit": UnitOfEnergy.MEGA_WATT_HOUR,
        "device_class": SensorDeviceClass.POWER,
        "display_precision": 3,
    },
    "SEMISCHEDULEDGENERATION": {
        "unit": UnitOfEnergy.MEGA_WATT_HOUR,
        "device_class": SensorDeviceClass.POWER,
        "display_precision": 3,
    },
    "APCFLAG": {
        "unit": None,
        "device_class": None,
        "display_precision": 0,
    },
}
REGIONS = ["NSW1", "QLD1", "VIC1", "SA1", "TAS1"]
PERIODS = ["ACTUAL", "FORECAST"]
