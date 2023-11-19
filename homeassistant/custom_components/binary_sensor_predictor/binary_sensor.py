"""
The binary sensor module for binary sensor predictor integration.
"""
import logging
from datetime import datetime, timedelta
from typing import Final, List, Union, cast

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import RestoreSensor
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)
from homeassistant.core import CALLBACK_TYPE, Event, State, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
    async_track_time_interval,
)
from homeassistant.helpers.typing import HomeAssistantType

from .const import (
    ATTR_CURRENT_STATE,
    ATTR_CURRENT_TIME_BLOCK,
    ATTR_CURRENT_TIME_BLOCK_STATE,
    ATTR_PROBABILITIES,
    ATTR_PROBABILITY,
    CONF_BINARY_SENSOR,
    CONF_FADING,
    CONF_PERIOD,
    CONF_THRESHOLD,
    CONF_TIME_BLOCK_PERIOD,
)

_LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-instance-attributes
class BinarySensorPredictor(BinarySensorEntity, RestoreSensor):
    """
    Represents a binary sensor predictor binary sensor.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        unique_id: str,
        name: str,
        binary_sensor_entity_id: str,
        period: int,
        time_block_period: int,
        fading: float,
        threshold: float,
    ):
        """
        Initialize a new instance of `BinarySensorPredictor` class.
        """
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_state = False
        self._unsubscribe_state_change: Union[CALLBACK_TYPE, None] = None
        self._unsubscribe_time_change: Union[CALLBACK_TYPE, None] = None
        self._binary_sensor_entity_id: Final[str] = binary_sensor_entity_id
        self._fading: Final[float] = fading
        self._threshold: Final[float] = threshold
        self._period: Final[int] = period
        self._time_block_period: Final[int] = time_block_period
        self._attr_should_poll = False
        self._attr_state = False
        self._first_time_block_elapsed = False
        self._attr_extra_state_attributes = {}

        self.probabilities = self._get_probabilities_attribute_default()
        self.current_time_block_index = self._get_current_time_block_index()
        self.probability = 0.5
        self.current_time_block_state = STATE_UNKNOWN

    @property
    def probabilities(self) -> list[float]:
        return self._attr_extra_state_attributes[ATTR_PROBABILITIES]

    @probabilities.setter
    def probabilities(self, value: list[float]) -> None:
        self._attr_extra_state_attributes[ATTR_PROBABILITIES] = value

    @property
    def current_time_block_index(self) -> int:
        return self._attr_extra_state_attributes[ATTR_CURRENT_TIME_BLOCK]

    @current_time_block_index.setter
    def current_time_block_index(self, value: int) -> None:
        self._attr_extra_state_attributes[ATTR_CURRENT_TIME_BLOCK] = value

    @property
    def probability(self) -> float:
        return self._attr_extra_state_attributes[ATTR_PROBABILITY]

    @probability.setter
    def probability(self, value: float) -> None:
        self._attr_extra_state_attributes[ATTR_PROBABILITY] = value

    @property
    def current_time_block_state(self) -> str:
        return self._attr_extra_state_attributes[ATTR_CURRENT_TIME_BLOCK_STATE]

    @current_time_block_state.setter
    def current_time_block_state(self, value: str) -> None:
        self._attr_extra_state_attributes[ATTR_CURRENT_TIME_BLOCK_STATE] = value

    @property
    def current_state(self) -> str:
        return self._attr_extra_state_attributes.get(ATTR_CURRENT_STATE, STATE_UNKNOWN)

    @current_state.setter
    def current_state(self, value: str) -> None:
        self._attr_extra_state_attributes[ATTR_CURRENT_STATE] = value

    async def async_added_to_hass(self) -> None:
        """Executed when the sensor is added to Home Assistant."""
        _LOGGER.debug(f"Entity `{self.entity_id}` added to hass.")

        last_state = await self.async_get_last_state()
        if last_state:
            self.probabilities = last_state.attributes.get(
                ATTR_PROBABILITIES, self._get_probabilities_attribute_default()
            )

            _LOGGER.debug(
                f"{self.entity_id} restored probabilities: {self.probabilities}"
            )

        self._update_probability_attribute()
        self._update_state()

        self._unsubscribe_state_change = async_track_state_change_event(
            self.hass,
            self._binary_sensor_entity_id,
            self._predicted_entity_state_changed_listener,
        )

        self._schedule_update_for_next_time_block()

        return await super().async_added_to_hass()

    async def async_will_remove_from_hass(self) -> None:
        """Executed when the sensor will be removed from Home Assistant."""
        if self._unsubscribe_state_change is not None:
            self._unsubscribe_state_change()

        if self._unsubscribe_time_change is not None:
            self._unsubscribe_time_change()

        return await super().async_will_remove_from_hass()

    # pylint: disable=unused-argument,redefined-outer-name
    @callback
    async def _time_block_changed_listener(self, datetime: datetime) -> None:
        """
        Handles the case when a time block ends.

        Args:
            datetime: The date time when the listener executed.
        """
        _LOGGER.debug(f"Time block changed for `{self.entity_id}`, updating.")
        current_time_block_index = self._get_current_time_block_index()

        self.current_time_block_index = current_time_block_index

        if self.current_state != STATE_ON:
            self.current_time_block_state = STATE_OFF

        self._update_time_block_probability(
            current_time_block_index, self.current_state
        )

        self._first_time_block_elapsed = True

        self._update_probability_attribute()
        self._update_state()

        self.async_schedule_update_ha_state()

    @callback
    async def _predicted_entity_state_changed_listener(self, event: Event) -> None:
        """
        Handles the case when the predicted (observed) entity state has changed.

        Args:
            event: The state change event.
        """
        new_state = cast(State, event.data.get("new_state")).state
        _LOGGER.debug(
            f"Predicted entity has changed for `{self.entity_id}` to `{new_state}`, updating."
        )
        if (
            new_state == STATE_ON
            and self.current_time_block_state == STATE_OFF
            and self._first_time_block_elapsed
        ):
            self.current_time_block_state = STATE_ON

            # Previously at the time block beginning the probability was decreased
            # (because the current time block state was OFF at that time) so we have to restore
            # the previous probability before increasing it a new value.
            self.probabilities[self.current_time_block_index] = round(
                self.probabilities[self.current_time_block_index] * (1 / self._fading),
                6,
            )

            self._update_time_block_probability(self.current_time_block_index, STATE_ON)
            self._update_probability_attribute()
            self._update_state()

        self.current_state = new_state

        self.async_schedule_update_ha_state()

    def _update_time_block_probability(self, time_block: int, to_state: str):
        _LOGGER.debug(f"Updating probability at {time_block} based on `{to_state}`.")
        if to_state in (STATE_OFF, STATE_ON):
            self.probabilities[time_block] = round(
                int(to_state == STATE_ON) * (1 - self._fading)
                + self.probabilities[time_block] * self._fading,
                6,
            )

    def _schedule_update_for_next_time_block(self) -> None:
        """
        Schedules tracking of the next time block start.
        """
        next_time_block = self._get_next_time_block()
        _LOGGER.debug(
            f"Scheduling interval starts at `{next_time_block}` for `{self.entity_id}`."
        )

        async def schedule_interval(datetime: datetime):
            await self._time_block_changed_listener(datetime)

            self._unsubscribe_time_change = async_track_time_interval(
                self.hass, self._time_block_changed_listener, timedelta(minutes=5)
            )

        self._unsubscribe_time_change = async_track_time_change(
            self.hass,
            schedule_interval,
            next_time_block.hour,
            next_time_block.minute,
            next_time_block.second,
        )

    def _get_next_time_block(self) -> datetime:
        """
        Gets the start of the next time block.

        Returns:
            The start of the next time block.
        """
        return datetime.fromtimestamp(
            ((datetime.now().timestamp() // 60) // self._time_block_period + 1)
            * self._time_block_period
            * 60
        )

    def _update_probability_attribute(self) -> None:
        """
        Updates the probability attribute.
        """
        self.probability = self.probabilities[self.current_time_block_index]

    def _get_probabilities_attribute_default(self) -> List[float]:
        """
        Gets the default value of probabilities attribute.

        Returns:
            A list filled with `0` values with the proper length.
        """
        return self._period // self._time_block_period * [0.5]

    def _get_current_time_block_index(self) -> int:
        """
        Calculates the current time block's index.
        """
        current_minute = datetime.now().timestamp() // 60

        return int(
            (datetime.now().timestamp() // 60 // self._time_block_period)
            % (24 * 60 // self._time_block_period)
        )

    def _update_state(self):
        """
        Updates the state based on the current probability attribute and the threshold parameter.
        """
        self._attr_is_on = self.probability >= self._threshold


async def async_setup_entry(
    # pylint: disable=unused-argument
    hass: HomeAssistantType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """
    Sets up of Binary Sensor Predictor binary sensor platform based on
    the specified config entry.

    Args:
        hass:
            The Home Assistant instance.
        config_entry:
            The config entry which is used to create sensors.
        async_add_entities:
            The callback which can be used to add new entities to Home Assistant.

    Returns:
        The value indicates whether the setup succeeded.
    """
    _LOGGER.info(
        f"Setting up Binary Sensor Predictor binary sensor for {config_entry.data[CONF_BINARY_SENSOR]}."
    )

    async_add_entities(
        [
            BinarySensorPredictor(
                config_entry.data[CONF_UNIQUE_ID],
                config_entry.data[CONF_NAME],
                config_entry.data[CONF_BINARY_SENSOR],
                config_entry.data[CONF_PERIOD],
                config_entry.data[CONF_TIME_BLOCK_PERIOD],
                config_entry.data[CONF_FADING],
                config_entry.data[CONF_THRESHOLD],
            )
        ]
    )

    _LOGGER.info(
        f"Setting up Binary Sensor Predictor binary sensor for {config_entry.data[CONF_BINARY_SENSOR]} completed."
    )
