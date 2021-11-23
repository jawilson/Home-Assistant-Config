import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_NAME, CONF_ENTITY_ID
from .const import (
        DOMAIN,
        CONF_OPTIONS,
        DEFAULT_NAME,
        ALL_LANGUAGES,
        RESULT_TYPE,
        LOCATION_TYPE,
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Google Maps Reverse Geocode"""
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_intput is not None:
            return self.asnc_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)
                    ): cv.string,
                    vol.Required(CONF_API_KEY): cv.string,
                    vol.Required(CONF_ENTITY_ID): cv.entity_id,
                    vol.Optional(CONF_OPTIONS, default={}): vol.All(
                        dict, vol.Schema({
                            vol.Optional('language'): vol.In(ALL_LANGUAGES),
                            vol.Optional('result_type'): vol.In(RESULT_TYPE),
                            vol.Optional('location_type'): vol.In(LOCATION_TYPE)
                        }))
                }
            )
