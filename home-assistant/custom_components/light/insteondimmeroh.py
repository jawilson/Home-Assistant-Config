"""
Openhab light platform that implements lights.

"""
import logging
import requests

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light)

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Openhab Insteon Dimmer"
DEFAULT_BRIGHTNESS = "255"

SUPPORT_INSTEON_DIMMER = (SUPPORT_BRIGHTNESS)

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup Openhab Insteon Dimmer platform."""

    resource = config.get('resource')

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
        config.get('name', DEFAULT_NAME),
        config.get('resource'),
        config.get('brightness', DEFAULT_BRIGHTNESS))])

class OpenhabLight(Light):
    """Provide an Openhab light."""

    # pylint: disable=too-many-arguments
    def __init__(self, hass, name, resource, brightness):
        """Initialize the light."""
        self._state = None
        self._hass = hass
        self._name = name
        self._resource = resource
        self._brightness = brightness

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
        request = requests.get(self._resource+"/state", timeout=10)
        if not request.text.isnumeric():
            self._state = False
        elif int(float(request.text)) > 0:
            self._state = True
        else:
            self._state = False
        return self._state

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_INSTEON_DIMMER

    def turn_on(self, **kwargs):
        """Turn the light on."""
        try:
            # Clamp brightness from 0 to 255
            brightness = \
                max(0, min(kwargs.get(ATTR_BRIGHTNESS, int(self._brightness)), 255))
        except ValueError as ex:
            _LOGGER.warn("Failed to clamp brightness: %s", ex.__str__)
            return None

        onValue = str((brightness/255)*100)
        request = requests.post(self._resource,
                                data=onValue,
                                timeout=10)
        if (request.status_code == 200) or (request.status_code == 201):
            self._brightness = brightness
            self._state = True
        else:
            _LOGGER.info("HTTP Status Code: %s", request.status_code)
            _LOGGER.error("Can't turn on %s. Is resource/endpoint offline?", self._resource)

        self.update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the light off."""
        request = requests.post(self._resource, data="0", timeout=10)
        if (request.status_code == 200) or (request.status_code == 201):
            self._state = False
        else:
            _LOGGER.error("Can't turn off %s. Is resource/endpoint offline?",
                          self._resource)

        self.update_ha_state()
