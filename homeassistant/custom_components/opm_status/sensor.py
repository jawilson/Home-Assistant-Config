"""
Support for OPM Operating Status sensor.
"""
import logging

import voluptuous as vol

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

ATTR_POSTED = 'posted'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the OPM Operating Status platform"""
    if discovery_info is None:
        return
    add_entities([OPMOperatingStatusSensor(hass.data[DOMAIN])])


class OPMOperatingStatusSensor(Entity):
    """Representation of OPM Operating Status"""

    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'OPM Operating Status'

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._data.operating_status:
            return self._data.operating_status.status_summary

        return None

    async def async_update(self):
        """Get the latest data and update the state."""
        await self._data.async_update()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._data.operating_status:
            return {
                ATTR_POSTED: self._data.operating_status.date_status_posted
            }

        return {}

    @property
    def icon(self):
        return 'mdi:bank'
