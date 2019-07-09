if hass.states.is_state('binary_sensor.jeff_sleeping_at_home', 'on') or \
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
    hass.services.call('light', 'turn_on', {'entity_id': 'light.bathroom_lights'})
