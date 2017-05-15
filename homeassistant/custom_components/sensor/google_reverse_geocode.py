"""
Support for Google reverse geocoding sensors.
"""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_state_change
from homeassistant.const import (
    CONF_API_KEY, CONF_NAME, CONF_ENTITY_ID, EVENT_HOMEASSISTANT_START,
    ATTR_LATITUDE, ATTR_LONGITUDE)
import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.location as location

REQUIREMENTS = ['googlemaps==2.4.6']

_LOGGER = logging.getLogger(__name__)

ATTR_LOCATION_TYPE = 'location_type'
ATTR_TYPES = 'types'

CONF_OPTIONS = 'options'

DEFAULT_NAME = 'Google Reverse Geocode'

ALL_LANGUAGES = ['ar', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es',
                 'eu', 'fa', 'fi', 'fr', 'gl', 'gu', 'hi', 'hr', 'hu', 'id',
                 'it', 'iw', 'ja', 'kn', 'ko', 'lt', 'lv', 'ml', 'mr', 'nl',
                 'no', 'pl', 'pt', 'pt-BR', 'pt-PT', 'ro', 'ru', 'sk', 'sl',
                 'sr', 'sv', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'vi',
                 'zh-CN', 'zh-TW']

RESULT_TYPE = ['street_address', 'route', 'intersection', 'political',
               'country', 'administrative_area_level_1',
               'administrative_area_level_2', 'administrative_area_level_3',
               'administrative_area_level_4', 'administrative_area_level_5',
               'colloquial_area', 'locality', 'ward', 'sublocality',
               'sublocality_level_1', 'sublocality_level_2',
               'sublocality_level_3', 'sublocality_level_4',
               'sublocality_level_5', 'neighborhood', 'premise', 'subpremise',
               'postal_code', 'natural_feature', 'airport', 'park',
               'point_of_interest']
LOCATION_TYPE = ['ROOFTOP', 'RANGE_INTERPOLATED', 'RANGE_INTERPOLATED']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_ENTITY_ID): cv.entity_id,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_OPTIONS, default={}): vol.All(
        dict, vol.Schema({
            vol.Optional('language'): vol.In(ALL_LANGUAGES),
            vol.Optional('result_type'): vol.In(RESULT_TYPE),
            vol.Optional('location_type'): vol.In(LOCATION_TYPE)
        }))
})

TRACKABLE_DOMAINS = ['device_tracker', 'sensor']


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Google reverse geocoding platform."""
    def run_setup(event):
        """Delay the setup until Home Assistant is fully initialized.

        This allows any entities to be created already
        """
        options = config.get(CONF_OPTIONS)

        entity_id = config.get(CONF_ENTITY_ID)
        entity_name = hass.states.get(entity_id).attributes.get('friendly_name')
        formatted_name = "{} - {}".format(DEFAULT_NAME, entity_name)
        name = config.get(CONF_NAME, formatted_name)
        api_key = config.get(CONF_API_KEY)

        sensor = GoogleReverseGeocodeSensor(hass, name, api_key, entity_id,
                                            options)

        if sensor.valid_api_connection:
            add_devices_callback([sensor])

    # Wait until start event is sent to load this component.
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, run_setup)


class GoogleReverseGeocodeSensor(Entity):
    """Representation of a Google reverse geocode sensor."""

    def __init__(self, hass, name, api_key, entity_id, options):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._entity_id = entity_id
        self._options = options
        self.valid_api_connection = True

        # Check if location is a trackable entity
        if entity_id.split('.', 1)[0] in TRACKABLE_DOMAINS:
            self._entity_id = entity_id
        else:
            _LOGGER.error("Entity domnain not trackable %s", entity_id)
            self.valid_api_connection = False
            return

        import googlemaps
        self._client = googlemaps.Client(api_key, timeout=10)
        try:
            self.update()
        except googlemaps.exceptions.ApiError as exp:
            _LOGGER.error(exp)
            self.valid_api_connection = False
            return

        def force_refresh(*args):
            """Force the component to refresh."""
            self.schedule_update_ha_state(True)

        # Update value when tracked entity changes its state
        track_state_change(hass, entity_id, force_refresh)

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._geocode is None:
            return None

        return self._geocode['formatted_address']

    @property
    def name(self):
        """Get the name of the sensor."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._geocode is None:
            return None

        return {
            ATTR_LOCATION_TYPE: self._geocode['geometry']['location_type'],
            ATTR_TYPES: self._geocode['types']
        }

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    def update(self):
        """Get the latest data from Google."""
        options_copy = self._options.copy()

        # Convert device_trackers to google friendly location
        self._location = self._get_location_from_entity(
            self._entity_id
        )

        if not self._location:
            self._geocode = None
            return

        results = self._client.reverse_geocode(self._location, **options_copy)
        if results:
            self._geocode = results[0]
        else:
            self._geocode = None

    def _get_location_from_entity(self, entity_id):
        """Get the location from the entity state or attributes."""
        entity = self._hass.states.get(entity_id)

        if entity is None:
            _LOGGER.error("Unable to find entity %s", entity_id)
            self.valid_api_connection = False
            return None

        # Check if the entity has location attributes
        if location.has_location(entity):
            return self._get_location_from_attributes(entity)

        # When everything fails just return nothing
        return None

    @staticmethod
    def _get_location_from_attributes(entity):
        """Get the lat/long string from an entities attributes."""
        attr = entity.attributes
        return "%s,%s" % (attr.get(ATTR_LATITUDE), attr.get(ATTR_LONGITUDE))
