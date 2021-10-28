"""
Support for Google reverse geocoding sensors.
"""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.components.zone import async_active_zone
from homeassistant.components.device_tracker import ATTR_SOURCE_TYPE
from homeassistant.components.person import ATTR_SOURCE, ATTR_USER_ID
from homeassistant.helpers.event import track_state_change
from homeassistant.helpers.location import has_location
from homeassistant.helpers.network import get_url
from homeassistant.util.async_ import run_callback_threadsafe
from homeassistant.util.location import distance
from homeassistant.const import (
    CONF_API_KEY, CONF_NAME, CONF_ENTITY_ID, EVENT_HOMEASSISTANT_START,
    ATTR_LATITUDE, ATTR_LONGITUDE, ATTR_GPS_ACCURACY, STATE_NOT_HOME,
    ATTR_ENTITY_PICTURE, ATTR_ENTITY_ID)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

ATTR_LOCATION_TYPE = 'location_type'
ATTR_TYPES = 'types'

LOCATION_TYPE_ZONE = 'zone'

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

TRACKABLE_DOMAINS = ['device_tracker', 'sensor', 'person']
DOMAIN = 'google_reverse_geocode'


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the Google reverse geocoding platform."""
    def run_setup(now):
        """Delay the setup until Home Assistant is fully initialized.

        This allows any entities to be created already
        """
        hass.data.setdefault(DOMAIN, [])
        options = config.get(CONF_OPTIONS)

        entity_id = config.get(CONF_ENTITY_ID)
        entity_name = hass.states.get(entity_id).name
        formatted_name = "{} - {}".format(DEFAULT_NAME, entity_name)
        name = config.get(CONF_NAME, formatted_name)
        api_key = config.get(CONF_API_KEY)

        sensor = GoogleReverseGeocodeSensor(
            hass, name, api_key, entity_id, options)
        hass.data[DOMAIN].append(sensor)

        if sensor.valid_api_connection:
            add_devices_callback([sensor])

    # Wait until start event is sent to load this component.
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, run_setup)


class GoogleReverseGeocodeSensor(SensorEntity):
    """Representation of a Google reverse geocode sensor."""

    def __init__(self, hass, name, api_key, entity_id, options):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._api_key = api_key
        self._entity_id = entity_id
        self._options = options
        self.valid_api_connection = True
        self._entity_picture = None
        self._dev_attrs = {}
        self._zone = None
        self._geocode = None

        entity_domain, entity_name = entity_id.split('.', 1)

        # Check if location is a trackable entity
        if entity_domain in TRACKABLE_DOMAINS:
            self._entity_id = entity_id
        else:
            _LOGGER.error("Entity domnain not trackable %s", entity_id)
            self.valid_api_connection = False
            return

        self._unique_id = "{}_{}_{}".format(DOMAIN, entity_domain, entity_name)

        import googlemaps
        external_ip = get_url(hass, allow_internal=False, allow_ip=False, require_ssl=True,
                require_standard_port=True);
        self._client = googlemaps.Client(self._api_key, timeout=10, requests_kwargs={"headers":
            {"Referer": external_ip}});
        try:
            self.update()
        except googlemaps.exceptions.ApiError as exp:
            _LOGGER.error(exp)
            self.valid_api_connection = False
            return

        def force_refresh(entity_id, old_state, new_state):
            """Force the component to refresh."""
            if not has_location(new_state):
                _LOGGER.warn("Entity %s does not have a location, not refreshing", self._entity_id)
                self._zone = None
                self._geocode = None
                return

            traveled = distance(
                    self._dev_attrs.get(ATTR_LATITUDE),
                    self._dev_attrs.get(ATTR_LONGITUDE),
                    new_state.attributes.get(ATTR_LATITUDE),
                    new_state.attributes.get(ATTR_LONGITUDE)
                )

            if (traveled is None or traveled == 0.0 or ATTR_GPS_ACCURACY in new_state.attributes and
                    new_state.attributes.get(ATTR_GPS_ACCURACY) > traveled):
                _LOGGER.debug("Entity %s hasn't moved (enough), not refreshing", self._entity_id)
                return

            _LOGGER.debug("Scheduling update of %s", self._entity_id)
            self.schedule_update_ha_state(True)

        # Update value when tracked entity changes its state
        track_state_change(hass, entity_id, force_refresh)

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": DOMAIN,
            "identifiers": {(DOMAIN, self._api_key)},
            "entry_type": "service"
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID of entity."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._zone is not None:
            return self._zone

        if self._geocode is not None:
            return self._geocode['formatted_address']

        return None

    @property
    def entity_picture(self):
        """Return the picture of the tracked device."""
        return self._entity_picture

    @property
    def name(self):
        """Get the name of the sensor."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {ATTR_ENTITY_ID: self._entity_id, **self._dev_attrs}

        if self._zone is not None:
            attr[ATTR_LOCATION_TYPE] = LOCATION_TYPE_ZONE
        elif self._geocode is not None:
            attr[ATTR_LOCATION_TYPE] = self._geocode['geometry']['location_type'].lower()
            attr[ATTR_TYPES] = self._geocode['types']

        return attr

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    def update(self):
        """Get the latest data from Google."""
        entity = self._hass.states.get(self._entity_id)

        if entity is None:
            _LOGGER.error("Unable to find entity %s", self._entity_id)
            self.valid_api_connection = False
            return

        self._entity_picture = entity.attributes.get(ATTR_ENTITY_PICTURE)

        self._dev_attrs = {key: value for key, value in
                           ((ATTR_SOURCE_TYPE,
                               entity.attributes.get(ATTR_SOURCE_TYPE)),
                            (ATTR_SOURCE,
                               entity.attributes.get(ATTR_SOURCE)),
                            (ATTR_LATITUDE,
                                entity.attributes.get(ATTR_LATITUDE)),
                            (ATTR_LONGITUDE,
                                entity.attributes.get(ATTR_LONGITUDE)),
                            (ATTR_GPS_ACCURACY,
                                entity.attributes.get(ATTR_GPS_ACCURACY))) if value is not None}

        _LOGGER.debug("Found entity %s", self._entity_id)

        zone = self._hass.states.get(f"zone.{entity.state}")
        if has_location(zone):
            self._zone = zone.name
            entity = zone
        else:
            self._zone = None

        if not has_location(entity):
            _LOGGER.warn("Entity %s does not have a location", self._entity_id)
            self._zone = None
            self._geocode = None
            return

        # Convert device_trackers to google friendly location
        loc = self._get_location_from_attributes(entity)

        if not loc:
            _LOGGER.warn("Failed to get location of %s", entity.entity_id)
            self._geocode = None
            return

        _LOGGER.debug("Looking up location %s", loc)
        options_copy = self._options.copy()
        results = self._client.reverse_geocode(loc, **options_copy)
        if results:
            _LOGGER.debug("Reverse geocode results for %s: %s", entity.entity_id,
                    results)
            self._geocode = results[0]
        else:
            _LOGGER.warn("Failed to reverse geocode location of %s", self._entity_id)
            self._geocode = None

    @staticmethod
    def _get_location_from_attributes(entity):
        """Get the lat/long string from an entities attributes."""
        attr = entity.attributes
        return "%s,%s" % (attr.get(ATTR_LATITUDE), attr.get(ATTR_LONGITUDE))
