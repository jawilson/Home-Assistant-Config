hass.services.call('media_player', 'media_stop', {
    'entity_id': [
        'media_player.cast_kitchen',
        'media_player.cast_bedroom_mini',
        'media_player.cast_living_room_speaker',
        'media_player.cast_home_group',
        'media_player.gpm_desktop_player'
    ]
})

hass.services.call('light', 'turn_off', {
    'entity_id': [
        'light.kitchen',
        'light.dining_lights_level',
        'light.entryway'
    ]
})
hass.services.call('light', 'turn_off', {
    'transition': 5,
    'entity_id': [
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
