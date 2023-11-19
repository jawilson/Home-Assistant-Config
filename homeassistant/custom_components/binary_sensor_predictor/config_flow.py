""" The configuration flow for Helios Easy Controls integration. """
import logging
from typing import Any, Union

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.entity_registry import async_get_registry

from .const import (
    CONF_BINARY_SENSOR,
    CONF_FADING,
    CONF_FILTER_BINARY_SENSOR,
    CONF_PERIOD,
    CONF_THRESHOLD,
    CONF_TIME_BLOCK_PERIOD,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class BinarySensorPredictorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Configuration flow handler for Binary sensor predictor integration.
    """

    VERSION = 1

    async def async_step_user(
        self, user_input: Union[dict[str, Any], None] = None
    ) -> FlowResult:
        """
        Handles the step when integration added from the UI.
        """
        entity_registry = await async_get_registry(self.hass)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_BINARY_SENSOR): vol.In(
                    sorted(
                        [
                            entity_id
                            for entity_id in entity_registry.entities.keys()
                            if entity_id.startswith("binary_sensor.")
                            or entity_id.startswith("light.")
                            or entity_id.startswith("switch.")
                            or entity_id.startswith("input_boolean.")
                        ]
                    )
                ),
                vol.Required(CONF_FADING): cv.small_float,
                vol.Required(CONF_THRESHOLD): cv.small_float,
                vol.Required(CONF_UNIQUE_ID): cv.string,
            }
        )

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_UNIQUE_ID])
            self._abort_if_unique_id_configured()

            data = {
                CONF_NAME: user_input[CONF_NAME],
                CONF_UNIQUE_ID: user_input[CONF_UNIQUE_ID],
                CONF_BINARY_SENSOR: user_input[CONF_BINARY_SENSOR],
                CONF_FADING: user_input[CONF_FADING],
                CONF_THRESHOLD: user_input[CONF_THRESHOLD],
                CONF_PERIOD: 1440,
                CONF_TIME_BLOCK_PERIOD: 5,
            }

            return self.async_create_entry(title=data[CONF_NAME], data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )
