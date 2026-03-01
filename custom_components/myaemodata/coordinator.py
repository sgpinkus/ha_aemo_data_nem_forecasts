from datetime import timedelta
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import API_URL, HEADERS, PAYLOAD, LOGGER


class AemoCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            logger=LOGGER,
            name="aemo_5min",
            update_interval=timedelta(minutes=5),
        )
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        async with async_timeout.timeout(30):
            resp = await self.session.get(
                API_URL,
                headers=HEADERS,
                json=PAYLOAD,
            )
            resp.raise_for_status()
            return await resp.json()
