if hass.states.is_state('sun.sun', 'above_horizon'):
    dining_light_brightness = 255
    kitchen_light_brightness = 255
else:
    dining_light_brightness = 100
    kitchen_light_brightness = 160

dining_lights = hass.states.get('light.dining_lights')
if dining_lights.state != 'on' or \
        dining_lights.attributes.get('brightness') < dining_light_brightness:
    hass.services.call('light', 'turn_on', {'entity_id': 'light.dining_lights',
        'brightness': dining_light_brightness})

kitchen_lights = hass.states.get('light.kitchen_lights')
if kitchen_lights.state != 'on' or \
        kitchen_lights.attributes.get('brightness') < kitchen_light_brightness:
    hass.services.call('light', 'turn_on', {'entity_id': 'light.kitchen_lights',
        'brightness': kitchen_light_brightness})

hass.services.call('light', 'turn_on', {'entity_id': 'light.living_room_lamp'})
hass.services.call('switch', 'turn_on', {'entity_id': 'switch.living_area_fluxer'})
