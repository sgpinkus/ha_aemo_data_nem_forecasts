"""Constants for myaemodata."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)
DOMAIN = "myaemodata"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
API_URL = "https://visualisations.aemo.com.au/aemo/apps/api/report/5MIN"
HEADERS = {
    "Referer": "https://visualisations.aemo.com.au/aemo/apps/visualisation/index.html",
    "Content-Type": "application/json",
}
PAYLOAD = {"timeScale": ["30MIN"]}
METRICS = [
    "RRP",
    "TOTALDEMAND",
    "NETINTERCHANGE",
    "SCHEDULEDGENERATION",
    "SEMISCHEDULEDGENERATION",
]