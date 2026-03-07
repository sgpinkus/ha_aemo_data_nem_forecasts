from typing import Any, Literal
from logging import Logger, getLogger
from homeassistant.const import (
    CURRENCY_DOLLAR,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

MetricNameType = Literal["RRP", "TOTALDEMAND", "NETINTERCHANGE", "SCHEDULEDGENERATION", "SEMISCHEDULEDGENERATION", "APCFLAG"]

LOGGER: Logger = getLogger(__package__)
DOMAIN = "aemo_data_nem_forecasts"
ATTRIBUTION = "Data provided by https://www.aemo.com.au/"
METRICS: dict[MetricNameType, dict[str, Any]] = {
    "RRP": {
        "unit": f"{CURRENCY_DOLLAR}/{UnitOfEnergy.MEGA_WATT_HOUR}",
        "device_class": SensorDeviceClass.MONETARY,
        "state_class": None,
        "display_precision": 2,
    },
    "TOTALDEMAND": {
        "unit": UnitOfPower.MEGA_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "display_precision": 3,
    },
    "NETINTERCHANGE": {
        "unit": UnitOfPower.MEGA_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "display_precision": 3,
    },
    "SCHEDULEDGENERATION": {
        "unit": UnitOfPower.MEGA_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "display_precision": 3,
    },
    "SEMISCHEDULEDGENERATION": {
        "unit": UnitOfPower.MEGA_WATT,
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "display_precision": 3,
    },
    "APCFLAG": {
        "unit": None,
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "display_precision": 0,
    },
}
REGIONS = ["NSW1", "QLD1", "VIC1", "SA1", "TAS1"]
PERIODS = ["ACTUAL", "FORECAST"]
