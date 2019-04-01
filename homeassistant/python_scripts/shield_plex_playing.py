hass.services.call('python_script', 'call_service_if_state', {
    'state': 'playing',
    'service': 'media_player.media_pause',
    'entity_id': [
        'media_player.cast_kitchen_display',
        'media_player.cast_bedroom',
        'media_player.cast_living_room_speaker',
        'media_player.cast_everything_group'
    ]
})

hass.services.call('light', 'turn_off', {
    'entity_id': [
        'light.dining_lights_level',
    ]
})
hass.services.call('light', 'turn_off', {
    'transition': 5,
    'entity_id': [
        'light.entryway',
        'light.kitchen',
        'light.liquor_cabinet_lights',
        'light.bedroom',
        'light.closet'
    ]
})

bathroom_motion = int(hass.states.get('sensor.bathroom_alarm_level').state) > 0
showering = hass.states.is_state('binary_sensor.showering', 'on')

if not bathroom_motion and not showering:
    hass.services.call('light', 'turn_off', {
        'transition': 5,
        'entity_id': 'light.bathroom'
    })
