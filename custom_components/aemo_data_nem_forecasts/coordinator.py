from datetime import timedelta
from aiohttp import (
    ClientResponse,
    ClientSession,
    ClientResponseError,
    ServerTimeoutError,
)
import async_timeout
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import LOGGER
import json

API_URL = "https://visualisations.aemo.com.au/aemo/apps/api/report/5MIN"
HEADERS = {
    "Referer": "https://visualisations.aemo.com.au/aemo/apps/visualisation/index.html",
    "Content-Type": "application/json",
    "Host": "visualisations.aemo.com.au",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
}
PAYLOAD = {"timeScale": ["30MIN"]}


class AemoCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            logger=LOGGER,
            name="aemo_5min",
            update_interval=timedelta(seconds=600), # The forecast is 30m ahead.
            always_update=False, # If data is __eq__ dont fire update event on listening entities.
        )
        self.session: ClientSession = async_get_clientsession(hass)

    async def _async_update_data(self):
        async with async_timeout.timeout(30):
            try:
                resp: ClientResponse = await self.session.post(
                    API_URL,
                    headers=HEADERS,
                    json=PAYLOAD,
                )
                self.logger.info(f"Fetched data, status: {resp.status}")
                if (
                    resp.status == 204
                ):  # No content: success but nothing new; keep old data
                    self.logger.debug(
                        "API returned 204 No Content - keeping previous data"
                    )
                    return self.data

                resp.raise_for_status()  # Raises on 4xx/5xx

                self.logger.debug(f"API response: content-length={resp.headers.get('Content-Length')}, content-type={resp.headers.get('Content-Type')}")

                text = await resp.text()

                try:
                    return json.loads(text)
                except json.JSONDecodeError as err:
                    self.logger.error(
                        "Invalid JSON from API: %s - response was: %s", err, text
                    )
                    raise UpdateFailed(f"Invalid JSON response: {err}") from err
            except ServerTimeoutError:
                raise UpdateFailed("Request timed out after 30s")
            except ClientResponseError as err:
                raise UpdateFailed(f"HTTP error {err.status}: {err.message}") from err
            except Exception as err:
                self.logger.exception("Unexpected error fetching data")
                raise UpdateFailed(f"Unexpected error: {err}") from err
