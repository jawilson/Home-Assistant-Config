hass.services.call('media_player', 'media_stop', {
    'entity_id': [
        'media_player.cast_kitchen',
        'media_player.cast_bedroom_mini',
        'media_player.gpm_desktop_player'
    ]
})

hass.services.call('light', 'turn_off', {
    'entity_id': [
        'light.kitchen_lights',
        'light.dining_lights',
        'light.office_light'
    ]
})
hass.services.call('light', 'turn_off', {
    'transition': 5,
    'entity_id': [
        'light.liquor_cabinet_lights',
        'light.osram_lightify_br_tunable_white_0008a2d5_3',
        'light.bedroom',
        'light.closet'
    ]
})

bathroom_motion = int(hass.states.get('sensor.bathroom_alarm_level').state) > 0
showering = float(hass.states.get('sensor.bathroom_relative_humidity').state) > 80

if not bathroom_motion and not showering:
    hass.services.call('light', 'turn_off', {
        'transition': 5,
        'entity_id': 'light.bathroom'
    })

hass.services.call('switch', 'turn_off', {
    'entity_id': [
        'switch.christmas_tree',
    ]
})


