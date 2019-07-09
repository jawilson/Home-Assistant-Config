"""Google reverse geocode integration."""
import logging

DOMAIN = "google_reverse_geocode"
_LOGGER = logging.getLogger(__name__)



def setup(hass, config):
    """Setup the Google Reverse Geocode component."""
    def handle_lookup(call):
        """Look up coordinates."""
        __LOGGER.info('Received data', call.data)


    hass.services.register(DOMAIN, 'lookup', handle_lookup)

    return True
