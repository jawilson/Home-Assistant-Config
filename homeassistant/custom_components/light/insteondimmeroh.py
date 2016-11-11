"""
Openhab light platform that implements lights.

"""
import logging
import requests

import voluptuous as vol

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME, CONF_URL)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Openhab Insteon Dimmer"

SUPPORT_INSTEON_DIMMER = (SUPPORT_BRIGHTNESS)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_URL): cv.string
})

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup Openhab Insteon Dimmer platform."""

    resource = config.get(CONF_URL)

    if resource is None:
        _LOGGER.error("Missing required variable: resource")
        return False

    try:
        requests.get(resource, timeout=10)
    except requests.exceptions.MissingSchema:
        _LOGGER.error("Missing resource or schema in configuration. "
                      "Add http:// or https:// to your URL")
        return False
    except requests.exceptions.ConnectionError:
        _LOGGER.error("No route to resource/endpoint: %s", resource)
        return False

    add_devices_callback([OpenhabLight(
        hass,
        config.get(CONF_NAME),
        config.get(CONF_URL))])

class OpenhabLight(Light):
    """Provide an Openhab light."""

    # pylint: disable=too-many-arguments
    def __init__(self, hass, name, resource):
        """Initialize the light."""
        self._power = False
        self._hass = hass
        self._name = name
        self._resource = resource
        self._brightness = 255
        self.update()

    def update(self):
        request = requests.get(self._resource+"/state", timeout=10)

        try:
            brightness = int(float(request.text)/100*255)
        except ValueError:
            _LOGGER.error("Failed to update %s state, non-numeric value", self._resource)
            return

        if brightness > 0:
            self._power = True
            self._brightness = brightness
        else:
            self._power = False

    def set_brightness(self, brightness):
        onValue = str((brightness/255)*100)
        request = requests.post(self._resource,
                                data=onValue,
                                timeout=10)
        if (request.status_code != 200) and (request.status_code != 201):
            _LOGGER.info("HTTP Status Code: %s", request.status_code)
            _LOGGER.error("Can't set brightness of %s. Is resource/endpoint offline?", self._resource)
            return True
        else:
            return False

    @property
    def should_poll(self):
        """Polling for a light."""
        return True

    @property
    def name(self):
        """Return the name of the light if any."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._power

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_INSTEON_DIMMER

    def turn_on(self, **kwargs):
        """Turn the light on."""
        try:
            # Clamp brightness from 0 to 255
            brightness = \
                max(0, min(kwargs.get(ATTR_BRIGHTNESS, self._brightness), 255))
        except ValueError as ex:
            _LOGGER.warn("Failed to clamp brightness: %s", ex.__str__)
            return None

        if self.set_brightness(brightness):
            self._power = True if brightness > 0 else False
            self._brightness = brightness if brightness > 0 else self._brightness


    def turn_off(self, **kwargs):
        """Turn the light off."""
        if self.set_brightness(0):
            self._power = False
