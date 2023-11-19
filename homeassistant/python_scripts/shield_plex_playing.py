hass.services.call('python_script', 'call_service_if_state', {
    'state': 'playing',
    'service': 'media_player.media_pause',
    'entity_id': [
        'media_player.living_room_speaker',
        'media_player.sunroom',
        'media_player.kitchen_display',
        'media_player.bedroom_speaker',
        'media_player.bathroom_mini'
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
        'light.closet_lights',
        'light.bedroom_lights',
        'light.entryway_lights',
        'light.kitchen_lights',
        'light.sunroom_lights',
        'light.living_room_nook'
    ]
})

bathroom_motion = hass.states.is_state('binary_sensor.bathroom_motion', 'on')
showering = hass.states.is_state('binary_sensor.showering', 'on')

if not bathroom_motion and not showering:
    hass.services.call('light', 'turn_off', {
        'transition': 5,
        'entity_id': 'light.bathroom_lights'
    })
