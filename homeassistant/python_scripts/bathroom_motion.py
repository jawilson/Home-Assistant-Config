if hass.states.is_state('binary_sensor.jeff_sleeping_at_home', 'on') and \
        hass.states.is_state('group.other_guests', 'home') and \
        dt_util.now().weekday() < 5 and \
        dt_util.now().hour > 5 and \
        hass.states.is_state('binary_sensor.guests', 'off'):
    hass.services.call('script', 'bathroom_wakeup')
    hass.services.call('script', 'living_area_wakeup')

elif hass.states.is_state('binary_sensor.jeff_sleeping_at_home', 'on') or \
        hass.states.is_state('group.all_lights', 'off'):
    hass.services.call('switch', 'turn_off', {'entity_id':
        'switch.bathroom_fluxer'}, True)
    service_data = {
        'entity_id': 'light.bathroom_mirror_2',
        'brightness': 4,
        'color_temp': 454,
        'transition': 10
    }
    hass.services.call('light', 'turn_on', service_data)

else:
    hass.services.call('light', 'turn_on', {'entity_id': 'light.bathroom'})

    if hass.states.is_state('light.bedroom', 'on') and \
            hass.states.is_state('light.closet', 'off'):
        hass.services.call('light', 'turn_on', {'entity_id': 'light.closet'})
