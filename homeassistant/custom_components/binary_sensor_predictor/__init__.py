"""Binary sensor predictor integration module."""
from logging import getLogger

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

_LOGGER = getLogger(__name__)

# pylint: disable=unused-argument
async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """
    Set up the binary sensor predictor integration.

    Args:
        hass: The Home Assistant instance.
        config: The configuration.

    Returns:
        The value indicates whether the setup succeeded.
    """
    return True


async def async_setup_entry(hass: HomeAssistantType, config_entry: ConfigEntry) -> bool:
    """
    Initialize the predictor sensor based on the config entry.

    Args:
        hass: The Home Assistant instance.
        config_entry: The config entry which contains information gathered by the config flow.

    Returns:
        The value indicates whether the setup succeeded.
    """
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "binary_sensor")
    )
    return True


async def async_unload_entry(
    hass: HomeAssistantType, config_entry: ConfigEntry
) -> bool:
    """
    Executed when a config entry unloaded by Home Assistant.

    Args:
        hass: The Home Assistant instance.
        config_entry: The config entry being unloaded.

    Returns:
        The value indicates whether the unloading succeeded.
    """
    await hass.config_entries.async_forward_entry_unload(config_entry, "binary_sensor")

    return True
