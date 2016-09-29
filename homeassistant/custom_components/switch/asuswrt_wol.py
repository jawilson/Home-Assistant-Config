"""
Support for wake on lan via ASUSWRT routers.
"""
import logging

import voluptuous as vol

import custom_components.asuswrt as asuswrt
from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.loader import get_component
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, CONF_NAME)

DEPENDENCIES = ['asuswrt']

_LOGGER = logging.getLogger(__name__)

CONF_MAC_ADDRESS = 'mac_address'

DEFAULT_NAME = 'Wake on LAN'
DEFAULT_PING_TIMEOUT = 1

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MAC_ADDRESS): cv.string,
    vol.Optional(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Add wake on lan switch."""
    asuswrt = get_component('asuswrt')

    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    mac_address = config.get(CONF_MAC_ADDRESS)

    add_devices_callback([AsusWrtWOLSwitch(asuswrt.ASUSWRT, name, host, mac_address)])

class AsusWrtWOLSwitch(SwitchDevice):
    """Representation of a wake on lan switch using ASUS router."""
    def __init__(self, asuswrt, name, host, mac_address):
        """Initialize the WOL switch."""
        self._asuswrt = asuswrt
        self._name = name
        self._host = host
        self._mac_address = mac_address
        self._state = False
        self.update()

    @property
    def should_poll(self):
        """Poll for status regularly."""
        return True

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    @property
    def name(self):
        """The name of the switch."""
        return self._name

    def turn_on(self):
        """Turn the device on."""
        self._asuswrt.send_command("ether-wake -i br0 {}"\
                .format(self._mac_address))
        self.update_ha_state()

    def turn_off(self):
        """Do nothing."""
        pass

    def update(self):
        """Check if device is on and update the state."""
        status = self._asuswrt.send_command("ping -c 1 -W {} {}; echo $?"\
            .format(DEFAULT_PING_TIMEOUT, self._host)).split('\n')[-1]
        self._state = status == "0"
