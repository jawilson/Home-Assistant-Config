"""
Support for Logitech Harmony Hub
"""

import logging

import voluptuous as vol
import requests

import homeassistant.components.mqtt as mqtt
import homeassistant.loader as loader
from homeassistant.util import slugify
from homeassistant.components.media_player import (
    SUPPORT_PAUSE, SUPPORT_SELECT_SOURCE, MediaPlayerDevice, PLATFORM_SCHEMA,
    SUPPORT_TURN_OFF, SUPPORT_TURN_ON, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_SET,
    SUPPORT_STOP, SUPPORT_VOLUME_STEP, SUPPORT_PREVIOUS_TRACK, SUPPORT_NEXT_TRACK,
    DOMAIN)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, STATE_OFF, STATE_IDLE, ATTR_ENTITY_ID)

_LOGGER = logging.getLogger(__name__)

SERVICE_DEVICE_COMMAND = 'device_command'

ATTR_DEVICE = 'device'
ATTR_COMMAND = 'command'

DEPENDENCIES = ['mqtt']

CONF_TOPIC_NAMESPACE = 'topic_namespace'
CONF_DEFAULT_ACTIVITY = 'default_activity'

DEFAULT_TOPIC_NAMESPACE = 'harmony-api'

SUPPORT_HARMONY = SUPPORT_STOP | SUPPORT_PAUSE | SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_STEP | \
                  SUPPORT_PREVIOUS_TRACK | SUPPORT_NEXT_TRACK | SUPPORT_SELECT_SOURCE | \
                  SUPPORT_TURN_ON | SUPPORT_TURN_OFF

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_DEFAULT_ACTIVITY): cv.string,
    vol.Optional(CONF_TOPIC_NAMESPACE, default=DEFAULT_TOPIC_NAMESPACE):
        mqtt.valid_subscribe_topic
}).extend(mqtt.SCHEMA_BASE)

# Service call validation schemas
HARMONY_DEVICE_COMMAND_SCHEMA = vol.Schema({
    ATTR_DEVICE: cv.string,
    ATTR_COMMAND: cv.string
})

OFF_ACTIVITY = 'poweroff'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Add Harmony Hub"""
    host = 'http://%s' % config.get(CONF_HOST)
    r = requests.get('%s/hubs' % host)

    for slug in r.json().get('hubs'):
        add_devices([HarmonyHubDevice(
                hass,
                host,
                slug,
                config.get(CONF_DEFAULT_ACTIVITY),
                config.get(CONF_TOPIC_NAMESPACE),
                config.get(mqtt.CONF_QOS))])

class HarmonyHubDevice(MediaPlayerDevice):
    """Representation of a Logitech Harmony Hub device."""

    def __init__(self, hass, host, slug, default_activity, mqtt_namespace, qos):
        self._hass = hass
        self._name = slug.replace('-', ' ').title()
        self._hub_url = '%s/hubs/%s' % (host, slug)
        self._slug = slug
        self._mqtt_namespace = '%s/%s' % (mqtt_namespace, slug)
        self._qos = qos
        self._state = STATE_IDLE
        self._default_activity = default_activity
        self._activities = None
        self._current_activity = None
        self._devices = None
        self.update()

        def state_received(topic, payload, qos):
            """A new MQTT message has been received."""
            self.current_activity_update(payload)
            self.update_ha_state()

        activity_topic = '%s/current_activity' % self._mqtt_namespace
        mqtt.subscribe(self._hass, activity_topic, state_received, self._qos)

    def update(self):
        """Get the latest details from the device."""
        if self._activities is None:
            self.build_activity_list()

        r = requests.get('%s/status' % self._hub_url)
        state = r.json()
        self.current_activity_update(state['current_activity']['slug'])

    def build_activity_list(self):
        """Build the activity list."""
        r = requests.get('%s/activities' % self._hub_url)
        activities = r.json()
        self._reverse_activities_map = {a['slug']: a['label'] for a in
                activities['activities'] if a['slug'] != OFF_ACTIVITY}
        self._activities = {label: slug for slug, label in
            self._reverse_activities_map.items()}

        if self._default_activity is not None and \
           self._default_activity not in self._activities.keys():
            _LOGGER.warn(('Configured default activity %s not in harmony activities '
                    'list, using first activity') %
                    self._default_activity)
            self._default_activity = None

        if self._default_activity is None:
            self._default_activity = next(iter(self._activities.values()))

    def build_device_list(self):
        """Build the device list."""
        r = requests.get('%s/devices' % self._hub_url)
        devices = r.json()
        self._devices = {d['slug']: d['label'] for d in devices['devices']}

    def current_activity_update(self, activity):
        """Set the current activity and state based on the given activity"""
        if activity == OFF_ACTIVITY:
            self._current_activity = None
            self._state = STATE_OFF
        else:
            self._current_activity = self._reverse_activities_map[activity]
            self._state = STATE_IDLE


    def send_device_command(self, device, command):
        """Send a command to a device"""
        topic = '%s/devices/%s/command' % \
            (self._mqtt_namespace, device)
        mqtt.publish(self._hass, topic, command, self._qos)

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """State of the player."""
        return STATE_OFF if self._current_activity == OFF_ACTIVITY else STATE_IDLE

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return None

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return None

    @property
    def source(self):
        """Name of the current input source."""
        return self._current_activity

    @property
    def source_list(self):
        """List of available input sources."""
        return sorted(self._activities.keys())

    @property
    def supported_media_commands(self):
        """Flag media commands that are supported."""
        return SUPPORT_HARMONY

    def turn_on(self):
        """Set to default activity"""
        topic = '%s/activities/%s/command' % \
            (self._mqtt_namespace, self._default_activity)
        mqtt.publish(self._hass, topic, 'on', self._qos)

    def turn_off(self):
        """Turn off"""
        topic = '%s/activities/%s/command' % \
            (self._mqtt_namespace, self._default_activity)
        mqtt.publish(self._hass, topic, 'off', self._qos)

    def mute_volume(self, mute):
        """Mute the volume."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'mute', self._qos)

    def media_play(self):
        """Send play commmand."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'play', self._qos)

    def media_pause(self):
        """Send pause command."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'pause', self._qos)

    def media_stop(self):
        """Send stop command."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'stop', self._qos)

    def media_previous_track(self):
        """Send previous track command."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'skip-backward', self._qos)

    def media_next_track(self):
        """Send next track command."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'skip-forward', self._qos)

    def select_source(self, source):
        """Select input source."""
        activity_slug = self._activities[source]
        topic = '%s/activities/%s/command' % \
            (self._mqtt_namespace, activity_slug)
        mqtt.publish(self._hass, topic, 'on', self._qos)

    def volume_up(self):
        """Turn volume up for media player."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'volume-up', self._qos)

    def volume_down(self):
        """Turn volume down for media player."""
        topic = '%s/current_activity/command' % self._mqtt_namespace
        mqtt.publish(self._hass, topic, 'volume-down', self._qos)
