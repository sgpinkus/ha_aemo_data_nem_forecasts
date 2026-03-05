"""Constants for myaemodata."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)
DOMAIN = "myaemodata"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
METRICS = [
    "RRP",
    "TOTALDEMAND",
    "NETINTERCHANGE",
    "SCHEDULEDGENERATION",
    "SEMISCHEDULEDGENERATION",
    "APCFLAG",
]
REGIONS = ["NSW1", "QLD1", "VIC1", "SA1", "TAS1"]
PERIODS = ["ACTUAL", "FORECAST"]
