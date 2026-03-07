from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, LOGGER
from .coordinator import AemoCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = AemoCoordinator(hass)
    # await coordinator.async_config_entry_first_refresh() # Causes config flow to block (?)
    entry.async_create_task(hass, coordinator.async_refresh())
    LOGGER.info("Coordinator first refresh started")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
