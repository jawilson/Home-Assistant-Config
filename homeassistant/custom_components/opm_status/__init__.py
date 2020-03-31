"""OPM Operating Status integration."""
import async_timeout

from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = 'opm_status'


async def async_setup(hass, config):
    """Setup OPM Status platform"""
    websession = async_get_clientsession(hass)
    hass.data[DOMAIN] = await OPMData.create(websession)

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True


class OPMData:
    """Stores operating status the data retrieved from OPM.

    For each entity to use, acts as the single point responsible for fetching
    updates from the server.
    """

    def __init__(self, aioopm, websession, status_types):
        """Initialize the data object."""
        self._aioopm = aioopm
        self._websession = websession
        self._status_types = status_types
        self._operating_status = None

    @staticmethod
    async def create(websession):
        from . import aioopm
        status_types = await aioopm.get_status_types(websession)

        return OPMData(aioopm, websession, status_types)

    @property
    def operating_status(self):
        return self._operating_status

    @property
    def status_types(self):
        return self._status_types

    async def async_update(self, **kwargs):
        """Fetch the latest operating status info from OPM."""
        with async_timeout.timeout(10):
            self._operating_status = await self._aioopm.current_operating_status(self._websession)
